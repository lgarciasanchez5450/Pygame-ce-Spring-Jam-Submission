import os
import Async
import ResourceManager
from .Action import *
from .Animation import Animation

def listdir(path:str|None=None):
    return sorted(os.listdir(path))

class AnimationSequence(Action):
    __slots__ = 'animations','i','animation_names','timer'
    def __init__(self, name,animations:list[str|float], *, next = None):
        super().__init__(name, next=next)
        self.animation_names = animations
        self.i = 0
        self.timer:None|Async.Timer = None

    def start(self, gameObject:EntityType, game):
        self.animations:list[Animation|Async.Timer] = []
        animations_by_name = {anim.name:anim for anim in gameObject.getBehaviours(Animation)[::-1]}
        for name in self.animation_names:
            if type(name) in (int,float):
                self.animations.append(Async.Timer(name,game))
            else:
                self.animations.append(animations_by_name[name])

    def Run(self, gameObject, game):
        if not self.animations:
            self.RunNextAction(gameObject,game)
            return
        self.running = True
        self.i = 0
        self.animations[0].InnerRun()

    def update(self, gameObject:EntityType, map, dt:float, game:GameType):
        if not self.running: return
        cur_anim = self.animations[self.i]
        if not cur_anim.running:
            self.i += 1
            if self.i == len(self.animations):
                self.running = False
                self.RunNextAction(gameObject,game)
            else:
                next_anim = self.animations[self.i]
                if type(next_anim) is Async.Timer:
                    next_anim.start()
                else:
                    next_anim.InnerRun()
        
