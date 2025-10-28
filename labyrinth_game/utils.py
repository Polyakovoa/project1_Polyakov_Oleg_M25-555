from labyrinth_game.constants import ROOMS


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