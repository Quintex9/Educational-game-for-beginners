import pygame

STAR_EMOJI = "⭐"


def get_star_font(size, bold=False):
    return pygame.font.SysFont("Segoe UI Emoji", size, bold=bold)


def draw_star_emoji(screen, center, size, alpha=255):
    font = get_star_font(size)
    surf = font.render(STAR_EMOJI, True, (255, 255, 255))
    if alpha < 255:
        surf.set_alpha(alpha)
    rect = surf.get_rect(center=center)
    screen.blit(surf, rect)
    return rect
