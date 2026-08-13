"""Localized building blocks for AliKa's collaborative story adventure."""
from __future__ import annotations


SETTINGS = {
    "tr": ["büyülü orman", "bulutların üstündeki kale", "denizaltı şehri", "gece treni", "uzay istasyonu", "hareketli panayır", "gizli kütüphane", "dağ köyü"],
    "en": ["enchanted forest", "castle above the clouds", "underwater city", "night train", "space station", "travelling fair", "secret library", "mountain village"],
    "de": ["Zauberwald", "Schloss über den Wolken", "Unterwasserstadt", "Nachtzug", "Raumstation", "Wanderjahrmarkt", "geheime Bibliothek", "Bergdorf"],
    "es": ["bosque encantado", "castillo sobre las nubes", "ciudad submarina", "tren nocturno", "estación espacial", "feria ambulante", "biblioteca secreta", "pueblo de montaña"],
    "fr": ["forêt enchantée", "château au-dessus des nuages", "cité sous-marine", "train de nuit", "station spatiale", "fête foraine itinérante", "bibliothèque secrète", "village de montagne"],
    "pt": ["floresta encantada", "castelo acima das nuvens", "cidade submarina", "trem noturno", "estação espacial", "parque de diversões itinerante", "biblioteca secreta", "aldeia na montanha"],
    "ru": ["волшебный лес", "замок над облаками", "подводный город", "ночной поезд", "космическая станция", "передвижная ярмарка", "тайная библиотека", "горная деревня"],
    "ja": ["魔法の森", "雲の上の城", "海底都市", "夜行列車", "宇宙ステーション", "旅する遊園地", "秘密の図書館", "山あいの村"],
    "ko": ["마법의 숲", "구름 위의 성", "해저 도시", "야간 열차", "우주 정거장", "이동 놀이공원", "비밀 도서관", "산골 마을"],
}

OBJECTS = {
    "tr": ["parlayan anahtar", "konuşan pusula", "uçan şemsiye", "minik hazine sandığı", "zamanı durduran saat", "görünmezlik atkısı", "şarkı söyleyen harita", "gökkuşağı feneri"],
    "en": ["glowing key", "talking compass", "flying umbrella", "tiny treasure chest", "clock that stops time", "invisibility scarf", "singing map", "rainbow lantern"],
    "de": ["leuchtender Schlüssel", "sprechender Kompass", "fliegender Regenschirm", "winzige Schatzkiste", "Uhr, die die Zeit anhält", "Unsichtbarkeitsschal", "singende Karte", "Regenbogenlaterne"],
    "es": ["llave luminosa", "brújula parlante", "paraguas volador", "cofre diminuto", "reloj que detiene el tiempo", "bufanda de invisibilidad", "mapa cantarín", "farol arcoíris"],
    "fr": ["clé lumineuse", "boussole parlante", "parapluie volant", "minuscule coffre au trésor", "horloge qui arrête le temps", "écharpe d'invisibilité", "carte chantante", "lanterne arc-en-ciel"],
    "pt": ["chave brilhante", "bússola falante", "guarda-chuva voador", "baú de tesouro minúsculo", "relógio que para o tempo", "cachecol da invisibilidade", "mapa cantante", "lanterna arco-íris"],
    "ru": ["светящийся ключ", "говорящий компас", "летающий зонтик", "крошечный сундук", "часы, останавливающие время", "шарф-невидимка", "поющая карта", "радужный фонарь"],
    "ja": ["光る鍵", "しゃべる方位磁針", "空飛ぶ傘", "小さな宝箱", "時間を止める時計", "透明マフラー", "歌う地図", "虹色のランタン"],
    "ko": ["빛나는 열쇠", "말하는 나침반", "하늘을 나는 우산", "아주 작은 보물 상자", "시간을 멈추는 시계", "투명 망토", "노래하는 지도", "무지개 등불"],
}

TWISTS = {
    "tr": ["yer birden şarkı söylemeye başlar", "herkes yalnızca kafiyeyle konuşabilir", "en küçük eşya dev olur", "gökyüzünden renkli baloncuklar yağar", "kapı yalnızca komik bir sesle açılır", "gölgen yolu göstermeye başlar", "zaman beş dakika geriye gider", "beklenmedik biri yardım teklif eder"],
    "en": ["the ground suddenly starts singing", "everyone can speak only in rhymes", "the smallest object becomes enormous", "colourful bubbles rain from the sky", "the door opens only for a funny sound", "your shadow starts showing the way", "time jumps five minutes backwards", "an unexpected helper appears"],
    "de": ["der Boden plötzlich zu singen beginnt", "alle nur noch in Reimen sprechen können", "der kleinste Gegenstand riesig wird", "bunte Blasen vom Himmel regnen", "die Tür sich nur bei einem lustigen Geräusch öffnet", "dein Schatten den Weg zeigt", "die Zeit fünf Minuten zurückspringt", "unerwartet jemand Hilfe anbietet"],
    "es": ["el suelo empieza a cantar de repente", "todos solo pueden hablar con rimas", "el objeto más pequeño se vuelve enorme", "llueven burbujas de colores", "la puerta solo se abre con un sonido divertido", "tu sombra empieza a indicar el camino", "el tiempo retrocede cinco minutos", "aparece una ayuda inesperada"],
    "fr": ["le sol se met soudain à chanter", "tout le monde ne peut parler qu'en rimes", "le plus petit objet devient gigantesque", "des bulles colorées tombent du ciel", "la porte ne s'ouvre qu'avec un son amusant", "ton ombre commence à montrer le chemin", "le temps recule de cinq minutes", "une aide inattendue apparaît"],
    "pt": ["o chão começa a cantar de repente", "todos só conseguem falar em rimas", "o menor objeto fica gigantesco", "bolhas coloridas caem do céu", "a porta só abre com um som engraçado", "sua sombra começa a mostrar o caminho", "o tempo volta cinco minutos", "surge uma ajuda inesperada"],
    "ru": ["земля внезапно начинает петь", "все могут говорить только в рифму", "самый маленький предмет становится огромным", "с неба льются разноцветные пузыри", "дверь открывается только от смешного звука", "твоя тень начинает показывать путь", "время отскакивает на пять минут назад", "появляется неожиданный помощник"],
    "ja": ["地面が突然歌い出す", "みんな韻を踏んでしか話せなくなる", "一番小さな物が巨大になる", "空から色とりどりの泡が降る", "面白い音を出すと扉が開く", "自分の影が道案内を始める", "時間が5分巻き戻る", "思いがけない助っ人が現れる"],
    "ko": ["땅이 갑자기 노래하기 시작한다", "모두 운율에 맞춰서만 말할 수 있다", "가장 작은 물건이 거대해진다", "하늘에서 알록달록한 비눗방울이 내린다", "재미있는 소리를 내야 문이 열린다", "그림자가 길을 안내하기 시작한다", "시간이 5분 전으로 돌아간다", "뜻밖의 조력자가 나타난다"],
}

CATEGORY = {
    "tr": ("Macera", "Kültürel macera"), "en": ("Adventure", "Cultural adventure"),
    "de": ("Abenteuer", "Kulturabenteuer"), "es": ("Aventura", "Aventura cultural"),
    "fr": ("Aventure", "Aventure culturelle"), "pt": ("Aventura", "Aventura cultural"),
    "ru": ("Приключение", "Культурное приключение"), "ja": ("冒険", "文化の冒険"),
    "ko": ("모험", "문화 모험"),
}
