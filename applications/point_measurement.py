import cv2
import numpy as np
from core.camera import RealSenseCamera

def measure_3d_points():
    """Measure 3D coordinates of pixels in real-time"""
    camera = RealSenseCamera()
    
    # Get depth intrinsics
    depth_profile = camera.profile.get_stream(rs.stream.depth)
    depth_intrinsics = depth_profile.as_video_stream_profile().get_intrinsics()
    
    try:
        while True:
            frames = camera.get_frames()
            depth_frame = frames.get_depth_frame()
            color_frame = frames.get_color_frame()
            
            if depth_frame and color_frame:
                depth_image = np.asanyarray(depth_frame.get_data())
                color_image = np.asanyarray(color_frame.get_data())
                
                # Create a copy for drawing
                display_image = color_image.copy()
                
                # Get center pixel coordinates
                center_x, center_y = color_image.shape[1] // 2, color_image.shape[0] // 2
                
                # Draw crosshair at center
                cv2.drawMarker(display_image, (center_x, center_y), (0, 255, 0), 
                              cv2.MARKER_CROSS, 20, 2)
                
                # Get depth value at center
                depth = depth_frame.get_distance(center_x, center_y)
                
                if depth > 0:
                    # Deproject pixel to 3D point
                    point = rs.rs2_deproject_pixel_to_point(
                        depth_intrinsics, [center_x, center_y], depth
                    )
                    
                    # Display coordinates
                    cv2.putText(display_image, 
                               f"X: {point[0]:.2f}m, Y: {point[1]:.2f}m, Z: {point[2]:.2f}m", 
                               (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                
                cv2.imshow('3D Point Measurement', display_image)
                
            if cv2.waitKey(1) == ord('q'):
                break
                
    finally:
        camera.stop()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    measure_3d_points()