from .Action import *

class RunExternalAction(Action):
    __slots__ = 'entity','force','action'
    def __init__(self, name:str,entity:str,action:str, *,force:bool=False, next = None):
        super().__init__(name, next=next)
        self.entity = entity
        self.force = force
        self.action = action
    
    def Run(self, gameObject, game:GameType):
        entity = game.FindEntityByName(self.entity)
        assert entity is not None
        for action in entity.getBehaviours(Action):
            if action.name == self.action:
                if not action.running or self.force:
                    action.Run(entity,game)
                    self.RunNextAction(gameObject,game)
                return
        raise LookupError('Could not find action {} in entity {}'.format(self.action,self.entity))
