import sqlite3

conn = sqlite3.connect('resources/osm-2020-02-10-v3.11_europe_spain.mbtiles')
c = conn.cursor()

# Check map table structure
c.execute('PRAGMA table_info(map)')
print('Map table columns:', c.fetchall())

# Check if there's a separate images table
c.execute('PRAGMA table_info(images)')
print('Images table columns:', c.fetchall())

# Get a sample row from map
c.execute('SELECT * FROM map LIMIT 1')
row = c.fetchone()
print('Sample map row:', row)

# If there's tile_id, check what it references in images
if row and len(row) >= 4:
    tile_id = row[3]
    c.execute('SELECT * FROM images WHERE tile_id=?', (tile_id,))
    image_row = c.fetchone()
    print('Corresponding image row:', image_row)
    if image_row:
        print('Image data length:', len(image_row[1]) if len(image_row) > 1 else 'N/A')
        print('Image data starts with:', image_row[1][:20] if len(image_row) > 1 else 'N/A')

conn.close()