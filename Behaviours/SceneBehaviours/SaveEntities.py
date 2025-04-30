import typing
from gametypes import *
from Behaviours.SceneBehaviours.SceneBehaviour import SceneBehaviour
type CleanBehaviour = typing.Literal['save','kill','ignore']
class SaveEntities(SceneBehaviour):
    player:EntityType
    __slots__ = 'player','saved_entities','exceptions','default_behaviour'
    def __init__(self,exceptions:dict[str,CleanBehaviour]|None = None,default_behaviour:CleanBehaviour='save'):
        self.exceptions = exceptions
        self.saved_entities = None
        self.default_behaviour:CleanBehaviour = default_behaviour
    def start(self,scene:SceneType,game:GameType): 
        if self.saved_entities is None:
            self.saved_entities = scene.entities
        game.spawnEntities(self.saved_entities)

    def stop(self, scene:SceneType, game:GameType):
        if not self.exceptions:
            if self.default_behaviour == 'save':
                self.saved_entities = game.entities.copy()
                game.entities.clear()
            elif self.default_behaviour == 'ignore':
                pass
            elif self.default_behaviour == 'kill':
                game.entities.clear()
        else:
            transitioning_entities = []
            self.saved_entities = []
            for entity in game.entities:
                behaviour = self.exceptions.get(entity.name,self.default_behaviour)
                match behaviour:
                    case 'save':
                        self.saved_entities.append(entity)
                    case 'kill':
                        pass
                    case 'ignore':
                        transitioning_entities.append(entity)
            game.entities.clear()
            game.entities.extend(transitioning_entities)
