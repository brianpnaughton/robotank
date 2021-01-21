from picamera.array import PiRGBArray
from picamera import PiCamera 
import time 
import cv2 # OpenCV library
import logging
import base64
import re
import numpy as np
from threading import Thread
from tflite_runtime.interpreter import Interpreter

class ImageCapture(Thread):
  def __init__(self):
    super().__init__()

    self.logger = logging.getLogger(__name__)
    self.logger.debug('Init image capture')

    self.WIDTH=640
    self.HEIGHT=480

    # Initialize the camera
    self.camera = PiCamera() 
    # Set the camera resolution
    self.camera.resolution = (self.WIDTH, self.HEIGHT)
    # Set the number of frames per second
    self.camera.framerate = 32 
    # Generates a 3D RGB array and stores it in rawCapture
    self.raw_capture = PiRGBArray(self.camera, size=(self.WIDTH, self.HEIGHT))
    # Wait a certain number of seconds to allow the camera time to warmup
    time.sleep(0.1)

    # load COCO labels
    self.labels = {}
    self.load_labels("/tmp/coco_labels.txt")
    # init the tf interpreter
    self.interpreter = Interpreter("/tmp/detect.tflite")
    self.interpreter.allocate_tensors()
    _, self.input_height, self.input_width, _ = self.interpreter.get_input_details()[0]['shape']

    # current image
    self.image=None
    # loop bool
    self.running=True

  def run(self):
    self.logger.debug('starting capture thread')
    while self.running:
      # proces the next camera frame
      self.nextFrame()
      time.sleep(0.05)

  def nextFrame(self):
    self.logger.debug('Capturing next frame')
    # Capture frames continuously from the camera
    self.camera.capture(self.raw_capture, format="bgr", use_video_port=True)
    # analyse the raw image to detect objects
    self.analyse()
    # convert raw image to jpeg    
    res, self.image=cv2.imencode('.JPEG', self.raw_capture.array)
    # Clear the stream in preparation for the next frame
    self.raw_capture.truncate(0)

  def getEncodedImage(self):
    self.logger.debug('Returning current jpeg image base64 encoded')
    if self.image is not None:
      return base64.b64encode(self.image.tobytes()).decode('utf-8')
    return None

  def analyse(self):
    self.logger.debug('analyse raw frame for common objects')
    # resize the image
    resized = cv2.resize(self.raw_capture.array, (self.input_width,self.input_height), interpolation = cv2.INTER_AREA)
    results = self.detect_objects(resized, 0.4)
    self.annotate_objects(results)

  def load_labels(self, path):
    """Loads the labels file. Supports files with or without index numbers."""
    self.logger.debug('loading labels from '+path)
    with open(path, 'r', encoding='utf-8') as f:
      lines = f.readlines()
      for row_number, content in enumerate(lines):
        pair = re.split(r'[:\s]+', content.strip(), maxsplit=1)
        if len(pair) == 2 and pair[0].strip().isdigit():
          self.labels[int(pair[0])] = pair[1].strip()
        else:
          self.labels[row_number] = pair[0].strip()

  def set_input_tensor(self, image):
    """Sets the input tensor."""
    self.logger.debug('setting input tensor')
    tensor_index = self.interpreter.get_input_details()[0]['index']
    input_tensor = self.interpreter.tensor(tensor_index)()[0]
    input_tensor[:, :] = image

  def get_output_tensor(self, index):
    """Returns the output tensor at the given index."""
    self.logger.debug('getting output tensor')
    output_details = self.interpreter.get_output_details()[index]
    tensor = np.squeeze(self.interpreter.get_tensor(output_details['index']))
    return tensor

  def detect_objects(self, image, threshold):
    """Returns a list of detection results, each a dictionary of object info."""
    self.logger.debug('starting to detect objects')

    self.set_input_tensor(image)
    self.interpreter.invoke()

    # Get all output details
    boxes = self.get_output_tensor(0)
    classes = self.get_output_tensor(1)
    scores = self.get_output_tensor(2)
    count = int(self.get_output_tensor(3))

    results = []
    for i in range(count):
      if scores[i] >= threshold:
        result = {
            'bounding_box': boxes[i],
            'class_id': classes[i],
            'score': scores[i]
        }
        results.append(result)
    return results

  def annotate_objects(self, results):
    """Draws the bounding box and label for each object in the results."""
    self.logger.debug('annotate objects')
    for obj in results:
      # Convert the bounding box figures from relative coordinates
      # to absolute coordinates based on the original resolution
      ymin, xmin, ymax, xmax = obj['bounding_box']
      xmin = int(xmin * self.WIDTH)
      xmax = int(xmax * self.WIDTH)
      ymin = int(ymin * self.HEIGHT)
      ymax = int(ymax * self.HEIGHT)

      cv2.rectangle(self.raw_capture.array, (xmin,ymin), (xmax, ymax), (0,255,0), 2)
      cv2.putText(self.raw_capture.array, self.labels[obj['class_id']], (xmin, ymin - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

