import math
import Utils
import pygame
from pyglm import glm
from gametypes import *
from Behaviours.Behaviour import Behaviour

class PlayerController(Behaviour):
    camera_pos:Vec2        

    def start(self, gameObject, game:GameType):
        self.camera_pos = game.camera_pos
        self.target_rot = 0


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

        if movement.x or movement.y:
            self.target_rot = math.atan2(-movement.y,movement.x)
        if self.target_rot is not None:
            delta_rotation = Utils.angleDifference(self.target_rot,gameObject.rot)
            if not delta_rotation:
                pass
            elif abs(delta_rotation) < 0.01: #Make it more snappy
                gameObject.rot = self.target_rot
                gameObject.rot_vel = 0
                gameObject.dirty= True
            else:
                t = 0.1
                accel = 2 * (delta_rotation - gameObject.rot_vel * t) / (t*t)
                gameObject.rot_vel += dt * accel
                

    def onCollide(self, gameObject, other):
        self.target_rot = None