
import Utils
import GameStorage
from pyglm import glm
from pygame import font
from time import perf_counter
from .SceneBehaviour import *

class ShowDetail(SceneBehaviour):
    __slots__ = 'st','font','dirty','location','offset','s','surf','surf_pos','cache'
    def __init__(self,format:str,*,cache:bool=False,location:tuple[float,float] = (0,0),offset:tuple[int,int] = (0,0)):
        self.st = format
        self.cache = cache
        self.font = font.Font('./font/Pixeltype.ttf',30)
        self.location = glm.vec2(location)
        self.offset = offset
        self.dirty = True

    def start(self, scene, game):
        self.s = self.st.format(**GameStorage.__dict__)


    def postDraw(self, scene, game):
        if self.cache:
            s = self.st.format(**GameStorage.__dict__)
            if s != self.s:
                self.s = s
        else:
            self.s = self.st.format(**GameStorage.__dict__)

        if self.dirty:
            self.surf = self.font.render(self.s,True,'white')
            if self.cache:
                self.dirty = False
        self.surf_pos = self.location * (glm.vec2(game.game_manager.screen.get_size()) - self.surf.get_size())
        game.game_manager.screen.blit(self.surf,self.surf_pos + self.offset)