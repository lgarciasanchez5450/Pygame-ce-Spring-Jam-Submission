from pyglm import glm
from pygame import Surface

class Particle:
    __slots__ = 'pos','vel','surf','offset','dead'
    def __init__(self,pos:glm.vec2,vel:glm.vec2,surf:Surface):
        self.pos = pos
        self.vel = vel
        self.setSurf(surf)
        self.dead = False
        
    def setSurf(self,surf:Surface):
        self.surf = surf
        self.offset = surf.get_width()//2,surf.get_height()//2
        