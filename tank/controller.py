import logging
from tank.pi import tankpi

class Controller:

  def __init__(self):
    self.logger = logging.getLogger(__name__)
    self.logger.info('started controller')
    self.lastmove=None

    self.tpi=tankpi()

  def move(self, data):
    self.logger.debug('move tank event received '+str(data))

    newmove=None
    if data['up']:
      newmove="FORWARD"
    elif data['down']:
      newmove="BACKWARD"
    elif data['left']:
      newmove="LEFT"
    elif data['right']:
      newmove="RIGHT"

    # if different than last instruction update the move command
    if self.lastmove == None:
      self.logger.debug('starting new move')
      self.lastmove=newmove
      performMove(newmove)
    else:
      self.logger.debug('update move command if needed')
      if self.lastmove==newmove:
        return
      else:
        performMove(newmove)

  def performMove(move):
    self.logger.debug('perform move '+newmove)
    if move == "FORWARD":
      self.logger.debug('move tank forward')    
      tpi.forward()
    elif move == "BACKWARD":
      self.logger.debug('move tank backward')    
      tpi.backward()
    elif move == "LEFT":
      self.logger.debug('move tank backward')    
      tpi.left()
    elif move == "RIGHT":
      self.logger.debug('move tank right')    
      tpi.right()

  def stop(self, data):
  	self.logger.debug('stop the tank')
  	self.lastmove=None
