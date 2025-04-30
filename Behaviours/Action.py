from .Behaviour import *
class Action(Behaviour):
    name:str
    __slots__ = 'name','running','next'
    def __init__(self,name:str,*,next:str|None=None):
        self.name = name
        self.running = False
        self.next = next

    def RunNextAction(self,gameObject:EntityType,game:GameType,*,even_if_already_running:bool = False):
        if self.next is not None:
            n = self.getNext(gameObject)
            if not n.running or even_if_already_running:
                n.Run(gameObject,game)
                return True
        return False

    def getNext(self,gameObject:EntityType):
        if self.next is None: raise TypeError('Action {self.name} does not have a Connected Action')
        for action in gameObject.getBehaviours(Action):
            if action.name == self.next:
                return action
        raise NameError(f"Connected Action {self.next} not found on entity {gameObject.name} (Requested by Action {self.name})")

    def Run(self,gameObject:EntityType,game:EntityType,*args): ...