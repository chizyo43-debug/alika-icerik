"""AMI (AliKa satır içi işaretleme) v1 — saf ayrıştırıcı, düz metin yedeği ve kutu ölçüsü.

Dilbilgisi ve ortak test vektörleri ``shared/fixtures/ami/ami_v1_vectors.json``
içindedir; Android ``ui/ami/Ami.kt`` aynı vektörlerle sınanır. Bu modül Tk
içe aktarmaz: çizim ``ami_tk`` modülündedir.

İşaretler:
    ``**kalın**``  ``__altı çizili__`` (iç içe olabilir: ``**__değildir__**``)
    ``{{frac|p|q}}`` ``{{mixed|t|p|q}}`` ``{{sup|x}}`` ``{{sub|x}}``
    ``{{sqrt|x}}`` ``{{over|x}}`` ``{{arc|ABC}}`` ``{{blank}}``
    Kaçış: ``\\*`` ``\\_`` ``\\{`` ``\\}`` ``\\|`` ``\\\\``
    Üç ya da daha çok ardışık alt çizgi (``_____``) işaret değildir; boşluk
    çizgisi olarak aynen gösterilir (İngilizce boşluk doldurma).

Bozuk işaretleme (kapanmamış ``**``/``__``/``{{``, bilinmeyen etiket, eksik
argüman) :class:`AmiError` ile reddedilir; ham metin sessizce gösterilmez.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Callable, Union

VERSION = "alika-ami/1"

# Etiket adı -> argüman sayısı.
TAGS = {
    "frac": 2, "mixed": 3, "sup": 1, "sub": 1,
    "sqrt": 1, "over": 1, "arc": 1, "blank": 0,
}
_ESCAPABLE = set("*_{}|\\")


class AmiError(ValueError):
    """Kararlı kodlu sözdizimi hatası (``ami_unclosed_bold`` gibi)."""

    def __init__(self, code: str, position: int):
        super().__init__(f"{code}@{position}")
        self.code = code
        self.position = position


@dataclass(frozen=True)
class Text:
    value: str


@dataclass(frozen=True)
class Styled:
    kind: str  # "b" | "u"
    children: tuple["Node", ...]


@dataclass(frozen=True)
class Tag:
    name: str
    args: tuple[tuple["Node", ...], ...] = field(default_factory=tuple)


Node = Union[Text, Styled, Tag]


_UNDERLINE_MARK = re.compile(r"(?<!_)__(?!_)")


def has_markup(text: str) -> bool:
    """Metin AMI işareti taşıyor mu (hızlı yol: düz metin ayrıştırılmaz)."""
    if any(mark in text for mark in ("**", "{{", "}}", "\\")):
        return True
    return bool(_UNDERLINE_MARK.search(text))


def parse(text: str) -> tuple[Node, ...]:
    """AMI metnini düğüm ağacına çevirir; bozuk işaretlemede :class:`AmiError`."""
    if not isinstance(text, str):
        raise AmiError("ami_not_text", 0)
    parser = _Parser(text)
    nodes = parser.sequence(stops=())
    return nodes


def validate(text: str) -> str | None:
    """Hata kodunu (ya da ``None``) döndürür; doğrulayıcılar için."""
    # Hızlı yol: parse'ın reddedebileceği her işaret has_markup'ta aranır;
    # işaretsiz metni karakter karakter ayrıştırmak paket içe aktarmayı ~9 kat
    # yavaşlatıyordu (106 paket: 44,6 s → 4,8 s).
    if isinstance(text, str) and not has_markup(text):
        return None
    try:
        parse(text)
    except AmiError as exc:
        return exc.code
    return None


def source(nodes: tuple[Node, ...]) -> str:
    """Düğümleri yeniden AMI metnine yazar; ``parse(source(n)) == n``."""
    out: list[str] = []
    for node in nodes:
        if isinstance(node, Text):
            out.append("".join("\\" + ch if ch in _ESCAPABLE else ch for ch in node.value))
        elif isinstance(node, Styled):
            mark = "**" if node.kind == "b" else "__"
            out.append(mark + source(node.children) + mark)
        else:
            out.append("{{" + node.name + "".join("|" + source(arg) for arg in node.args) + "}}")
    return "".join(out)


class _Parser:
    def __init__(self, text: str):
        self.text = text
        self.pos = 0

    def sequence(self, stops: tuple[str, ...]) -> tuple[Node, ...]:
        """``stops`` içindeki işaretlerden birine kadar okur (işareti tüketmez)."""
        out: list[Node] = []
        buf: list[str] = []
        text = self.text

        def flush():
            if buf:
                out.append(Text("".join(buf)))
                buf.clear()

        while self.pos < len(text):
            ch = text[self.pos]
            two = text[self.pos:self.pos + 2]
            if ch == "\\" and self.pos + 1 < len(text) and text[self.pos + 1] in _ESCAPABLE:
                buf.append(text[self.pos + 1])
                self.pos += 2
                continue
            if text.startswith("___", self.pos):
                # 3+ alt çizgi boşluk çizgisidir; ``__`` açıp kapatmaz.
                end = self.pos
                while end < len(text) and text[end] == "_":
                    end += 1
                buf.append(text[self.pos:end])
                self.pos = end
                continue
            if any(text.startswith(stop, self.pos) for stop in stops):
                break
            if two in ("**", "__"):
                flush()
                start = self.pos
                self.pos += 2
                inner_stops = (two,) + tuple(s for s in stops if s != two)
                children = self.sequence(stops=inner_stops)
                if not text.startswith(two, self.pos):
                    raise AmiError("ami_unclosed_bold" if two == "**" else "ami_unclosed_underline", start)
                self.pos += 2
                out.append(Styled("b" if two == "**" else "u", children))
                continue
            if two == "{{":
                flush()
                out.append(self.tag())
                continue
            if two == "}}":
                raise AmiError("ami_stray_close", self.pos)
            buf.append(ch)
            self.pos += 1
        flush()
        return tuple(out)

    def tag(self) -> Tag:
        text = self.text
        start = self.pos
        self.pos += 2
        name_end = self.pos
        while name_end < len(text) and text[name_end].isalpha():
            name_end += 1
        name = text[self.pos:name_end]
        self.pos = name_end
        if name not in TAGS:
            if "}}" not in text[start:]:
                raise AmiError("ami_unclosed_tag", start)
            raise AmiError("ami_unknown_tag", start)
        args: list[tuple[Node, ...]] = []
        while True:
            if text.startswith("}}", self.pos):
                self.pos += 2
                break
            if self.pos >= len(text):
                raise AmiError("ami_unclosed_tag", start)
            if text[self.pos] != "|":
                raise AmiError("ami_bad_tag", start)
            self.pos += 1
            arg = self.sequence(stops=("|", "}}"))
            if self.pos >= len(text):
                raise AmiError("ami_unclosed_tag", start)
            if not _plain(arg).strip():
                raise AmiError("ami_empty_arg", start)
            args.append(arg)
        if len(args) != TAGS[name]:
            raise AmiError("ami_arity", start)
        return Tag(name, tuple(args))


# --- Düz metin yedeği -------------------------------------------------------

_SUP = str.maketrans("0123456789+-−=()n", "⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻⁻⁼⁽⁾ⁿ")
_SUB = str.maketrans("0123456789+-−=()", "₀₁₂₃₄₅₆₇₈₉₊₋₋₌₍₎")
_SUP_SAFE = set("0123456789+-−=()n")
_SUB_SAFE = set("0123456789+-−=()")
_COMPOUND = set(" +−-⋅×÷/:=")


def _wrap(value: str) -> str:
    return f"({value})" if any(ch in _COMPOUND for ch in value) else value


def _plain(nodes: tuple[Node, ...]) -> str:
    parts: list[str] = []
    for node in nodes:
        if isinstance(node, Text):
            parts.append(node.value)
        elif isinstance(node, Styled):
            parts.append(_plain(node.children))
        else:
            args = [_plain(arg) for arg in node.args]
            name = node.name
            if name == "frac":
                parts.append(f"{_wrap(args[0])}/{_wrap(args[1])}")
            elif name == "mixed":
                parts.append(f"{args[0]} {_wrap(args[1])}/{_wrap(args[2])}")
            elif name == "sup":
                value = args[0]
                parts.append(value.translate(_SUP) if set(value) <= _SUP_SAFE else f"^({value})")
            elif name == "sub":
                value = args[0]
                parts.append(value.translate(_SUB) if set(value) <= _SUB_SAFE else f"_({value})")
            elif name == "sqrt":
                parts.append(f"√({args[0]})")
            elif name == "over":
                parts.append("".join(ch + "̅" for ch in args[0]))
            elif name == "arc":
                parts.append(args[0])
            elif name == "blank":
                parts.append("- - - -")
    return "".join(parts)


def plain(text: str) -> str:
    """İşaretsiz okunur metin (erişilebilirlik, anahtar, uzunluk ölçümü).

    Bozuk işaretlemede metnin kendisi döner; reddetmek doğrulayıcının işidir.
    """
    if not isinstance(text, str):
        return ""
    if not has_markup(text):
        return text
    try:
        return _plain(parse(text))
    except AmiError:
        return text


# Yazdırma sayfası (study_plan) için: kesir/kök CSS ile, dış bağımlılık yok.
HTML_CSS = """
.ami-frac { display: inline-block; vertical-align: middle; text-align: center;
  font-size: 90%; margin: 0 .1em; }
.ami-frac > span { display: block; padding: 0 .12em; }
.ami-frac > .ami-den { border-top: .07em solid currentColor; }
.ami-mixed { white-space: nowrap; }
.ami-sqrt { white-space: nowrap; }
.ami-sqrt > .ami-rad { border-top: .07em solid currentColor; padding: 0 .1em; }
.ami-over { text-decoration: overline; }
.ami-arc { border-top: .07em solid currentColor; border-radius: 50% 50% 0 0;
  padding-top: .05em; }
.ami-blank { display: inline-block; min-width: 3em; border-bottom: .07em dashed currentColor; }
"""


def to_html(text: str) -> str:
    """Kaçışlı HTML parçası; bozuk ya da işaretsiz metin düz kaçışla döner."""
    from html import escape
    if not isinstance(text, str):
        return ""
    if not has_markup(text):
        return escape(text)
    try:
        nodes = parse(text)
    except AmiError:
        return escape(text)

    def render(items: tuple[Node, ...]) -> str:
        parts: list[str] = []
        for node in items:
            if isinstance(node, Text):
                parts.append(escape(node.value))
            elif isinstance(node, Styled):
                tag = "strong" if node.kind == "b" else "u"
                parts.append(f"<{tag}>{render(node.children)}</{tag}>")
            else:
                args = [render(arg) for arg in node.args]
                name = node.name
                frac = ('<span class="ami-frac"><span class="ami-num">{}</span>'
                        '<span class="ami-den">{}</span></span>')
                if name == "frac":
                    parts.append(frac.format(args[0], args[1]))
                elif name == "mixed":
                    parts.append(f'<span class="ami-mixed">{args[0]}'
                                 f'{frac.format(args[1], args[2])}</span>')
                elif name in ("sup", "sub"):
                    parts.append(f"<{name}>{args[0]}</{name}>")
                elif name == "sqrt":
                    parts.append(f'<span class="ami-sqrt">√<span class="ami-rad">'
                                 f'{args[0]}</span></span>')
                elif name in ("over", "arc"):
                    parts.append(f'<span class="ami-{name}">{args[0]}</span>')
                elif name == "blank":
                    parts.append('<span class="ami-blank"></span>')
        return "".join(parts)

    return render(nodes)


def to_json(nodes: tuple[Node, ...]) -> list:
    """Vektör karşılaştırması için kararlı JSON biçimi."""
    out: list = []
    for node in nodes:
        if isinstance(node, Text):
            out.append(["t", node.value])
        elif isinstance(node, Styled):
            out.append([node.kind, to_json(node.children)])
        else:
            out.append([node.name, *[to_json(arg) for arg in node.args]])
    return out


# --- Kutu ölçüsü (iki platformda aynı oranlar) -----------------------------

# Oranlar yazı boyutuna (s) göredir; Android ``AmiLayout`` aynı değerleri kullanır.
LAYOUT = {
    "fracScale": 0.9,        # en dıştaki kesrin pay/paydası
    "nestedScale": 0.78,     # kesir/kök içindeki kesir ve üs
    "minScale": 0.55,
    "mixedFracScale": 0.72,  # tam sayılı kesirde küçük kesir
    "scriptScale": 0.7,      # üs ve alt simge
    "supRaise": 0.42,
    "subDrop": 0.18,
    "axis": 0.27,            # kesir çizgisinin taban çizgisinden yüksekliği
    "rule": 0.065,           # çizgi kalınlığı
    "fracGap": 0.1,          # pay/payda ile çizgi arası
    "fracPad": 0.08,         # çizginin iki yandan taşması
    "nestedPad": 0.22,       # iç içe kesirde dış çizginin ek taşması
    "radicalWidth": 0.5,
    "radicalGap": 0.1,
    "overGap": 0.08,
    "arcHeight": 0.22,
    "blankDash": 0.32,
    "blankGap": 0.22,
    "blankDashes": 4,
}


@dataclass
class Box:
    """Taban çizgisine göre ölçülmüş kutu. ``ops`` (x, y) taban çizgisine göredir.

    ``ops`` öğeleri: ``("text", x, y_baseline, value, size, bold)``,
    ``("line", x1, y1, x2, y2, width)``, ``("poly", [(x, y)...], width)``,
    ``("arc", x, y_top, w, h, width)``. y aşağı doğru artar (ekran düzeni),
    taban çizgisi y=0.
    """

    width: float
    ascent: float
    descent: float
    ops: list = field(default_factory=list)

    def shifted(self, dx: float, dy: float) -> list:
        moved = []
        for op in self.ops:
            kind = op[0]
            if kind == "text":
                moved.append(("text", op[1] + dx, op[2] + dy, op[3], op[4], op[5]))
            elif kind == "line":
                moved.append(("line", op[1] + dx, op[2] + dy, op[3] + dx, op[4] + dy, op[5]))
            elif kind == "poly":
                moved.append(("poly", [(x + dx, y + dy) for x, y in op[1]], op[2]))
            elif kind == "arc":
                moved.append(("arc", op[1] + dx, op[2] + dy, op[3], op[4], op[5]))
        return moved


# measure(text, size, bold) -> (width, ascent, descent)
Measurer = Callable[[str, float, bool], tuple[float, float, float]]


def layout_tag(tag: Tag, size: float, bold: bool, measure: Measurer, depth: int = 0) -> Box:
    """Matematik etiketini ölçer; ``depth`` iç içelik (küçültme için)."""
    L = LAYOUT
    rule = max(1.0, L["rule"] * size)
    name = tag.name

    def inner(nodes, scale):
        return layout_run(nodes, max(size * scale, size * L["minScale"]), bold, measure, depth + 1)

    if name == "frac" or name == "mixed":
        whole = None
        if name == "mixed":
            whole = layout_run(tag.args[0], size, bold, measure, depth)
            num_nodes, den_nodes = tag.args[1], tag.args[2]
            scale = L["mixedFracScale"]
        else:
            num_nodes, den_nodes = tag.args
            scale = L["fracScale"] if depth == 0 else L["nestedScale"]
        num = inner(num_nodes, scale)
        den = inner(den_nodes, scale)
        pad = L["fracPad"] * size
        if any(isinstance(n, Tag) and n.name in ("frac", "mixed")
               for n in (*num_nodes, *den_nodes)):
            pad += L["nestedPad"] * size  # dış kesir çizgisi içtekinden belirgin uzun
        width = max(num.width, den.width) + 2 * pad
        gap = L["fracGap"] * size
        axis = L["axis"] * size
        bar_y = -axis
        ops: list = []
        x0 = 0.0
        if whole is not None:
            ops += whole.shifted(0, 0)
            x0 = whole.width + 0.06 * size
        num_base = bar_y - rule / 2 - gap - num.descent
        den_base = bar_y + rule / 2 + gap + den.ascent
        ops += num.shifted(x0 + (width - num.width) / 2, num_base)
        ops += den.shifted(x0 + (width - den.width) / 2, den_base)
        ops.append(("line", x0, bar_y, x0 + width, bar_y, rule))
        ascent = max(-(num_base - num.ascent), whole.ascent if whole else 0.0)
        descent = max(den_base + den.descent, whole.descent if whole else 0.0)
        return Box(x0 + width, ascent, descent, ops)
    if name in ("sup", "sub"):
        child = inner(tag.args[0], L["scriptScale"])
        dy = -L["supRaise"] * size if name == "sup" else L["subDrop"] * size
        _w, base_ascent, base_descent = measure("0", size, bold)
        ascent = max(child.ascent - dy, 0.0)
        descent = max(child.descent + dy, 0.0)
        if name == "sup":
            descent = max(descent, 0.0)
        return Box(child.width + 0.04 * size, ascent, descent, child.shifted(0.02 * size, dy))
    if name == "sqrt":
        child = inner(tag.args[0], 1.0 if depth == 0 else L["nestedScale"])
        gap = L["radicalGap"] * size
        rw = L["radicalWidth"] * size
        top = -(child.ascent + gap + rule / 2)
        bottom = child.descent
        ops = child.shifted(rw + 0.04 * size, 0)
        ops.append(("poly", [
            (0.0, bottom - (bottom - top) * 0.45),
            (rw * 0.3, bottom - (bottom - top) * 0.55),
            (rw * 0.62, bottom),
            (rw, top),
            (rw + 0.08 * size + child.width, top),
        ], rule))
        return Box(rw + 0.12 * size + child.width, -top + rule, bottom, ops)
    if name == "over":
        child = layout_run(tag.args[0], size, bold, measure, depth)
        y = -(child.ascent + L["overGap"] * size)
        ops = child.shifted(0, 0)
        ops.append(("line", 0.04 * size, y, child.width - 0.02 * size, y, rule))
        return Box(child.width, -y + rule, child.descent, ops)
    if name == "arc":
        child = layout_run(tag.args[0], size, bold, measure, depth)
        h = L["arcHeight"] * size
        top = -(child.ascent + 0.05 * size + h)
        ops = child.shifted(0, 0)
        ops.append(("arc", 0.0, top, child.width, h * 2, rule))
        return Box(child.width, -top + rule, child.descent, ops)
    if name == "blank":
        dash = L["blankDash"] * size
        gap_w = L["blankGap"] * size
        n = int(L["blankDashes"])
        y = -L["axis"] * size * 0.5
        ops = []
        x = 0.06 * size
        for _ in range(n):
            ops.append(("line", x, y, x + dash, y, rule))
            x += dash + gap_w
        width = x - gap_w + 0.06 * size
        _w, ascent, descent = measure("-", size, bold)
        return Box(width, ascent, descent, ops)
    raise AmiError("ami_unknown_tag", 0)


def layout_run(nodes: tuple[Node, ...], size: float, bold: bool, measure: Measurer,
               depth: int = 0) -> Box:
    """Satır kırmadan bir düğüm dizisini yan yana dizer (matematik argümanı)."""
    x = 0.0
    ascent = 0.0
    descent = 0.0
    ops: list = []
    for node in nodes:
        if isinstance(node, Text):
            if not node.value:
                continue
            w, a, d = measure(node.value, size, bold)
            ops.append(("text", x, 0.0, node.value, size, bold))
            x += w
            ascent, descent = max(ascent, a), max(descent, d)
        elif isinstance(node, Styled):
            child = layout_run(node.children, size, bold or node.kind == "b", measure, depth)
            ops += child.shifted(x, 0)
            if node.kind == "u":
                y = child.descent * 0.5 + 1
                ops.append(("line", x, y, x + child.width, y, max(1.0, LAYOUT["rule"] * size)))
            x += child.width
            ascent, descent = max(ascent, child.ascent), max(descent, child.descent)
        else:
            box = layout_tag(node, size, bold, measure, depth)
            ops += box.shifted(x, 0)
            x += box.width
            ascent, descent = max(ascent, box.ascent), max(descent, box.descent)
    return Box(x, ascent, descent, ops)


# --- Akış düzeni (satır kırma) -------------------------------------------

@dataclass
class FlowLine:
    top: float
    width: float
    ascent: float
    descent: float
    first_op: int = 0
    end_op: int = 0


@dataclass
class Flow:
    """Satırlara kırılmış metin. ``ops`` kutu ops biçiminde, y bloğun üstünden."""

    width: float
    height: float
    lines: list
    ops: list


_PIECES = re.compile(r"\n| +|[^ \n]+")
#: Konuşma çizgisi: satır başındaki «—» sonrası kırık satırlar asılı girintilidir.
DIALOGUE_DASH = "—"


def _atoms(nodes, size, bold, underline, measure, out):
    for node in nodes:
        if isinstance(node, Text):
            for piece in _PIECES.findall(node.value):
                if piece == "\n":
                    out.append(("nl", None, False))
                    continue
                w, a, d = measure(piece, size, bold)
                ops = [] if piece[0] == " " else [("text", 0.0, 0.0, piece, size, bold)]
                out.append(("sp" if piece[0] == " " else "w", Box(w, a, d, ops), underline))
        elif isinstance(node, Styled):
            _atoms(node.children, size, bold or node.kind == "b",
                   underline or node.kind == "u", measure, out)
        else:
            out.append(("m", layout_tag(node, size, bold, measure), underline))


def _split_word(box: Box, max_width: float, measure) -> list:
    """Satırdan uzun tek sözcüğü harf harf böler (yalnız düz metin)."""
    _kind, _x, _y, value, size, bold = box.ops[0]
    parts, current = [], ""
    for char in value:
        if current and measure(current + char, size, bold)[0] > max_width:
            parts.append(current)
            current = char
        else:
            current += char
    parts.append(current)
    out = []
    for part in parts:
        w, a, d = measure(part, size, bold)
        out.append(Box(w, a, d, [("text", 0.0, 0.0, part, size, bold)]))
    return out


def flow(nodes: tuple[Node, ...], size: float, bold: bool, measure: Measurer,
         max_width: float | None = None, line_gap: float = 0.3) -> Flow:
    """Sözcük sınırında satır kırar; matematik kutusu ve ona bitişik metin
    (``x{{sup|2}}``, ``{{frac|1|2}}'si``) bölünmez. Açık satır sonu ve satır
    başı girintisi (şiir) korunur; kırılan satırın başındaki boşluk atılır,
    «— » ile başlayan satırın (konuşma çizgisi) devamı çizgiden sonraki metin
    hizasından başlar (asılı girinti). Altı çizili alan satır kırılsa da her
    parçada çizilir. Android ``Ami.flow`` aynı kuralı uygular.
    """
    atoms: list = []
    _atoms(nodes, size, bold, False, measure, atoms)
    _w, base_ascent, base_descent = measure("Ag", size, bold)
    under_y = base_descent * 0.5 + 1
    rule = max(1.0, LAYOUT["rule"] * size)
    gap = line_gap * size
    limit = max_width if max_width and max_width > 0 else float("inf")

    # Bitişik sözcük/matematik atomları tek kırılmaz küme olur.
    tokens: list = []
    cluster: list = []
    for atom in atoms:
        if atom[0] in ("w", "m"):
            cluster.append(atom)
            continue
        if cluster:
            tokens.append(("c", cluster))
            cluster = []
        tokens.append(atom)
    if cluster:
        tokens.append(("c", cluster))

    lines: list = []
    ops: list = []
    current: list = []  # (x, box, underline)
    pending: list = []
    state = {"x": 0.0, "top": 0.0, "fresh": True, "line_start": True,
             "dash_pending": False, "hang": 0.0}

    def finish():
        ascent = max([base_ascent] + [b.ascent for _x, b, _u in current])
        descent = max([base_descent] + [b.descent for _x, b, _u in current])
        baseline = state["top"] + ascent
        width = 0.0
        first = len(ops)
        for x, box, underline in current:
            ops.extend(box.shifted(x, baseline))
            if underline and box.width > 0:
                y = baseline + under_y
                ops.append(("line", x, y, x + box.width, y, rule))
            width = max(width, x + box.width)
        lines.append(FlowLine(state["top"], width, ascent, descent, first, len(ops)))
        state["top"] = baseline + descent + gap
        state["x"] = 0.0
        current.clear()
        pending.clear()

    def place(box, underline):
        current.append((state["x"], box, underline))
        state["x"] += box.width

    def wrap_line():
        finish()
        state["fresh"] = False
        state["x"] = state["hang"]

    for token in tokens:
        kind = token[0]
        if kind == "nl":
            finish()
            state.update(fresh=True, line_start=True, dash_pending=False, hang=0.0)
            continue
        if kind == "sp":
            if not current:
                if state["fresh"]:
                    place(token[1], False)  # satır başı girintisi
                continue
            pending.append(token)
            continue
        boxes = token[1]
        width = sum(b.width for _k, b, _u in boxes)
        spaces = sum(b.width for _k, b, _u in pending)
        if current and state["x"] + spaces + width > limit:
            wrap_line()
        else:
            first_underline = boxes[0][2]
            for _k, box, underline in pending:
                place(box, underline and first_underline)
            pending.clear()
        if state["dash_pending"]:
            state["hang"] = state["x"]
            state["dash_pending"] = False
        if state["line_start"]:
            state["line_start"] = False
            state["dash_pending"] = (len(boxes) == 1 and boxes[0][0] == "w"
                                     and boxes[0][1].ops[0][3] == DIALOGUE_DASH)
        if not current and state["x"] + width > limit and all(k == "w" for k, _b, _u in boxes):
            room = max(limit - state["x"], size)
            pieces = []
            for _k, box, underline in boxes:
                pieces += [(p, underline) for p in _split_word(box, room, measure)]
            for box, underline in pieces:
                if current and state["x"] + box.width > limit:
                    wrap_line()
                place(box, underline)
            continue
        for _k, box, underline in boxes:
            place(box, underline)
    if current or not lines:
        finish()
    height = max(0.0, state["top"] - gap)
    return Flow(max((line.width for line in lines), default=0.0), height, lines, ops)
