#!/usr/bin/env python3
from labyrinth_game.constants import COMMANDS
from labyrinth_game.player_actions import (
    get_input,
    move_player,
    show_inventory,
    take_item,
    use_item,
)
from labyrinth_game.utils import (
    attempt_open_treasure,
    describe_current_room,
    show_help,
    solve_puzzle,
)


def main():
    """Точка входа: инициализация состояния и запуск игрового цикла."""
    # Инициализация состояния игры
    game_state = {
        'player_inventory': [],
        'current_room': 'entrance',
        'game_over': False,
        'steps_taken': 0,
    }

    print("Добро пожаловать в Лабиринт сокровищ!")

    # Описание стартовой комнаты
    describe_current_room(game_state)

    # Основной игровой цикл
    while not game_state['game_over']:
        command = get_input("> ")
        if not command:
            continue
        process_command(game_state, command, COMMANDS)


def process_command(game_state, command, commands_help=COMMANDS):
    """Обрабатывает команду пользователя."""
    parts = command.strip().split(maxsplit=1)
    action = parts[0].lower() if parts else ''
    arg = parts[1].strip() if len(parts) > 1 else ''

    # Поддержка однословных направлений без 'go'
    if action in ('north', 'south', 'east', 'west'):
        move_player(game_state, action)
        return

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
        case 'solve':
            current_room_name = game_state.get('current_room')
            if current_room_name == 'treasure_room':
                attempt_open_treasure(game_state)
            else:
                solve_puzzle(game_state)
        case 'quit':
            game_state['game_over'] = True
            print("Игра завершена. До встречи!")
        case 'help':
            show_help(commands_help)
        case _:
            print("Неизвестная команда. Наберите 'help' для списка команд.")


if __name__ == '__main__':
    main()