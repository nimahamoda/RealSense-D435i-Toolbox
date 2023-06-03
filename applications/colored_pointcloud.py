import open3d as o3d
from core.camera import RealSenseCamera
from core.pointcloud_utils import PointCloudGenerator

def view_colored_pointcloud():
    """View real-time colored point cloud"""
    camera = RealSenseCamera()
    
    # Get depth intrinsics
    depth_profile = camera.profile.get_stream(rs.stream.depth)
    depth_intrinsics = depth_profile.as_video_stream_profile().get_intrinsics()
    
    # Create point cloud generator
    pc_generator = PointCloudGenerator(depth_intrinsics)
    
    # Create visualizer
    vis = o3d.visualization.Visualizer()
    vis.create_window()
    
    # Add initial geometry
    pcd = o3d.geometry.PointCloud()
    vis.add_geometry(pcd)
    
    try:
        while True:
            frames = camera.get_frames()
            depth_frame = frames.get_depth_frame()
            color_frame = frames.get_color_frame()
            
            if depth_frame and color_frame:
                # Create colored point cloud
                colored_pc = pc_generator.create_colored_pointcloud(depth_frame, color_frame)
                
                # Update visualizer
                pcd.points = colored_pc.points
                pcd.colors = colored_pc.colors
                
                vis.update_geometry(pcd)
                vis.poll_events()
                vis.update_renderer()
                
    finally:
        camera.stop()
        vis.destroy_window()

if __name__ == "__main__":
    view_colored_pointcloud()