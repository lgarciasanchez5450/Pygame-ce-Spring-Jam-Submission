from .Action import *


class MoveEntities(Action):
    __slots__ = 'force_next','match_all','entities'
    def __init__(self,name:str,entities:list[tuple[str,tuple[int,int]]],*,match_all:bool=False,next:str|None=None,force_next:bool=False):
        super().__init__(name,next=next)
        self.force_next = force_next
        self.match_all = match_all
        self.entities = entities

    def Run(self,gameObject:EntityType,game:GameType):
        for name,pos in self.entities:
            if self.match_all:
                for entity in game.FindEntitiesByName(name):
                    entity.pos.xy = pos
            else:
                ent = game.FindEntityByName(name)
                ent.pos.xy = pos
    
        self.RunNextAction(gameObject,game,self.force_next)