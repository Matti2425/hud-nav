# gps_reader.py - Real GPS reading using serial
import serial
import time

class GPSReader:
    def __init__(self, port='/dev/ttyUSB0', baudrate=9600):
        # Initialize GPS connection, e.g., serial port for USB GPS
        try:
            self.ser = serial.Serial(port, baudrate, timeout=1)
            print(f"Connected to GPS on {port}")
        except Exception as e:
            print(f"Failed to connect to GPS: {e}")
            self.ser = None
        self.lat = 0.0
        self.lon = 0.0
        self.speed = 0.0
        self.heading = 'N'

    def parse_nmea(self, line):
        if line.startswith('$GPRMC'):
            parts = line.split(',')
            if len(parts) > 10 and parts[2] == 'A':  # Valid fix
                lat_str = parts[3]
                lon_str = parts[5]
                speed_str = parts[7]
                heading_str = parts[8]
                try:
                    self.lat = float(lat_str[:2]) + float(lat_str[2:]) / 60.0
                    if parts[4] == 'S':
                        self.lat = -self.lat
                    self.lon = float(lon_str[:3]) + float(lon_str[3:]) / 60.0
                    if parts[6] == 'W':
                        self.lon = -self.lon
                    self.speed = float(speed_str) * 1.852  # knots to km/h
                    self.heading = heading_str
                except ValueError:
                    pass

    def update(self):
        if self.ser:
            try:
                line = self.ser.readline().decode('ascii', errors='ignore').strip()
                if line:
                    self.parse_nmea(line)
            except Exception as e:
                print(f"Error reading GPS: {e}")

    def get_position(self):
        return self.lat, self.lon

    def get_speed(self):
        return self.speed

    def get_heading(self):
        return self.heading