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
    if data['data']['up']:
      newmove="FORWARD"
    elif data['data']['down']:
      newmove="BACKWARD"
    elif data['data']['left']:
      newmove="LEFT"
    elif data['data']['right']:
      newmove="RIGHT"

    # if different than last instruction update the move command
    if self.lastmove == None:
      self.logger.debug('starting new move')
      self.lastmove=newmove
      self.performMove(newmove)
    else:
      self.logger.debug('update move command if needed')
      if self.lastmove==newmove:
        return
      else:
        self.performMove(newmove)

  def performMove(self, move):
    self.logger.debug('perform move '+move)
    if move == "FORWARD":
      self.logger.debug('move tank forward')    
      self.tpi.forward()
    elif move == "BACKWARD":
      self.logger.debug('move tank backward')    
      self.tpi.backward()
    elif move == "LEFT":
      self.logger.debug('move tank backward')    
      self.tpi.left()
    elif move == "RIGHT":
      self.logger.debug('move tank right')    
      self.tpi.right()

  def stop(self):
    self.logger.debug('stop the tank')
    self.lastmove=None
    self.tpi.stop()
