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
from GameConstants import BG_CHUNK_SIZE
from background_image_generator import generate
from Behaviours.PlayerController import PlayerController
from Map import Map
pygame.init()
main_font = pygame.font.Font('./font/Pixeltype.ttf', 26)

class GameManager:
    def __init__(self,game:GameType,window:pygame.Window):
        self.space_bg = {}
        self.game = game
        self.window = window
        self.screen = self.window.get_surface()
        self.scenes = {
            'docks':Scene('Scenes/docks.scene'),
            'living_quarters1':Scene('Scenes/living_quarters.scene')
        }
        self.pre_draw_layers = {
            -1:1
        }
        
        player_surf = ResourceManager.loadAlpha('./Images/Game/Player/head.png')
        # self.player = Entity.Entity(glm.vec2(500,500),glm.vec2(),1,
        #                             0,0,physics.calculateMomentOfInertia(player_surf,1),
        #                             player_surf)
        # self.player.behaviours.append(
        #     PlayerController()
        # )

    def start_game(self):
        self.scene = self.scenes['living_quarters1']
        self.map = Map(self.scene)
        # self.game.spawnEntity(self.player)
        self.game.spawnEntities(self.scene.entities)
        self.scene.start(self.game)
        # surf = ResourceManager.loadColorKey('./Images/Game/Crates/Wooden.png',(1,0,0))

        # self.game.spawnEntity(
        #     Entity.Entity(glm.vec2(600,500),glm.vec2(),1,
        #                   0,0,physics.calculateMomentOfInertia(surf,1),
        #                   surf
        #     )
        # )

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

    def ui_draw(self): ...
