# config.py
import os

# Display settings
RESOLUTIONS = {'1': (800,480), '2':(1280,720), '3':(1920,1080)}
CURRENT_RES_KEY = '1'
WIDTH, HEIGHT = RESOLUTIONS[CURRENT_RES_KEY]
FPS_TARGET = 25
ZOOM = 10

# Initial position
INITIAL_LAT, INITIAL_LON = 41.385, 2.173
INITIAL_SPEED = 35
INITIAL_HEADING = 'NNE'

# Modes
INTERFACE_MODE = 'maps'  # 'maps', 'scifi', 'speedo'
MAP_STYLE = 'raster'  # 'vector' or 'raster'

# Paths
MBTILES_PATH = "resources/osm-2020-02-10-v3.11_europe_spain.mbtiles"
STYLE_PATH = "src/maps/map_style.json"
CACHE_DIR = 'maps_cache'

# Simulation
SIMULATE_MOVEMENT = True  # Set to False for real GPS
FLIP_DISPLAY = False
MOVE_SPEED = 0.0002

# GPS
GPS_PORT = '/dev/ttyUSB0'  # For Raspberry Pi, change if needed
GPS_BAUDRATE = 9600