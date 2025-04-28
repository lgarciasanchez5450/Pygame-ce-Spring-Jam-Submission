from .Behaviour import *
class Action(Behaviour):
    name:str
    __slots__ = 'name',
    def __init__(self,name:str):
        self.name = name
    
    def Run(self,gameObject:EntityType,game:EntityType,*args): ...