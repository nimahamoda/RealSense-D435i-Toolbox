import cv2
import numpy as np
from core.camera import RealSenseCamera

def view_depth_stream():
    """View color and depth streams side by side"""
    camera = RealSenseCamera()
    
    try:
        while True:
            frames = camera.get_frames()
            depth_frame = frames.get_depth_frame()
            color_frame = frames.get_color_frame()
            
            if depth_frame and color_frame:
                depth_image = np.asanyarray(depth_frame.get_data())
                color_image = np.asanyarray(color_frame.get_data())
                
                # Apply colormap to depth image
                depth_colormap = cv2.applyColorMap(
                    cv2.convertScaleAbs(depth_image, alpha=0.03), 
                    cv2.COLORMAP_JET
                )
                
                # Stack images horizontally
                images = np.hstack((color_image, depth_colormap))
                
                cv2.imshow('Color and Depth Streams', images)
                
            if cv2.waitKey(1) == ord('q'):
                break
                
    finally:
        camera.stop()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    view_depth_stream()