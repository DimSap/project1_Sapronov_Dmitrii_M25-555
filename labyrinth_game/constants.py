ROOMS = {
    'entrance': {
        'description': 'Вы в темном входе лабиринта. Стены покрыты мхом. На полу лежит старый факел.',
        'exits': {'north': 'hall', 'east': 'trap_room'},
        'items': ['torch'],
        'puzzle': None,
        'reward': None,
    },
    'hall': {
        'description': 'Большой зал с эхом. По центру стоит пьедестал с запечатанным сундуком.',
        'exits': {'south': 'entrance', 'west': 'library', 'north': 'treasure_room'},
        'items': [],
        'puzzle': (
            'На пьедестале надпись: "Назовите число, которое идет после девяти". Введите ответ цифрой или словом.',
            ['10', 'десять'],
        ),
        'reward': 'treasure_key',
    },
    'trap_room': {
        'description': 'Комната с хитрой плиточной поломкой. На стене видна надпись: "Осторожно — ловушка".',
        'exits': {'west': 'entrance'},
        'items': ['rusty_key'],
        'puzzle': (
            'Система плит активна. Чтобы пройти, назовите слово "шаг" три раза подряд (введите "шаг шаг шаг")',
            ['шаг шаг шаг'],
        ),
        'reward': 'old_map',
    },
    'library': {
        'description': 'Пыльная библиотека. На полках старые свитки. Где-то здесь может быть ключ от сокровищницы.',
        'exits': {'east': 'hall', 'north': 'armory'},
        'items': ['ancient_book'],
        'puzzle': (
            'В одном свитке загадка: "Что растет, когда его съедают?" (ответ одно слово)',
            ['резонанс'],
        ),
        'reward': 'book_of_shadows',
    },
    'armory': {
        'description': 'Старая оружейная комната. На стене висит меч, рядом — небольшая бронзовая шкатулка.',
        'exits': {'south': 'library', 'east': 'observatory'},
        'items': ['sword', 'bronze_box'],
        'puzzle': None,
        'reward': None,
    },
    'observatory': {
        'description': 'Небольшая обсерватория под куполом. Через трещину в крыше видно звезды.',
        'exits': {'west': 'armory', 'north': 'riddle_room'},
        'items': ['star_chart'],
        'puzzle': (
            'Сколько букв в слове "пять"? Введите число.',
            ['4', 'четыре'],
        ),
        'reward': 'bronze_key',
    },
    'riddle_room': {
        'description': 'Комната загадок: стены покрыты символами и стрелками, указывающими на потайные двери.',
        'exits': {'south': 'observatory', 'east': 'treasure_room'},
        'items': ['silver_key'],
        'puzzle': (
            'Назовите столицу Франции (ответ одно слово).',
            ['париж', 'Paris'],
        ),
        'reward': 'armor',
    },
    'treasure_room': {
        'description': 'Комната, на столе большой сундук. Дверь заперта — нужен особый ключ.',
        'exits': {'south': 'hall', 'west': 'riddle_room'},
        'items': ['treasure_chest'],
        'puzzle': (
            'Дверь защищена кодом. Введите код (подсказка: это число пятикратного шага, 2*5= ? )',
            ['10', 'десять'],
        ),
        'reward': None,
    },
}


COMMANDS = {
    "go <direction>": "перейти в направлении (north/south/east/west)",
    "look": "осмотреть текущую комнату",
    "take <item>": "поднять предмет",
    "use <item>": "использовать предмет из инвентаря",
    "inventory": "показать инвентарь",
    "solve": "попытаться решить загадку в комнате",
    "quit": "выйти из игры",
    "help": "показать это сообщение",
    "north|south|east|west": "движение без 'go' (например, 'north')",
}

# Параметры вероятностей и событий
EVENT_PROBABILITY_MODULO = 10  # Вероятность срабатывания случайного события при перемещении (1 из 10)
RANDOM_EVENT_KIND_COUNT = 3    # Количество типов случайных событий
TRAP_DEATH_PROBABILITY_MODULO = 10  # Диапазон для проверки урона ловушки
TRAP_DEATH_THRESHOLD = 3            # Порог, ниже которого ловушка заканчивает игру

# Коэффициенты псевдослучайного генератора
PRNG_MULTIPLIER = 12.9898
PRNG_SCALE = 43758.5453
