import pyrealsense2 as rs
import numpy as np

class RealSenseCamera:
    """Main camera class to handle RealSense operations"""
    
    def __init__(self, enable_color=True, enable_depth=True, enable_ir=False):
        self.pipeline = rs.pipeline()
        self.config = rs.config()
        self.align = rs.align(rs.stream.color)
        
        if enable_color:
            self.config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
        if enable_depth:
            self.config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
        if enable_ir:
            self.config.enable_stream(rs.stream.infrared, 1, 640, 480, rs.format.y8, 30)
            self.config.enable_stream(rs.stream.infrared, 2, 640, 480, rs.format.y8, 30)
        
        self.profile = self.pipeline.start(self.config)
        self.depth_scale = self.profile.get_device().first_depth_sensor().get_depth_scale()
        
    def get_frames(self):
        """Get aligned frames from camera"""
        frames = self.pipeline.wait_for_frames()
        aligned_frames = self.align.process(frames)
        return aligned_frames
    
    def get_depth_frame(self):
        """Get depth frame"""
        frames = self.get_frames()
        return frames.get_depth_frame()
    
    def get_color_frame(self):
        """Get color frame"""
        frames = self.get_frames()
        return frames.get_color_frame()
    
    def get_ir_frames(self):
        """Get IR frames (left and right)"""
        frames = self.pipeline.wait_for_frames()
        left_ir = frames.get_infrared_frame(1)
        right_ir = frames.get_infrared_frame(2)
        return left_ir, right_ir
    
    def stop(self):
        """Stop the camera pipeline"""
        self.pipeline.stop()