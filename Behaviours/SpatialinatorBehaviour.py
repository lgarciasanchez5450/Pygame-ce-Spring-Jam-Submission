import math
import Input
import Async
import Loader
import pygame
import GameStorage
from pyglm import glm
import ResourceManager
from .Behaviour import *
from pygame import constants as const
from Behaviours.PlayerController import PlayerController
from Behaviours.Animation import Animation


class SpatialinatorBehaviour(Behaviour):
    def __init__(self,loc:tuple[float,float],offset:tuple[int,int]):
        font = pygame.font.Font('./font/PixelType.ttf',35)
        self.surf = ResourceManager.loadAlpha('./Images/Game/Entities/spatialinator.png')
        self.loc = loc
        self.offset = offset
        self.key = const.K_c
        self.mine = Loader.loadEntity('spatial_mine.prefab')
        self.mine.clean()
        self.explosion_size = ResourceManager.loadAlpha('./Images/Game/Entities/MineExplosion/20.png').size
        self.explosion = Loader.loadEntity('explosion.prefab')
        self.mine.dead = True
        self.key_surf = font.render(pygame.key.name(self.key),True,'white')
        self.key_surf2 = font.render(pygame.key.name(self.key),True,(200,200,200))
        self.key_surf_half_size = glm.vec2(self.key_surf.get_size())/2
        self.press_start = None
        
    def start(self, gameObject:EntityType, game:GameType):
        self.ctrlr = gameObject.getBehaviour(PlayerController)
        assert self.ctrlr
        game.asyncCtx.StartCoroutine(self.drawUI(game))
    
    def update(self, gameObject, map, dt, game):
        if not GameStorage.found_spatial: return
        if Input.getKeyJustPressed(self.key):
            self.press_start = game.time
        elif Input.getKeyPressed(self.key):
            dir = glm.vec2(
                    (Input.getKeyPressed(pygame.K_d) or Input.getKeyPressed(pygame.K_RIGHT)) - (Input.getKeyPressed(pygame.K_a) or Input.getKeyPressed(pygame.K_LEFT)),
                    (Input.getKeyPressed(pygame.K_s) or Input.getKeyPressed(pygame.K_DOWN)) - (Input.getKeyPressed(pygame.K_w) or Input.getKeyPressed(pygame.K_UP)),
                )
            if dir.x or dir.y:
                self.ctrlr.target_rot = math.atan2(-dir.y,dir.x)
        if Input.getKeyJustReleased(self.key) and self.press_start:
            if self.mine.dead:
                time_down = min(game.time - self.press_start,1.5)
                dir = glm.vec2(glm.cos(-gameObject.rot),glm.sin(-gameObject.rot))
                self.mine.pos.xy = gameObject.pos
                vel = time_down * 600 * dir
                self.mine.vel.xy = vel
                self.mine.dead = False
                game.entities.insert(1,self.mine)
            else:
                game.asyncCtx.StartCoroutine(self.explosionCoro(gameObject,map,game))
            self.press_start = None
               
            


    def explosionCoro(self,gameObject:EntityType,map:MapType,game:GameType):
        import physics
        self.explosion.dead = False
        self.mine.dead = True
        self.explosion.pos.xy = self.mine.pos
        game.spawnEntity(self.explosion)
        anim = self.explosion.getBehaviour(Animation)
        if not anim.running:
            anim.Run(self.explosion,game)
        r = pygame.Rect((0,0),self.explosion_size)
        r.center = self.mine.pos
        yield Async.WaitForSeconds(0.62*len(anim.frames)/anim.fps)
        colliding =list(physics.get_colliding(r,map,0b111))
        for ent in colliding:
            if ent is self.mine: continue
            if math.isfinite(ent.mass):
                ent.pos += gameObject.pos - self.mine.pos
        
        gameObject.pos.xy = self.mine.pos
        while anim.running:
            yield
        self.explosion.dead = True

    def drawUI(self,game:GameType):
        screen = game.game_manager.screen
        surf_size = glm.vec2(self.surf.get_size())
        while True:
            if GameStorage.found_spatial:
                pos = self.loc * (screen.get_size()-surf_size) + self.offset
                screen.fill((100,100,100),(pos,surf_size),const.BLEND_ADD)
                screen.fill((100,100,100),(pos,surf_size),const.BLEND_MULT)
                screen.blit(self.surf,(pos,surf_size))
                key_pos = pos + surf_size - self.key_surf_half_size
                if Input.getKeyPressed(self.key):
                    screen.fill((90,90,90),(key_pos+(-2,3),(15,16)))
                    screen.blit(self.key_surf2,key_pos+(0,1))
                else:
                    screen.fill((100,100,100),(key_pos+(-2,2),(15,16)))

                    screen.blit(self.key_surf,key_pos)
            yield

