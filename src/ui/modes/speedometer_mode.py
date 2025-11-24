from ui.styles import draw_speedometer

class SpeedometerMode:
    def __init__(self, screen, font):
        self.screen = screen
        self.font = font

    def draw(self, lat, lon, speed, heading, zoom):
        # Black background
        self.screen.fill((0, 0, 0))
        draw_speedometer(self.screen, self.font, speed)