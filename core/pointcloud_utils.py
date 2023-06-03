import numpy as np
import open3d as o3d
import pyrealsense2 as rs

class PointCloudGenerator:
    """Class to generate and process point clouds"""
    
    def __init__(self, depth_intrinsics):
        self.depth_intrinsics = depth_intrinsics
        
    def create_pointcloud_from_depth(self, depth_frame):
        """Create point cloud from depth frame"""
        depth_image = np.asanyarray(depth_frame.get_data())
        height, width = depth_image.shape
        
        # Generate grid of coordinates
        u, v = np.meshgrid(np.arange(width), np.arange(height), indexing='xy')
        
        # Calculate 3D coordinates
        z = depth_image * self.depth_scale
        x = (u - self.depth_intrinsics.ppx) / self.depth_intrinsics.fx * z
        y = (v - self.depth_intrinsics.ppy) / self.depth_intrinsics.fy * z
        
        # Stack coordinates and filter invalid points
        points = np.stack((x, y, z), axis=-1)
        valid_mask = z > 0
        points = points[valid_mask]
        
        return points
    
    def create_colored_pointcloud(self, depth_frame, color_frame):
        """Create colored point cloud from depth and color frames"""
        depth_image = np.asanyarray(depth_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data())
        height, width = depth_image.shape
        
        # Generate grid of coordinates
        u, v = np.meshgrid(np.arange(width), np.arange(height), indexing='xy')
        
        # Calculate 3D coordinates
        z = depth_image * self.depth_scale
        x = (u - self.depth_intrinsics.ppx) / self.depth_intrinsics.fx * z
        y = (v - self.depth_intrinsics.ppy) / self.depth_intrinsics.fy * z
        
        # Stack coordinates and colors, filter invalid points
        points = np.stack((x, y, z), axis=-1)
        colors = color_image.reshape(-1, 3) / 255.0
        valid_mask = z.flatten() > 0
        
        points = points.reshape(-1, 3)[valid_mask]
        colors = colors[valid_mask]
        
        # Create Open3D point cloud
        pcd = o3d.geometry.PointCloud()
        pcd.points = o3d.utility.Vector3dVector(points)
        pcd.colors = o3d.utility.Vector3dVector(colors)
        
        return pcd
    
    def deproject_pixel_to_point(self, pixel, depth):
        """Deproject a pixel to 3D point"""
        return rs.rs2_deproject_pixel_to_point(self.depth_intrinsics, pixel, depth)