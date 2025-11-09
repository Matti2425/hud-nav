import pygame
import sys
import time
from map_fetcher import latlon_to_tile, get_tile
from ui_styles import draw_maps_style, draw_scifi_style
from PIL import Image

pygame.init()

# --- Configurable ---
simulate_movement = True
allow_download_tiles = True
flip_display = False
interface_mode = 'maps'

resolutions = {
    '1': (800, 480),
    '2': (1280, 720),
    '3': (1920, 1080)
}
current_res_key = '1'
WIDTH, HEIGHT = resolutions[current_res_key]

# Coordenadas iniciales
lat = 41.387
lon = 2.170
speed = 35
heading = 'NNE'
zoom = 15

screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption('HUD Map Prototype')
render_surface = pygame.Surface((WIDTH, HEIGHT))  # Surface intermedio

font = pygame.font.SysFont('monospace', 24)
clock = pygame.time.Clock()


def pil_to_surface(img_pil):
    mode = img_pil.mode
    size = img_pil.size
    data = img_pil.tobytes()
    return pygame.image.fromstring(data, size, mode).convert()


def render_map_center(lat, lon, zoom, w, h):
    x_tile, y_tile = latlon_to_tile(lat, lon, zoom)
    pil = get_tile(zoom, x_tile, y_tile, allow_download=allow_download_tiles)
    surf = pil_to_surface(pil)
    surf = pygame.transform.scale(surf, (w, h))
    return surf


x_off = 0
y_off = 0
move_speed = 0.0002
running = True
t = 0


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

            elif event.key in (pygame.K_1, pygame.K_2, pygame.K_3):
                current_res_key = chr(event.key)
                WIDTH, HEIGHT = resolutions[current_res_key]
                screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
                render_surface = pygame.Surface((WIDTH, HEIGHT))

            elif event.key == pygame.K_m:
                interface_mode = 'maps'
            elif event.key == pygame.K_s:
                interface_mode = 'scifi'
            elif event.key == pygame.K_SPACE:
                simulate_movement = not simulate_movement

            elif event.key == pygame.K_f:
                flip_display = not flip_display
                print("Flip HUD:", flip_display)

    keys = pygame.key.get_pressed()
    if simulate_movement:
        if keys[pygame.K_UP]: lat += move_speed
        if keys[pygame.K_DOWN]: lat -= move_speed
        if keys[pygame.K_LEFT]: lon -= move_speed
        if keys[pygame.K_RIGHT]: lon += move_speed

    try:
        map_surf = render_map_center(lat, lon, zoom, WIDTH, HEIGHT)
    except Exception:
        map_surf = pygame.Surface((WIDTH, HEIGHT))
        map_surf.fill((30, 30, 30))

    # DIBUJAR TODO EN EL SURFACE INTERMEDIO
    render_surface.blit(map_surf, (0, 0))
    pygame.draw.circle(render_surface, (0, 255, 0), (WIDTH // 2, HEIGHT // 2), 8)

    if interface_mode == 'maps':
        draw_maps_style(render_surface, font, lat, lon, speed, heading)
    else:
        draw_scifi_style(render_surface, font, lat, lon, speed, heading, t)

    help_text = font.render('1/2/3: res M: maps S: scifi SPACE: sim F: flip', True, (200, 200, 200))
    render_surface.blit(help_text, (10, HEIGHT - 30))

    # SI HUD INVERTIDO → VOLTEAR
    if flip_display:
        flipped = pygame.transform.flip(render_surface, True, False)
        screen.blit(flipped, (0, 0))
    else:
        screen.blit(render_surface, (0, 0))

    pygame.display.flip()
    t += 1
    clock.tick(30)

pygame.quit()
sys.exit()
