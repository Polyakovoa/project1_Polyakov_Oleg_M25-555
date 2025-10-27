from labyrinth_game.constants import ROOMS, DIRECTIONS


def show_inventory(game_state):
    """
    Display player's inventory.
    
    Args:
        game_state: Current game state dictionary
    """
    inventory = game_state['player_inventory']
    
    if inventory:
        print("Ваш инвентарь:")
        for item in inventory:
            print(f"  - {item}")
    else:
        print("Ваш инвентарь пуст.")

def get_input(prompt="> "):
    """
    Get user input with error handling.
   
    """
    try:
        return input(prompt)
    except (KeyboardInterrupt, EOFError):
        print("\nВыход из игры.")
        return "quit"