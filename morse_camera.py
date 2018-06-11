import cv2
import time
from morse_log import log

class Camera():
    # Constructor...
    def __init__(self):
        w = 640  # Frame width...
        h = 480  # Frame hight...
        fps = 20.0  # Frames per second...
        resolution = (w, h)  # Frame size/resolution...
        self.cap = cv2.VideoCapture(0)  # Prepare the camera...
        print("Camera warming up ...")
        time.sleep(1)
        # Prepare Capture
        self.ret, self.frame = self.cap.read()


    # Frame generation for Browser streaming
    def get_frame(self):
        success, image = self.cap.read()
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()


    def __del__(self):
        self.cap.release()
        cv2.destroyAllWindows()
        print("Camera disabled and all output windows closed")
        log("Camera disabled and all output windows closed")
        return ()

