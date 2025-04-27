import os
import time
import pygame
import random
import physics
import ResourceManager
from pyglm import glm
from gametypes import *
from EntityTags import *
from Scene import Scene
from Entities import Entity
from gui.utils import utils as g_utils
from GameConstants import BG_CHUNK_SIZE,SCENE_FOLDER
from background_image_generator import generate
from Map import Map

pygame.init()
main_font = pygame.font.Font('./font/Pixeltype.ttf', 26)

class GameManager:
    def __init__(self,game:GameType,window:pygame.Window):
        self.space_bg = {}
        self.game = game
        self.window = window
        self.screen = self.window.get_surface()
        self.scenes:dict[str,Scene] = {}

        for filename in os.listdir(SCENE_FOLDER):
            if filename.endswith('.scene'):
                name = filename.removesuffix('.scene')
                if name in self.scenes:
                    raise NameError(f'Error Loading Scenes: There are two scenes with the name: {name}')
                fqn = os.path.abspath(os.path.join(SCENE_FOLDER,filename))
                self.scenes[name] = Scene(fqn)
        self.pre_draw_layers = {
            -1:1
        }




    def start_game(self):
        self.scene = self.scenes['living_quarters']
        self.map = Map(self.scene)
        self.scene.start(self.game)

    def pre_update(self): ...

    def post_update(self,map:MapType): ...

    def pre_draw(self):
        self.scene.preDraw(self.game)
        game = self.game
        game.screen_rect.center = game.camera_pos
        for cpos in physics.collide_chunks2d(game.screen_rect.left,game.screen_rect.top,game.screen_rect.right,game.screen_rect.bottom,BG_CHUNK_SIZE):
            surf = g_utils.useCache(generate,cpos,self.space_bg)
            self.screen.blit(surf,glm.floor(game.half_screen_size + glm.vec2(cpos) * BG_CHUNK_SIZE - game.camera_pos))

        self.screen.blit(self.scene.map,glm.floor(game.half_screen_size - game.camera_pos))

    def ui_draw(self): 
        self.scene.postDraw(self.game)

    #Public Utility Methods

    def PopDialogue(self,text:str,chars_per_second:int)

    def StartScene(self,scene:Scene):
        if self.scene is scene:
            #freak out /aka get freaky
            pass
        else:
            self.scene.stop(self.game)
            self.scene = scene
            self.scene.start(self.game)