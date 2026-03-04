import pygame
from utils.settings import (CONSOLE_BG, CONSOLE_BORDER, HEADER_BG, 
                     LED_OFF, LED_ON, LED_GLOW, TEXT_COLOR_K)

def draw_console(screen: pygame.Surface, level_config: dict):
    grid_w = level_config["GRID_WIDTH"]
    grid_h = level_config["GRID_HEIGHT"]
    console_w = level_config["CONSOLE_WIDTH"]

    # Pozícia konzoly 
    x = grid_w
    y = 0

    # Horný panel (s LEDkami a názvom)
    header_h = 70
    header_rect = pygame.Rect(x, y, console_w, header_h)
    
    # Header pozadie
    pygame.draw.rect(screen, HEADER_BG, header_rect)
    
    # Okraj header
    pygame.draw.line(screen, CONSOLE_BORDER, (x, y + header_h), (x + console_w, y + header_h), width=3)
    pygame.draw.line(screen, (100, 160, 80), (x, 0), (x, header_h), width=2)

    # LED indikátory s žiarením 
    led_radius = 8
    led_spacing = 30
    led_start_x = x + 30
    led_y = y + header_h // 2

    leds = [
        (led_start_x, led_y, LED_ON, True),
        (led_start_x + led_spacing, led_y, LED_OFF, False),
        (led_start_x + 2 * led_spacing, led_y, LED_OFF, False)
    ]

    for lx, ly, color, is_on in leds:
        # Žiarenie pre zapnuté LED
        if is_on:
            for glow_size in range(led_radius + 5, led_radius + 2, -1):
                alpha = 30 - (glow_size - led_radius - 2) * 5
                glow_surf = pygame.Surface((glow_size * 2, glow_size * 2), pygame.SRCALPHA)
                pygame.draw.circle(glow_surf, (*LED_GLOW, alpha), (glow_size, glow_size), glow_size)
                screen.blit(glow_surf, (lx - glow_size, ly - glow_size))
        
        # Tmavý okraj LED
        pygame.draw.circle(screen, (20, 25, 30), (lx, ly), led_radius + 4)
        # Hlavná LED
        pygame.draw.circle(screen, color, (lx, ly), led_radius)
        # Svetlý okraj
        pygame.draw.circle(screen, (min(255, color[0] + 30), min(255, color[1] + 30), min(255, color[2] + 30)), 
                          (lx, ly), led_radius - 2)

    # Názov konzoly s tieňom 
    font = pygame.font.SysFont("Consolas", 24, bold=True)
    label = font.render("CONTROL PANEL", True, TEXT_COLOR_K)
    screen.blit(label, (x + 115, y + 23))

    #  Telo konzoly 
    workspace_rect = pygame.Rect(
        x,                     # zarovnanie na okraj
        y + header_h,           # hneď pod horný panel
        console_w,              # celá šírka konzoly
        grid_h - header_h       # celá výška po spodok
    )

    # Pozadie konzoly
    pygame.draw.rect(screen, CONSOLE_BG, workspace_rect)
    
    # Vnútorný okraj
    pygame.draw.line(screen, CONSOLE_BORDER, (x, y + header_h), (x, y + grid_h), width=2)

    return workspace_rect
