import RPi.GPIO as GPIO
import time 
import sys

class tankpi:

  def __init__(self):
    self.logger = logging.getLogger(__name__)

    self.out1 = 11
    self.out2 = 12
    self.out3 = 15
    self.out4 = 16
    self.en1 = 13
    self.en2 = 18
    self.p1 = None
    self.p2 = None

    self.setupGPIO()

  def setupGPIO(self):
    self.logger.debug('setting up GPIO')

    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(self.out1,GPIO.OUT)
    GPIO.setup(self.out2,GPIO.OUT)
    GPIO.setup(self.out3,GPIO.OUT)
    GPIO.setup(self.out4,GPIO.OUT)
    GPIO.setup(self.en1,GPIO.OUT)
    GPIO.setup(self.en2,GPIO.OUT)
    self.p1=GPIO.PWM(self.en1,1000)
    self.p1.start(0)
    self.p2=GPIO.PWM(self.en2,1000)
    self.p2.start(0)

  def setspeed(self, speed):
    self.logger.debug('set speed to '+str(speed))
    self.p1.ChangeDutyCycle(speed)
    self.p2.ChangeDutyCycle(speed)

  def stop(self):
    self.logger.debug('stopping tank')
    self.leftstop()
    self.rightstop()

  def forward(self):
    self.logger.debug('move tank forward')
    rightforward()
    leftforward()

  def backward(self):
    self.logger.debug('move tank forward')
    rightbackward()
    leftbackward()

  def right(self):
    self.logger.debug('move tank forward')
    rightbackward()
    leftforward()

  def left(self):
    self.logger.debug('move tank forward')
    rightforward()
    leftbackward()

  def rightforward(self):
    GPIO.output(out1,GPIO.LOW)
    GPIO.output(out2,GPIO.HIGH)

  def rightbackward(self):
    GPIO.output(out1,GPIO.HIGH)
    GPIO.output(out2,GPIO.LOW)

  def rightstop(self):
    GPIO.output(out1,GPIO.LOW)
    GPIO.output(out2,GPIO.LOW)

  def leftbackward(self):
    GPIO.output(out3,GPIO.HIGH)
    GPIO.output(out4,GPIO.LOW)

  def leftstop(self):
    GPIO.output(out3,GPIO.LOW)
    GPIO.output(out4,GPIO.LOW)

  def leftforward(self):
    GPIO.output(out3,GPIO.LOW)
    GPIO.output(out4,GPIO.HIGH)