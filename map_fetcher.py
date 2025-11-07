# map_fetcher.py
import os
import math
from io import BytesIO
from PIL import Image
import requests


CACHE_DIR = 'maps_cache'
USER_AGENT = 'hud-prototype/1.0 (+https://example.local)'


os.makedirs(CACHE_DIR, exist_ok=True)


def latlon_to_tile(lat, lon, zoom):
    xtile = int((lon + 180.0) / 360.0 * (2 ** zoom))
    ytile = int((1.0 - math.log(math.tan(math.radians(lat)) + 1.0 / math.cos(math.radians(lat))) / math.pi)/ 2.0 * (2 ** zoom))
    return xtile, ytile


def tile_path(zoom, x, y):
    folder = os.path.join(CACHE_DIR, str(zoom), str(x))
    os.makedirs(folder, exist_ok=True)
    return os.path.join(folder, f"{y}.png")


def fetch_tile_online(zoom, x, y):
    url = f"https://tile.openstreetmap.org/{zoom}/{x}/{y}.png"
    headers = {'User-Agent': USER_AGENT}
    r = requests.get(url, headers=headers, timeout=10)
    r.raise_for_status()
    return Image.open(BytesIO(r.content)).convert('RGBA')


def get_tile(zoom, x, y, allow_download=True):
    """Devuelve un objeto PIL Image del tile. Si no está en cache y allow_download=True lo descarga."""
    path = tile_path(zoom, x, y)
    if os.path.isfile(path):
        try:
            return Image.open(path).convert('RGBA')
        except Exception:
            # si está corrupto, borra y re-descarga
            os.remove(path)
    if not allow_download:
        # generar tile en gris si no hay conexión
        img = Image.new('RGBA', (256, 256), (40, 40, 40, 255))
        return img
    img = fetch_tile_online(zoom, x, y)
    img.save(path)
    return img


# función de ayuda para obtener tile centrado en lat/lon (devuelve tile imagen escala 256x256)
def get_tile_for_latlon(lat, lon, zoom, allow_download=True):
    x, y = latlon_to_tile(lat, lon, zoom)
    return get_tile(zoom, x, y, allow_download)