#!/usr/bin/env python3
"""Author 15 Grade 5 mathematics error-analysis questions (grade rows 886-900)."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from build_unique_question_banks import ROOT


SOURCE = ROOT / "turkiye/5-sinif/matematik/matematik-tum.jsonl"
OUTPUT = ROOT / "authoring/question-bank-blueprints/grade-5.jsonl"
LABELS_OUTPUT = ROOT / "authoring/question-bank-blueprints/grade-5-labels.json"


# note id, stem, correct correction, three misconceptions, solution
ITEMS = [
    (
        "tr.g05.mat.5.1.1.note.01",
        "407 030 216 sayısındaki 3 rakamı için bir öğrenci 'yüz binler basamağındadır ve değeri 300 000' diyor. Bu çözümün hatasını bütünüyle düzelten ifade hangisidir?",
        "3, on binler basamağındadır; basamak değeri 30 000'dir.",
        ["3, binler basamağındadır; değeri 3 000'dir.", "3, yüz binler basamağındadır; değeri 30 000'dir.", "Sıfır bulunan bölüklerde basamak değeri belirlenemez."],
        "407 | 030 | 216 ayrımında 030 binler bölüğüdür; buradaki 3 on binler basamağında 30 000 değerini taşır.",
    ),
    (
        "tr.g05.mat.5.1.1.note.02",
        "52 006 090 sayısını bir öğrenci 'elli iki milyon altı yüz doksan' diye okuyor. Bölüklerin yerini koruyan düzeltme hangisidir?",
        "Elli iki milyon altı bin doksan.",
        ["Elli iki milyon altı yüz bin doksan.", "Beş yüz yirmi milyon altı bin dokuz.", "Elli iki bin altı milyon doksan."],
        "52 milyonlar, 006 binler ve 090 birler bölüğüdür; 006 bölüğü altı bin, 090 bölüğü doksan okunur.",
    ),
    (
        "tr.g05.mat.5.1.1.note.03",
        "'Sekiz yüz üç milyon kırk iki bin beş' ifadesini 803 420 005 yazan öğrencinin sıfır yerleştirme hatasını düzelten sayı hangisidir?",
        "Bölükleri 803 milyon | 042 bin | 005 birler olarak koruyan 803 042 005",
        ["Milyonlar bölüğünde rakamları yer değiştiren 830 042 005", "Birler bölüğündeki sıfırları sona taşıyan 803 042 500", "Binler bölüğünü kırk iki yerine dört yüz yirmi okuyan 803 420 005"],
        "Milyonlar bölüğü 803, binler bölüğü 042, birler bölüğü 005 olmalıdır; eksik basamaklar sıfırla korunur.",
    ),
    (
        "tr.g05.mat.5.1.2.note.01",
        "Her birinde 28 kalem bulunan 16 kutudan 173 kalem kullanılıyor. Bir öğrenci kalan için 16 + 28 - 173 işlemini kuruyor. Doğru işlem modeli ve sonuç hangisidir?",
        "Önce toplam stoku bulup kullanımı çıkarma: 16 × 28 - 173 = 275 kalem",
        ["Verileri ilişkisini kurmadan toplama: 16 + 28 + 173 = 217 kalem", "Çıkarma yönünü ters kurma: 173 - (16 × 28) = -275 kalem", "Kutu sayısını kullanılan miktardan çıkarıp gruplama: 28 × (173 - 16) = 4 396 kalem"],
        "Önce eş büyüklükte 16 grubun toplamı 16 × 28 = 448 bulunur; kullanılan 173 çıkarılınca 275 kalır.",
    ),
    (
        "tr.g05.mat.5.1.2.note.02",
        "398 × 21 işlemi için 400 × 20 = 8 000 tahmini yapılıyor. Kesin sonucu 8 358 bulan öğrenci, 'Tahminden farklı olduğu için sonuç yanlıştır.' diyor. Uygun değerlendirme hangisidir?",
        "8 358, 8 000'e yakın ve 398 × 21'in doğru kesin sonucudur; tahmin eşit olmak zorunda değildir.",
        ["Kesin sonuç mutlaka 8 000 olmalıdır.", "Tahmin yalnız kesin sonuçtan büyükse kullanılabilir.", "398 × 21 işleminin kesin sonucu 8 038'dir."],
        "398 × 21 = 398 × 20 + 398 = 7 960 + 398 = 8 358'dir; 8 000 yalnız makul yakınlık kontrolüdür.",
    ),
    (
        "tr.g05.mat.5.1.3.note.01",
        "2 tam 3/4 sayısını 5/4'e çeviren öğrenci, tam kısmı paya doğrudan ekliyor. Doğru dönüşüm ve gerekçesi hangisidir?",
        "2 × 4 + 3 = 11 olduğundan sonuç 11/4'tür.",
        ["2 + 3 = 5 olduğundan sonuç 5/4'tür.", "Payda da tam kısma eklenir ve sonuç 5/6 olur.", "Tam kısım paydayla çarpılır, fakat pay atıldığı için sonuç 8/4'tür."],
        "İki bütün sekiz tane dörtte bir içerir; üç tane dörtte bir daha eklenince toplam on bir tane dörtte bir olur.",
    ),
    (
        "tr.g05.mat.5.1.4.note.01",
        "Bir öğrenci 7/12'nin 9/12'den büyük olduğunu, çünkü 7'nin sayı doğrusunda önce geldiğini söylüyor. Doğru karşılaştırma hangisidir?",
        "9/12 > 7/12; paydalar eşitken daha çok eş parça alan kesir daha büyüktür.",
        ["7/12 > 9/12; küçük pay her zaman büyük kesir verir.", "7/12 = 9/12; payda eşitse bütün kesirler eşittir.", "Karşılaştırma için pay ve payda ayrı ayrı toplanmalıdır."],
        "Bütünler aynı büyüklükte on iki eş parçaya ayrılmıştır; dokuz parça yedi parçadan fazladır.",
    ),
    (
        "tr.g05.mat.5.1.4.note.02",
        "3/4 ile 5/8'i karşılaştıran öğrenci 3 < 5 olduğu için 3/4 < 5/8 sonucuna ulaşıyor. Ortak paydalı doğru düzeltme hangisidir?",
        "3/4 = 6/8 olduğundan 3/4 > 5/8'dir.",
        ["3/4 = 3/8 olduğundan 3/4 < 5/8'dir.", "Paylar ve paydalar toplanır; 8/12 elde edilir.", "Paydalar farklı olduğu için bu kesirler karşılaştırılamaz."],
        "3/4 kesrinin payı ve paydası 2 ile çarpılarak 6/8 elde edilir; 6/8, 5/8'den büyüktür.",
    ),
    (
        "tr.g05.mat.5.1.4.note.03",
        "Bir öğrenci 0,45; %45 ve 9/20 gösterimlerini farklı büyüklükler olarak sıralıyor. Miktarı koruyan doğru ilişki hangisidir?",
        "0,45 = %45 = 45/100 = 9/20",
        ["0,45 > %45 > 9/20", "%45 = 45/10 ve 0,45 = 45/1000", "9/20 = %9 ve bu nedenle en küçüktür"],
        "9/20 kesri 5 ile genişletilince 45/100 olur; bu değer hem 0,45 hem de %45 biçiminde yazılır.",
    ),
    (
        "tr.g05.mat.5.2.note.01",
        "36 + 27 = 40 + □ eşitliğinde kutuya 27 yazan öğrenci yalnız ilk toplananı artırıyor. Eşitliği koruyan düzeltme hangisidir?",
        "Kutu 23 olmalıdır; iki taraf da 63 eder.",
        ["Kutu 27 olmalıdır; eşitlik işareti yalnız sonucu başlatır.", "Kutu 31 olmalıdır; 36'daki 4 fark öteki tarafa eklenir.", "Kutu 67 olmalıdır; eşitliğin iki tarafı toplanır."],
        "36'yı 40 yapmak için 4 eklenmiştir; toplam 63 sabit kalacağından 27'den 4 çıkarılıp 23 bulunur.",
    ),
    (
        "tr.g05.mat.5.2.note.02",
        "18 + 6 × 4 işlemini soldan sağa 24 × 4 = 96 bulan öğrenci hangi düzeltmeyi yapmalıdır?",
        "İşlem önceliğini kullanma: Önce 6 × 4 = 24, sonra 18 + 24 = 42 yapılmalıdır.",
        ["Soldan sağa koşulsuz ilerleme: Önce 18 + 6 = 24, sonra 24 × 4 = 96 yapılmalıdır.", "Çarpmanın iki yanındaki sayıları eşleştirme: Önce 18 × 4 = 72, sonra 6 eklenip 78 bulunmalıdır.", "İşlem işaretlerini tek adıma indirme: Toplama ve çarpma aynı anda yapılıp 28 bulunmalıdır."],
        "Parantez olmadığında çarpma toplama işleminden önce yapılır; bu nedenle doğru sonuç 42'dir.",
    ),
    (
        "tr.g05.mat.5.2.note.03",
        "5, 11, 17, 23, ... örüntüsünün beşinci terimini 35 bulan öğrenci artış miktarını değiştiriyor. Doğru sonuç hangisidir?",
        "Kural her adımda 6 eklemektir; beşinci terim 29'dur.",
        ["Kural her adımda 12 eklemektir; beşinci terim 35'tir.", "Kural sırayla 6 ve 12 eklemektir; beşinci terim 41'dir.", "Yalnız ilk iki terimden sonra kural belirlenemez."],
        "Ardışık farkların tümü 6'dır; 23 + 6 = 29 işlemi beşinci terimi verir.",
    ),
    (
        "tr.g05.mat.5.2.note.04",
        "864 ÷ 24 işleminin sonucunu 34 bulan öğrenci kontrol için 24 × 34 = 816 hesaplıyor ve işlemi bitiriyor. Algoritmayı doğrulayan düzeltme hangisidir?",
        "864 ÷ 24 = 36'dır; çünkü 24 × 36 = 864 olur.",
        ["Sonuç 34'tür; bölmede çarpma ile kontrol yapılmaz.", "Sonuç 38'dir; çünkü 864 - 816 = 48 doğrudan bölüme eklenir.", "Sonuç 816'dır; bölme işlemi ilk ara çarpımda biter."],
        "816 ile 864 arasında 48 fark vardır ve 48 iki tane 24 içerir; 34 + 2 = 36 bulunur ve çarpımla doğrulanır.",
    ),
    (
        "tr.g05.mat.5.4.note.01",
        "Çevresi 62 cm, uzun kenarı 18 cm olan dikdörtgende kısa kenarı 62 - 18 = 44 cm bulan öğrenci hangi düzeltmeyi yapmalıdır?",
        "Yarı çevre 31 cm'dir; kısa kenar 31 - 18 = 13 cm olur.",
        ["Çevre 4'e bölünür; iki kenar da 15,5 cm olur.", "Kısa kenar 44 cm'dir; çevreden bir uzun kenar çıkarmak yeterlidir.", "Kısa kenar 26 cm'dir; çevreden iki uzun kenar çıkarılıp sonuç değişmeden alınır."],
        "Dikdörtgende bir uzun ve bir kısa kenarın toplamı çevrenin yarısıdır; 18 + 13 = 31 ve 2 × 31 = 62'dir.",
    ),
    (
        "tr.g05.mat.5.5.note.01",
        "Tabloda her çizgi 3 öğrenciyi göstermektedir. Sütun yükseklikleri I için 4, II için 7, III için 5 çizgidir. Öğrenci sıklıkları 4, 7, 5 ve toplamı 16 okuyor. Ölçek hatasını düzelten sonuç hangisidir?",
        "Ölçeği her kategoriye uygulama: Sıklıklar 12, 21 ve 15; toplam 48 öğrencidir.",
        ["Çizgi yüksekliğini sıklık sanma: Sıklıklar 4, 7 ve 5; toplam 16 öğrencidir.", "Ölçeği yalnız en yüksek sütuna uygulama: Yalnız II çarpılır ve toplam 30 sanılır.", "Ölçeği ters işlemle kullanma: Çizgi sayıları 3'e bölünür ve toplam 16/3 sanılır."],
        "Her sütunun çizgi sayısı ölçek değeri 3 ile ayrı ayrı çarpılır: 4 × 3 = 12, 7 × 3 = 21, 5 × 3 = 15.",
    ),
]


def notes() -> dict[str, dict[str, Any]]:
    rows = [json.loads(line) for line in SOURCE.read_text(encoding="utf-8-sig").splitlines() if line.strip()]
    return {str(row.get("id")): row for row in rows if row.get("type") == "note"}


def rotate(values: list[str], reasons: list[str], target: int) -> tuple[list[str], list[str]]:
    return (
        [*values[1:1 + target], values[0], *values[1 + target:]],
        [*reasons[1:1 + target], reasons[0], *reasons[1 + target:]],
    )


def data_table(qid: str, labels: dict[str, str]) -> dict[str, Any]:
    prefix = qid.replace("-", ".")
    h1, h2, alt = f"{prefix}.h1", f"{prefix}.h2", f"{prefix}.alt"
    labels[h1], labels[h2] = "Kategori", "Sütun yüksekliği (çizgi)"
    labels[alt] = "Üç kategorinin sütun yüksekliklerini 4, 7 ve 5 çizgi olarak veren tablo; sıklıklar hesaplanmamıştır."
    return {
        "kind": "table", "headerKeys": [h1, h2], "altTextKey": alt,
        "rows": [[{"v": "I"}, {"v": "4"}], [{"v": "II"}, {"v": "7"}], [{"v": "III"}, {"v": "5"}]],
    }


def make(local: int, entry: tuple[Any, ...], note_map: dict[str, dict[str, Any]], labels: dict[str, str]) -> dict[str, Any]:
    note_id, stem, correct_text, wrongs, explanation = entry
    note = note_map[note_id]
    objective = str((note.get("objectives") or [""])[0])
    global_number = 885 + local
    correct = (global_number - 1) % 4
    raw_choices = [correct_text, *wrongs]
    raw_reasons = [
        f"Doğru matematiksel denetim: {explanation}",
        f"İlk işlem yanılgısı: Bu seçenek verilen basamak, işlem veya karşılaştırma ilişkisini değiştirmeden kontrol etmez. {explanation}",
        f"Kuralı eksik uygulama yanılgısı: Bu seçenek gerekli dönüşümün ya da işlem sırasının yalnız bir bölümünü uygular. {explanation}",
        f"Dayanaksız sonuç yanılgısı: Bu seçenekteki değer verilenlerden programdaki kuralla elde edilemez. {explanation}",
    ]
    choices, distractor_why = rotate(raw_choices, raw_reasons, correct)
    qid = f"tr-g05-bank-mat-s01-q{local:03d}"
    fig = data_table(qid, labels) if local == 15 else None
    visual_need = ({
        "level": "required", "role": "evidence",
        "rationale": "Kategori sütunlarının çizgi yükseklikleri yalnız tabloda birlikte gösterilir.",
        "acceptableKinds": ["table"], "evidenceDimensions": ["kategori", "çizgi yüksekliği", "ölçek"],
    } if fig else {
        "level": "none", "role": "none",
        "rationale": "Hatalı öğrenci işlemi ve düzeltme için gereken bütün sayısal veriler metinde verilmiştir.",
        "acceptableKinds": [], "evidenceDimensions": [],
    })
    level = 3 if local <= 5 else 4
    return {
        "type": "question", "id": qid, "questionId": qid, "questionNumber": global_number,
        "subject": "Matematik", "grade": 5,
        "unitKey": note.get("unitKey"), "topicKey": note.get("topicKey"),
        "subtopicKey": note.get("subtopicKey"), "topic": note.get("topic"),
        "title": f"{note['title']} — hata analizi",
        "objective": objective, "objectiveId": objective,
        "noteId": note_id, "noteKey": note_id,
        "question": stem, "choices": choices, "correct": correct,
        "correctIndex": correct, "correctOption": choices[correct],
        "distractorWhy": distractor_why,
        "explanation": f"Öğrenci çözümü verilen ilişkiyle yeniden kontrol edilir. {explanation}",
        "level": level,
        "difficultyReason": (
            f"Düzey {level}; hazır sonucu seçmek yerine öğrencinin işlemindeki kavramsal yanılgıyı bulmayı, "
            "doğru yöntemi uygulamayı ve sonucu ters işlemle denetlemeyi gerektirir."
        ),
        "questionType": "error-analysis", "familyId": f"tr-g05-bank-mat-family-{global_number:03d}",
        "objectiveSource": note.get("objectiveSource"),
        "objectiveEvidenceId": note.get("objectiveEvidenceId"),
        "sourceRefs": note.get("sourceRefs") or [], "visualNeed": visual_need, "figure": fig,
        "hintsCount": 0, "hintsForbidden": True,
    }


def main() -> int:
    existing = [json.loads(line) for line in OUTPUT.read_text(encoding="utf-8").splitlines() if line.strip()]
    if len(existing) != 885:
        raise RuntimeError("the 885 science and English questions must be regenerated first")
    labels = json.loads(LABELS_OUTPUT.read_text(encoding="utf-8"))
    note_map = notes()
    rows = [make(local, entry, note_map, labels) for local, entry in enumerate(ITEMS, 1)]
    OUTPUT.write_text(
        "\n".join(json.dumps(row, ensure_ascii=False, separators=(",", ":")) for row in [*existing, *rows]) + "\n",
        encoding="utf-8", newline="\n",
    )
    LABELS_OUTPUT.write_text(
        json.dumps(labels, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
        encoding="utf-8", newline="\n",
    )
    print(json.dumps({"mathQuestions": 15, "mathTotal": 15, "gradeTotal": 900}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
