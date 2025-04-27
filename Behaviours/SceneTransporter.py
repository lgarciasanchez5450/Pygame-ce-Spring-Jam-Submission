from .Behaviour import *
from gametypes import *

class SceneTransporter(Behaviour):
    __slots__ = 'dest','collider_index','collider'
    def __init__(self,destination_scene:str,collider:int=-1):
        self.dest = destination_scene
        self.collider_index = collider
    
    def start(self, gameObject:EntityType, game:GameType):
        if self.collider_index == -1:
            for c in gameObject.colliders:
                if c.isTrigger:
                    self.collider = c
                    break
            else:
                raise RuntimeError(f'No trigger collider found for entity: {gameObject.name}')
        else:
            self.collider = gameObject.colliders[self.collider_index]
            if not self.collider.isTrigger:
                raise RuntimeError(f'Specified collider not trigger for entity: {gameObject.name}')
            
    

    def onTriggerEnter(self, gameObject:EntityType, other:EntityType,game:GameType):
        if other.name == 'Player':
            game.asyncCtx.StartCoroutine(self.goToNextCoroutine(gameObject,game))

    def goToNextCoroutine(self,gameObject:EntityType,game:GameType):
        import Async
        import pygame
        from pyglm import glm
        from Utils import easing
        from gui.utils.utils import lerp        
        from .SceneBehaviours.CameraFollowPlayer import CameraFollowPlayer
        screen = game.window.get_surface()

        cfp = game.game_manager.scene.GetBehaviour(CameraFollowPlayer)
        if cfp is None:
            return None
        class FakeEntity:
            pos:Vec2
            __slots__ = 'pos',
        player,cfp.player = cfp.player,FakeEntity()
        start_pos = glm.vec2(player.pos)
        end_pos = glm.vec2(gameObject.pos)


        #Move Camera to SceneTransporter object
        timer = Async.Timer(2,game)
        timer.start()
        while timer.isRunning():
            t = timer.getTimePassedPercent()
            cfp.player.pos = lerp(start_pos,end_pos,t)
            yield
        
        #fade to black
        timer.start()
        while timer.isRunning():
            t = timer.getTimeLeftPercent()
            screen.fill((255*t,255*t,255*t),special_flags=pygame.BLEND_MULT)
            yield

        #stay black for 1 seconds
        
        timer =  Async.Timer(1,game)
        timer.start()
        while timer.isRunning():
            screen.fill((0,0,0))
            cfp.player = player
            game.game_manager.game.game_manager.game.game_manager.game.game_manager.game.game_manager.game.game_manager.game.game_manager.StartScene(game.game_manager.scenes[self.dest])
            yield
        
        timer = Async.Timer(2,game)
        timer.start()
        while timer.isRunning():
            t = timer.getTimePassedPercent()
            screen.fill((255*t,255*t,255*t),special_flags=pygame.BLEND_MULT)
            yield