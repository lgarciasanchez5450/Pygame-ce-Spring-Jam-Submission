from .Behaviour import *
from .Action import Action

class ActionTrigger(Behaviour):
    action:str
    action_b:Action
    __slots__ = 'action','behaviour','action_b'
    def __init__(self,action:str):
        self.action = action
        

    def start(self, gameObject:EntityType, game:GameType):
        for behaviour in gameObject.getBehaviours(Action):
            if behaviour.name == self.action:
                self.action_b = behaviour
                break
        else:
            raise LookupError('Action Trigger Could not find bound action: {}'.format(repr(self.action)))
        
    
    