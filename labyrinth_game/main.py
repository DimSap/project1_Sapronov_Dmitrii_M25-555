#!/usr/bin/env python3
from labyrinth_game.utils import describe_current_room
from labyrinth_game.player_actions import get_input, show_inventory, move_player, take_item, use_item


def main() -> None:
    # Инициализация состояния игры
    game_state = {
        'player_inventory': [],
        'current_room': 'entrance',
        'game_over': False,
        'steps_taken': 0,
    }

    # Приветствие
    print("Добро пожаловать в Лабиринт сокровищ!")

    # Описание стартовой комнаты
    describe_current_room(game_state)

    # Основной игровой цикл
    while not game_state['game_over']:
        command = get_input("> ")
        if not command:
            continue
        process_command(game_state, command)


def process_command(game_state, command):
    """Обрабатывает команду пользователя"""
    parts = command.strip().split(maxsplit=1)
    action = parts[0].lower() if parts else ''
    arg = parts[1].strip() if len(parts) > 1 else ''

    match action:
        case 'look':
            describe_current_room(game_state)
        case 'go':
            if arg:
                move_player(game_state, arg.lower())
            else:
                print("Укажите направление: например, 'go north'.")
        case 'take':
            if arg:
                take_item(game_state, arg)
            else:
                print("Укажите предмет: например, 'take torch'.")
        case 'use':
            if arg:
                use_item(game_state, arg)
            else:
                print("Укажите предмет: например, 'use torch'.")
        case 'inventory':
            show_inventory(game_state)
        case 'quit':
            game_state['game_over'] = True
            print("Игра завершена. До встречи!")
        case _:
            print("Неизвестная команда. Доступные: look, go, take, use, inventory, solve, open, quit.")


if __name__ == '__main__':
    main()