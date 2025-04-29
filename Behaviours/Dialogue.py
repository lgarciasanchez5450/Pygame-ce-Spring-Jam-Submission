import pygame
from pyglm import glm
from gametypes import *
from .Action import Action
import Input

class Dialogue(Action):
    __slots__ = 'dialogue',
    def __init__(self,name:str,dialogue:list[tuple[str,float]]):
        super().__init__(name)
        self.dialogue = dialogue

    def Run(self, gameObject, game:GameType):
        self.running = True
        game.asyncCtx.StartCoroutine(self.doDialogueCoro(game))

    def doDialogueCoro(self,game:GameType):

        i = 0
        while i < len(self.dialogue):
            dialogue_state = game.game_manager.PopDialogue(self.dialogue[i])
            yield
            while True:
                if Input.getKeyJustPressed(Input.K_SPACE):
                    if dialogue_state.running:
                        dialogue_state.done = True
                    elif dialogue_state.done:
                        break
                yield
            i += 1
        game.game_manager.PopDialogue(None)
        yield
        self.running = False

