from .Behaviour import *
import Input
import pygame

class InteractNotifier(Behaviour):
    __slots__ = 'pressing_surf','og_surf'
    def start(self, gameObject:EntityType, game:GameType):
        self.pressing_surf = gameObject._surf.copy()
        self.og_surf = gameObject._surf
        self.pressing_surf.fill((200,200,200),special_flags=pygame.BLEND_RGB_MULT)

    def update(self, gameObject, map, dt, game):
        if Input.getKeyPressed(Input.K_DOWN) and gameObject._surf is self.og_surf:
            gameObject._surf = self.pressing_surf
            gameObject.dirty = True
        elif not Input.getKeyPressed(Input.K_DOWN) and gameObject._surf is self.pressing_surf:
            gameObject._surf = self.og_surf
            gameObject.dirty = True