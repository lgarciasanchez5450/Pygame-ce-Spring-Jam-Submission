import pygame
from pyglm import glm
from gametypes import *
from .Action import Action

class Dialogue(Action):
    def __init__(self,name:str,dialogue:list[tuple[str,float]]):
        super().__init__(name)
        self.dialogue = dialogue

    def Run(self, gameObject, game:GameType):
        game.asyncCtx.StartCoroutine(self.doDialogueCoro(game))

    def doDialogueCoro(self,game:GameType):
        i = 0
        while i < len(self.dialogue):
            game.game_manager.PopDialogue(self.dialogue[i])
            yield
            while not pygame.key.get_just_pressed()[pygame.K_SPACE]:
                yield
            i += 1
        game.game_manager.PopDialogue(None)

