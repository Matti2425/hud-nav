import pygame
import math

# -----------------------------
# Modo Maps (light/dark)
# -----------------------------
def draw_maps_style(screen, font, lat, lon, speed, heading):
    """
    Dibuja información básica sobre el mapa:
    - Latitud / Longitud
    - Velocidad
    - Heading
    """
    w, h = screen.get_size()
    
    # Fondo semitransparente
    info_bg = pygame.Surface((220, 80), pygame.SRCALPHA)
    info_bg.fill((0, 0, 0, 120))  # negro con alpha
    screen.blit(info_bg, (10, 10))

    # Texto
    lat_text = font.render(f"Lat: {lat:.5f}", True, (255, 255, 255))
    lon_text = font.render(f"Lon: {lon:.5f}", True, (255, 255, 255))
    speed_text = font.render(f"Speed: {speed} km/h", True, (255, 255, 255))
    heading_text = font.render(f"Heading: {heading}", True, (255, 255, 255))

    screen.blit(lat_text, (20, 15))
    screen.blit(lon_text, (20, 35))
    screen.blit(speed_text, (20, 55))
    screen.blit(heading_text, (120, 55))

# -----------------------------
# Modo Sci-Fi
# -----------------------------
def draw_scifi_style(screen, font, lat, lon, speed, heading, t):
    """
    Dibuja una interfaz tipo futurista / sci-fi
    """
    w, h = screen.get_size()
    
    # Fondo gradiente simple
    for i in range(h):
        color = (0, 0, min(50 + i // 10, 255))
        pygame.draw.line(screen, color, (0, i), (w, i))

    # Líneas diagonales animadas
    for i in range(0, w, 40):
        pygame.draw.line(screen, (0, 255, 255), (i - t % 40, 0), (i - t % 40, h), 1)

    # Texto futurista
    info_font = pygame.font.SysFont('monospace', 20, bold=True)
    speed_text = info_font.render(f"SPEED: {speed} km/h", True, (0, 255, 255))
    heading_text = info_font.render(f"HEADING: {heading}", True, (0, 255, 255))
    lat_text = info_font.render(f"LAT: {lat:.5f}", True, (0, 255, 255))
    lon_text = info_font.render(f"LON: {lon:.5f}", True, (0, 255, 255))

    screen.blit(speed_text, (20, 20))
    screen.blit(heading_text, (20, 50))
    screen.blit(lat_text, (20, 80))
    screen.blit(lon_text, (20, 110))

# -----------------------------
# Velocímetro
# -----------------------------
def draw_speedometer(screen, font, speed):
    """
    Dibuja un velocímetro circular en la esquina inferior derecha
    """
    w, h = screen.get_size()
    radius = min(w, h) // 6
    center = (w - radius - 20, h - radius - 20)

    # Fondo del velocímetro
    pygame.draw.circle(screen, (50, 50, 50), center, radius)
    pygame.draw.circle(screen, (200, 200, 200), center, radius, 4)

    # Aguja
    angle = (speed / 200) * 180  # velocidad máxima 200 km/h
    end_x = center[0] + int(radius * 0.9 * math.cos(math.radians(180 - angle)))
    end_y = center[1] - int(radius * 0.9 * math.sin(math.radians(180 - angle)))
    pygame.draw.line(screen, (255, 0, 0), center, (end_x, end_y), 4)

    # Texto velocidad
    speed_text = font.render(f"{int(speed)} km/h", True, (255, 255, 255))
    text_rect = speed_text.get_rect(center=(center[0], center[1] + radius + 15))
    screen.blit(speed_text, text_rect)