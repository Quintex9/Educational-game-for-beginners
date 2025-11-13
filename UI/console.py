import pygame
from settings import CONSOLE_BG, CONSOLE_BORDER, HEADER_BG, LED_OFF, LED_ON, TEXT_COLOR_K

def draw_console(screen: pygame.Surface, level_config: dict):
    grid_w = level_config["GRID_WIDTH"]
    grid_h = level_config["GRID_HEIGHT"]
    console_w = level_config["CONSOLE_WIDTH"]

    # --- Pozícia konzoly ---
    x = grid_w
    y = 0

    # --- Horný panel (s LEDkami a názvom) ---
    header_h = 60
    header_rect = pygame.Rect(x, y, console_w, header_h)
    pygame.draw.rect(screen, HEADER_BG, header_rect)
    pygame.draw.line(screen, CONSOLE_BORDER, (x, y + header_h), (x + console_w, y + header_h), width=2)

    # --- LED indikátory ---
    led_radius = 7
    led_spacing = 25
    led_start_x = x + 25
    led_y = y + header_h // 2

    leds = [
        (led_start_x, led_y, LED_ON),
        (led_start_x + led_spacing, led_y, LED_OFF),
        (led_start_x + 2 * led_spacing, led_y, LED_OFF)
    ]

    for lx, ly, color in leds:
        pygame.draw.circle(screen, (25, 25, 25), (lx, ly), led_radius + 3)
        pygame.draw.circle(screen, color, (lx, ly), led_radius)

    # --- Názov konzoly ---
    font = pygame.font.SysFont("Consolas", 20, bold=True)
    label = font.render("CONTROL PANEL", True, TEXT_COLOR_K)
    screen.blit(label, (x + 100, y + 18))

    # --- Telo konzoly (celá plocha vyplnená až po rám) ---
    workspace_rect = pygame.Rect(
        x,                     # zarovnanie na okraj
        y + header_h,           # hneď pod horný panel
        console_w,              # celá šírka konzoly
        grid_h - header_h       # celá výška po spodok
    )

    pygame.draw.rect(screen, CONSOLE_BG, workspace_rect)

    return workspace_rect
