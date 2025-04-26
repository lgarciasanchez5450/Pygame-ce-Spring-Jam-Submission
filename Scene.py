import json
import Utils.utils as utils
import physics
import ResourceManager
from pyglm import glm
from gametypes import *
from pygame import image
from pygame import Surface

from Behaviours.Behaviour import Behaviour
from Behaviours.SceneBehaviours.SceneBehaviour import SceneBehaviour
from Colliders.Collider import Collider
from Entities.Entity import Entity


class Scene:
    '''This class is more of a data-holder that the Game object uses to implement scenes'''
    map:Surface
    entities:list[EntityType]
    behaviours:list[SceneBehaviour]

    def __init__(self,path:str):
        with open(path,'r') as file:
            map_data:dict = json.load(file)
        self.map = image.load(map_data.pop('map_path')).convert()
        self.entities = []
        for ent_data in map_data.pop('entities'):
            ent_data:dict
            try:
                name = str(ent_data['name'])
            except KeyError:
                raise KeyError(f'Error Loading `{path}`. Entity Property "name" not found.')
            pos = glm.vec2(ent_data.get('pos',(0,0)))
            vel = glm.vec2(ent_data.get('vel',(0,0)))
            mass = str(ent_data.get('mass',1))
            if mass in ('infinity','inf'):
                mass = float('inf')
            else:
                mass = float(mass)
            rot = float(ent_data.get('rot',0))
            rot_vel = float(ent_data.get('rot_vel',0))
            try:
                surf = ResourceManager.loadAlpha(ent_data['surf_path'])
            except KeyError:
                surf = None
            mo_inertia = ent_data.get('moment of inertia')
            if mo_inertia is None:
                mo_inertia = physics.calculateMomentOfInertia(surf,mass)
            else:
                mo_inertia = float(mo_inertia)
            cols = ent_data.get('collider')
            if cols is None:
                cols = ent_data.get('colliders')
            else:
                cols = [cols]
            if cols is None:
                cols = []
            
            cols:list[str]
            colliders:list[Collider] = []
            for col in cols:
                if '(' in col:
                    i = col.index('(')
                    args = col[i:]
                    col = col[:i]
                else:
                    args = '()'
                if col is not None:
                    try:
                        colliders.append(Collider._subclasses_[col](*utils.safeEval(args)))
                    except KeyError:
                        likely_meant = utils.sortBySimilarity(behav,Collider._subclasses_.keys())[0]
                        raise LookupError(f'Collider {col} not found! Did you mean {likely_meant}')
           
            behavs:list[str] = list(ent_data.get('behaviours',[]))
            behaviours:list[Behaviour] = []
            for behav in behavs:
                if '(' in col :
                    i = col.index('(')
                    args = col[i:]
                    behav = col[:i]
                else:
                    args = '()'
                b = Behaviour._subclasses_.get(behav)
                if b is None:
                    likely_meant = utils.sortBySimilarity(behav,Behaviour._subclasses_.keys())
                    raise LookupError(f'Behaviour {behav} not found! Did you mean {likely_meant[0]}')
                behaviours.append(b(*utils.safeEval(args)))
            if mass < 1e-6:
                raise ValueError(f'Error Loading `{path}` Invalid Mass: {mass}')
            #make entity
            ent = Entity(name,pos,vel,mass,rot,rot_vel,mo_inertia,colliders,surf)
            ent.behaviours = behaviours
            self.entities.append(ent)
        self.behaviours = []
        try:
            s_behavs = map_data.pop('behaviours')
        except KeyError:
            s_behavs = []
        for s_behav in s_behavs:
            b = SceneBehaviour._subclasses_.get(s_behav)
            if b is None:
                likely_meant = utils.sortBySimilarity(s_behav,SceneBehaviour._subclasses_.keys())
                raise LookupError(f'Behaviour {s_behav} not found! Did you mean {likely_meant[0]}')
            self.behaviours.append(b())


        if map_data: 
            print(f'[Scene Loading Warning] Scene {path} has unused data: {tuple(map_data.keys())}')

    def start(self,game:GameType):
        for b in self.behaviours: b.start(self,game)

    def update(self,game:GameType):
        for b in self.behaviours: b.update(self,game)

    def preDraw(self,game:GameType):
        for b in self.behaviours: b.preDraw(self,game)