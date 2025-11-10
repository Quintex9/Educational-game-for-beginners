elif state == "Level 1":
        window.draw_background((131, 106, 98))
        level_config = set_level_size(3, window.width, window.height)
        draw_grid(window.screen, level_config)
        draw_console(window.screen,level_config)