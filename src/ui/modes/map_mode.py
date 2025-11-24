from ui.styles import draw_maps_style
from maps.vector_renderer import VectorMapRenderer
from maps.raster_renderer import MapRenderer
from config import MBTILES_PATH, STYLE_PATH, MAP_STYLE

class MapMode:
    def __init__(self, screen, font):
        self.screen = screen
        self.font = font
        if MAP_STYLE == 'vector':
            self.map_renderer = VectorMapRenderer(MBTILES_PATH, style_path=STYLE_PATH)
        else:
            self.map_renderer = MapRenderer(MBTILES_PATH)

    def draw(self, lat, lon, speed, heading, zoom):
        # Render map
        map_surf = self.map_renderer.render(lat, lon, zoom, self.screen.get_width(), self.screen.get_height())
        self.screen.blit(map_surf, (0, 0))
        # Draw UI
        draw_maps_style(self.screen, self.font, lat, lon, speed, heading)