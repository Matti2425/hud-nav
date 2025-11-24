import math
from config import SIMULATE_MOVEMENT, MOVE_SPEED

class GPSSimulator:
    def __init__(self, lat, lon, speed, heading):
        self.lat = lat
        self.lon = lon
        self.speed = speed
        self.heading = heading
        self.t = 0

    def update(self, dt):
        if SIMULATE_MOVEMENT:
            self.t += dt
            # Simulate movement
            self.lat += MOVE_SPEED * (math.sin(self.t * 0.1) * 0.01)
            self.lon += MOVE_SPEED * (math.cos(self.t * 0.1) * 0.01)
            self.speed = 30 + 10 * math.sin(self.t * 0.1)
            headings = ['N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE', 'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW']
            self.heading = headings[int(self.t * 0.5) % len(headings)]

    def get_position(self):
        return self.lat, self.lon

    def get_speed(self):
        return self.speed

    def get_heading(self):
        return self.heading