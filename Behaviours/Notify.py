import Async
import pygame
from pyglm import glm
from gametypes import *
from .Action import Action
from Utils import easing
from Utils.TextRenderer import TextRenderer

class Notify(Action):
    def __init__(self,name:str,text:str,time:float,offset:tuple[int,int]=(0,0),vel:tuple[int,int]=(0,0),*,next:str|None=None):
        super().__init__(name,next=next)
        self.text = text
        self.time = time
        self.offset = offset
        self.vel = glm.vec2(vel)
        
        self.font = pygame.font.Font('./font/Pixeltype.ttf',30)

    def Run(self, gameObject, game:GameType):
        self.running = True
        game.asyncCtx.StartCoroutine(self.doDialogueCoro(gameObject,game))
        self.RunNextAction(gameObject,game)
        self.running = False


    def doDialogueCoro(self,gameObject:EntityType,game:GameType):
        timer = Async.Timer(self.time,game)
        gm= game.game_manager
        renderer = TextRenderer(self.font,(255,255,255))
        timer.start()
        surf = renderer.render_align(self.text,0.5)
        text_pos = glm.vec2(gameObject.pos) - glm.vec2(surf.get_size())//2  + self.offset

        while timer.isRunning():
            t = timer.getTimeLeftPercent()
            text_pos += self.vel * game.dt
            alpha = int(255*easing.ease_out_circ(t))
            surf.set_alpha(alpha)
            gm.screen.blit(surf,text_pos-game.camera_pos+game.half_screen_size)
            yield

