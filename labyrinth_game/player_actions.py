def show_inventory(game_state: dict) -> None:
    """Отображает содержимое инвентаря игрока или сообщает, что он пуст."""
    inventory = game_state.get('player_inventory', [])
    if inventory:
        print(f"Инвентарь: {', '.join(inventory)}")
    else:
        print("Инвентарь пуст.")


