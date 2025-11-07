import pygame
import sys
import time
from map_fetcher import latlon_to_tile, get_tile, get_tile_for_latlon
from ui_styles import draw_maps_style, draw_scifi_style
from PIL import Image
import pygame


pygame.init()


# --- Configurable ---
simulate_movement = True # poner False cuando uses GPS real
allow_download_tiles = True # la primera vez descarga; luego puedes poner False
interface_mode = 'maps' # 'maps' o 'scifi'
resolutions = {
    '1': (800, 480),
    '2': (1280, 720),
    '3': (1920, 1080)
}
current_res_key = '1'
WIDTH, HEIGHT = resolutions[current_res_key]


# Coordenadas iniciales (ejemplo: Barcelona)
lat = 41.387
lon = 2.170
speed = 35
heading = 'NNE'
zoom = 15


screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption('HUD Map Prototype')
font = pygame.font.SysFont('monospace', 24)
clock = pygame.time.Clock()


# util: convertir PIL image a surface
def pil_to_surface(img_pil):
    mode = img_pil.mode
    size = img_pil.size
    data = img_pil.tobytes()
    return pygame.image.fromstring(data, size, mode).convert()


# función para obtener y escalar tile central (offline-first)


def render_map_center(lat, lon, zoom, w, h):
    # obtenemos el tile central y lo escalamos a la ventana
    x_tile, y_tile = latlon_to_tile(lat, lon, zoom)
    pil = get_tile(zoom, x_tile, y_tile, allow_download=allow_download_tiles)
    surf = pil_to_surface(pil)
    surf = pygame.transform.scale(surf, (w, h))
    return surf


# Variables para simulación
x_off = 0
y_off = 0
move_speed = 0.0002 # grados por frame (ajustable)


running = True
t = 0


## While loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
        elif event.key in (pygame.K_1, pygame.K_2, pygame.K_3):
            # cambiar resolución
            current_res_key = chr(event.key)
            WIDTH, HEIGHT = resolutions[current_res_key]
            screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
        elif event.key == pygame.K_m:
            interface_mode = 'maps'
        elif event.key == pygame.K_s:
            interface_mode = 'scifi'
        elif event.key == pygame.K_SPACE:
            simulate_movement = not simulate_movement
    
    keys = pygame.key.get_pressed()
    if simulate_movement:
        if keys[pygame.K_UP]:
            lat += move_speed
        if keys[pygame.K_DOWN]:
            lat -= move_speed
        if keys[pygame.K_LEFT]:
            lon -= move_speed
        if keys[pygame.K_RIGHT]:
            lon += move_speed

    # render map
    try:
        map_surf = render_map_center(lat, lon, zoom, WIDTH, HEIGHT)
    except Exception as e:
        # en caso de fallo, crear fondo gris
        map_surf = pygame.Surface((WIDTH, HEIGHT))
        map_surf.fill((30, 30, 30))

    screen.blit(map_surf, (0, 0))


    # dibujar marcador del coche en el centro
    pygame.draw.circle(screen, (0, 255, 0), (WIDTH // 2, HEIGHT // 2), 8)


    # UI por modo
    if interface_mode == 'maps':
        draw_maps_style(screen, font, lat, lon, speed, heading)
    else:
        draw_scifi_style(screen, font, lat, lon, speed, heading, t)


    # texto ayuda (pequeño)
    help_text = font.render('1/2/3: res M: maps S: scifi SPACE: toggle sim', True, (200,200,200))
    screen.blit(help_text, (10, HEIGHT - 30))


    pygame.display.flip()
    t += 1
    clock.tick(30)


pygame.quit()
sys.exit()