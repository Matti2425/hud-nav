import pygame
from config import *
from gps import GPSSimulator
from ui.modes import MapMode, ScifiMode, SpeedometerMode

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("HUD Navigation")
font = pygame.font.SysFont('monospace', 24)
clock = pygame.time.Clock()

gps = GPSSimulator(INITIAL_LAT, INITIAL_LON, INITIAL_SPEED, INITIAL_HEADING)

modes = {
    'maps': MapMode(screen, font),
    'scifi': ScifiMode(screen, font),
    'speedo': SpeedometerMode(screen, font)
}

current_mode = modes[INTERFACE_MODE]

running = True
while running:
    dt = clock.tick(FPS_TARGET) / 1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key in (pygame.K_1, pygame.K_2, pygame.K_3):
                CURRENT_RES_KEY = chr(event.key)
                WIDTH, HEIGHT = RESOLUTIONS[CURRENT_RES_KEY]
                screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
            elif event.key == pygame.K_m:
                INTERFACE_MODE = 'maps'
                current_mode = modes['maps']
            elif event.key == pygame.K_s:
                INTERFACE_MODE = 'scifi'
                current_mode = modes['scifi']
            elif event.key == pygame.K_p:
                INTERFACE_MODE = 'speedo'
                current_mode = modes['speedo']

    gps.update(dt)
    lat, lon = gps.get_position()
    speed = gps.get_speed()
    heading = gps.get_heading()

    screen.fill((0, 0, 0))
    current_mode.draw(lat, lon, speed, heading, ZOOM)
    pygame.display.flip()

pygame.quit()