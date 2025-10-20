from labyrinth_game.constants import ROOMS
import math

def show_help():
    print("\nДоступные команды:")
    print("  go <direction>  - перейти в направлении (north/south/east/west)")
    print("  look            - осмотреть текущую комнату")
    print("  take <item>     - поднять предмет")
    print("  use <item>      - использовать предмет из инвентаря")
    print("  inventory       - показать инвентарь")
    print("  solve           - попытаться решить загадку в комнате")
    print("  quit            - выйти из игры")
    print("  help            - показать это сообщение") 

def describe_current_room(game_state):
    """
    Выводит описание текущей комнаты на экран на основе состояния игры.
    Ожидается, что в game_state есть ключ 'current_room' с именем комнаты.
    """
    current_room_name = game_state.get('current_room')
    room = ROOMS.get(current_room_name, {})

    # Название комнаты в верхнем регистре
    if current_room_name:
        print(f"== {current_room_name.upper()} ==")

    # Описание комнаты
    description = room.get('description')
    if description:
        print(description)

    # Список видимых предметов
    items = room.get('items', [])
    if items:
        print(f"Заметные предметы: {', '.join(items)}")

    # Доступные выходы
    exits = room.get('exits', {})
    if exits:
        print(f"Выходы: {', '.join(exits.keys())}")

    # Сообщение о наличии загадки
    if room.get('puzzle'):
        print("Кажется, здесь есть загадка (используйте команду solve).")


def solve_puzzle(game_state):
    """
    Пытается решить загадку в текущей комнате.

    Если загадки нет — сообщает об этом. Если ответ верный, убирает загадку из
    комнаты и добавляет игроку награду.
    """
    from labyrinth_game.player_actions import get_input

    current_room_name = game_state.get('current_room')
    room = ROOMS.get(current_room_name, {})
    puzzle = room.get('puzzle')

    if not puzzle:
        print("Загадок здесь нет.")
        return

    question, right_answer = puzzle
    print(question)

    user_answer = get_input("Ваш ответ: ").strip().lower()
    if user_answer == str(right_answer).strip().lower():
        print("Верно! Вы разгадали загадку.")
        # Убираем загадку, чтобы её нельзя было решить повторно
        room['puzzle'] = None

        # Награда: выдаём ключ от сокровищницы, если его ещё нет
        inventory = game_state.setdefault('player_inventory', [])
        if 'treasure_key' not in inventory:
            inventory.append('treasure_key')
            print("Вы получаете награду: treasure_key.")
    else:
        print("Неверно. Попробуйте снова.")


def attempt_open_treasure(game_state):
    """
    Пытается открыть сундук в комнате сокровищ.

    С ключом — немедленное открытие и победа. Без ключа — предложение ввести
    код (ответ загадки комнаты). При успехе — победа.
    """
    from labyrinth_game.player_actions import get_input

    current_room_name = game_state.get('current_room')
    room = ROOMS.get(current_room_name, {})
    items = room.get('items', [])

    if 'treasure_chest' not in items:
        print("Здесь нет сундука.")
        return

    inventory = game_state.get('player_inventory', [])
    if 'treasure_key' in inventory:
        print("Вы применяете ключ, и замок щёлкает. Сундук открыт!")
        items.remove('treasure_chest')
        print("В сундуке сокровище! Вы победили!")
        game_state['game_over'] = True
        return

    choice = get_input("Сундук заперт. У вас нет ключа. Ввести код? (да/нет): ").strip().lower()
    if choice == 'да':
        puzzle = room.get('puzzle')
        _, right_answer = puzzle
        code = get_input("Введите код: ").strip().lower()
        if code == str(right_answer).strip().lower():
            print("Код верный. Сундук открыт!")
            items.remove('treasure_chest')
            print("В сундуке сокровище! Вы победили!")
            game_state['game_over'] = True
        else:
            print("Неверный код. Замок не поддается.")
    else:
        print("Вы отступаете от сундука.")


def pseudo_random(seed, modulo):
    """Детерминированный псевдослучайный генератор на базе синуса.

    Возвращает целое в диапазоне [0, modulo).
    """
    if modulo <= 0:
        return 0
    x = math.sin(seed * 12.9898) * 43758.5453
    fractional_part = x - math.floor(x)
    return int(math.floor(fractional_part * modulo))


def trigger_trap(game_state):
    """Симулирует срабатывание ловушки с негативными последствиями."""
    print("Ловушка активирована! Пол стал дрожать...")

    inventory = game_state.get('player_inventory', [])
    steps = game_state.get('steps_taken', 0)

    if inventory:
        index_to_remove = pseudo_random(steps, len(inventory))
        lost_item = inventory.pop(index_to_remove)
        print(f"Вы потеряли предмет: {lost_item}")
        return

    # Инвентарь пуст — риск урона/поражения
    roll = pseudo_random(steps, 10)  # 0..9
    if roll < 3:
        print("Ловушка сработала слишком сильно! Вы падаете и теряете сознание. Игра окончена.")
        game_state['game_over'] = True
    else:
        print("Вы чудом уцелели, но это было опасно.")


def random_event(game_state):
    """Случайные события, происходящие при перемещении игрока."""
    steps = game_state.get('steps_taken', 0)

    # Низкая вероятность события
    if pseudo_random(steps, 10) != 0:
        return

    current_room_name = game_state.get('current_room')
    room = ROOMS.get(current_room_name, {})
    inventory = game_state.get('player_inventory', [])

    event_kind = pseudo_random(steps + 1, 3)  # 0..2

    if event_kind == 0:
        # Находка
        print("Вы замечаете на полу монетку.")
        items = room.setdefault('items', [])
        items.append('coin')
        print("В этой комнате теперь лежит: coin.")
    elif event_kind == 1:
        # Испуг
        print("Где-то рядом слышится шорох... Вы настораживаетесь.")
        if 'sword' in inventory:
            print("Вы инстинктивно вскидываете меч — существо отступает.")
    else:
        # Срабатывание ловушки (в опасной комнате и без факела)
        if current_room_name == 'trap_room' and 'torch' not in inventory:
            print("Воздух сгущается — что-то не так! Это место опасно без света.")
            trigger_trap(game_state)
