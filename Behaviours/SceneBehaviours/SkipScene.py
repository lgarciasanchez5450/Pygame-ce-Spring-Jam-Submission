import Input
import typing
import pygame
from pyglm import glm
from .SceneBehaviour import *

class SkipScene(SceneBehaviour):
    def __init__(self,
                 key:str,
                 scene:str,
                 hold_threshold:int=1,
                 font_size:int=20,
                 alphas:dict[str,int] = {'inactive':0,'active':255},
                 color:tuple[int,int,int]|str = 'white',
                 location:tuple[float,float] = (0,0),
                 offset:tuple[int,int] = (0,0)
                 ):
        self.key = pygame.key.key_code(key)
        self.key_s = key
        self.scene = scene
        self.hold_threshold = hold_threshold
        self.alphas = alphas
        self.location = location
        self.offset = offset
        self.t_color = color
        self.active_alpha = alphas['active']
        self.font = pygame.font.Font('./font/Pixeltype.ttf',font_size)
        self.text = self.font.render(f'Hold {key} to skip',True,color)
        self.surf_rect = pygame.Surface((self.text.get_width(),self.text.get_height()//2))
        self.surf_rect.fill(color)
        self.hold_end = None
        self.text.set_alpha(alphas['inactive'])

    def update(self, scene:SceneType, game:GameType):
        if Input.getKeyJustPressed(self.key):
            self.hold_start = game.time
            self.hold_end = game.time + self.hold_threshold
            self.text.set_alpha(self.alphas['active'])
            self.surf_rect.set_alpha(self.alphas['active'])
        elif Input.getKeyJustReleased(self.key):
            self.hold_end = None
            self.text.set_alpha(self.alphas['inactive'])
            self.surf_rect.set_alpha(self.alphas['inactive'])

        elif Input.getKeyPressed(self.key):
            if game.time >= self.hold_end:
                gm = game.game_manager
                gm.StartScene(gm.scenes[self.scene])
        
    def postDraw(self, scene:SceneType, game:GameType):
        self.show:typing.Literal['always','never','active']
        screen = game.game_manager.screen
        xy = (glm.vec2(screen.get_size()) - self.text.get_size()) * self.location + self.offset
        screen.blit(self.text,xy)
        if self.hold_end is not None and self.hold_threshold > 0:
            percent_passed = min((game.time - self.hold_start)/self.hold_threshold,1)
            screen.blit(self.surf_rect,(xy.x,xy.y+self.text.get_height()),(0,0,percent_passed*self.surf_rect.get_width(),self.surf_rect.get_height()))