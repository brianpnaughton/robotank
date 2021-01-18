from picamera.array import PiRGBArray
from picamera import PiCamera 
import time 
import cv2 # OpenCV library
import logging
import base64
import io
from threading import Thread

class ImageCapture(Thread):
  def __init__(self):
    super().__init__()

    self.logger = logging.getLogger(__name__)
    self.logger.debug('Init image capture')

    # Initialize the camera
    self.camera = PiCamera() 
    # Set the camera resolution
    self.camera.resolution = (640, 480)
    # Set the number of frames per second
    self.camera.framerate = 32 
    # Generates a 3D RGB array and stores it in rawCapture
    self.raw_capture = PiRGBArray(self.camera, size=(640, 480))

    # Wait a certain number of seconds to allow the camera time to warmup
    time.sleep(0.1)

    # current image
    self.image=None

    # loop bool
    self.running=True

  def run(self):
    self.logger.debug('starting capture thread')
    while self.running:
      self.nextFrame()
      time.sleep(0.5)

  def nextFrame(self):
    self.logger.debug('Capturing next frame')

    # Capture frames continuously from the camera
    self.camera.capture(self.raw_capture, format="bgr", use_video_port=True)
    
    res, self.image=cv2.imencode('.JPEG', self.raw_capture.array)

    # Clear the stream in preparation for the next frame
    self.raw_capture.truncate(0)

  def getEncodedImage(self):
    self.logger.debug('Returning current image encoded')
    if self.image is not None:
      return base64.b64encode(self.image.tobytes()).decode('utf-8')
    return None
