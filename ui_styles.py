# ui_styles.py
import pygame


# Colores
GREEN = (0, 255, 0)
DARK_GREEN = (0, 120, 0)
WHITE = (255, 255, 255)
CYAN = (0, 200, 200)


def draw_maps_style(screen, font, lat, lon, speed, heading):
    """Estilo tipo Google Maps: simple overlay con caja y texto"""
    w, h = screen.get_size()
    # panel inferior
    pygame.draw.rect(screen, (0, 0, 0, 160), (0, h - 100, w, 100))
    # mostrar datos
    screen.blit(font.render(f"LAT: {lat:.5f}", True, GREEN), (20, h - 90))
    screen.blit(font.render(f"LON: {lon:.5f}", True, GREEN), (20, h - 60))
    screen.blit(font.render(f"SPD: {speed} km/h", True, GREEN), (20, h - 30))
    # Flecha simple dirección
    pygame.draw.polygon(screen, (255, 200, 0), [(w-120, h-60), (w-80, h-80), (w-80, h-40)])
    screen.blit(font.render(f"{heading}", True, WHITE), (w-160, h-90))

def draw_scifi_style(screen, font, lat, lon, speed, heading, t):
    """Estilo Sci-Fi: líneas y HUD con animación suave"""
    w, h = screen.get_size()
    # sombras y líneas
    for i in range(0, w, 80):
        pygame.draw.line(screen, (0, 50, 50), (i, 0), (i, h), 1)
    for j in range(0, h, 60):
        pygame.draw.line(screen, (0, 50, 50), (0, j), (w, j), 1)

    # centro: retícula
    cx, cy = w // 2, h // 2
    pygame.draw.circle(screen, (0, 255, 200), (cx, cy), 10, 2)
    # datos en formato futurista
    screen.blit(font.render(f"{lat:.5f}", True, CYAN), (20, 20))
    screen.blit(font.render(f"{lon:.5f}", True, CYAN), (20, 50))
    screen.blit(font.render(f"SPD {speed}km/h", True, CYAN), (20, 80))
    # animación de barra
    bar_w = int((w - 40) * (0.5 + 0.5 * (pygame.math.sin(t / 20))))
    pygame.draw.rect(screen, (0, 255, 200), (20, h - 40, bar_w, 8))
    pygame.draw.rect(screen, (0, 100, 100), (20, h - 40, w - 40, 8), 1)
    # heading
    screen.blit(font.render(f"HDG {heading}", True, CYAN), (w - 140, 20))
