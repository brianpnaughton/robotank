from picamera.array import PiRGBArray
from picamera import PiCamera 
import time 
import cv2 # OpenCV library
import logging
from threading import Thread
import base64

class ImageCapture(Thread):
  def __init__(self, socketio):
    super().__init__()
    self.logger = logging.getLogger(__name__)
    self.logger.debug('Init image capture')

    self.socketio=socketio

    # Initialize the camera
    self.camera = PiCamera() 
    # Set the camera resolution
    self.camera.resolution = (640, 480)
    # Set the number of frames per second
    self.camera.framerate = 32 
    # Generates a 3D RGB array and stores it in rawCapture
    self.raw_capture = PiRGBArray(camera, size=(640, 480))
    # Wait a certain number of seconds to allow the camera time to warmup
    time.sleep(0.1)
    # current image
    self.image=None
    # loop bool
    self.running=True

  def run(self):
    self.logger('entering run loop')
    # collect images and send to 
    self.capture()

  def stop(self):
    self.logger('stopping image capture thread')
    self.running=False

  def capture(self):
    self.logger.debug('Start capturing video')
    # Capture frames continuously from the camera
    for frame in camera.capture_continuous(self.raw_capture, format="bgr", use_video_port=True):        
      # Grab the raw NumPy array representing the image
      self.image = frame.array
      # Display the frame using OpenCV
      # cv2.imshow("Frame", self.image)

      # send the image to connected clients
      self.sendImage()      

      # Clear the stream in preparation for the next frame
      self.raw_capture.truncate(0)
      if self.running is False:
        self.camera.close()
        break

  def sendImage(self):
    self.logger('sending image')
    socketio.emit('image', {'buffer': base64.b64encode(self.image) } )

  def getImage(self):
    self.logger.debug('Return current image')
    return self.image

class AnalyseImages:
  def __init__(self):
    self.logger = logging.getLogger(__name__)

class ImagePusher:
  def __init__(self, socketio):
    self.logger = logging.getLogger(__name__)
    self.socketio=socketio
