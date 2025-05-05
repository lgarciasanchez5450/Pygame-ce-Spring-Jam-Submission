from .ActionTrigger import *
import Loader
import Input

class ActionTriggerTimeout(ActionTrigger):
    def __init__(self, action,time:float):
        super().__init__(action)
        self.time = time
        self.done = False

    def update(self, gameObject, map, dt, game):
        if self.done: return
        self.time -= game.dt
        if self.time <= 0:
            self.done = True
            self.action_b.Run(gameObject,game)