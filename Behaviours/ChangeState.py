from .Action import *
import GameStorage
from .Condition import quickdirty_parse


class ChangeState(Action):
    def __init__(self,name:str,variable:str,value:str,*,short_circuit:bool=True,next:str|None=None):
        super().__init__(name,next=next)
        self.variable = variable
        self.value = value
        self.short_circuit = short_circuit
    def start(self, gameObject, game):
        if self.variable not in GameStorage.__dict__:
            raise RuntimeError(f'Could not find variable: {repr(self.variable)} specified in "Condition" Action.')
        
    def Run(self,gameObject:EntityType,game:EntityType,):
        value =quickdirty_parse(self.value,GameStorage.__dict__)
        setattr(GameStorage,self.variable,value)
        self.RunNextAction(gameObject,game)
        self.running = False


        
