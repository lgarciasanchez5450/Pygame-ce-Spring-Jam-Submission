from Utils import easing
import Async
import GameStorage
from Utils.TextRenderer import TextRenderer
from .Action import *
import Input
import pygame
from pygame.transform import box_blur
class GetInput(Action):
    def __init__(self,name:str,options:list[str],*,alignment:int=0.5,next:str|None=None): 
        super().__init__(name,next=next)
        font = pygame.font.Font('./font/Pixeltype.ttf',40)
        self.options = options
        self.alignment = alignment
        self.renderer = TextRenderer(font,(255,255,255))

    def Run(self, gameObject, game:GameType, *args):
        self.running = True
        game.asyncCtx.StartCoroutine(self.loop(gameObject,game))


    def loop(self,gameObject:EntityType,game:GameType):
        screen = game.game_manager.screen
        bg = screen.copy()
        self.surfs = [self.renderer.render_align(s.format(**GameStorage.__dict__),self.alignment) for s in self.options]
        selected_index = 0
        timer= Async.Timer(0.5,game)
        r = pygame.Rect()
        for surf in self.surfs:
            r.union_ip(surf.get_rect())
        extra_y_space = screen.get_height()-r.height*len(self.surfs)
        spacing = extra_y_space / (len(self.surfs)+1)
        positions = []
        y = spacing
        for surf in self.surfs:
            positions.append(y)
            y += r.height + spacing
        r.centerx = screen.get_width()//2
        timer.start()
        while timer.isRunning():
            t = timer.getTimePassedPercent()
            box_blur(screen,round(t*4),dest_surface=bg)
            c = int(255*(1-t/4))
            y_offset = -100*(1-easing.ease_out(t))
            bg.fill((c,c,c),special_flags=pygame.BLEND_MULT)
            screen.blit(bg)
            for ypos,surf in zip(positions,self.surfs):
                r.top = ypos + y_offset
                pygame.draw.rect(screen,(160,160,160),r,0,5)
                screen.blit(surf,r)
            yield            
        while True:
            if Input.getKeyJustPressed(pygame.K_DOWN):
                selected_index += 1
                if selected_index ==len(self.surfs):
                    selected_index = len(self.surfs)
            elif Input.getKeyJustPressed(pygame.K_UP):
                selected_index -= 1
                if selected_index < 0:
                    selected_index = 0
            elif Input.getKeyJustPressed(pygame.K_RETURN) or Input.getKeyJustPressed(pygame.K_SPACE):
                GameStorage.user_input_index = selected_index
                break
            screen.blit(bg)
            for i,(ypos,surf) in enumerate(zip(positions,self.surfs)):
                r.top = ypos
                if i == selected_index:
                    pygame.draw.rect(screen,(240,240,240),r.inflate(18,18),0,5)    
                pygame.draw.rect(screen,(160,160,160),r.inflate(10,10),0,5)
                screen.blit(surf,r)
            yield
        timer.time = 0.2
        timer.start()
        while timer.isRunning():
            t = timer.getTimeLeftPercent()
            box_blur(screen,round(t*4),dest_surface=bg)
            c = int(255*(1-t/4))
            y_offset = -100*(1-easing.ease_out(t))
            bg.fill((c,c,c),special_flags=pygame.BLEND_MULT)
            screen.blit(bg)
            for ypos,surf in zip(positions,self.surfs):
                r.top = ypos + y_offset
                pygame.draw.rect(screen,(160,160,160),r,0,5)
                screen.blit(surf,r)
            yield            
        self.running = False
        self.RunNextAction(gameObject,game)

