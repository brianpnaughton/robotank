#!/usr/bin/python3

from flask_socketio import SocketIO, emit
from flask import Flask, render_template, url_for, copy_current_request_context
#from tank.controller import Controller
from tank.camera import ImageCapture
import logging
import sys
import json

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p',stream=sys.stdout, level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)

#controller = Controller()
imageCaptureThread=None

#turn the flask app into a socketio app
socketio = SocketIO(app)

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

@socketio.on('connect')
def controller_connect():
  logger.debug('Controller client connected')
  imageCaptureThread = ImageCapture(socketio)
  imageCaptureThread.run()

@socketio.on('move')
def handle_controller_move_message(data):
  logger.debug('received move message: ' + str(data))
  #d = json.loads(data)
  controller.move(data)

@socketio.on('stop')
def handle_controller_stop_message(data):
  logger.debug('received stop message')
  controller.stop()

@socketio.on('disconnect')
def controller_disconnect():
  logger.debug('Controller client disconnected')
  controller.stop()

if __name__ == "__main__":
  logger.info('Starting socketio')
  socketio.run(app, host='0.0.0.0', port=5000)
