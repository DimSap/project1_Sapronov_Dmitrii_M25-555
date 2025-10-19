def show_inventory(game_state: dict) -> None:
    """Отображает содержимое инвентаря игрока или сообщает, что он пуст."""
    inventory = game_state.get('player_inventory', [])
    if inventory:
        print(f"Инвентарь: {', '.join(inventory)}")
    else:
        print("Инвентарь пуст.")


def get_input(prompt: str = "> ") -> str:
    """Безопасно запрашивает ввод пользователя. Возвращает строку команды.

    При прерывании ввода (Ctrl+C / Ctrl+D) возвращает команду 'quit'.
    """
    try:
        return input(prompt).strip()
    except (KeyboardInterrupt, EOFError):
        print("\nВыход из игры.")
        return "quit"

