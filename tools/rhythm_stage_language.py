"""Localized stage and instrument themes for AliKa Rhythm Stage."""
from __future__ import annotations


KITS = {
    "tr": [
        {"stage": "Anadolu meydanı", "primary": "darbuka", "primary_sound": "hand_drum", "secondary": "zil", "secondary_sound": "metal_bell"},
        {"stage": "Ege şenliği", "primary": "tef", "primary_sound": "frame_drum", "secondary": "el çırpması", "secondary_sound": "clap"},
        {"stage": "Karadeniz yaylası", "primary": "davul", "primary_sound": "bass_drum", "secondary": "tahta kaşık", "secondary_sound": "wood_click"},
        {"stage": "İstanbul ritim sahnesi", "primary": "bendir", "primary_sound": "frame_drum", "secondary": "çan", "secondary_sound": "bell"},
        {"stage": "Akdeniz gecesi", "primary": "ritim davulu", "primary_sound": "hand_drum", "secondary": "şakşak", "secondary_sound": "wood_click"},
    ],
    "en": [
        {"stage": "jazz club", "primary": "snare drum", "primary_sound": "snare", "secondary": "hand clap", "secondary_sound": "clap"},
        {"stage": "village fair", "primary": "tambourine", "primary_sound": "frame_drum", "secondary": "handbell", "secondary_sound": "bell"},
        {"stage": "parade square", "primary": "marching drum", "primary_sound": "bass_drum", "secondary": "wood block", "secondary_sound": "wood_click"},
        {"stage": "island festival", "primary": "steel pan", "primary_sound": "metal_bell", "secondary": "shaker", "secondary_sound": "shaker"},
        {"stage": "family music hall", "primary": "hand drum", "primary_sound": "hand_drum", "secondary": "finger snap", "secondary_sound": "clap"},
    ],
    "de": [
        {"stage": "Alpenfest", "primary": "Rahmentrommel", "primary_sound": "frame_drum", "secondary": "Kuhglocke", "secondary_sound": "bell"},
        {"stage": "Stadtplatz", "primary": "Marschtrommel", "primary_sound": "snare", "secondary": "Holzblock", "secondary_sound": "wood_click"},
        {"stage": "Wintermarkt", "primary": "Handtrommel", "primary_sound": "hand_drum", "secondary": "Glöckchen", "secondary_sound": "metal_bell"},
        {"stage": "Volksmusikbühne", "primary": "Tamburin", "primary_sound": "frame_drum", "secondary": "Klatschen", "secondary_sound": "clap"},
        {"stage": "Rheinuferfest", "primary": "Basstrommel", "primary_sound": "bass_drum", "secondary": "Rassel", "secondary_sound": "shaker"},
    ],
    "es": [
        {"stage": "patio andaluz", "primary": "cajón", "primary_sound": "hand_drum", "secondary": "palmas", "secondary_sound": "clap"},
        {"stage": "plaza de fiesta", "primary": "bombo", "primary_sound": "bass_drum", "secondary": "campana", "secondary_sound": "bell"},
        {"stage": "escenario caribeño", "primary": "conga", "primary_sound": "hand_drum", "secondary": "maracas", "secondary_sound": "shaker"},
        {"stage": "encuentro de montaña", "primary": "tambor de marco", "primary_sound": "frame_drum", "secondary": "claves", "secondary_sound": "wood_click"},
        {"stage": "festival del puerto", "primary": "tambor", "primary_sound": "snare", "secondary": "cencerro", "secondary_sound": "metal_bell"},
    ],
    "fr": [
        {"stage": "place de village", "primary": "tambourin", "primary_sound": "frame_drum", "secondary": "cloche", "secondary_sound": "bell"},
        {"stage": "quai en fête", "primary": "tambour", "primary_sound": "snare", "secondary": "claquement de mains", "secondary_sound": "clap"},
        {"stage": "bal populaire", "primary": "grosse caisse", "primary_sound": "bass_drum", "secondary": "hochet", "secondary_sound": "shaker"},
        {"stage": "cour provençale", "primary": "tambour à main", "primary_sound": "hand_drum", "secondary": "bloc de bois", "secondary_sound": "wood_click"},
        {"stage": "scène lumineuse", "primary": "tambour sur cadre", "primary_sound": "frame_drum", "secondary": "carillon", "secondary_sound": "metal_bell"},
    ],
    "pt": [
        {"stage": "roda brasileira", "primary": "pandeiro", "primary_sound": "frame_drum", "secondary": "agogô", "secondary_sound": "metal_bell"},
        {"stage": "festa de rua", "primary": "surdo", "primary_sound": "bass_drum", "secondary": "reco-reco", "secondary_sound": "wood_click"},
        {"stage": "praça portuguesa", "primary": "adufe", "primary_sound": "frame_drum", "secondary": "palmas", "secondary_sound": "clap"},
        {"stage": "palco atlântico", "primary": "tambor de mão", "primary_sound": "hand_drum", "secondary": "chocalho", "secondary_sound": "shaker"},
        {"stage": "festival do porto", "primary": "caixa", "primary_sound": "snare", "secondary": "sino", "secondary_sound": "bell"},
    ],
    "ru": [
        {"stage": "деревенская ярмарка", "primary": "бубен", "primary_sound": "frame_drum", "secondary": "деревянные ложки", "secondary_sound": "wood_click"},
        {"stage": "городская сцена", "primary": "барабан", "primary_sound": "snare", "secondary": "колокольчики", "secondary_sound": "bell"},
        {"stage": "зимний праздник", "primary": "ручной барабан", "primary_sound": "hand_drum", "secondary": "трещотка", "secondary_sound": "shaker"},
        {"stage": "площадь мастеров", "primary": "большой барабан", "primary_sound": "bass_drum", "secondary": "хлопки", "secondary_sound": "clap"},
        {"stage": "северный фестиваль", "primary": "рамочный барабан", "primary_sound": "frame_drum", "secondary": "металлический звонок", "secondary_sound": "metal_bell"},
    ],
    "ja": [
        {"stage": "夏祭りの舞台", "primary": "太鼓", "primary_sound": "bass_drum", "secondary": "鉦", "secondary_sound": "metal_bell"},
        {"stage": "竹林の広場", "primary": "締太鼓", "primary_sound": "snare", "secondary": "拍子木", "secondary_sound": "wood_click"},
        {"stage": "城下町の舞台", "primary": "鼓", "primary_sound": "hand_drum", "secondary": "鈴", "secondary_sound": "bell"},
        {"stage": "海辺の祭り", "primary": "団扇太鼓", "primary_sound": "frame_drum", "secondary": "手拍子", "secondary_sound": "clap"},
        {"stage": "光の音楽堂", "primary": "平太鼓", "primary_sound": "bass_drum", "secondary": "鳴子", "secondary_sound": "shaker"},
    ],
    "ko": [
        {"stage": "마을 축제마당", "primary": "장구", "primary_sound": "hand_drum", "secondary": "꽹과리", "secondary_sound": "metal_bell"},
        {"stage": "궁궐 뜰", "primary": "북", "primary_sound": "bass_drum", "secondary": "박", "secondary_sound": "wood_click"},
        {"stage": "바닷가 공연장", "primary": "소고", "primary_sound": "frame_drum", "secondary": "손뼉", "secondary_sound": "clap"},
        {"stage": "산골 잔치", "primary": "장구", "primary_sound": "hand_drum", "secondary": "방울", "secondary_sound": "bell"},
        {"stage": "빛의 음악당", "primary": "큰북", "primary_sound": "bass_drum", "secondary": "흔들이", "secondary_sound": "shaker"},
    ],
}
