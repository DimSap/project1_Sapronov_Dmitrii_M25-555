#!/usr/bin/env python3
from labyrinth_game.utils import describe_current_room
from labyrinth_game.player_actions import get_input


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


if __name__ == '__main__':
    main()