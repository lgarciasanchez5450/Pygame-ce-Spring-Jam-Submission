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
from DialogueManager import DialogueManager
from GameConstants import BG_CHUNK_SIZE,SCENE_FOLDER
from background_image_generator import generate

pygame.init()
main_font = pygame.font.Font('./font/Pixeltype.ttf', 26)

class GameManager:
    def __init__(self,game:GameType,window:pygame.Window):
        self.space_bg = {}
        self.game = game
        self.window = window
        self.screen = self.window.get_surface()
        self.scenes:dict[str,Scene] = {}
        self.dialogue_manager = DialogueManager()

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

        self.current_dialogue:None|tuple[str|int] = None



    def start_game(self):
        self.scene = self.scenes['start_cs']
        self.scene.start(self.game)

    def pre_update(self): ...

    def post_update(self,map:MapType): ...

    def pre_draw(self):
        self.screen.fill('black')
        self.scene.preDraw(self.game)
        game = self.game
        game.screen_rect.center = game.camera_pos
        # for cpos in physics.collide_chunks2d(game.screen_rect.left,game.screen_rect.top,game.screen_rect.right,game.screen_rect.bottom,BG_CHUNK_SIZE):
        #     surf = g_utils.useCache(generate,cpos,self.space_bg)
        #     self.screen.blit(surf,glm.floor(game.half_screen_size + glm.vec2(cpos) * BG_CHUNK_SIZE - game.camera_pos))

        self.screen.blit(self.scene.map,glm.floor(game.half_screen_size - game.camera_pos))

    def ui_draw(self): 
        if (d:= self.dialogue_manager.getText(self.game.dt)) is not None:
            dialogue_rect = d.get_rect()
            dialogue_rect.centerx = self.screen.get_width()//2
            dialogue_rect.bottom = self.screen.get_height() - 50
            border_rect = dialogue_rect.inflate(10,8).move(0,-2)
            pygame.draw.rect(self.screen,(120,120,120),border_rect,0,2)
            pygame.draw.rect(self.screen,(190,190,190),border_rect,1,2)
            self.screen.blit(d,dialogue_rect)
        self.scene.postDraw(self.game)

    #Public Utility Methods

    def PopDialogue(self,dialogue:tuple[str,float]|None):
        return self.dialogue_manager.setCurrentDialogue(dialogue)

    def StartScene(self,scene:Scene):
        if self.scene is scene:
            #freak out /aka get freaky
            pass
        else:
            self.scene.stop(self.game)
            self.scene = scene
            self.scene.start(self.game)