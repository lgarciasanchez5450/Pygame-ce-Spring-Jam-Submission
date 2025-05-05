import os
import ResourceManager
from .Action import *

def listdir(path:str|None=None):
    return sorted(os.listdir(path))

class Animation(Action):
    def __init__(self, name, *,fps:int,frames:list[str]|None=None,dir:str|None=None,alpha:tuple[int,int,int]|bool=True,reverse:bool=False, next = None):
        super().__init__(name, next=next)
        if (frames and dir):
            raise RuntimeError(f'Animation[{name}] Both frames and directory supplied to animation. Can only take one')
        if not (frames or dir):
            raise RuntimeError(f'Animation[{name}] Neither frames and directory supplied to animation, needs one.')
        if frames:
            if alpha is True:
                self.frames = [ResourceManager.loadAlpha(path) for path in frames]
            elif alpha is False:
                self.frames = [ResourceManager.loadOpaque(path) for path in frames]
            else:
                assert isinstance(alpha,tuple), f'Animation[{name}] Alpha must be bool or colorkey: {repr(alpha)}'
                colorkey = alpha
                self.frames = [ResourceManager.loadColorKey(path,colorkey) for path in frames]
        elif dir:
            if alpha is True:
                self.frames = [ResourceManager.loadAlpha(os.path.join(dir,name)) for name in listdir(dir)]
            elif alpha is False:
                self.frames = [ResourceManager.loadOpaque(os.path.join(dir,name)) for name in listdir(dir)]
            else:
                assert isinstance(alpha,tuple), f'Animation[{name}] Alpha must be bool or colorkey: {repr(alpha)}'
                self.frames = [ResourceManager.loadColorKey(os.path.join(dir,name),colorkey) for name in listdir(dir)]
        if reverse:
            self.frames.reverse()
        self.fps = fps
        self.t = 0

    def Run(self, gameObject, game):
        self.InnerRun()

    def InnerRun(self):
        self.running = True
        self.t = 0
    
    def update(self, gameObject:EntityType, map, dt:float, game:GameType):
        if not self.running: return
            
        if self.t == 0:
            self.t += dt * self.fps
            frame_surf = self.frames[0]
            gameObject._surf = frame_surf
            gameObject.dirty = True
            return
        
        last_frame = self.t.__trunc__()
        self.t += dt * self.fps
        cur_frame = self.t.__trunc__()
        if last_frame != cur_frame:
            # print(cur_frame)
            if cur_frame == len(self.frames):
                self.running = False
            else:
                frame_surf = self.frames[cur_frame]

                gameObject._surf = frame_surf
                gameObject.dirty = True