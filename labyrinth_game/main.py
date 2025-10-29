from labyrinth_game.player_actions import (
    move_player,
    show_inventory,
    take_item,
    use_item,
)
from labyrinth_game.utils import attempt_open_treasure, describe_current_room

# Define game state
game_state = {
    'player_inventory': [],  # Инвентарь игрока
    'current_room': 'entrance',  # Текущая комната
    'game_over': False,  # Значения окончания игры
    'steps_taken': 0,  # Количество шагов
    'score': 0  # Добавляем счетчик очков
}

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

    directions = ['north', 'south', 'east', 'west', 'север', 'юг', 'восток', 'запад']
    if action in directions:
        move_player(game_state, action)
        return
    
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
        case 'use':
            if argument:
                use_item(game_state, argument)
            else:
                print("Укажите предмет: use [предмет]")
        case 'inventory':
            show_inventory(game_state)
        case 'solve':
            if game_state['current_room'] == 'treasure_room':
                attempt_open_treasure(game_state)
            else:
                from labyrinth_game.utils import solve_puzzle
                solve_puzzle(game_state)
        case 'help' | 'помощь':
            from labyrinth_game.utils import show_help
            show_help()
        case 'quit' | 'exit':
            game_state['game_over'] = True
            print("Спасибо за игру!")
        case _:
            print("Неизвестная команда. Попробуйте: look, go [направление], "
                  "take [предмет], use [предмет], inventory, solve, quit")

def main():
    """Main function для старта игры."""
    
    print("Добро пожаловать в Лабиринт сокровищ!")
    
    describe_current_room(game_state)
    
    while not game_state['game_over']:
        try:
            command = input("\nВведите команду: ").strip().lower()
            process_command(game_state, command)
        except UnicodeDecodeError:
            print("Ошибка кодировки. Попробуйте еще раз.")
        except (KeyboardInterrupt, EOFError):
            print("\nВыход из игры.")
            break


if __name__ == "__main__":
    main()