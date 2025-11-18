

def execute_commands(player, commands, grid_size):
    
    for cmd in commands:
        action = cmd.command
        
        new_x = player.x
        new_y = player.y
        
        if action == "move_up":
            new_y -= 1
        elif action == "move_down":
            new_y += 1
        elif action == "move_right":
            new_x += 1
        elif action == "move_left":
            new_x -= 1
        
        if 0 <= new_x < grid_size and 0 <= new_y < grid_size:
            player.x = new_x
            player.y = new_y