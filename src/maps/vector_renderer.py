import sqlite3
import io
import pygame
from mapbox_vector_tile import decode
import math
import json

class VectorMapRenderer:
    def __init__(self, mbtiles_path, style_path=None, cache_size=200, tile_size=256):
        self.mbtiles_path = mbtiles_path
        self.tile_size = tile_size
        self.cache_size = cache_size
        self.tile_cache = {}  # {(z,x,y): surface}
        self.style = {}
        if style_path:
            self.set_style(style_path)
        try:
            self.conn = sqlite3.connect(self.mbtiles_path)
            self.cursor = self.conn.cursor()
        except Exception as e:
            print(f"Error connecting to MBTiles: {e}")
            self.conn = None

    def set_style(self, style_path):
        with open(style_path, "r") as f:
            self.style = json.load(f)

    def deg2num(self, lat_deg, lon_deg, zoom):
        """Convert lat/lon to tile numbers."""
        lat_rad = math.radians(lat_deg)
        n = 2.0 ** zoom
        xtile = int((lon_deg + 180.0) / 360.0 * n)
        ytile = int((1.0 - math.log(math.tan(lat_rad) + 1.0 / math.cos(lat_rad)) / math.pi) / 2.0 * n)
        return xtile, ytile

    def get_tile_data(self, z, x, y):
        """Get tile data from the MBTiles 'map' table joined with 'images' table."""
        if not self.conn:
            return None
        tms_y = (2 ** z - 1) - y
        # Join map and images tables to get tile data
        self.cursor.execute("SELECT i.tile_data FROM map m JOIN images i ON m.tile_id = i.tile_id WHERE m.zoom_level=? AND m.tile_column=? AND m.tile_row=?", (z, x, tms_y))
        row = self.cursor.fetchone()
        if row:
            tile_data = row[0]
            # Handle gzip compression if present
            if tile_data.startswith(b'\x1f\x8b'):  # gzip header
                import gzip
                tile_data = gzip.decompress(tile_data)
            return tile_data
        else:
            print(f"No tile data for z={z}, x={x}, y={y} (tms_y={tms_y})")
            return None

    def render_tile(self, z, x, y):
        key = (z, x, y)
        if key in self.tile_cache:
            return self.tile_cache[key]

        data = self.get_tile_data(z, x, y)
        surf = pygame.Surface((self.tile_size, self.tile_size), pygame.SRCALPHA)

        if data:
            try:
                tile = decode(data)
                for layer_name, layer in tile.items():
                    for feature in layer.get("features", []):
                        geom = feature["geometry"]
                        self._draw_geometry(surf, geom, layer_name)
            except Exception as e:
                print(f"Decode failed: {e}")

        if len(self.tile_cache) >= self.cache_size:
            self.tile_cache.pop(next(iter(self.tile_cache)))
        self.tile_cache[key] = surf
        return surf

    def _draw_geometry(self, surf, geom, layer_name):
        """Draw polygons, lines, or points using style JSON."""
        layer_style = self.style.get("layers", {}).get(layer_name, {})
        fill_color = layer_style.get("fill-color", (150,150,150,150))
        line_color = layer_style.get("line-color", (0,0,0,200))
        line_width = layer_style.get("line-width", 2)

        # Convert string colors to pygame.Color if needed
        if isinstance(fill_color, str): fill_color = pygame.Color(fill_color)
        if isinstance(line_color, str): line_color = pygame.Color(line_color)

        if geom["type"] == "Polygon":
            for ring in geom["coordinates"]:
                pygame.draw.polygon(surf, fill_color, [(int(x), int(y)) for x,y in ring])
                pygame.draw.polygon(surf, line_color, [(int(x), int(y)) for x,y in ring], line_width)
        elif geom["type"] == "LineString":
            pygame.draw.lines(surf, line_color, False, [(int(x), int(y)) for x,y in geom["coordinates"]], line_width)
        elif geom["type"] == "Point":
            x, y = geom["coordinates"]
            pygame.draw.circle(surf, fill_color, (int(x), int(y)), 3)

    def render(self, lat, lon, zoom, width, height):
        """Render the map centered at lat/lon with specified width/height."""
        xtile, ytile = self.deg2num(lat, lon, zoom)
        tiles_x = math.ceil(width / self.tile_size) + 2
        tiles_y = math.ceil(height / self.tile_size) + 2

        surf = pygame.Surface((tiles_x*self.tile_size, tiles_y*self.tile_size), pygame.SRCALPHA)
        start_x = xtile - tiles_x//2
        start_y = ytile - tiles_y//2

        for dx in range(tiles_x):
            for dy in range(tiles_y):
                tile_surf = self.render_tile(zoom, start_x+dx, start_y+dy)
                surf.blit(tile_surf, (dx*self.tile_size, dy*self.tile_size))

        # recortar al tamaño de la ventana
        center_x = (tiles_x*self.tile_size)//2
        center_y = (tiles_y*self.tile_size)//2
        rect = pygame.Rect(center_x - width//2, center_y - height//2, width, height)
        return surf.subsurface(rect).copy()