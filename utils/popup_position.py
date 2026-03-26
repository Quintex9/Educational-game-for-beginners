import pygame


def compute_selection_popup_rect(anchor_rect, popup_width, popup_height, bounds_rect, gap=10):
    # Vráti popup rect vedľa IF/FOR rectu, vpravo ak je možné inak dole
    right_rect = pygame.Rect(
        anchor_rect.right + gap,
        anchor_rect.y,
        popup_width,
        popup_height,
    )

    if (
        right_rect.left >= bounds_rect.left
        and right_rect.right <= bounds_rect.right
        and right_rect.top >= bounds_rect.top
        and right_rect.bottom <= bounds_rect.bottom
    ):
        return right_rect

    # Fallback
    x = anchor_rect.x
    x = max(bounds_rect.left, min(x, bounds_rect.right - popup_width))

    below_y = anchor_rect.bottom + gap
    # Keep popup as low as possible; if it would overflow bottom, clamp to bottom edge.
    y = min(below_y, bounds_rect.bottom - popup_height)
    y = max(bounds_rect.top, y)

    return pygame.Rect(x, y, popup_width, popup_height)
