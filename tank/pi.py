import RPi.GPIO as GPIO
import time 
import sys
import logging

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
    self.speed = 0

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
    self.p1.start(self.speed)
    self.p2=GPIO.PWM(self.en2,1000)
    self.p2.start(self.speed)

  def setspeed(self, speed):
    self.logger.debug('set speed to '+str(speed))
    self.p1.ChangeDutyCycle(speed)
    self.p2.ChangeDutyCycle(speed)

  def stop(self):
    self.logger.debug('stopping tank')
    self.setspeed(0)
    self.leftstop()
    self.rightstop()

  def forward(self):
    self.logger.debug('move tank forward')
    if self.speed == 0:
      self.setspeed(90)
    self.rightforward()
    self.leftforward()

  def backward(self):
    self.logger.debug('move tank forward')
    if self.speed == 0:
      self.setspeed(90)
    self.rightbackward()
    self.leftbackward()

  def right(self):
    self.logger.debug('move tank forward')
    if self.speed == 0:
      self.setspeed(90)
    self.rightbackward()
    self.leftforward()

  def left(self):
    self.logger.debug('move tank forward')
    if self.speed == 0:
      self.setspeed(90)
    self.rightforward()
    self.leftbackward()

  def rightforward(self):
    GPIO.output(self.out1,GPIO.HIGH)
    GPIO.output(self.out2,GPIO.LOW)

  def rightbackward(self):
    GPIO.output(self.out1,GPIO.LOW)
    GPIO.output(self.out2,GPIO.HIGH)

  def rightstop(self):
    GPIO.output(self.out1,GPIO.LOW)
    GPIO.output(self.out2,GPIO.LOW)

  def leftbackward(self):
    GPIO.output(self.out3,GPIO.LOW)
    GPIO.output(self.out4,GPIO.HIGH)

  def leftstop(self):
    GPIO.output(self.out3,GPIO.LOW)
    GPIO.output(self.out4,GPIO.LOW)

  def leftforward(self):
    GPIO.output(self.out3,GPIO.HIGH)
    GPIO.output(self.out4,GPIO.LOW)
