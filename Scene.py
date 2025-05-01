import json
import typing
import Utils
import physics
import ResourceManager
from pyglm import glm
from gametypes import *
from pygame import image
from pygame import Surface

from Behaviours.SceneBehaviours.SceneBehaviour import SceneBehaviour
import Loader

BT = typing.TypeVar('BT',bound=SceneBehaviourType)

class Scene:
    '''This class is more of a data-holder that the Game object uses to implement scenes'''
    map:Surface
    entities:list[EntityType]
    behaviours:list[SceneBehaviour]

    def __init__(self,path:str):
        try:    
            with open(path,'r',encoding='utf-8') as file:
                map_data:dict = json.load(file)

            self.map = ResourceManager.loadOpaque(map_data.pop('map_path'))
            self.entities = []
            for ent_data in map_data.pop('entities'):
                self.entities.append(Loader.loadEntity(ent_data))
            self.behaviours = []
            try:
                s_behavs = map_data.pop('behaviours')
            except KeyError:
                s_behavs = []
            s_behav:list[str]
            for s_behav in s_behavs:
                self.behaviours.append(Loader.parseComplexType(s_behav,SceneBehaviour))
            if map_data: 
                print(f'[Scene Loading Warning] Scene {path} has unused data: {tuple(map_data.keys())}')
        except Exception as err:
            err.add_note("Error Loading Scene {}".format(path))
            raise err
    

    def start(self,game:GameType):
        for b in self.behaviours: b.start(self,game)
    def update(self,game:GameType):
        for b in self.behaviours: b.update(self,game)
    def stop(self,game:GameType):
        for b in self.behaviours: b.stop(self,game)


    def preDraw(self,game:GameType):
        for b in self.behaviours: b.preDraw(self,game)
    def postDraw(self,game:GameType):
        for b in self.behaviours: b.postDraw(self,game)
    def GetBehaviour(self,bt:type[BT]) -> BT:
        for b in self.behaviours:
            if type(b) is bt:
                return b
