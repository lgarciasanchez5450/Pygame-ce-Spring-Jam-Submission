import pygame
from pyglm import glm
from gametypes import *
from Behaviours.Behaviour import Behaviour

class PlayerController(Behaviour):
    camera_pos:Vec2        

    def start(self, gameObject, game:GameType):
        self.camera_pos = game.camera_pos


    def update(self, gameObject:EntityType, map, dt:float, game:GameType):
        keys = pygame.key.get_pressed()
        mouse_pressed = pygame.mouse.get_pressed()
        mouse_pos = pygame.mouse.get_pos()
        # updating forwards and backwards + velocity movement
        movement = glm.vec2(
                    keys[pygame.K_d] - keys[pygame.K_a],
                    keys[pygame.K_s] - keys[pygame.K_w],
                )
        
        gameObject.vel += movement * 500 * dt# * gameObject.mass * 20
        
        # changing rotation based on cursor positioning 
        # difference = game.toWorldCoords(mouse_pos) - gameObject.pos
        # gameObject.rot = glm.atan(-difference.y, difference.x)