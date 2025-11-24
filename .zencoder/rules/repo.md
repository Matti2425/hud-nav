---
description: Repository Information Overview
alwaysApply: true
---

# HUD Navigation Information

## Summary
A Python application using Pygame to render vector maps in a heads-up display style for navigation, supporting multiple resolutions and styles.

## Structure
- **main.py**: Main entry point for the Pygame application, handling the game loop, user input, and rendering modes.
- **map_fetcher.py**: Module for fetching map data.
- **map_renderer.py**: Base map rendering functionality.
- **map_renderer_vector.py**: Vector-based map renderer implementation.
- **tilefile_reader.py**: Utility for reading tile files.
- **ui_styles.py**: Defines UI styling functions for different display modes.
- **map_style.json**: JSON configuration for map styling.
- **requirements.txt**: Python dependencies.
- **resources/**: Directory containing assets like MBTiles files (git-ignored).
- **maps_cache/**: Directory for cached map tiles.
- **hud-env/**: Python virtual environment (git-ignored).
- **__pycache__/**: Compiled Python bytecode.

## Language & Runtime
**Language**: Python  
**Version**: 3.11  
**Build System**: None  
**Package Manager**: pip  

## Dependencies
**Main Dependencies**:  
- pygame==2.5.2  
- Pillow==10.4.0  
- requests==2.32.3  
- python-dotenv==1.0.1  
- mapbox-vector-tile==2.2.0  

## Build & Installation
```bash
pip install -r requirements.txt
```

## Main Files & Resources
**Entry Point**: main.py  
**Configuration Files**: map_style.json  
**Assets**: resources/ (MBTiles, images, etc.)  

To run the application:  
```bash
python main.py
```