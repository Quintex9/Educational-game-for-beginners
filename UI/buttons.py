import pygame
import math
from utils.settings import START_BUTTON_COLOR, START_BUTTON_HOVER, START_BUTTON_SHADOW, START_TEXT_COLOR, HEADER_BG, CONSOLE_BORDER
from utils.paths import resource_path

# Cache pre načítaný SVG obrázok hviezdy
_star_image_cache = None

def _load_star_svg(size):
    """Načíta SVG obrázok hviezdy a vráti pygame Surface"""
    global _star_image_cache
    
    # Ak už máme načítaný obrázok, použijeme ho
    if _star_image_cache is not None:
        return pygame.transform.scale(_star_image_cache, (size, size))
    
    svg_path = resource_path("assets/star.svg")
    
    # Skúsi načítať pomocou PIL (ak je dostupný)
    try:
        from PIL import Image
        import io
        
        # Načíta SVG súbor
        with open(svg_path, 'r', encoding='utf-8') as f:
            svg_content = f.read()
        
        # Vytvorí PNG z SVG pomocou PIL (ak má podporu)
        # Alternatívne: použijeme cairosvg alebo svglib
        try:
            import cairosvg
            png_data = cairosvg.svg2png(file_obj=io.BytesIO(svg_content.encode()))
            img = Image.open(io.BytesIO(png_data))
        except:
            # Fallback: vytvorí jednoduchú hviezdu pomocou PIL
            img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
            from PIL import ImageDraw
            draw = ImageDraw.Draw(img)
            # Nakreslí hviezdu
            center = size // 2
            outer_radius = size // 2 - 2
            inner_radius = outer_radius * 0.4
            points = []
            for i in range(10):
                angle = (i * math.pi / 5) - math.pi / 2
                if i % 2 == 0:
                    radius = outer_radius
                else:
                    radius = inner_radius
                px = center + radius * math.cos(angle)
                py = center + radius * math.sin(angle)
                points.append((px, py))
            draw.polygon(points, fill=(255, 215, 0), outline=(255, 200, 0))
        
        # Konvertuje PIL Image na pygame Surface
        img_str = img.tobytes()
        img_surface = pygame.image.fromstring(img_str, img.size, img.mode)
        _star_image_cache = img_surface
        return pygame.transform.scale(img_surface, (size, size))
        
    except Exception as e:
        # Fallback: nakreslí hviezdu pomocou pygame
        surface = pygame.Surface((size, size), pygame.SRCALPHA)
        center = size // 2
        outer_radius = size // 2 - 2
        inner_radius = outer_radius * 0.4
        
        points = []
        for i in range(10):
            angle = (i * math.pi / 5) - math.pi / 2
            if i % 2 == 0:
                radius = outer_radius
            else:
                radius = inner_radius
            px = center + radius * math.cos(angle)
            py = center + radius * math.sin(angle)
            points.append((int(px), int(py)))
        
        pygame.draw.polygon(surface, (255, 215, 0), points)
        pygame.draw.polygon(surface, (255, 200, 0), points, width=1)
        _star_image_cache = surface
        return surface


def _draw_button(screen, rect, text, font_size, mouse_pos, border_radius=12):
    hovered = rect.collidepoint(mouse_pos)
    shadow_rect = rect.move(2, 2)
    pygame.draw.rect(screen, START_BUTTON_SHADOW, shadow_rect, border_radius=border_radius)
    pygame.draw.rect(screen, START_BUTTON_HOVER if hovered else START_BUTTON_COLOR, rect, border_radius=border_radius)
    # Tmavo zelený border - svetlejší pri hover
    border_color = (60, 160, 40) if hovered else (80, 140, 60)
    pygame.draw.rect(screen, border_color, rect, width=2, border_radius=border_radius)
    font = pygame.font.SysFont("Consolas", font_size, bold=True)
    txt = font.render(text, True, START_TEXT_COLOR)
    screen.blit(txt, txt.get_rect(center=rect.center))
    return rect


def _draw_console_button(screen, rect, text, font_size, mouse_pos):
    """Vykreslí kompaktné tlačidlo v konzole s odlišným štýlom"""
    hovered = rect.collidepoint(mouse_pos)
    # Tmavšie zelené pozadie pre tlačidlá v konzole
    bg_color = (90, 150, 70) if hovered else (70, 130, 50)
    border_color = (110, 170, 90) if hovered else (90, 150, 70)
    
    pygame.draw.rect(screen, bg_color, rect, border_radius=8)
    pygame.draw.rect(screen, border_color, rect, width=2, border_radius=8)
    
    font = pygame.font.SysFont("Consolas", font_size, bold=True)
    txt = font.render(text, True, (255, 255, 255))
    screen.blit(txt, txt.get_rect(center=rect.center))
    return rect


def _get_console_buttons_area(level_config):
    """Vráti rect pre oblasť tlačidiel v konzole (hneď pod headerom)"""
    grid_w = level_config["GRID_WIDTH"]
    console_w = level_config["CONSOLE_WIDTH"]
    header_h = 70
    
    # Pozícia hneď pod headerom konzoly
    x = grid_w
    y = header_h
    w = console_w
    h = 50  # Výška oblasti pre tlačidlá
    
    return pygame.Rect(x, y, w, h)


def _console_button_rect(level_config, button_index, total_buttons):
    """Vypočíta pozíciu tlačidla v konzole"""
    area = _get_console_buttons_area(level_config)
    padding = 10
    spacing = 8
    btn_w = (area.width - 2 * padding - (total_buttons - 1) * spacing) // total_buttons
    btn_h = area.height - 2 * padding
    
    x = area.x + padding + button_index * (btn_w + spacing)
    y = area.y + padding
    
    return pygame.Rect(x, y, btn_w, btn_h)


def draw_start_button(screen, level_config, mouse_pos):
    """Vykreslí START tlačidlo v paneli"""
    grid_h = level_config["GRID_HEIGHT"]
    panel_h = level_config["PANEL_HEIGHT"]
    
    # START tlačidlo je v paneli, nie v konzole
    available_left = level_config["GRID_WIDTH"] + 20
    available_right = level_config["GRID_WIDTH"] + level_config["CONSOLE_WIDTH"] - 20
    available_w = max(220, available_right - available_left)
    btn_w = min(340, available_w)
    btn_h = 110
    x = available_left + (available_w - btn_w) // 2
    y = grid_h + (panel_h - btn_h) // 2
    rect = pygame.Rect(x, y, btn_w, btn_h)
    return _draw_button(screen, rect, "START", 32, mouse_pos, border_radius=15)


def draw_console_buttons_area(screen, level_config, has_mode=False):
    """Vykreslí oblasť pre tlačidlá v konzole (pozadie)"""
    area = _get_console_buttons_area(level_config)
    # Pozadie s odlíšením od zvyšku konzoly
    pygame.draw.rect(screen, HEADER_BG, area)
    pygame.draw.line(screen, CONSOLE_BORDER, (area.x, area.bottom), (area.right, area.bottom), width=2)


def _draw_star_icon(screen, center_x, center_y, size):
    """Vykreslí ikonu hviezdy z SVG"""
    star_surface = _load_star_svg(size)
    star_rect = star_surface.get_rect(center=(center_x, center_y))
    screen.blit(star_surface, star_rect)

def draw_stars_info_button(screen, level_config, mouse_pos, has_mode=False):
    """Vykreslí tlačidlo na zobrazenie informácií o hviezdičkách s ikonou hviezdy"""
    total = 4 if has_mode else 3
    index = 3 if has_mode else 2
    rect = _console_button_rect(level_config, index, total)
    
    hovered = rect.collidepoint(mouse_pos)
    # Tmavšie zelené pozadie pre tlačidlá v konzole
    bg_color = (90, 150, 70) if hovered else (70, 130, 50)
    border_color = (110, 170, 90) if hovered else (90, 150, 70)
    
    pygame.draw.rect(screen, bg_color, rect, border_radius=8)
    pygame.draw.rect(screen, border_color, rect, width=2, border_radius=8)
    
    # Vykreslí žltú hviezdu v strede tlačidla
    star_size = min(rect.width, rect.height) - 8
    _draw_star_icon(screen, rect.centerx, rect.centery, star_size)
    
    return rect


def draw_menu_button(screen, level_config, mouse_pos, has_mode=False):
    """Vykreslí MENU tlačidlo v konzole"""
    total = 4 if has_mode else 3
    index = 2 if has_mode else 1
    rect = _console_button_rect(level_config, index, total)
    return _draw_console_button(screen, rect, "MENU", 16, mouse_pos)


def draw_reset_button(screen, level_config, mouse_pos, has_mode=False):
    """Vykreslí RESET tlačidlo v konzole"""
    total = 4 if has_mode else 3
    index = 1 if has_mode else 0
    rect = _console_button_rect(level_config, index, total)
    return _draw_console_button(screen, rect, "RESET", 16, mouse_pos)


def draw_mode_toggle_button(screen, level_config, mouse_pos, text_mode):
    """Vykreslí MODE tlačidlo v konzole"""
    rect = _console_button_rect(level_config, 0, 4)
    text = "TEXT" if not text_mode else "DRAG"
    return _draw_console_button(screen, rect, text, 14, mouse_pos)
