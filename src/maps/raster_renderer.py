import sqlite3
import io
import pygame
from PIL import Image
import math
import os
from .online_fetcher import get_tile

class MapRenderer:
    def __init__(self, mbtiles_path, tile_size=256, cache_size=100):
        self.mbtiles_path = mbtiles_path
        self.tile_size = tile_size
        self.cache_size = cache_size
        self.tile_cache = {}  # {(z,x,y): surface}
        self.use_online = False
        try:
            self.conn = sqlite3.connect(self.mbtiles_path)
            self.cursor = self.conn.cursor()
        except Exception as e:
            print(f"Error connecting to MBTiles: {e}. Falling back to online tiles.")
            self.conn = None
            self.use_online = True
    
    def __del__(self):
        if self.conn:
            self.conn.close()

    def deg2num(self, lat_deg, lon_deg, zoom):
        """Convert lat/lon to tile numbers"""
        lat_rad = math.radians(lat_deg)
        n = 2.0 ** zoom
        xtile = int((lon_deg + 180.0) / 360.0 * n)
        ytile = int((1.0 - math.log(math.tan(lat_rad) + 1.0 / math.cos(lat_rad)) / math.pi) / 2.0 * n)
        return xtile, ytile

    def get_tile(self, z, x, y):
        key = (z, x, y)
        if key in self.tile_cache:
            return self.tile_cache[key]
        if self.conn:
            # Try 'tiles' table first, then 'map'
            for table in ['tiles', 'map']:
                tms_y = (2 ** z - 1) - y
                self.cursor.execute(f"SELECT tile_data FROM {table} WHERE zoom_level=? AND tile_column=? AND tile_row=?",
                                    (z, x, tms_y))
                row = self.cursor.fetchone()
                if row:
                    try:
                        img = Image.open(io.BytesIO(row[0])).convert("RGBA")
                        surf = pygame.image.fromstring(img.tobytes(), img.size, img.mode)
                        if len(self.tile_cache) >= self.cache_size:
                            self.tile_cache.pop(next(iter(self.tile_cache)))
                        self.tile_cache[key] = surf
                        return surf
                    except Exception as e:
                        print(f"Error loading tile from {table}: {e}")
                        continue
        # Tile vacío (gris)
        surf = pygame.Surface((self.tile_size, self.tile_size))
        surf.fill((100, 100, 100))  # Lighter gray to distinguish
        return surf

    def render(self, lat, lon, zoom, width, height):
        """Renderiza la ventana centrada en lat/lon"""
        xtile, ytile = self.deg2num(lat, lon, zoom)
        tiles_x = math.ceil(width / self.tile_size) + 2
        tiles_y = math.ceil(height / self.tile_size) + 2

        surf = pygame.Surface((tiles_x * self.tile_size, tiles_y * self.tile_size))
        start_x = xtile - tiles_x // 2
        start_y = ytile - tiles_y // 2

        for dx in range(tiles_x):
            for dy in range(tiles_y):
                tile_surf = self.get_tile(zoom, start_x + dx, start_y + dy)
                surf.blit(tile_surf, (dx * self.tile_size, dy * self.tile_size))

        # Crop al tamaño exacto de ventana
        center_x = self.tile_size * (tiles_x // 2) + self.tile_size // 2
        center_y = self.tile_size * (tiles_y // 2) + self.tile_size // 2
        rect = pygame.Rect(center_x - width // 2, center_y - height // 2, width, height)
        return surf.subsurface(rect).copy()