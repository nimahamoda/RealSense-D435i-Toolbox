# Intel RealSense D435i Applications

A collection of Python applications for Intel RealSense D435i depth camera, featuring a modular and object-oriented design.

## Features

- Camera calibration and parameter management
- Infrared stream viewing
- Color and depth stream viewing
- Background removal based on depth
- 3D point measurement
- Real-time colored point cloud visualization

## Installation

1. Install Intel RealSense SDK 2.0: https://github.com/IntelRealSense/librealsense
3. Clone this repo
2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. First, calibrate the camera:
   ```bash
   python scripts/calibrate_camera.py
   ```

2. Run any of the applications:
   ```bash
   python applications/infrared_viewer.py
   python applications/depth_viewer.py
   python applications/background_removal.py
   python applications/point_measurement.py
   python applications/colored_pointcloud.py
   ```

## Project Structure

- `config/`: Camera calibration configuration
- `core/`: Core functionality (camera handling, point cloud generation)
- `applications/`: Various applications using the camera
- `scripts/`: Utility scripts
