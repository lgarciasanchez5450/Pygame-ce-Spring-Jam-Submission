from GameConstants import RAD_TO_DEG,TWO_PI,PI_OVER_TWO,PI
from Colliders.Collider import *
from Colliders.MaskCollider import *
from pygame import transform
from math import sin,cos


class BoxCollider(MaskCollider):
    __slots__ = 'size','_surf','rot',
    def __init__(self,size:tuple[int,int]|list[int],isTrigger=False,layers:int=1):
        self.isTrigger = isTrigger
        self.size = tuple(size)
        self.rect = Rect(0,0,*size)
        self._surf = Surface(size,depth=8)
        self._surf.set_colorkey((0,0,0))
        self._surf.fill((255,255,255))
        self.layers = layers
        
        self.mask = mask.from_surface(self._surf)
    
    def recalculate(self, gameObject:EntityType):
        r = self.rot = gameObject.rot 
        w,h = self.size
        width  = w * abs(cos(r)) + h * abs(sin(r))
        height = w * abs(sin(r)) + h * abs(cos(r))
        self.rect.width = width
        self.rect.height = height
        self.mask = mask.from_surface(transform.rotate(self._surf,r * RAD_TO_DEG))
        self.rect.center = gameObject.pos
        
    def update(self, gameObject):
        self.rect.center = gameObject.pos
# class BoxCollider(Collider):
#     _global_cache:dict[tuple[Surface,int],Mask] = {}

#     size:Vec2
#     rot:float
#     def __init__(self,size:tuple[float,float]|list[int]|Vec2):
#         self.size = glm.vec2(size)
#         self.rect = Rect(0,0,*size)

#     def recalculate(self, gameObject:EntityType):
#         assert gameObject._surf is not None
#         r = self.rot = gameObject.rot
#         w,h = self.size
#         width  = w * abs(glm.cos(r)) + h * abs(glm.sin(r))
#         height = w * abs(glm.sin(r)) + h * abs(glm.cos(r))
#         self.rect.width = width
#         self.rect.height = height
#         self.pos = self.rect.center = gameObject.pos

#     def update(self, gameObject:EntityType):
#         self.pos = self.rect.center = gameObject.pos
        

#     def collideBox(self,other:"BoxCollider"):
#         rel_pos = other.pos - self.pos
#         s_n1 = glm.vec2(glm.cos(self.rot),glm.sin(self.rot))
#         s_n2 = glm.vec2(-s_n1.y,s_n1.x) #rotated by 90 degrees
#         s_closest = max(s_n1,s_n2,-s_n1,-s_n2,lambda v: glm.dot(rel_pos,v))
        
#         o_n1 = glm.vec2(glm.cos(other.rot),glm.sin(other.rot))
#         o_n2 = glm.vec2(-o_n1.y,o_n1.x)
#         o_closest = max(o_n1,o_n2,-o_n1,-o_n2,lambda v: glm.dot(-rel_pos,v))




#         s_min = float('inf')
#         s_max = -s_min
#         s_vertices = [
#             glm.vec2(self.size.x,self.size.ys)
#         ]
        