from ui.styles import draw_scifi_style

class ScifiMode:
    def __init__(self, screen, font):
        self.screen = screen
        self.font = font
        self.t = 0

    def draw(self, lat, lon, speed, heading, zoom):
        self.t += 1
        draw_scifi_style(self.screen, self.font, lat, lon, speed, heading, self.t)