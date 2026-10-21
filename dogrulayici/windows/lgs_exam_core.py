"""LGS denemesinin ekrandan bağımsız ortak mantığı (L3, L4, L6 ve L1 yardımcıları).

Android karşılığı ``exam/LgsExamSession.kt`` ile birebir aynadır; iki
platformun aynı kararı verdiği ortak altın fikstür
``shared/fixtures/lgs_exam_golden.json`` ile kanıtlanır (exam_core deseni).

Deneme bir ölçümdür. Sorular içerik paketinden gelir: form, oturum ve sıra
paketteki ``lgs`` bloğundadır, uygulama soru seçmez ve sırayı karıştırmaz.
İşlenmemiş kazanımların soruları çıkarılınca deneme kendiliğinden küçülür.

Bu modül saf mantıktır: Tk, config, i18n ya da depo içe aktarmaz. Paket
doğrulayıcısı (``tools/pack_validate.py``) da kuralları buradan okur.
"""
from __future__ import annotations

import re
from datetime import date

# --- sabitler (lgs_exam_golden.json "constants" bloğu ile aynı olmalı) -------
ASSESSMENT_KIND = "lgs-deneme"
SESSIONS = ("sozel", "sayisal")
#: Kapsamla süzülmüş deneme bu sayının altında başlatılmaz (ebeveyn mesajı).
LGS_MIN_QUESTIONS = 10
#: Sayısal oturum sözelin bitişinden bu kadar dakika sonra başlar.
LGS_BREAK_MINUTES = 30
#: Sorusu olan bir oturumun en kısa süresi (dakika).
MIN_SESSION_MINUTES = 5
LEVEL_MIN, LEVEL_MAX = 1, 5
SCOPE_TAUGHT = "taught"
SCOPE_FULL = "full"
SCOPES = (SCOPE_TAUGHT, SCOPE_FULL)
#: Ağırlıklı net: 4 × (Türkçe + Matematik + Fen) + 1 × diğerleri.
HEAVY_SUBJECTS = ("Türkçe", "Matematik", "Fen Bilimleri")
HEAVY_WEIGHT = 4
LIGHT_WEIGHT = 1

#: MEB kazanım kodu biçimi: M.8.1.1.2, F.8.1.1.1, T.8.3.8, İTA.8.1.1, 8.1.1, E8.1.R1
OBJECTIVE_CODE = re.compile(r"^(?:[A-ZÇĞİÖŞÜ]{1,4}\.?)?\d+(?:\.[0-9A-Z]+)+$")
_DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def _norm(value) -> str:
    return str(value or "").strip().casefold()


def _int(value) -> int | None:
    return value if type(value) is int else None


# --- paket sözleşmesi (L1) -----------------------------------------------------

def assessment_errors(assessment) -> list[str]:
    """Paket başlığındaki ``assessment`` bloğunun biçim hataları."""
    if not isinstance(assessment, dict):
        return ["assessment nesne değil"]
    errors: list[str] = []
    if assessment.get("kind") != ASSESSMENT_KIND:
        errors.append(f"assessment.kind {ASSESSMENT_KIND!r} olmalı")
    if not isinstance(assessment.get("exam"), str) or not assessment["exam"].strip():
        errors.append("assessment.exam boş")
    if not isinstance(assessment.get("examOnly"), bool):
        errors.append("assessment.examOnly true/false olmalı")
    forms = assessment.get("forms")
    if (not isinstance(forms, list) or not forms
            or any(_int(f) is None or f < 1 for f in forms) or len(set(forms)) != len(forms)):
        errors.append("assessment.forms pozitif, tekrarsız tam sayı listesi olmalı")
    full = assessment.get("fullForm")
    if not isinstance(full, dict) or set(full) != set(SESSIONS):
        errors.append("assessment.fullForm yalnız sozel ve sayisal oturumlarını taşımalı")
    else:
        for session in SESSIONS:
            block = full.get(session)
            minutes = block.get("minutes") if isinstance(block, dict) else None
            subjects = block.get("subjects") if isinstance(block, dict) else None
            if _int(minutes) is None or minutes < 1:
                errors.append(f"fullForm.{session}.minutes pozitif tam sayı olmalı")
            if (not isinstance(subjects, dict) or not subjects
                    or any(_int(n) is None or n < 1 for n in subjects.values())):
                errors.append(f"fullForm.{session}.subjects ders → pozitif soru sayısı olmalı")
    calendar = assessment.get("calendar")
    if calendar is not None:
        if not isinstance(calendar, dict):
            errors.append("assessment.calendar nesne olmalı")
        else:
            for code, day in calendar.items():
                if not OBJECTIVE_CODE.match(str(code)):
                    errors.append(f"calendar kazanım kodu geçersiz: {code!r}")
                if not isinstance(day, str) or not _valid_day(day):
                    errors.append(f"calendar[{code!r}] tarih YYYY-AA-GG olmalı")
    return errors


def _valid_day(value: str) -> bool:
    if not _DATE.match(value):
        return False
    try:
        date.fromisoformat(value)
    except ValueError:
        return False
    return True


def lgs_errors(lgs, assessment, level=None) -> list[str]:
    """Bir sorunun ``lgs`` bloğu ve seviyesi için biçim hataları."""
    if not isinstance(lgs, dict):
        return ["lgs nesne değil"]
    errors: list[str] = []
    forms = assessment.get("forms") if isinstance(assessment, dict) else None
    form = _int(lgs.get("form"))
    if form is None or not isinstance(forms, list) or form not in forms:
        errors.append(f"lgs.form assessment.forms içinde değil: {lgs.get('form')!r}")
    if lgs.get("session") not in SESSIONS:
        errors.append(f"lgs.session geçersiz: {lgs.get('session')!r}")
    order = _int(lgs.get("order"))
    if order is None or order < 1:
        errors.append(f"lgs.order pozitif tam sayı olmalı: {lgs.get('order')!r}")
    requires = lgs.get("requires")
    if not isinstance(requires, list):
        errors.append("lgs.requires liste olmalı")
    else:
        for code in requires:
            if not isinstance(code, str) or not OBJECTIVE_CODE.match(code):
                errors.append(f"lgs.requires kazanım kodu geçersiz: {code!r}")
    for key in ("unitKey", "unitName"):
        if not isinstance(lgs.get(key), str) or not lgs[key].strip():
            errors.append(f"lgs.{key} boş")
    shared = lgs.get("sharedText")
    if shared is not None and (not isinstance(shared, str) or not shared.strip()):
        errors.append("lgs.sharedText boş olmayan metin olmalı")
    if _int(level) is None or not LEVEL_MIN <= level <= LEVEL_MAX:
        errors.append(f"level {LEVEL_MIN}-{LEVEL_MAX} arası olmalı: {level!r}")
    return errors


def pack_errors(assessment, questions) -> list[tuple[str, str]]:
    """Paket geneli LGS kuralları: (form, oturum, sıra) tekliği ve fullForm sınırı.

    ``questions``: kaynak soru sözlükleri. Dönen değer (soru kimliği, mesaj).
    """
    errors: list[tuple[str, str]] = []
    full = assessment.get("fullForm") if isinstance(assessment, dict) else None
    limits: dict[tuple[str, str], int] = {}
    if isinstance(full, dict):
        for session, block in full.items():
            subjects = block.get("subjects") if isinstance(block, dict) else None
            for subject, count in (subjects or {}).items():
                limits[(session, _norm(subject))] = count
    seen: dict[tuple, str] = {}
    per_subject: dict[tuple, int] = {}
    shared: dict[tuple, list[int]] = {}
    for q in questions:
        lgs = q.get("lgs") if isinstance(q.get("lgs"), dict) else {}
        qid = str(q.get("id") or "")
        form, session, order = lgs.get("form"), lgs.get("session"), lgs.get("order")
        if _int(form) is None or session not in SESSIONS or _int(order) is None:
            continue
        slot = (form, session, order)
        if slot in seen:
            errors.append((qid, f"form {form} {session} sıra {order} yinelenmiş ({seen[slot]})"))
        else:
            seen[slot] = qid
        key = (form, session, _norm(q.get("subject")))
        per_subject[key] = per_subject.get(key, 0) + 1
        if lgs.get("sharedText"):
            shared.setdefault((form, lgs["sharedText"]), []).append(order)
    for (form, session, subject), count in sorted(per_subject.items(), key=str):
        limit = limits.get((session, subject))
        if limit is None:
            errors.append(("", f"form {form}: {subject!r} fullForm.{session} içinde yok"))
        elif count > limit:
            errors.append(("", f"form {form}: {subject!r} {count} soru, fullForm {limit}"))
    for (form, group), orders in sorted(shared.items(), key=str):
        orders = sorted(orders)
        if len(orders) < 2 or orders[-1] - orders[0] != len(orders) - 1:
            errors.append(("", f"form {form}: sharedText {group!r} ardışık en az iki soru değil"))
    return errors


def merge_assessments(assessments) -> tuple[dict | None, list[str]]:
    """Ders paketlerinin ``assessment`` bloklarını tek deneme tanımında birleştirir.

    Her ders paketi kendi takvimini taşır; ``fullForm`` ve ``exam`` ise bütün
    paketlerde aynı olmalıdır. Takvimler birleşir (aynı kod iki tarihle gelirse
    erken tarih), formlar sıralı birleşim olur. Dönen değer (birleşik blok,
    tutarsızlık mesajları); geçerli blok yoksa (None, mesajlar).
    """
    blocks = [a for a in assessments or [] if isinstance(a, dict) and not assessment_errors(a)]
    if not blocks:
        return None, ["geçerli assessment yok"]
    first = blocks[0]
    errors: list[str] = []
    forms: set[int] = set()
    calendar: dict[str, str] = {}
    for block in blocks:
        if block.get("fullForm") != first.get("fullForm"):
            errors.append("paketlerin fullForm blokları farklı")
        if block.get("exam") != first.get("exam"):
            errors.append("paketlerin exam değerleri farklı")
        forms.update(block.get("forms") or [])
        for code, day in (block.get("calendar") or {}).items():
            if code not in calendar or day < calendar[code]:
                calendar[code] = day
    merged = {
        "kind": ASSESSMENT_KIND,
        "exam": first.get("exam"),
        "examOnly": all(b.get("examOnly") is True for b in blocks),
        "forms": sorted(forms),
        "fullForm": first.get("fullForm"),
        "calendar": dict(sorted(calendar.items())),
    }
    return merged, sorted(set(errors))


def is_lgs_question(question: dict) -> bool:
    """Kaynak soru (ya da depo metadata'sı) LGS deneme sorusu mu?"""
    return isinstance(question, dict) and isinstance(question.get("lgs"), dict)


# --- kapsam (L3) ----------------------------------------------------------------

def unit_scope_key(subject, unit_key) -> str:
    """Ünite → kazanım haritasının anahtarı: ders + ünite kimliği.

    Aynı ``unit_key`` başka bir derste de olabilir; ders anahtarın parçasıdır.
    """
    return f"{_norm(subject)}\x1f{_norm(unit_key)}"


def _whole_grade(record: dict) -> bool:
    """Yalnız sınıfı dolu kayıt: "bu sınıfın bütün konuları işlendi"."""
    return bool(record.get("grade")) and not any(
        str(record.get(key) or "").strip()
        for key in ("subject", "topic", "topic_key", "objective", "unit_key"))


def coverage(*, mode: str, taught=None, topic_objectives=None, unit_objectives=None,
             calendar=None, today: date | None = None, grade: int = 8) -> dict:
    """İşlenmiş sayılan kazanım kümesi.

    Dönen sözlük: ``full`` (süzgeç yok), ``objectives`` (işlenmiş kodlar,
    büyük-küçük harf duyarsız), ``subjects`` (tamamı işlenmiş dersler) ve
    ``source`` (``full`` | ``taught`` | ``calendar``).

    * ``mode == "full"``: süzgeç uygulanmaz.
    * Bu sınıfa (ya da sınıfı boş) ait ``taught`` kaydı varsa:

      - bütün sınıf kaydı (yalnız ``grade``) → tam kapsam, kaynak ``taught``;
      - ünite kaydı (``subject`` + ``unit_key``) → ``unit_objectives``
        (:func:`unit_scope_key` → kazanım listesi) içindeki kodlar. LGS
        paketinin ``lgs.unitKey`` değerleri kütüphane ünitesi değildir;
        eşleşme yalnız kazanım kodu üzerinden olur, haritada olmayan ünite
        kapsam eklemez;
      - ``objective`` ∪ ``topic_key``'i işaretlenen konuların kazanımları
        (``topic_objectives``: topic_key → kazanım listesi);
      - yalnız dersi dolu kayıt bütün dersi kapsar.
    * Kayıt yoksa: paketteki ``calendar`` tarihi bugüne kadar geçmiş kazanımlar.
    """
    if mode == SCOPE_FULL:
        return {"full": True, "objectives": set(), "subjects": set(), "source": SCOPE_FULL}
    records = [r for r in (taught or []) if isinstance(r, dict)
               and r.get("grade") in (0, None, grade)]
    if records:
        if any(_whole_grade(record) for record in records):
            return {"full": True, "objectives": set(), "subjects": set(), "source": SCOPE_TAUGHT}
        objectives: set[str] = set()
        subjects: set[str] = set()
        by_key = {_norm(k): v for k, v in (topic_objectives or {}).items()}
        by_unit = {_norm(k): v for k, v in (unit_objectives or {}).items()}
        for record in records:
            if record.get("objective"):
                objectives.add(_norm(record["objective"]))
            key = _norm(record.get("topic_key"))
            if key:
                objectives.update(_norm(code) for code in by_key.get(key, ()))
            unit = _norm(record.get("unit_key"))
            if unit:
                wanted = unit_scope_key(record.get("subject"), unit)
                for unit_id, codes in by_unit.items():
                    # Dersi boş ünite kaydı (eski sözleşme) her dersteki bu üniteyi kapsar.
                    if unit_id == wanted or (wanted.startswith("\x1f")
                                             and unit_id.endswith(wanted)):
                        objectives.update(_norm(code) for code in codes)
            elif (not record.get("topic") and not key and not record.get("objective")
                    and record.get("subject")):
                subjects.add(_norm(record["subject"]))
        objectives.discard("")
        return {"full": False, "objectives": objectives, "subjects": subjects,
                "source": SCOPE_TAUGHT}
    day = (today or date.today()).isoformat()
    objectives = {_norm(code) for code, when in (calendar or {}).items()
                  if isinstance(when, str) and when <= day}
    return {"full": False, "objectives": objectives, "subjects": set(), "source": "calendar"}


def in_scope(question: dict, cov: dict) -> bool:
    """Soru çıkabilir mi: ``requires`` boşsa her zaman; değilse hepsi işlenmişse."""
    if cov.get("full"):
        return True
    if _norm(question.get("subject")) in cov.get("subjects", ()):
        return True
    lgs = question.get("lgs") or {}
    requires = lgs.get("requires") or []
    return all(_norm(code) in cov.get("objectives", ()) for code in requires)


# --- deneme kurma (L4) -----------------------------------------------------------

def _full_counts(assessment: dict) -> dict[str, dict[str, int]]:
    full = assessment.get("fullForm") or {}
    return {s: dict((full.get(s) or {}).get("subjects") or {}) for s in SESSIONS}


def session_minutes(count: int, session: str, assessment: dict) -> int:
    """Oturum süresi: ceil(soru × tam süre / tam soru); sorusu varsa en az 5 dk."""
    if count <= 0:
        return 0
    block = (assessment.get("fullForm") or {}).get(session) or {}
    total = sum((block.get("subjects") or {}).values())
    minutes = block.get("minutes") or 0
    if total <= 0 or minutes <= 0:
        return MIN_SESSION_MINUTES
    # Tam sayı aritmetiği: kayan nokta yuvarlaması iki platformda ayrışmasın.
    return max(MIN_SESSION_MINUTES, -(-count * minutes // total))


def build_form(questions, form: int, cov: dict, assessment: dict) -> dict:
    """Form ``form`` için kapsamla süzülmüş deneme planı.

    ``questions``: ``id``, ``subject``, ``level`` ve ``lgs`` alanlı sözlükler.
    sharedText grubunun bir sorusu kapsam dışıysa grubun hepsi çıkar.
    Dönen plan iki oturumu (``sessions``) sıra numarasıyla, süreleriyle,
    ders başına çıkan/tam sayıyla ve kapsam yüzdesiyle verir.
    """
    pool = [q for q in questions or []
            if isinstance(q, dict) and is_lgs_question(q) and q["lgs"].get("form") == form
            and q["lgs"].get("session") in SESSIONS]
    allowed = {id(q): in_scope(q, cov) for q in pool}
    groups: dict[str, bool] = {}
    for q in pool:
        group = q["lgs"].get("sharedText")
        if group:
            groups[group] = groups.get(group, True) and allowed[id(q)]
    chosen = [q for q in pool if allowed[id(q)]
              and (not q["lgs"].get("sharedText") or groups[q["lgs"]["sharedText"]])]
    full_counts = _full_counts(assessment)
    sessions = []
    per_subject = []
    total = full_total = 0
    for session in SESSIONS:
        items = sorted((q for q in chosen if q["lgs"]["session"] == session),
                       key=lambda q: (q["lgs"]["order"], str(q.get("id"))))
        for subject, full_n in full_counts[session].items():
            n = sum(1 for q in items if _norm(q.get("subject")) == _norm(subject))
            per_subject.append({"session": session, "subject": subject,
                                "count": n, "full": full_n})
            full_total += full_n
        total += len(items)
        sessions.append({
            "session": session,
            "question_ids": [str(q.get("id")) for q in items],
            "orders": [q["lgs"]["order"] for q in items],
            "minutes": session_minutes(len(items), session, assessment),
        })
    return {
        "form": form,
        "sessions": [s for s in sessions if s["question_ids"]],
        "per_subject": per_subject,
        "total": total,
        "full_total": full_total,
        "coverage_percent": (total * 100 // full_total) if full_total else 0,
        "source": cov.get("source", ""),
    }


def session_offsets(plan: dict, break_minutes: int = LGS_BREAK_MINUTES) -> list[dict]:
    """Oturumların başlangıç dakikaları (deneme saatine göre).

    Sayısal oturum sözelin bitişinden ``break_minutes`` sonra başlar; sözel
    atlanmışsa sayısal deneme saatinde başlar.
    """
    out, offset = [], 0
    for index, session in enumerate(plan.get("sessions") or []):
        if index:
            offset += max(0, int(break_minutes))
        out.append({"session": session["session"], "start": offset,
                    "end": offset + session["minutes"]})
        offset += session["minutes"]
    return out


def can_start(plan: dict, min_questions: int = LGS_MIN_QUESTIONS) -> bool:
    return plan.get("total", 0) >= max(1, min_questions)


def available_forms(questions, assessment: dict) -> list[int]:
    """Pakette sorusu bulunan formlar (assessment.forms sırasıyla)."""
    present = {q["lgs"].get("form") for q in questions or [] if is_lgs_question(q)}
    return [f for f in assessment.get("forms") or [] if f in present]


# --- puanlama (L6) ----------------------------------------------------------------

def net_hundredths(correct: int, wrong: int) -> int:
    """D − Y/3'ün yüzde biri, yarım yukarı yuvarlanmış tam sayı.

    Tam sayı aritmetiği: kayan nokta iki platformda farklı yuvarlanmasın.
    (3D − Y) × 100 / 3 için floor((2x + 3) / 6) = floor(x/3 + 1/2).
    """
    x = (3 * correct - wrong) * 100
    return (2 * x + 3) // 6


def net(correct: int, wrong: int) -> float:
    """D − Y/3, iki ondalık (yarım yukarı; Android ile aynı)."""
    return net_hundredths(correct, wrong) / 100


def weight(subject: str) -> int:
    return HEAVY_WEIGHT if _norm(subject) in {_norm(s) for s in HEAVY_SUBJECTS} else LIGHT_WEIGHT


def unit_key(question: dict) -> str:
    """Karne kırılımı 'ders|ünite|seviye'; seviye 1–5 kırpılmadan korunur."""
    lgs = question.get("lgs") or {}
    level = question.get("level")
    level = level if type(level) is int and LEVEL_MIN <= level <= LEVEL_MAX else 3
    unit = str(lgs.get("unitName") or question.get("topic") or "").strip()
    return f"{str(question.get('subject') or '').strip()}|{unit}|{level}"


def grade(questions, answers) -> dict:
    """Ders bazında D/Y/B ve net, ağırlıklı net, ünite × seviye kırılımı.

    ``answers[i]``: seçilen şık indeksi; -1 ya da eksik = boş.
    ``questions[i]['answer']``: doğru şık indeksi (karıştırılmış sıraya göre).
    """
    questions = list(questions or [])
    answers = list(answers or [])
    subjects: dict[str, dict] = {}
    units: dict[str, list[int]] = {}
    for i, q in enumerate(questions):
        subject = str(q.get("subject") or "").strip()
        cell = subjects.setdefault(subject, {"subject": subject, "correct": 0,
                                             "wrong": 0, "blank": 0})
        unit = units.setdefault(unit_key(q), [0, 0, 0])
        given = answers[i] if i < len(answers) and type(answers[i]) is int else -1
        if given < 0:
            cell["blank"] += 1
            unit[2] += 1
        elif given == q.get("answer"):
            cell["correct"] += 1
            unit[0] += 1
        else:
            cell["wrong"] += 1
            unit[1] += 1
    rows = []
    weighted = 0
    for subject, cell in subjects.items():
        hundredths = net_hundredths(cell["correct"], cell["wrong"])
        cell["net"] = hundredths / 100
        weighted += weight(subject) * hundredths
        rows.append(cell)
    return {
        "total": len(questions),
        "correct": sum(r["correct"] for r in rows),
        "wrong": sum(r["wrong"] for r in rows),
        "blank": sum(r["blank"] for r in rows),
        "subjects": rows,
        "weighted_net": weighted / 100,
        "units": units,
    }
