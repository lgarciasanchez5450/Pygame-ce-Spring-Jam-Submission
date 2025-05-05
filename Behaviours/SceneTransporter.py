import Async
import pygame
from pyglm import glm
from Utils import easing
from .Action import *
from gametypes import *
from gui.utils.utils import lerp        
from .SceneBehaviours.CameraFollowPlayer import CameraFollowPlayer

class SceneTransporter(Action):
    __slots__ = 'dest','collider_index','collider','force_next','as_new'
    def __init__(self,name:str,destination_scene:str,*,as_new:bool=False,next:str|None=None,force_next:bool=False):
        super().__init__(name,next=next)
        self.dest = destination_scene
        self.as_new = as_new
        self.force_next = force_next
        

    def Run(self, gameObject:EntityType,game:GameType):
        game.asyncCtx.StartCoroutine(self.goToNextCoroutine(gameObject,game))

    def goToNextCoroutine(self,gameObject:EntityType,game:GameType):
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
        screen.fill((0,0,0))        
        yield
        timer =  Async.Timer(1,game)
        timer.start()
        gm = game.game_manager
        if self.as_new:
            import Loader
            import Scene
            scene = Scene.Scene.fromFile('./Scenes/'+self.dest+'.scene')
            gm.StartScene(scene)
        else:
            gm.StartScene(gm.scenes[self.dest])
            cfp.player = player
        self.RunNextAction(gameObject,game,even_if_already_running=self.force_next)
        while timer.isRunning():
            screen.fill((0,0,0))
            yield
        
        timer = Async.Timer(2,game)
        timer.start()
        while timer.isRunning():
            t = timer.getTimePassedPercent()
            screen.fill((255*t,255*t,255*t),special_flags=pygame.BLEND_MULT)
            yield