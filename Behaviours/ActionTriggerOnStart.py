from .ActionTrigger import *

class ActionTriggerOnStart(ActionTrigger):
    def start(self, gameObject:EntityType, game:GameType):
        super().start(gameObject,game)   
        self.action_b.Run(gameObject,game)