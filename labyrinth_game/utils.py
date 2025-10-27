from labyrinth_game.constants import ROOMS


def describe_current_room(game_state):
    """
    Describe the current room with all details.
    
    Args:
        game_state: Current game state dictionary
    """
    current_room = game_state['current_room']
    room_data = ROOMS[current_room]
    
    # Room name in uppercase
    print(f"== {current_room.upper()} ==")
    
    # Room description
    print(room_data['description'])
    
    # Visible items
    if room_data['items']:
        print("\nЗаметные предметы:")
        for item in room_data['items']:
            print(f"  - {item}")
    
    # Available exits
    exits = room_data['exits']
    if exits:
        print("\nВыходы:")
        for direction, room_name in exits.items():
            print(f"  - {direction}: {room_name}")
    
    # Puzzle hint
    if room_data['puzzle']:
        print("\nКажется, здесь есть загадка (используйте команду solve).")