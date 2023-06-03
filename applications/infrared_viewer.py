import cv2
import numpy as np
from core.camera import RealSenseCamera

def view_infrared_stream():
    """View left and right infrared streams"""
    camera = RealSenseCamera(enable_color=False, enable_depth=False, enable_ir=True)
    
    try:
        while True:
            left_ir, right_ir = camera.get_ir_frames()
            
            if left_ir and right_ir:
                left_ir_image = np.asanyarray(left_ir.get_data())
                right_ir_image = np.asanyarray(right_ir.get_data())
                
                # Display the images side by side
                both_ir_images = np.hstack((left_ir_image, right_ir_image))
                cv2.imshow('Left and Right Infrared Images', both_ir_images)
                
            if cv2.waitKey(1) == ord('q'):
                break
                
    finally:
        camera.stop()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    view_infrared_stream()