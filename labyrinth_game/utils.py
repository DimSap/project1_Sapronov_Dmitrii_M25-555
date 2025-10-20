from labyrinth_game.constants import ROOMS

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
