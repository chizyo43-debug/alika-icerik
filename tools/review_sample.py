"""Build a deterministic AI-review sample for changed Grade 5 packages.

The report never claims human review. One question is selected for every
objective in the English and Social Studies packages, so no curriculum strand
can disappear behind a global random sample.
"""
from __future__ import annotations

import hashlib
import json
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
OUTPUT = ROOT / "reports" / "GRADE5_AI_REVIEW_SAMPLE.md"
TARGETS = (
    ROOT / "turkiye" / "5-sinif" / "ingilizce" / "ingilizce-tum.jsonl",
    ROOT
    / "turkiye"
    / "5-sinif"
    / "sosyal-bilgiler"
    / "sosyal-bilgiler-tum.jsonl",
)


def read_jsonl(path: Path) -> list[dict]:
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8-sig").splitlines()
        if line.strip()
    ]


def choose_by_objective(questions: list[dict]) -> list[dict]:
    grouped: dict[str, list[dict]] = defaultdict(list)
    for question in questions:
        grouped[str(question.get("objective") or "PENDING")].append(question)
    selected = []
    for objective, rows in sorted(grouped.items()):
        selected.append(
            min(
                rows,
                key=lambda row: hashlib.sha256(
                    f"2026-08-07\0{objective}\0{row['id']}".encode("utf-8")
                ).hexdigest(),
            )
        )
    return selected


def build_report() -> str:
    lines = [
        "# 5. Sınıf Bağımsız AI İnceleme Örneklemi",
        "",
        "**Tarih:** 7 Ağustos 2026",
        "",
        "**İnceleyen:** Codex Sol (`ai-only`, insan onayı yok)",
        "",
        "**Yöntem:** Değişen İngilizce ve Sosyal Bilgiler paketlerinde her "
        "kazanımdan deterministik bir soru; doğru cevap, açıklama, çeldirici "
        "gerekçeleri, not bağı ve görsel erişilebilirliği birlikte incelenir.",
        "",
        "> Bu dosya insan onayı iddia etmez. Tam paketler ayrıca tüm kayıtları "
        "kapsayan deterministik doğrulayıcı ve gerçek AliKa içe aktarma "
        "kapısından geçmek zorundadır.",
        "",
    ]
    total = 0
    for path in TARGETS:
        rows = read_jsonl(path)
        pack = next(row for row in rows if row.get("type") == "pack")
        notes = {
            row["id"]: row for row in rows if row.get("type") == "note"
        }
        questions = [
            row for row in rows if row.get("type") == "question"
        ]
        selected = choose_by_objective(questions)
        total += len(selected)
        lines.extend(
            [
                f"## {pack['subject']}",
                "",
                f"- Paket: `{path.relative_to(ROOT).as_posix()}`",
                f"- Kapsama: {len(selected)}/{len(questions)} soru; "
                f"{len(selected)} kazanımın tamamından birer kayıt",
                "",
            ]
        )
        for question in selected:
            note = notes.get(question.get("noteId"), {})
            correct = question["choices"][question["correct"]]
            figure = question.get("figure")
            figure_kind = (
                figure.get("kind", "yok")
                if isinstance(figure, dict)
                else "yok"
            )
            lines.extend(
                [
                    f"### {question['id']}",
                    "",
                    f"- Kazanım: `{question.get('objective')}`",
                    f"- Konu anlatımı: `{question.get('noteId')}` — "
                    f"{note.get('title', 'BULUNAMADI')}",
                    f"- Soru: {question['question']}",
                    f"- Doğru cevap: **{correct}**",
                    f"- Açıklama: {question.get('explanation', '')}",
                    f"- Doğru cevap gerekçesi: "
                    f"{question.get('distractorWhy', [])[question['correct']]}",
                    f"- Görsel: {figure_kind}",
                    "",
                ]
            )
    lines.extend(
        [
            "## Kapsama özeti",
            "",
            f"- İncelenecek kayıt: **{total}**",
            "- Seçim rastgele kullanıcı girdisine bağlı değildir; aynı içerik "
            "aynı örneklemi üretir.",
            "- Yayın kararı yalnız bu örnekleme dayanmaz.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> None:
    OUTPUT.write_text(build_report(), encoding="utf-8", newline="\n")
    print(OUTPUT.relative_to(ROOT).as_posix())


if __name__ == "__main__":
    main()
