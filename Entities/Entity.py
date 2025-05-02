import typing
from pyglm import glm
from pygame import Mask
from pygame import Rect
from pygame import Surface
from pygame import transform

from EntityTags import *
from gametypes import *

BT = typing.TypeVar('BT',bound=BehaviourType)


class IEntity(typing.Protocol):
    name:str
    pos:Vec2
    vel:Vec2
    mass:Vec2
    rot:Vec2
    surf:Surface
    dirty:bool
    rect:Rect
    mask:Mask
    dead:bool
    def update(map:MapType,dt:float,game:GameType): ...
    def regenerate_physics(self): ...
    def onCollide(self,other:"IEntity",info:CollisionInfoType,normal:Vec2): ...
    def onDeath(self,map:MapType,dt:float,game:GameType): ...


class Entity:
    _global_cache:dict[tuple[Surface,int],Surface] = {}
    name:str
    pos:Vec2 # current position 
    vel:glm.vec2 # current velocity
    n_vel:glm.vec2 # next_velocity 
    mass:float
    rot:float
    surf:Surface|None # surface to draw each frame
    colliders:list[ColliderType]
    dirty:bool
    behaviours:list[BehaviourType]
    # The Following are for physics
    tags:int

    __slots__ = 'name','pos','vel','mass', \
                'rot','rot_vel','mo_inertia', \
                'colliders', \
                'surf','_surf','dirty','dead','mask','force','behaviours','bounciness','tags'

    def __init__(self,name:str,
                 pos:Vec2,vel:Vec2,mass:float,
                 rot:float,rot_vel:float,mo_inertia:float,
                 colliders:list[ColliderType],
                 _surf:Surface|None,behaviours:list[BehaviourType],tags:int=0):
        self.name = name
        #Translation
        self.pos = pos
        self.vel = vel
        self.mass = mass
        #Angular
        self.rot = rot #Radians
        self.rot_vel = rot_vel
        self.mo_inertia = mo_inertia #moment of inertia
        self.colliders = colliders
        for collider in colliders:
            collider.gameObject = self

        self.bounciness = 0
        self._surf = _surf
        self.surf = None
        self.force = glm.vec2()
        self.dirty = True
        self.dead = False
        self.behaviours = behaviours
        self.tags = tags

    def start(self,game:GameType):
        for b in self.behaviours: b.start(self,game)
    
    def update(self,map:MapType,dt:float,game:GameType):
        for b in self.behaviours: b.update(self,map,dt,game)

        #Translational Motion
        # self.vel += glm.rotate(self.force,-self.rot) * (dt / self.mass)
        # self.force *= 0 #clear force
        self.pos += self.vel * dt
        self.vel *= glm.exp(-dt*5)

        #Rotational Motion
        if self.rot_vel: 
            self.rot += self.rot_vel * dt
            self.dirty = True
            self.rot_vel *= glm.exp(-dt*2)
            if abs(self.rot_vel) < 0.01:
                self.rot_vel = 0
        for collider in self.colliders:
            collider.update(self)

    def clean(self):
        if self._surf:
            degrees = self.rot*(180/3.141592653589793)#Radians to Degrees
            self.surf = transform.rotate(self._surf,degrees)
        for collider in self.colliders:
            collider.recalculate(self)
    
    def onCollide(self,other:"Entity",info:CollisionInfoType,normal:glm.vec2):
        for b in self.behaviours: b.onCollide(self,other)

    def onTriggerEnter(self,other:"Entity",game:GameType):
        for b in self.behaviours: b.onTriggerEnter(self,other,game)

    def onTriggerStay(self,other:"Entity",game:GameType):
        for b in self.behaviours: b.onTriggerStay(self,other,game)

    def onTriggerLeave(self,other:"Entity",game:GameType):
        for b in self.behaviours: b.onTriggerLeave(self,other,game)
 
    def addRelForce(self,force:glm.vec2):
        self.force += force

    def onDeath(self,map:MapType,dt:float,game:GameType):
        for b in self.behaviours:
            b.onDeath(self,map,dt,game)

    def getBehaviour(self,behaviour_type:type[BT]) -> BT | None:
        for b in self.behaviours:
            if type(b) is behaviour_type:
                return b
            
    def getBehaviours(self,behaviour_type:type[BT]) -> list[BT]:
        return [b for b in self.behaviours if isinstance(b,behaviour_type)]



    def __repr__(self):
        return f'<Entity object {self.name} at {hex(id(self))}>'