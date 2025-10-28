from labyrinth_game.constants import ROOMS
from labyrinth_game.utils import describe_current_room
from labyrinth_game.player_actions import get_input, move_player, take_item

# Define game state
game_state = {
    'player_inventory': [],  # Инвентарь игрока
    'current_room': 'entrance',  # Текущая комната
    'game_over': False,  # Значения окончания игры
    'steps_taken': 0  # Количество шагов
}


def main():
    """Main function для старта игры."""
    
    print("Добро пожаловать в Лабиринт сокровищ!")
    
    describe_current_room(game_state)
    
    while not game_state['game_over']:
        command = input("\nВведите команду: ").strip().lower()
        print(f"Вы ввели: {command}")

if __name__ == "__main__":
    main()

def process_command(game_state, command):
    """
    Обрабатывает команды игрока.
    
    """
    # Разделяем команду на части
    parts = command.split()
    if not parts:
        return
    
    action = parts[0]
    argument = parts[1] if len(parts) > 1 else None
    
    match action:
        case 'look':
            describe_current_room(game_state)
        case 'go':
            if argument:
                move_player(game_state, argument)
            else:
                print("Укажите направление: go [направление]")
        case 'take':
            if argument:
                take_item(game_state, argument)
            else:
                print("Укажите предмет: take [предмет]")
        case 'inventory':
            print(f"Инвентарь: {game_state['player_inventory']}")
        case 'quit' | 'exit':
            game_state['game_over'] = True
            print("Спасибо за игру!")
        case _:
            print("Неизвестная команда. Попробуйте: look, go [направление], take [предмет], inventory, quit")