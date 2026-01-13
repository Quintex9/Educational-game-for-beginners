
def execute_commands(player, commands, grid_size):
    
    for cmd in commands:
        action = cmd.command
        
        # Získa aktuálnu pozíciu pred pohybom
        old_x, old_y = player.get_position()
        
        if action == "move_up":
            player.move_up()
        elif action == "move_down":
            player.move_down()
        elif action == "move_right":
            player.move_right()
        elif action == "move_left":
            player.move_left()
        
        new_x, new_y = player.get_position()
        if not (0 <= new_x < grid_size and 0 <= new_y < grid_size):
            player.set_position(old_x, old_y)
            