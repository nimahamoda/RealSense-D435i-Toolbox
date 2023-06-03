from config.camera_calibration import CameraCalibration

def main():
    """Calibrate camera and save parameters"""
    calibrator = CameraCalibration()
    if calibrator.calibrate_camera():
        print("Camera calibration successful!")
        print("Parameters saved to config/calibration.json")
    else:
        print("Camera calibration failed!")

if __name__ == "__main__":
    main()