import pyrealsense2 as rs
import numpy as np
import json
import os

class CameraCalibration:
    """Class to handle camera calibration parameters"""
    
    def __init__(self, config_path="config/calibration.json"):
        self.config_path = config_path
        self.camera_params = {}
        
    def calibrate_camera(self):
        """Calibrate camera and save parameters to file"""
        pipeline = rs.pipeline()
        config = rs.config()
        config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
        config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
        
        try:
            pipeline.start(config)
            frames = pipeline.wait_for_frames()
            depth = frames.get_depth_frame()
            color = frames.get_color_frame()
            
            depth_profile = depth.get_profile()
            color_profile = color.get_profile()
            
            cvsprofile = rs.video_stream_profile(color_profile)
            dvsprofile = rs.video_stream_profile(depth_profile)
            
            color_intrin = cvsprofile.get_intrinsics()
            depth_intrin = dvsprofile.get_intrinsics()
            extrin = depth_profile.get_extrinsics_to(color_profile)
            
            self.camera_params = {
                "color_intrinsics": {
                    "width": color_intrin.width,
                    "height": color_intrin.height,
                    "fx": color_intrin.fx,
                    "fy": color_intrin.fy,
                    "ppx": color_intrin.ppx,
                    "ppy": color_intrin.ppy,
                    "coeffs": color_intrin.coeffs,
                    "model": str(color_intrin.model)
                },
                "depth_intrinsics": {
                    "width": depth_intrin.width,
                    "height": depth_intrin.height,
                    "fx": depth_intrin.fx,
                    "fy": depth_intrin.fy,
                    "ppx": depth_intrin.ppx,
                    "ppy": depth_intrin.ppy,
                    "coeffs": depth_intrin.coeffs,
                    "model": str(depth_intrin.model)
                },
                "extrinsics": {
                    "rotation": extrin.rotation,
                    "translation": extrin.translation
                }
            }
            
            # Save to file
            os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
            with open(self.config_path, 'w') as f:
                json.dump(self.camera_params, f, indent=4)
                
            return True
            
        except Exception as e:
            print(f"Calibration failed: {e}")
            return False
        finally:
            pipeline.stop()
    
    def load_calibration(self):
        """Load calibration parameters from file"""
        try:
            with open(self.config_path, 'r') as f:
                self.camera_params = json.load(f)
            return True
        except FileNotFoundError:
            print("Calibration file not found. Run calibration first.")
            return False