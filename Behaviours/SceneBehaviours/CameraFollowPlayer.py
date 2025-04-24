from gametypes import *
from Behaviours.SceneBehaviours.SceneBehaviour import SceneBehaviour


class CameraFollowPlayer(SceneBehaviour):
    player:EntityType
    def start(self,scene:SceneType,game:GameType): 
        player = game.FindEntityByName('Player',True)
        if player is None: raise RuntimeError('Could not find player!')
        self.player = player

    def update(self,scene:SceneType,game:GameType): ... 
    def preDraw(self,scene:SceneType,game:GameType): 
        game.camera_pos = self.player.pos
