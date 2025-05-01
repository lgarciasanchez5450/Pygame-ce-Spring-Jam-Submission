import pygame
from pyglm import glm
from gametypes import *
from .Action import Action
import Input

class Dialogue(Action):
    __slots__ = 'dialogue',
    def __init__(self,name:str,dialogue:list[tuple[str,float]],*,next:str|None=None):
        super().__init__(name,next=next)
        self.dialogue = dialogue

    def Run(self, gameObject, game:GameType):
        self.running = True
        game.asyncCtx.StartCoroutine(self.doDialogueCoro(gameObject,game))

    def doDialogueCoro(self,gameObject,game:GameType):
        gm= game.game_manager
        scene = gm.scene
        i = 0
        while i < len(self.dialogue):
            dialogue_state = gm.PopDialogue(self.dialogue[i])
            yield
            while True:
                if Input.getKeyJustPressed(Input.K_SPACE):
                    if dialogue_state.running:
                        dialogue_state.done = True
                    elif dialogue_state.done:
                        break
                if gm.scene is not scene:
                    gm.PopDialogue(None)
                    self.running = False
                    return
                yield
            i += 1
        gm.PopDialogue(None)
        yield
        self.RunNextAction(gameObject,game)
        self.running = False

