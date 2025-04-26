from .Behaviour import *
from gametypes import *

class SceneTransporter(Behaviour):
    __slots__ = 'dest',
    def __init__(self,destination_scene:str):
        self.dest = destination_scene

    def update(self, gameObject:EntityType, map:MapType, dt:float, game:GameType):
        if gameObject.collider:
            pass