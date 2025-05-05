from pyglm import glm
import Async
import Input
import random
import GameStorage
from .Behaviour import *
from .RobotControllerAdvanced import RobotControllerAdvanced


class BossHappyStage(Behaviour):
    def __init__(self,bad_work_path:str,good_work_path:str):
        self.good_work_path = good_work_path

    def start(self, gameObject, game):
        self.timer = Async.Timer(random.randint(14,18),game)
        player = game.FindEntityByName('Player',True)
        assert player is not None
        self.player = player
        self.current_action = None
        self.timer.start()
        self.ctrlr = gameObject.getBehaviour(RobotControllerAdvanced)
        assert self.ctrlr is not None,'Boss Behaviour could not find Controller'

    def update(self, gameObject, map, dt, game):
        if self.timer and self.timer.isDone():
            self.timer = None
            if GameStorage.scrap_collected_today < 10:
                gameObject.get
                self.bad_work_path
                next_action = self.micromanage_player(gameObject,game)
            # self.timer.time = random.randint(140,180)
            # self.timer.start()
            if self.current_action:
                game.asyncCtx.StopCoroutine(self.current_action)
            self.current_action = next_action
            game.asyncCtx.StartCoroutine(self.current_action)

    def micromanage_player(self,gameObject:EntityType,game:GameType):
        player = self.player
        ctrlr = self.ctrlr
        i = 0
        dialogue = [
            ('§Cf00Hey You, what do you think your doing?!!',20)
        ]
        while True:
            if (dist_to_player:=glm.distance(gameObject.pos,player.pos)) > 55: 
                dif = player.pos - gameObject.pos
                dif /= dist_to_player
                ctrlr.Move(dif)
            
            game.game_manager.PopDialogue()
            yield