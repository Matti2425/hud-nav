# HUD Navigation

A Python-based offline map navigation application with HUD-style interface, designed for Raspberry Pi with USB GPS module.

## Features

- Offline vector map rendering using MBTiles
- Multiple UI modes: Map navigation, Sci-Fi interface, Speedometer
- GPS simulation (configurable for real GPS input)
- Resizable display with multiple resolutions
- Modular architecture for easy extension

## Installation

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Download or obtain MBTiles file for your region (e.g., from OpenMapTiles) and place it in `resources/` as `osm-2020-02-10-v3.11_europe_spain.mbtiles`

## Usage

Run the application:
```bash
python src/main.py
```

### Controls
- **1, 2, 3**: Change resolution
- **M**: Switch to Map mode
- **S**: Switch to Sci-Fi mode
- **P**: Switch to Speedometer mode
- **ESC**: Exit

## Configuration

Edit `src/config.py` to adjust settings like initial position, simulation parameters, and paths.

Set `SIMULATE_MOVEMENT = False` in `src/config.py` for real GPS on Raspberry Pi.

## Architecture

- `src/config.py`: Configuration settings
- `src/gps/`: GPS handling (simulator and real GPS reader)
- `src/maps/`: Map rendering modules (vector, raster, online fetcher)
- `src/ui/`: User interface components and modes
- `src/main.py`: Main application loop

## Raspberry Pi Setup

1. Connect USB GPS module (ensure it's on `/dev/ttyUSB0` or update `GPS_PORT` in config).
2. Install dependencies as above.
3. Run in headless mode if needed (use VNC or SSH with X forwarding).
4. For better performance, consider using a display like HDMI or touchscreen.

## Future Enhancements

- Integrate real GPS module for live navigation
- Add routing and turn-by-turn directions
- Implement additional UI modes
- Optimize for Raspberry Pi performance