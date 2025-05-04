
import Utils
import GameStorage
from pyglm import glm
from pygame import font
from time import perf_counter
from .SceneBehaviour import *

class TrackTime(SceneBehaviour):
    __slots__ = 'draw','font','dirty','location','offset','t_start','time_surf','time_surf_pos','start_time'
    def __init__(self,*,show_time:bool=True,location:tuple[float,float] = (0,0),offset:tuple[int,int] = (0,0)):
        self.draw = show_time
        self.font = font.Font('./font/Pixeltype.ttf',30)
        self.dirty = True
        self.location = glm.vec2(location)
        self.offset = offset

    def start(self, scene, game):
        self.t_start = game.time
        self.start_time = 60*GameStorage.current_hour + GameStorage.current_minute

    def update(self, scene, game):
        t_elapsed = game.time - self.t_start
        t_elapsed += self.start_time
        hour = t_elapsed / 60
        minute = int(60*(hour%1))
        hour = int(hour)
        if GameStorage.current_hour != hour:
            GameStorage.current_hour = hour
            self.dirty = True
        if GameStorage.current_minute != minute:
            GameStorage.current_minute = minute
            self.dirty = True
        


    def postDraw(self, scene, game):
        if self.draw:
            if self.dirty:
                self.time_surf = self.font.render(f'{Utils.formatTime(GameStorage.current_hour,GameStorage.current_minute)}',True,'white')
                self.time_surf_pos = self.location * (glm.vec2(game.game_manager.screen.get_size()) - self.time_surf.get_size())
                self.dirty = True
            game.game_manager.screen.blit(self.time_surf,self.time_surf_pos + self.offset)