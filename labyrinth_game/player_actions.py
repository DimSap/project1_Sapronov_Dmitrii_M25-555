from labyrinth_game.constants import ROOMS
from labyrinth_game.utils import describe_current_room, random_event

def show_inventory(game_state):
    """Отображает содержимое инвентаря игрока или сообщает, что он пуст."""
    inventory = game_state.get('player_inventory', [])
    if inventory:
        print(f"Инвентарь: {', '.join(inventory)}")
    else:
        print("Инвентарь пуст.")


def get_input(prompt = "> "):
    """Запрашивает ввод пользователя. Возвращает строку команды.

    При прерывании ввода (Ctrl+C / Ctrl+D) возвращает команду 'quit'.
    """
    try:
        return input(prompt).strip()
    except (KeyboardInterrupt, EOFError):
        print("\nВыход из игры.")
        return "quit"


def move_player(game_state, direction):
    """Перемещает игрока в указанном направлении, если выход существует.

    Обновляет текущую комнату, увеличивает счётчик шагов и выводит её описание.
    Если выхода нет, сообщает об этом.
    """

    current_room_name = game_state.get('current_room')
    room = ROOMS.get(current_room_name, {})
    exits = room.get('exits', {})

    next_room = exits.get(direction)
    if next_room:
        # Проверка доступа в комнату сокровищ
        if next_room == 'treasure_room':
            inventory = game_state.get('player_inventory', [])
            if 'rusty_key' in inventory:
                print("Вы используете найденный ключ, чтобы открыть путь в комнату сокровищ.")
            else:
                print("Дверь заперта. Нужен ключ, чтобы пройти дальше.")
                return

        game_state['current_room'] = next_room
        game_state['steps_taken'] = game_state.get('steps_taken', 0) + 1
        describe_current_room(game_state)
        # Случайные события после успешного перемещения
        random_event(game_state)
    else:
        print("Нельзя пойти в этом направлении.")


def take_item(game_state, item_name):
    """Подбирает предмет из текущей комнаты, если он там есть."""

    current_room_name = game_state.get('current_room')
    room = ROOMS.get(current_room_name, {})
    items = room.get('items', [])

    if item_name in items:
        if item_name == 'treasure_chest':
            print("Вы не можете поднять сундук, он слишком тяжелый.")
            return
            
        inventory = game_state.setdefault('player_inventory', [])
        inventory.append(item_name)
        items.remove(item_name)
        print(f"Вы подняли: {item_name}")
    else:
        print("Такого предмета здесь нет.")


def use_item(game_state, item_name):
    """Использует предмет из инвентаря, выполняя уникальное действие."""
    inventory = game_state.get('player_inventory', [])

    if item_name not in inventory:
        print("У вас нет такого предмета.")
        return

    match item_name:
        case 'torch':
            print("Вы зажгли факел. Стало заметно светлее.")
        case 'sword':
            print("Вы крепче сжимаете меч. Чувствуете уверенность и силу.")
        case 'bronze_box':
            # Открытие бронзовой шкатулки: добавить ключ, если его ещё нет
            if 'rusty_key' not in inventory:
                inventory.append('rusty_key')
                print("Вы открываете бронзовую шкатулку. Внутри ржавый ключ — вы кладёте его в инвентарь.")
            else:
                print("Шкатулка пуста.")
        case _:
            print("Вы не знаете, как использовать этот предмет.")

