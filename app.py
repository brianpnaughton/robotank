#!/usr/bin/python3

from flask_socketio import SocketIO, emit
from flask import Flask, render_template, url_for, copy_current_request_context
from tank.controller import Controller
from tank.camera import ImageCapture
import logging
import sys
import json

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p',stream=sys.stdout, level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)

#controller = Controller()
imageCapture=ImageCapture()
sendImageThread = None
numClients=0

#turn the flask app into a socketio app
socketio = SocketIO(app,logger=True,engine_logger=True,async_mode='gevent')

@app.route('/')
def mainRoute():
  logger.debug("main route")
  return render_template('debug.html')

@app.route('/joystick')
def joystickRoute():
  logger.debug("joystick route")
  return render_template('joystick.html')

@app.route('/dashboard')
def dashboardRoute():
  logger.debug("dashboard route")
  return render_template('dashboard.html')

def sendImage():
  logger.debug('sending images from camera')
  global numClients
  while numClients>0:
    image=imageCapture.getEncodedImage()
    logger.debug('sending image to client')
    if image is not None:
      socketio.emit('image', image, broadcast=True)
      socketio.sleep(1)
    else:
      logger.debug('null image from camera')
  logger.debug('finished send image thread')

@socketio.on('connect')
def controller_connect():
  logger.debug('Controller client connected')
  global numClients
  numClients += 1
  global sendImageThread
  if (sendImageThread is None) and (numClients > 0):
    logger.debug('starting send image thread')
    sendImageThread = socketio.start_background_task(target=sendImage)
 
@socketio.on('move')
def handle_controller_move_message(data):
  logger.debug('received move message: ' + str(data))
#  controller.move(data)

@socketio.on('stop')
def handle_controller_stop_message(data):
  logger.debug('received stop message')
#  controller.stop()

@socketio.on('disconnect')
def controller_disconnect():
  logger.debug('Controller client disconnected')
  global numClients
  numClients -= 1
  global sendImageThread
  if (numClients == 0) and (sendImageThread is not None):
    sendImageThread = None
#  controller.stop()

if __name__ == "__main__":
  logger.info('Starting socketio')
  imageCapture.start()
  socketio.run(app, host='0.0.0.0', port=5000)
