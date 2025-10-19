from labyrinth_game.constants import ROOMS


def describe_current_room(game_state: dict) -> None:
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


