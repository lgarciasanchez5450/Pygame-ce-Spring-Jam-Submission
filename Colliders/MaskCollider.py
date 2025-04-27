from GameConstants import RAD_TO_DEG
from Colliders.Collider import *
from pygame import mask
from pygame import Surface
from pygame import Mask

class MaskCollider(Collider):
    _global_cache:dict[tuple[Surface,int],Mask] = {}
    mask:Mask
    __slots__ = 'cache','mask'
    def __init__(self,isTrigger=False,layers:int=1,cache:int=2):
        self.cache = cache
        self.isTrigger = isTrigger
        self.layers = layers

    def recalculate(self, gameObject:EntityType):
        assert gameObject._surf is not None
        if not self.cache:
            self.mask = mask.from_surface(gameObject.surf,0)
        else:
            cache = MaskCollider._global_cache
            degrees = gameObject.rot * RAD_TO_DEG
            rot_hash = int(degrees * self.cache) % (360*self.cache)
            key = (gameObject._surf,rot_hash)
            if key not in cache:
                mask_ = mask.from_surface(gameObject.surf,0)
                cache[key] = mask_
            else:
                mask_ = cache[key]
            self.mask = mask_

        self.rect = gameObject.surf.get_rect(center=gameObject.pos)

    def update(self, gameObject:EntityType):
        self.rect.center = gameObject.pos
