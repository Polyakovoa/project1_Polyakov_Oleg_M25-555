from labyrinth_game.constants import ROOMS
from labyrinth_game.utils import describe_current_room


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
        game_state['current_room'] = exits[direction]
        game_state['steps_taken'] += 1
        describe_current_room(game_state)
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
                print("Внутри Вы нашли rusty_key!")
        case _:
            print("Вы не знаете, как использовать этот предмет.")