from labyrinth_game.constants import ROOMS
from labyrinth_game.player_actions import get_input
import math

def pseudo_random(seed, modulo):
    """
    Generate pseudo-random number based on seed and modulo.
    
    """
    sin_value = math.sin(seed * 12.9898)
    multiplied = sin_value * 43758.5453
    fractional = multiplied - math.floor(multiplied)
    result = math.floor(fractional * modulo)
    
    return result

def trigger_trap(game_state):
    """
    Trigger a trap with negative consequences for the player.
    
    """
    print("Ловушка активирована! Пол стал дрожать...")
    
    inventory = game_state['player_inventory']
    
    if inventory:
        # Выбираем и удаляем случайный предмент с помощью pseudo_random
        item_index = pseudo_random(game_state['steps_taken'], len(inventory))
        lost_item = inventory[item_index]
        inventory.remove(lost_item)
        print(f"Из вашего инвентаря выпал и потерялся: {lost_item}")
        
    else:
        # предметов нет
        damage_chance = pseudo_random(game_state['steps_taken'], 10)
        
        if damage_chance < 3:
            print("Вы не успели увернуться! Ловушка нанесла смертельный урон.")
            print("Игра окончена.")
            game_state['game_over'] = True
        else:
            print("Вам удалось увернуться от ловушки! Вы уцелели.")

def random_event(game_state):
    """
    Trigger random events during player movement.
    
    """
    # Проверяем, произойдет ли событие (10% вероятностьe)
    event_chance = pseudo_random(game_state['steps_taken'], 10)
    
    if event_chance != 0:
        return  
    
    # Выбираем, что произойдет
    event_type = pseudo_random(game_state['steps_taken'] + 1, 3)
    
    match event_type:
        case 0:
            # Сценарий 1. Нашли монетку
            current_room = game_state['current_room']
            room_data = ROOMS[current_room]
            room_data['items'].append('coin')
            print("Вы заметили что-то блестящее на полу...")
            print("Это монетка! Она добавлена в комнату.")
            
        case 1:
            # Сценарий 2. Слышим шорох
            print("Вы слышите странный шорох в темноте...")
            inventory = game_state['player_inventory']
            if 'sword' in inventory:
                print("Вы достаете меч, и существо убегает!")
            else:
                print("Шорох усиливается...")
                
        case 2:
            # Сценарий 3. Ловушка активирована
            current_room = game_state['current_room']
            inventory = game_state['player_inventory']
            
            if current_room == 'trap_room' and 'torch' not in inventory:
                print("Вы не заметили ловушку в темноте! Опасность!")
                trigger_trap(game_state)
            else:
                print("Вы почувствовали, что что-то не так, но опасность миновала.")

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
        
        if current_room == 'trap_room':
            reward = 15  
            print(f"Вы получили {reward} очков! Ловушка деактивирована.")
        elif current_room == 'treasure_room':
            reward = 20  
            print(f"Вы получили {reward} очков!")
        else:
            reward = 10  
            print(f"Вы получили {reward} очков!")
        
        game_state['score'] += reward
    else:
        print("Неверно. Попробуйте снова.")
        
        if current_room == 'trap_room':
            print("Неправильный ответ активировал ловушку!")
            trigger_trap(game_state)

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