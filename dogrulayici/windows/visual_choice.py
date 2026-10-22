"""Strict, local-only visual choice and language-free quiz layout.

v1 3x3 grid, v2 2x2/3x3/4x4 grid (analogy only). v3 adds coloured tile cards
(`kind: tiles`, a visualChoice-only closed list, not a Figure Spec kind) and the
modes analogy, sequence, odd and matrix. Android `VisualChoiceContract` is the twin.
"""
from __future__ import annotations

import json
import math
import re

# Sürüm başına izin verilen ızgara kenarı; bir sorudaki bütün şekiller aynı boyuttadır.
GRID_SIZES = {1: (3,), 2: (2, 3, 4), 3: (1, 2, 3, 4)}
SHAPES = ("circle", "square", "diamond", "triangle", "star", "heart", "arrow", "corner")
# Yalnız yönü olan şekiller döner; diğerlerinde `turn` yazılmaz (aynı görünen iki kart olmasın).
TURNING = ("arrow", "triangle", "corner")
# Okabe-Ito renk körü dostu tonlar; Android `VisualTiles.COLORS` ile aynı.
TILE_COLORS = {
    "red": "#D55E00", "orange": "#E69F00", "yellow": "#F0E442",
    "green": "#009E73", "blue": "#0072B2", "pink": "#CC79A7",
}
AXES = ("vertical", "horizontal")
# Mod → yükteki zorunlu alanlar (version, mode ve options dışında).
MODE_FIELDS = {
    "analogy": {"inputFigures", "examples"},
    "sequence": {"frames"},
    "odd": {"example"},
    "matrix": {"cells"},
}
INK = "#15202B"
CELL_LINE = "#C9D1DE"
FRAME_LINE = "#3E4C66"
ODD_RING = "#1F9D55"


def validate_visual_choice(value, choices, correct, labels):
    def require(ok, message):
        if not ok:
            raise ValueError("visualChoice: " + message)

    require(isinstance(value, dict), "object required")
    require(len(json.dumps(value, ensure_ascii=False, separators=(",", ":"))) <= 16000, "payload too large")
    version = value.get("version")
    require(type(version) is int and version in GRID_SIZES, "unsupported version")
    require(type(correct) is int and 0 <= correct < 4, "correct index")
    if version == 3:
        return _validate_v3(value, choices, correct, labels, require)
    require(set(value) == {"version", "inputFigures", "examples", "options"}, "unsupported fields")
    inputs = value.get("inputFigures")
    require(isinstance(inputs, list) and len(inputs) in (1, 2), "one or two inputs required")
    size = inputs[0].get("rows") if isinstance(inputs[0], dict) else None
    require(type(size) is int and size in GRID_SIZES[version], "grid size not allowed for version")

    def grid(figure):
        require(isinstance(figure, dict), "grid required")
        require(set(figure) == {"kind", "rows", "cols", "shaded", "altTextKey"}, "unsupported grid fields")
        require(figure.get("kind") == "grid" and type(figure.get("rows")) is int and figure["rows"] == size
                and type(figure.get("cols")) is int and figure["cols"] == size, "same-size square grid required")
        cells = figure.get("shaded")
        require(isinstance(cells, list) and all(type(i) is int and 0 <= i < size * size for i in cells), "invalid cells")
        require(bool(cells) and cells == sorted(set(cells)), "cells must be nonempty sorted unique")
        key = figure.get("altTextKey")
        require(key == "visual.grid" and key in labels, "missing accessibility label")
        return tuple(sorted(cells))

    for figure in inputs:
        grid(figure)
    _analogy(value, len(inputs), grid, require)
    figures, identities = _options(value, grid, require)
    require(len(set(figures)) == 4, "duplicate options")
    _choices(choices, identities, require)
    return value


def _validate_v3(value, choices, correct, labels, require):
    mode = value.get("mode")
    require(isinstance(mode, str) and mode in MODE_FIELDS, "unsupported mode")
    require(set(value) == {"version", "mode", "options"} | MODE_FIELDS[mode], "unsupported fields")
    options = value.get("options")
    require(isinstance(options, list) and len(options) == 4, "four options required")
    first = options[0].get("figure") if isinstance(options[0], dict) else None
    size = first.get("rows") if isinstance(first, dict) else None
    require(type(size) is int and size in GRID_SIZES[3], "grid size not allowed for version")

    def tiles(figure):
        require(isinstance(figure, dict), "tiles required")
        require({"kind", "rows", "cols", "tiles", "altTextKey"} <= set(figure)
                <= {"kind", "rows", "cols", "tiles", "altTextKey", "axis"}, "unsupported tiles fields")
        require(figure.get("kind") == "tiles" and type(figure.get("rows")) is int and figure["rows"] == size
                and type(figure.get("cols")) is int and figure["cols"] == size, "same-size square tiles required")
        key = figure.get("altTextKey")
        require(key == "visual.tiles" and key in labels, "missing accessibility label")
        axis = figure.get("axis", "")
        require("axis" not in figure or axis in AXES, "invalid axis")
        items = figure.get("tiles")
        require(isinstance(items, list) and 1 <= len(items) <= size * size, "invalid tiles")
        last, parts = -1, []
        for tile in items:
            require(isinstance(tile, dict) and {"cell", "shape", "color"} <= set(tile)
                    <= {"cell", "shape", "color", "turn"}, "invalid tile")
            cell = tile.get("cell")
            require(type(cell) is int and last < cell < size * size, "tiles must be sorted unique cells")
            last = cell
            shape, color = tile.get("shape"), tile.get("color")
            require(isinstance(shape, str) and shape in SHAPES, "unknown shape")
            require(isinstance(color, str) and color in TILE_COLORS, "unknown color")
            turn = tile.get("turn", 0)
            require("turn" not in tile or (type(turn) is int and shape in TURNING and 1 <= turn <= 3), "invalid turn")
            parts.append((cell, shape, color, turn))
        return (axis, tuple(parts))

    def series(name, counts):
        figures = value.get(name)
        require(isinstance(figures, list) and len(figures) in counts, name + " count")
        return [tiles(figure) for figure in figures]

    if mode == "analogy":
        _analogy(value, len(series("inputFigures", (1, 2))), tiles, require)
    elif mode == "sequence":
        series("frames", (3,))
    elif mode == "matrix":
        series("cells", (3, 8))
    else:
        example = value.get("example")
        require(isinstance(example, dict) and set(example) == {"figures", "odd"}, "invalid odd example")
        figures = example.get("figures")
        require(isinstance(figures, list) and len(figures) == 4, "odd example needs four figures")
        odd = example.get("odd")
        require(type(odd) is int and 0 <= odd < 4, "odd index")
        require(_one_odd([tiles(figure) for figure in figures], odd), "odd example is ambiguous")
    figures, identities = _options(value, tiles, require)
    _choices(choices, identities, require)
    if mode == "odd":
        require(_one_odd(figures, identities.index(choices[correct])), "odd options are ambiguous")
    else:
        require(len(set(figures)) == 4, "duplicate options")
    return value


def _one_odd(figures, odd):
    """Farklı olan tek: diğer üçünden ayrı; o üçü ya hepsi aynı ya hepsi farklı."""
    rest = [figure for index, figure in enumerate(figures) if index != odd]
    return figures[odd] not in rest and len(set(rest)) in (1, 3)


def _analogy(value, arity, figure, require):
    examples = value.get("examples")
    require(isinstance(examples, list) and len(examples) == 2, "two examples required")
    for example in examples:
        require(isinstance(example, dict) and set(example) == {"inputFigures", "outputFigure"}, "invalid example")
        require(isinstance(example["inputFigures"], list) and len(example["inputFigures"]) == arity, "example arity")
        for item in example["inputFigures"]:
            figure(item)
        figure(example["outputFigure"])


def _options(value, figure, require):
    identities, figures = [], []
    for option in value.get("options"):
        require(isinstance(option, dict) and set(option) == {"id", "figure"}, "invalid option")
        identity = option.get("id")
        require(isinstance(identity, str) and re.fullmatch(r"[A-Za-z0-9_-]{1,40}", identity) is not None, "invalid option id")
        identities.append(identity)
        figures.append(figure(option["figure"]))
    return figures, identities


def _choices(choices, identities, require):
    require(len(set(identities)) == 4, "duplicate options")
    require(isinstance(choices, list) and len(choices) == 4 and set(choices) == set(identities), "choices must map to option ids")


def grid_size(value) -> int:
    """Doğrulanmış yükte şekillerin kenarı (v1/v2: 2–4, v3: 1–4)."""
    return value["options"][0]["figure"]["rows"]


def mode(value) -> str:
    return value.get("mode", "analogy")


def card_heights(size: int) -> tuple[int, int, int]:
    """(örnek/soru satırı, şık çizimi, şık düğmesi) yüksekliği; 4x4 hücre okunur kalsın diye büyür."""
    return (92, 104, 128) if size >= 4 else (76, 88, 112)


def ordered_figures(value, choices):
    mapping = {option["id"]: option["figure"] for option in value["options"]}
    return [mapping[identity] for identity in choices]


def _rotate(points, turn):
    for _ in range(turn):
        points = [(1 - y, x) for x, y in points]
    return points


def _heart():
    points = []
    for step in range(32):
        t = 2 * math.pi * step / 32
        points.append((16 * math.sin(t) ** 3, -(13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t))))
    xs, ys = [p[0] for p in points], [p[1] for p in points]
    scale = 0.72 / max(max(xs) - min(xs), max(ys) - min(ys))
    cx, cy = (max(xs) + min(xs)) / 2, (max(ys) + min(ys)) / 2
    return [(0.5 + (x - cx) * scale, 0.52 + (y - cy) * scale) for x, y in points]


def _star():
    return [(0.5 + r * math.cos(math.radians(-90 + 36 * i)), 0.53 + r * math.sin(math.radians(-90 + 36 * i)))
            for i, r in ((i, 0.38 if i % 2 == 0 else 0.17) for i in range(10))]


# Birim hücrede (0–1, y aşağı) çokgenler; Android `VisualTiles.outline` ile aynı noktalar.
OUTLINES = {
    "square": [(0.18, 0.18), (0.82, 0.18), (0.82, 0.82), (0.18, 0.82)],
    "diamond": [(0.5, 0.12), (0.88, 0.5), (0.5, 0.88), (0.12, 0.5)],
    "triangle": [(0.5, 0.14), (0.86, 0.82), (0.14, 0.82)],
    "arrow": [(0.5, 0.12), (0.86, 0.5), (0.64, 0.5), (0.64, 0.88), (0.36, 0.88), (0.36, 0.5), (0.14, 0.5)],
    "corner": [(0.14, 0.14), (0.14, 0.86), (0.86, 0.86)],
    "star": _star(),
    "heart": _heart(),
}


def tile_outline(shape: str, turn: int = 0):
    """Şeklin birim hücredeki çokgeni, saat yönünde `turn` çeyrek döndürülmüş; daire için None."""
    return None if shape == "circle" else _rotate(OUTLINES[shape], turn)


def make_tile_view(parent, figure, height, background, ring=None):
    """Renkli şekil kartı: kendi beyaz zemininde hücre çizgileri, şekiller ve isteğe bağlı eksen."""
    import tkinter as tk
    from library.figure_renderer import figure_ui_scale
    scale = figure_ui_scale(parent)
    frame = tk.Frame(parent, bg=background)
    canvas = tk.Canvas(frame, height=round(height * scale), width=round(70 * scale), bg="#FFFFFF",
                       highlightthickness=round(3 * scale) if ring else 0,
                       highlightbackground=ring or "#FFFFFF", takefocus=True)
    canvas.pack(fill="both", expand=True)
    frame.canvas, frame.figure, frame.cell = canvas, figure, 0.0

    def redraw(_event=None):
        canvas.delete("all")
        w, h = max(canvas.winfo_width(), 40), max(canvas.winfo_height(), 40)
        n = figure["rows"]
        cell = min((w - 4) / n, (h - 4) / n)
        frame.cell = cell
        left, top = (w - n * cell) / 2, (h - n * cell) / 2
        for i in range(n * n):
            x, y = left + (i % n) * cell, top + (i // n) * cell
            canvas.create_rectangle(x, y, x + cell, y + cell, fill="#FFFFFF", outline=CELL_LINE)
        canvas.create_rectangle(left, top, left + n * cell, top + n * cell, outline=FRAME_LINE, width=2)
        stroke = max(1.5, cell * 0.04)
        for tile in figure["tiles"]:
            x, y = left + (tile["cell"] % n) * cell, top + (tile["cell"] // n) * cell
            fill = TILE_COLORS[tile["color"]]
            outline = tile_outline(tile["shape"], tile.get("turn", 0))
            if outline is None:
                r = 0.34 * cell
                canvas.create_oval(x + cell / 2 - r, y + cell / 2 - r, x + cell / 2 + r, y + cell / 2 + r,
                                   fill=fill, outline=INK, width=stroke, tags=("tile",))
            else:
                canvas.create_polygon([v for px, py in outline for v in (x + px * cell, y + py * cell)],
                                      fill=fill, outline=INK, width=stroke, tags=("tile",))
        axis = figure.get("axis")
        if axis == "vertical":
            canvas.create_line(w / 2, top - 4, w / 2, top + n * cell + 4, fill=INK, width=3, dash=(6, 4), tags=("axis",))
        elif axis == "horizontal":
            canvas.create_line(left - 4, h / 2, left + n * cell + 4, h / 2, fill=INK, width=3, dash=(6, 4), tags=("axis",))

    canvas.bind("<Configure>", redraw)
    frame.redraw = redraw
    frame.after_idle(redraw)
    return frame


def figure_view(parent, figure, labels, *, height, background, ring=None):
    """v1/v2 ızgarası üretim çizicisiyle, v3 kartı renkli şekil çizicisiyle."""
    if figure.get("kind") == "tiles":
        return make_tile_view(parent, figure, height, background, ring)
    from library.figure_renderer import FigureView
    return FigureView(parent, figure, labels, height=height, background=background, compact_grid=True)


def show_prompt(parent, value, labels, background):
    import tkinter as tk
    from library.diagram_paint import contrast_ratio
    # Ok ve soru işareti koyu temada da okunur: zemine göre koyu ya da açık yazı.
    red, green, blue = (channel // 257 for channel in parent.winfo_rgb(background))
    surface = f"#{red:02X}{green:02X}{blue:02X}"
    ink = "#15202B" if contrast_ratio("#15202B", surface) >= 4.5 else "#FFF7E9"
    height = card_heights(grid_size(value))[0]

    def row_frame():
        row = tk.Frame(parent, bg=background)
        row.pack(fill="x")
        return row

    def view(row, figure, ring=None):
        figure_view(row, figure, labels, height=height, background=background, ring=ring).pack(
            side="left", fill="x", expand=True)

    def arrow(row):
        tk.Label(row, text="→", font=("Segoe UI", 24), bg=background, fg=ink).pack(side="left")

    def missing(row):
        tk.Label(row, text="?", font=("Segoe UI", 32), bg=background, fg=ink, width=5).pack(side="left", expand=True)

    kind = mode(value)
    if kind == "sequence":
        row = row_frame()
        for figure in value["frames"]:
            view(row, figure)
        arrow(row)
        missing(row)
    elif kind == "matrix":
        side = 2 if len(value["cells"]) == 3 else 3
        for start in range(0, side * side, side):
            row = row_frame()
            for figure in value["cells"][start:start + side]:
                view(row, figure)
            if start + side > len(value["cells"]):
                missing(row)
    elif kind == "odd":
        row = row_frame()
        for index, figure in enumerate(value["example"]["figures"]):
            view(row, figure, ODD_RING if index == value["example"]["odd"] else None)
    else:
        for inputs, output in [(e["inputFigures"], e["outputFigure"]) for e in value["examples"]] + [(value["inputFigures"], None)]:
            row = row_frame()
            for figure in inputs:
                view(row, figure)
            arrow(row)
            if output:
                view(row, output)
            else:
                missing(row)
