import math
import Utils
import pygame
from pyglm import glm
from gametypes import *
from Behaviours.Behaviour import Behaviour

class PlayerController(Behaviour):
    camera_pos:Vec2        
    active:bool

    def start(self, gameObject, game:GameType):
        self.active = True
        self.camera_pos = game.camera_pos
        self.target_rot = 0

    def update(self, gameObject:EntityType, map, dt:float, game:GameType):
        if not self.active:return
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

    def onDeath(self, gameObject, map, dt, game:GameType):
        game.asyncCtx.StartCoroutine(self.fjkaldfkl(game))

    def fjkaldfkl(self,game:GameType):
        import Async
        import GameStorage
        from Utils.TextRenderer import TextRenderer
        timer = Async.Timer(2,game)
        screen = game.game_manager.screen
        timer.start()

        while timer.isRunning():
            screen.fill((200,200,200),special_flags=pygame.BLEND_MULT)
            yield
        timer.start()
        tr = TextRenderer(GameStorage.death_font)
        death_note = tr.render_align(GameStorage.death_messsage or 'You Died')
        while timer.isRunning():
            screen.fill((200,200,200),special_flags=pygame.BLEND_MULT)
            screen.blit(death_note,death_note.get_rect(center=screen.get_rect().center))
            yield
        timer.start()
        while timer.isRunning():
            screen.fill((200,200,200),special_flags=pygame.BLEND_MULT)
            screen.blit(death_note,death_note.get_rect(center=screen.get_rect().center))
            t = timer.getTimeLeftPercent()
            screen.fill((255*t,255*t,255*t),special_flags=pygame.BLEND_MULT)
            yield
        
        quitEvent = pygame.Event(pygame.QUIT,{'code':1})
        pygame.event.post(quitEvent)
        screen.fill((0,0,0))
        yield
