import sqlite3
import math

def deg2num(lat_deg, lon_deg, zoom):
    lat_rad = math.radians(lat_deg)
    n = 2.0 ** zoom
    xtile = int((lon_deg + 180.0) / 360.0 * n)
    ytile = int((1.0 - math.log(math.tan(lat_rad) + 1.0 / math.cos(lat_rad)) / math.pi) / 2.0 * n)
    return xtile, ytile

lat = 41.385
lon = 2.173
zoom = 10

x, y = deg2num(lat, lon, zoom)
print(f"Tile: z={zoom}, x={x}, y={y}")
tms_y = (2 ** zoom - 1) - y
print(f"TMS y: {tms_y}")

conn = sqlite3.connect('resources/osm-2020-02-10-v3.11_europe_spain.mbtiles')
c = conn.cursor()

# Try 'map' table
c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='map'")
if c.fetchone():
    table = 'map'
else:
    table = 'tiles'

print(f"Using table: {table}")

c.execute(f"SELECT tile_data FROM {table} WHERE zoom_level=? AND tile_column=? AND tile_row=?", (zoom, x, tms_y))
row = c.fetchone()
if row:
    print("Tile found, length:", len(row[0]))
    data = row[0]
    if data.startswith(b'\x1a'):
        print("Data is vector (protobuf)")
    elif data.startswith(b'\x89PNG'):
        print("Data is PNG raster")
    else:
        print("Data type unknown")
else:
    print("Tile not found")

conn.close()