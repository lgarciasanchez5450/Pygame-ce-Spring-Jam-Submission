from .Action import *
from gametypes import *

class SceneTransporter(Action):
    __slots__ = 'dest','collider_index','collider'
    def __init__(self,name:str,destination_scene:str):
        super().__init__(name)
        self.dest = destination_scene

    def Run(self, gameObject:EntityType,game:GameType):
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