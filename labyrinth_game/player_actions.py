from labyrinth_game.constants import ROOMS
from labyrinth_game.utils import random_event

def show_inventory(game_state):
    """
    Показывет инвентарь игрока.
  
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
    Ввод команд игроком.
   
    """
    try:
        return input(prompt)
    except (KeyboardInterrupt, EOFError):
        print("\nВыход из игры.")
        return "quit"
    
def move_player(game_state, direction):
    """
    Передвижение игрока.
    
    """
    current_room = game_state['current_room']
    
    current_room_data = ROOMS.get(current_room, {})
    exits = current_room_data.get('exits', {})
    
    if direction in exits:
        target_room = exits[direction]

        if target_room == 'treasure_room' and 'rusty_key' not in game_state['player_inventory']:
            print("Дверь заперта. Нужен ключ, чтобы пройти дальше.")
            return
        
        game_state['current_room'] = target_room
        game_state['steps_taken'] += 1

        if target_room == 'treasure_room' and 'rusty_key' in game_state['player_inventory']:
            print("Вы используете найденный ключ, чтобы открыть путь в комнату сокровищ.")
        
        new_room = game_state['current_room']
        new_room_data = ROOMS[new_room]
        
        print(f"== {new_room.upper()} ==")
        print(new_room_data['description'])
        
        if new_room_data['items']:
            print("\nЗаметные предметы:")
            for item in new_room_data['items']:
                print(f"  - {item}")
        
        new_exits = new_room_data['exits']
        if new_exits:
            print("\nВыходы:")
            for exit_direction, exit_room in new_exits.items():
                print(f"  - {exit_direction}: {exit_room}")
        
        if new_room_data['puzzle']:
            print("\nКажется, здесь есть загадка (используйте команду solve).")

        random_event(game_state)
            
    else:
        print("Нельзя пойти в этом направлении.")

def take_item(game_state, item_name):
    """
    Взять предмет.
   
    """
    current_room = game_state['current_room']
    current_room_data = ROOMS.get(current_room, {})
    room_items = current_room_data.get('items', [])
    
    if item_name in room_items:
        if item_name == 'treasure_chest':
            print("Вы не можете поднять сундук, он слишком тяжелый.")
            return
        game_state['player_inventory'].append(item_name)
        room_items.remove(item_name)
        print(f"Вы подняли: {item_name}")
    else:
        print("Такого предмета здесь нет.")

def use_item(game_state, item_name):
    """
    Используем инвентарь.
    
    """
    inventory = game_state['player_inventory']

    if item_name not in inventory:
        print('У Вас нет такого предмета.')
        return
    
    match item_name:
        case 'torch':
            print("Вы зажгли факел. Стало светлее.")
        case 'sword':
            print("Вы почувствовали уверенность с мечом в руках.")
        case 'bronze_box':
            print("Вы открыли бронзовую шкатулку.")
            if 'rusty_key' not in inventory:
                inventory.append('rusty_key')
                print("Внутри Вы нашли ржавый rusty_key!")
                print("(Этот ключ может пригодиться для открытия сокровищницы!)")
        case 'rusty_key':
            print("Осмотрев ржавый ключ Вы замечаете на нем символы сокровищницы!")
            print("Это и есть ключ от сокровищницы!")
        case 'leather_armor':
            print("Вы получаете +10 к защите.")
        case 'healing_herbs':
            print("Вы получаете +10 к здоровью.")
        case _:
            print("Вы не знаете, как использовать этот предмет.")