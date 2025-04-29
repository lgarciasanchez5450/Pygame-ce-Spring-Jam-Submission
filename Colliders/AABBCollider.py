from Colliders.Collider import *
from Colliders.MaskCollider import *
from math import sin,cos

class AABBCollider(MaskCollider):
    __slots__ = 'size','rotates'
    def __init__(self,size:tuple[int,int]|list[int],rotates=True,isTrigger=False,layers:int=1):
        self.size = tuple(size)
        self.rect = Rect(0,0,*size)
        self.mask = Mask(size)
        if not rotates:
            self.mask.fill()
        self.isTrigger = isTrigger
        self.layers = layers
        self.rotates = rotates
        
    
    def recalculate(self, gameObject:EntityType):
        if not self.rotates: return
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