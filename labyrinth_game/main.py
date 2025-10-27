from labyrinth_game.constants import ROOMS
from labyrinth_game.utils import describe_current_room

# Define game state
game_state = {
    'player_inventory': [],  # Инвентарь игрока
    'current_room': 'entrance',  # Текущая комната
    'game_over': False,  # Значения окончания игры
    'steps_taken': 0  # Количество шагов
}


def main():
    """Main function to start the game."""
    # Welcome message
    print("Добро пожаловать в Лабиринт сокровищ!")
    
    # Describe starting room
    describe_current_room(game_state)
    
    # Main game loop
    while not game_state['game_over']:
        # Read user command
        command = input("\nВведите команду: ").strip().lower()
        
        # TODO: Process commands in next steps
        print(f"Вы ввели: {command}")

if __name__ == "__main__":
    main()