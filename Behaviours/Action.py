from .Behaviour import *
class Action(Behaviour):
    name:str
    __slots__ = 'name','running'
    def __init__(self,name:str):
        self.name = name
        self.running = False
    
    def Run(self,gameObject:EntityType,game:EntityType,*args): ...