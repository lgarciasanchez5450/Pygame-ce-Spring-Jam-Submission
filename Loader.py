import os
import json
import Utils
import typing
import physics
import ResourceManager
from pyglm import glm
from Entities.Entity import Entity
from Behaviours.Behaviour import Behaviour
from Colliders.Collider import Collider

T = typing.TypeVar('T')

PATH = [
    './Prefabs',
]

def loadEntity(e:str|dict) -> Entity:
    if type(e) is str: #prefab name
        for directory in PATH:
            filenames = os.listdir(directory)
            if e in filenames:
                fqn = os.path.join(directory,e)
                with open(fqn,'r') as file:
                    return loadEntity(json.load(file))
        raise FileNotFoundError(f"Prefab {repr(e)} could not be found in PATH")
    elif type(e) is dict:
        return _parseEntityData(e)
    else:
        raise TypeError(f'Cannot Convert type {type(e).__name__} to Entity')


def _parseEntityData(data:dict[str,typing.Any]) -> Entity:
    SENTINEL = object()
    try:
        name = str(data['name'])
    except KeyError:
        raise KeyError(f'Entity Property "name" not found.')
    pos = glm.vec2(data.get('pos',(0,0)))
    vel = glm.vec2(data.get('vel',(0,0)))
    mass = str(data.get('mass',1))
    if mass in ('infinity','inf'):
        mass = float('inf')
    else:
        mass = float(mass)
    rot = float(data.get('rot',0))
    rot_vel = float(data.get('rot_vel',0))
    try:
        surf = ResourceManager.loadAlpha(data['surf_path'])
    except KeyError:
        surf = None
    mo_inertia = data.get('moment of inertia',SENTINEL)
    if mo_inertia is SENTINEL:
        mo_inertia = physics.calculateMomentOfInertia(surf,mass)
    else:
        mo_inertia = float(mo_inertia)
    cols = data.get('collider',SENTINEL)
    if cols is SENTINEL:
        cols = data.get('colliders',SENTINEL)
        if type(cols) not in (list,tuple):
            raise ValueError(f'Cannot Convert {cols} to Entity Colliders')
    else:
        cols = [cols]
    if cols is SENTINEL:
        cols = []
    
    cols:list[str]
    colliders:list[Collider] = []
    for col in cols:
        colliders.append(parseComplexType(col,Collider))
    
    behavs:list[str] = list(data.get('behaviours',[]))
    behaviours:list[Behaviour] = []
    for behav in behavs:
        if '(' in behav :
            i = behav.index('(')
            args = behav[i:]
            behav = behav[:i]
        else:
            args = '()'
        args,kwargs = Utils.evalArgs(args)
        b = Behaviour._subclasses_.get(behav)
        if b is None:
            likely_meant = Utils.sortBySimilarity(behav,Behaviour._subclasses_.keys())
            raise LookupError(f'Behaviour {behav} not found! Did you mean {likely_meant[0]}')
        behaviours.append(b(*args,**kwargs))
    if mass < 1e-6:
        raise ValueError(f'Invalid Mass: {mass}')
    #make entity
    ent = Entity(name,pos,vel,mass,rot,rot_vel,mo_inertia,colliders,surf,behaviours)
    return ent

def parseComplexType(s:str,parentType:type[T],only_subtypes:bool = True) -> T:
    lookup:dict[str,type[T]] = {}
    if only_subtypes:
        if not hasattr(parentType,'_subclasses_'):
            raise LookupError('Could not find subclasses')
        lookup = parentType._subclasses_
    else:
        if not hasattr(parentType,'_subclasses_'):
            lookup = {parentType.__name__:parentType}
    if '(' in s:
        i = s.index('(')
        args = s[i:]
        s = s[:i] 
    else:
        args = '()'
    args,kwargs = Utils.evalArgs(args)
    try:
        t = lookup[s]
    except KeyError:
        likely_meant = Utils.sortBySimilarity(s,lookup.keys())[0]
        raise LookupError(f'{parentType.__name__} {s} not found! Did you mean {likely_meant}')
    else:
        return t(*args,**kwargs)