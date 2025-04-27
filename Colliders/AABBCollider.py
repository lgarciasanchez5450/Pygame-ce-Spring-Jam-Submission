from Colliders.Collider import *
from Colliders.MaskCollider import *
from math import sin,cos

class AABBCollider(MaskCollider):
    __slots__ = 'size','_surf',
    def __init__(self,size:tuple[int,int]|list[int],isTrigger=False,layers:int=1):
        self.size = tuple(size)
        self.rect = Rect(0,0,*size)
        self._surf = Surface(size,depth=8)
        self.isTrigger = isTrigger
        self.layers = layers
        
    
    def recalculate(self, gameObject:EntityType):
        r = gameObject.rot 
        w,h = self.size
        width  = w * abs(cos(r)) + h * abs(sin(r))
        height = w * abs(sin(r)) + h * abs(cos(r))
        self.rect.width = width
        self.rect.height = height
        self.mask = mask.Mask(self.rect.size)
        self.mask.fill()
        self.rect.center = gameObject.pos
    
    def update(self, gameObject):
        self.rect.center = gameObject.pos