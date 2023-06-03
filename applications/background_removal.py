import cv2
import numpy as np
from core.camera import RealSenseCamera

def remove_background():
    """Remove background based on depth threshold"""
    camera = RealSenseCamera()
    
    # Set clipping distance (1 meter)
    clipping_distance = 1.0 / camera.depth_scale
    
    try:
        while True:
            frames = camera.get_frames()
            depth_frame = frames.get_depth_frame()
            color_frame = frames.get_color_frame()
            
            if depth_frame and color_frame:
                depth_image = np.asanyarray(depth_frame.get_data())
                color_image = np.asanyarray(color_frame.get_data())
                
                # Remove background
                grey_color = 153
                depth_image_3d = np.dstack((depth_image, depth_image, depth_image))
                bg_removed = np.where(
                    (depth_image_3d > clipping_distance) | (depth_image_3d <= 0), 
                    grey_color, 
                    color_image
                )
                
                # Apply colormap to depth image
                depth_colormap = cv2.applyColorMap(
                    cv2.convertScaleAbs(depth_image, alpha=0.03), 
                    cv2.COLORMAP_JET
                )
                
                # Stack images horizontally
                images = np.hstack((bg_removed, depth_colormap))
                
                cv2.imshow('Background Removal', images)
                
            if cv2.waitKey(1) == ord('q'):
                break
                
    finally:
        camera.stop()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    remove_background()