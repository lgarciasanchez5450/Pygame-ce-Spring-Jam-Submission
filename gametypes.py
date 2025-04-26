'''
This module is purely for type-hinting purposes ONLY
importing this module should not have any side effects 
(i.e. this module should only import typing)
'''

import typing
if typing.TYPE_CHECKING:
    from Entities.Entity import Entity
    from game import Game
    from Behaviours.Behaviour import Behaviour
    from Behaviours.SceneBehaviours.SceneBehaviour import SceneBehaviour
    from Colliders.Collider import Collider
    from pyglm import glm
    from physics import CollisionInfo
    from Scene import Scene
__all__ = [
    'MapType','GameType','EntityType','BehaviourType','Vec2','CollisionInfoType','SceneType','SceneBehaviourType','ColliderType'
]


type MapType = dict[tuple[int,int],list['Collider']]
type GameType = 'Game'
type EntityType = 'Entity'
type BehaviourType = 'Behaviour'
type ColliderType = 'Collider'
type SceneBehaviourType = 'SceneBehaviour'
type Vec2 = 'glm.vec2'
type CollisionInfoType = 'CollisionInfo'
type SceneType = 'Scene'