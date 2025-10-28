from labyrinth_game.constants import ROOMS
from labyrinth_game.player_actions import get_input


def describe_current_room(game_state):
    """
    Describe the current room with all details.
    
    """
    current_room = game_state['current_room']
    room_data = ROOMS[current_room]
    
    print(f"== {current_room.upper()} ==")
    
    print(room_data['description'])
    
    if room_data['items']:
        print("\nЗаметные предметы:")
        for item in room_data['items']:
            print(f"  - {item}")
    
    exits = room_data['exits']
    if exits:
        print("\nВыходы:")
        for direction, room_name in exits.items():
            print(f"  - {direction}: {room_name}")
    
    if room_data['puzzle']:
        print("\nКажется, здесь есть загадка (используйте команду solve).")

def solve_puzzle(game_state):
    """
    Решаем загадку.
    
    """
    current_room = game_state['current_room']
    room_data = ROOMS[current_room]
    
    if not room_data['puzzle']:
        print("Загадок здесь нет.")
        return
    
    question, correct_answers = room_data['puzzle']
    
    print(question)
    
    user_answer = get_input("Ваш ответ: ").strip().lower()

    correct_answers_lower = [ans.lower() for ans in correct_answers]
    
    if user_answer in correct_answers_lower:
        print("Правильно! Загадка решена.")
        
        room_data['puzzle'] = None
        
        game_state['steps_taken'] += 10  # Награда за решение загадки
        print("Вы получили 10 очков!")
    else:
        print("Неверно. Попробуйте снова.")

def attempt_open_treasure(game_state):
    """
    Пытаемся открыть сундук сокровищ.
    
    """
    current_room = game_state['current_room']
    room_data = ROOMS[current_room]
    inventory = game_state['player_inventory']
    
    # Есть ли treasure_key?
    if 'rusty_key' in inventory:
        print("Вы применяете ржавый ключ, и замок щёлкает. Сундук открыт!")
        if 'treasure_chest' in room_data['items']:
            room_data['items'].remove('treasure_chest')
        print("В сундуке сокровище! Вы победили!")
        game_state['game_over'] = True
        return
    
    # Нет ключа, предлагаем ввести код
    print("Сундук заперт. На замке есть клавиатура для ввода кода.")
    answer = get_input("Ввести код? (да/нет): ").strip().lower()
    
    if answer == 'да':
        code = get_input("Введите код: ").strip()
        if room_data['puzzle'] and code == room_data['puzzle'][1]:
            print("Замок щёлкает! Сундук открыт!")
            if 'treasure_chest' in room_data['items']:
                room_data['items'].remove('treasure_chest')
            print("В сундуке сокровище! Вы победили!")
            game_state['game_over'] = True
        else:
            print("Неверный код. Замок не открылся.")
    else:
        print("Вы отступаете от сундука.")

def show_help():
    print("\nДоступные команды:")
    print("  go <direction>  - перейти в направлении (north/south/east/west)")
    print("  look            - осмотреть текущую комнату")
    print("  take <item>     - поднять предмет")
    print("  use <item>      - использовать предмет из инвентаря")
    print("  inventory       - показать инвентарь")
    print("  solve           - попытаться решить загадку в комнате")
    print("  quit            - выйти из игры")
    print("  help            - показать это сообщение") 