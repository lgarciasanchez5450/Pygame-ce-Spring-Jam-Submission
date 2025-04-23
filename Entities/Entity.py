import utils
from pyglm import glm
from pygame import Surface
from pygame import Mask
from pygame import Rect

from pygame import transform
from pygame import mask
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


_cache_misses = 0
class Entity:
    _global_physics_cache:dict[tuple[Surface,int],tuple[Surface,Mask]] = {}
    name:str
    pos:Vec2 # current position 
    vel:glm.vec2 # current velocity
    n_vel:glm.vec2 # next_velocity 
    mass:float
    rot:float
    surf:Surface # surface to draw each frame
    dirty:bool
    behaviours:list[BehaviourType]
    # The Following are for physics
    rect:Rect # bounding Rect of the surface
    mask:Mask # mask from surface
    tags:int

    __slots__ = 'name','pos','vel','mass', \
                'rot','rot_vel','mo_inertia', \
                'surf','_surf','dirty','dead','rect','mask','force','behaviours','bounciness',#'tags',

    def __init__(self,name:str,
                 pos:Vec2,vel:Vec2,mass:float,
                 rot:float,rot_vel:float,mo_inertia:float,
                 _surf:Surface):
        self.name = name
        #Translation
        self.pos = pos
        self.vel = vel
        self.mass = mass
        #Angular
        self.rot = rot #Radians
        self.rot_vel = rot_vel
        self.mo_inertia = mo_inertia #moment of inertia
        
        self.bounciness = 0
        self._surf = _surf
        self.force = glm.vec2()
        self.dirty = True
        self.dead = False
        self.behaviours = []

    def start(self,game:GameType):
        for b in self.behaviours: b.start(self,game)
    
    def update(self,map:MapType,dt:float,game:GameType):
        for b in self.behaviours: b.update(self,map,dt,game)

        #Translational Motion
        # self.vel += utils.rotateAbout(self.force,self.dir) * (dt / self.mass)
        # self.vel += glm.rotate(self.force,-self.rot) * (dt / self.mass)
        # self.force *= 0 #clear force
        self.pos += self.vel * dt
        self.rect.center = self.pos
        self.vel *= glm.exp(-dt*5)

        #Rotational Motion
        if self.rot_vel: 
            self.rot += self.rot_vel * dt
            self.dirty = True
        self.rot_vel *= glm.exp(-dt*2)

    
    def regenerate_physics(self):
        degrees = self.rot*(180/3.141592653589793)#Radians to Degrees
        if not 0:
            self.surf = transform.rotate(self._surf,degrees)
            self.mask = mask.from_surface(self.surf,0)
        else:
            rot_hash = int(degrees*10) % (360*10) // self.cache_every
            cache = Entity._global_physics_cache
            key = (self._surf,rot_hash)
            if key not in cache:
                surf = transform.rotate(self._surf,degrees)
                mask_ = mask.from_surface(surf,0)
                if len(cache) < 1000:
                    global _cache_misses
                    _cache_misses += 1
                    cache[key] = surf,mask_
            else:
                surf,mask_ = cache[key]
            self.surf = surf
            self.mask = mask_
        self.rect = self.surf.get_rect()
        self.rect.center = self.pos

    def onCollide(self,other:"Entity",info:CollisionInfoType,normal:glm.vec2):
        for b in self.behaviours: b.onCollide(self,other)

 
    def addRelForce(self,force:glm.vec2):
        self.force += force

    def onDeath(self,map:MapType,dt:float,game:GameType):
        for b in self.behaviours:
            b.onDeath(self,map,dt,game)

    def getBehaviour(self,behaviour_type:type[BT]) -> BT | None:
        for b in self.behaviours:
            if type(b) is behaviour_type:
                return b


