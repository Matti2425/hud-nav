import sys
sys.path.append('src')

from maps.raster_renderer import MapRenderer
import pygame

pygame.init()

# Test raster renderer
print("Testing raster renderer...")
renderer = MapRenderer('resources/osm-2020-02-10-v3.11_europe_spain.mbtiles')

# Test coordinates from check_tile.py
lat, lon, zoom = 41.385, 2.173, 10
x, y = renderer.deg2num(lat, lon, zoom)
print(f"Tile coordinates: z={zoom}, x={x}, y={y}")

try:
    surf = renderer.get_tile(zoom, x, y)
    print(f"Tile loaded successfully! Size: {surf.get_size()}")
except Exception as e:
    print(f"Error loading tile: {e}")

# Test vector renderer
print("\nTesting vector renderer...")
from maps.vector_renderer import VectorMapRenderer

vector_renderer = VectorMapRenderer('resources/osm-2020-02-10-v3.11_europe_spain.mbtiles', 'src/maps/map_style.json')

try:
    data = vector_renderer.get_tile_data(zoom, x, y)
    if data:
        print(f"Vector tile data loaded successfully! Length: {len(data)} bytes")
        print(f"Data starts with: {data[:20]}")
    else:
        print("No vector tile data found")
except Exception as e:
    print(f"Error loading vector tile: {e}")