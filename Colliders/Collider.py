from gametypes import *
from pygame import Rect

class Collider:

    _subclasses_:dict[str,type['Collider']] = {}
    def __init_subclass__(cls):
        name = cls.__name__
        if name in Collider._subclasses_:
            raise NameError(f'Collider {cls} conflicts with another. Maybe two behaviours have the same name? (<- this cannot happen)')
        Collider._subclasses_[name] = cls


    gameObject:EntityType
    rect:Rect
    isTrigger:bool
    layers:int
    __slots__ = 'gameObject','rect','isTrigger','layers'

    def recalculate(self,gameObject:EntityType): ...
    def update(self,gameObject:EntityType): ...

    def __repr__(self):
        return f'{type(self)} for {self.gameObject}'