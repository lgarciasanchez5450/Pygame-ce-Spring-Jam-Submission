from .Action import *

class RunExternalAction(Action):
    __slots__ = 'entity','force','action','action_b'
    def __init__(self, name:str,entity:str,action:str, *,force:bool=False, next = None):
        super().__init__(name, next=next)
        self.entity = entity
        self.force = force
        self.action = action
    
    def Run(self, gameObject, game:GameType):
        entity = game.FindEntityByName(self.entity)
        self.running = True
        assert entity is not None, f'Could not find entity: {self.entity}'
        for action in entity.getBehaviours(Action):
            if action.name == self.action:
                if not action.running or self.force:
                    self.action_b = action
                    action.Run(entity,game)
                return
        raise LookupError('Could not find action {} in entity {}'.format(self.action,self.entity))

    def update(self, gameObject, map, dt, game):
        if self.running:
            if not self.action_b.running:
                self.running = False
                self.RunNextAction(gameObject,game)
