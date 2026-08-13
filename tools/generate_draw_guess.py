"""Generate deterministic draw-and-guess pools for every AliKa language and age band."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from charades_language import ACTIONS, CATEGORY, LANGUAGES, SUBJECTS


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "games" / "draw-guess" / "cards"
BANDS = ("young", "mid", "teen", "senior")
SOURCE = "https://shop.mattel.com/products/pictionary-dkd47"
TIPS = {
    "tr": ["Önce büyük şekli çiz.", "Basit çizgiler kullan.", "En belirgin ayrıntıyı ekle.", "Resmi parçalara ayır."],
    "en": ["Draw the big shape first.", "Use simple lines.", "Add the clearest detail.", "Split the picture into parts."],
    "de": ["Zeichne zuerst die große Form.", "Nutze einfache Linien.", "Füge das deutlichste Detail hinzu.", "Teile das Bild in Teile."],
    "es": ["Dibuja primero la forma grande.", "Usa líneas sencillas.", "Añade el detalle más claro.", "Divide el dibujo en partes."],
    "fr": ["Dessine d'abord la grande forme.", "Utilise des lignes simples.", "Ajoute le détail le plus clair.", "Divise le dessin en parties."],
    "pt": ["Desenhe primeiro a forma maior.", "Use linhas simples.", "Acrescente o detalhe mais claro.", "Divida o desenho em partes."],
    "ru": ["Сначала нарисуй большую форму.", "Используй простые линии.", "Добавь самую заметную деталь.", "Раздели рисунок на части."],
    "ja": ["まず大きな形を描こう。", "簡単な線を使おう。", "一番分かりやすい特徴を足そう。", "絵をいくつかの部分に分けよう。"],
    "ko": ["큰 모양부터 그려요.", "간단한 선을 사용해요.", "가장 눈에 띄는 특징을 더해요.", "그림을 여러 부분으로 나눠요."],
}


def _id(language: str, band: str, subject_index: int, action_index: int) -> str:
    raw = f"draw-guess-v1:{language}:{band}:{subject_index}:{action_index}".encode()
    return "drw_" + hashlib.sha256(raw).hexdigest()[:20]


def generate() -> None:
    for language in LANGUAGES:
        subjects = SUBJECTS[language]
        for band in BANDS:
            actions = ACTIONS[band][language]
            rows = []
            for subject_index, subject in enumerate(subjects):
                local = subject_index >= 20
                for action_index, action in enumerate(actions):
                    rows.append({
                        "card_id": _id(language, band, subject_index, action_index),
                        "prompt": f"{subject} — {action}",
                        "category": CATEGORY[language][1 if local else 0],
                        "difficulty": BANDS.index(band) + 1,
                        "draw_tip": TIPS[language][(subject_index + action_index) % 4],
                        "source": {"title": "Official family drawing game design", "url": SOURCE},
                        "culture_tags": [f"culture:{language}"] if local else ["culture:universal"],
                        "review_status": "ai-draft",
                    })
            if len(rows) != 200:
                raise ValueError(f"{language}/{band}: expected 200 cards")
            path = OUT / language / f"{band}.jsonl"
            path.parent.mkdir(parents=True, exist_ok=True)
            text = "".join(json.dumps(row, ensure_ascii=False, sort_keys=True,
                                      separators=(",", ":")) + "\n" for row in rows)
            path.write_text(text, encoding="utf-8", newline="\n")


def main() -> int:
    argparse.ArgumentParser().parse_args()
    generate()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
