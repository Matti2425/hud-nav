import sqlite3

conn = sqlite3.connect('resources/osm-2020-02-10-v3.11_europe_spain.mbtiles')
c = conn.cursor()

c.execute('SELECT name FROM sqlite_master WHERE type="table"')
tables = [row[0] for row in c.fetchall()]
print("Tables:", tables)

if 'map' in tables:
    c.execute('PRAGMA table_info(map)')
    print("Columns in map:", c.fetchall())
    # Check data type
    c.execute('SELECT tile_data FROM map LIMIT 1')
    row = c.fetchone()
    if row:
        data = row[0]
        if data.startswith(b'\x1a'):  # Protobuf start byte
            print("Data in 'map' table appears to be vector (protobuf)")
        else:
            print("Data in 'map' table appears to be raster (image)")
elif 'tiles' in tables:
    c.execute('PRAGMA table_info(tiles)')
    print("Columns in tiles:", c.fetchall())
    c.execute('SELECT tile_data FROM tiles LIMIT 1')
    row = c.fetchone()
    if row:
        data = row[0]
        if data.startswith(b'\x89PNG') or data.startswith(b'\xff\xd8'):  # PNG or JPEG
            print("Data in 'tiles' table appears to be raster (image)")
        else:
            print("Data in 'tiles' table appears to be vector (protobuf)")
else:
    print("No 'map' or 'tiles' table found")

conn.close()