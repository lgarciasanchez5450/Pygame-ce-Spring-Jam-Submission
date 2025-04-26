from Colliders.Collider import *
from Colliders.MaskCollider import *
from math import sin,cos

class AABBCollider(MaskCollider):
    def __init__(self,size:tuple[int,int]|list[int],isTrigger=False):
        self.size = tuple(size)
        self.rect = Rect(0,0,*size)
        self._surf = Surface(size,depth=8)
        self.isTrigger = isTrigger
        
    
    def recalculate(self, gameObject:EntityType):
        r = self.rot = gameObject.rot 
        w,h = self.size
        width  = w * abs(cos(r)) + h * abs(sin(r))
        height = w * abs(sin(r)) + h * abs(cos(r))
        self.rect.width = width
        self.rect.height = height
        self.mask = mask.Mask(self.rect.size)
        self.mask.fill()

        self.pos = self.rect.center = gameObject.pos
    
    def update(self, gameObject):
        self.pos = self.rect.center = gameObject.pos