#!/usr/bin/python

import RPi.GPIO as GPIO
import time 
import sys

out1 = 11
out2 = 12
out3 = 15
out4 = 16
en1 = 13
en2 = 18

GPIO.setmode(GPIO.BOARD)
GPIO.setup(out1,GPIO.OUT)
GPIO.setup(out2,GPIO.OUT)
GPIO.setup(out3,GPIO.OUT)
GPIO.setup(out4,GPIO.OUT)
GPIO.setup(en1,GPIO.OUT)
GPIO.setup(en2,GPIO.OUT)
p1=GPIO.PWM(en1,1000)
p1.start(0)
p2=GPIO.PWM(en2,1000)
p2.start(0)

def rightforward():
  GPIO.output(out1,GPIO.LOW)
  GPIO.output(out2,GPIO.HIGH)

def rightbackward():
  GPIO.output(out1,GPIO.HIGH)
  GPIO.output(out2,GPIO.LOW)

def rightstop():
  GPIO.output(out1,GPIO.LOW)
  GPIO.output(out2,GPIO.LOW)

def leftbackward():
  GPIO.output(out3,GPIO.HIGH)
  GPIO.output(out4,GPIO.LOW)

def leftstop():
  GPIO.output(out3,GPIO.LOW)
  GPIO.output(out4,GPIO.LOW)

def leftforward():
  GPIO.output(out3,GPIO.LOW)
  GPIO.output(out4,GPIO.HIGH)

if __name__ == "__main__":
  while(1):
    x=raw_input()
    if x=='f':
      print("forward")
      leftforward()
      rightforward()
      x='z'

    elif x=='s':
      print("stop")
      leftstop()
      rightstop()
      x='z'

    elif x=='b':
      print("back")
      leftbackward()
      rightbackward()
      x='z'

    elif x=='l':
      print("low")
      p1.ChangeDutyCycle(25)
      p2.ChangeDutyCycle(25)
      x='z'

    elif x=='m':
      print("medium")
      p1.ChangeDutyCycle(50)
      p2.ChangeDutyCycle(50)
      x='z'

    elif x=='h':
      print("high")
      p1.ChangeDutyCycle(75)
      p2.ChangeDutyCycle(75)
      x='z'
    
    elif x=='e':
      GPIO.cleanup()
      break
    
    else:
      print("<<<  wrong data  >>>")
      print("please enter the defined data to continue.....")
