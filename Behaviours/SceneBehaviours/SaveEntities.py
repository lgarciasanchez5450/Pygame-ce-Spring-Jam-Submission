from gametypes import *
from Behaviours.SceneBehaviours.SceneBehaviour import SceneBehaviour


class SaveEntities(SceneBehaviour):
    player:EntityType
    __slots__ = 'player','saved_entities'
    def __init__(self):
        self.saved_entities = None
    def start(self,scene:SceneType,game:GameType): 
        if self.saved_entities is None:
            self.saved_entities = scene.entities
        game.spawnEntities(self.saved_entities)

    def stop(self, scene:SceneType, game:GameType):
        self.saved_entities = game.entities.copy()
        game.entities.clear()