import math
import json
import Loader
import random
from GameConstants import TWO_PI,PI,PI_OVER_TWO
from pygame import Rect
from pyglm import glm
from .Behaviour import *
from .RobotControllerAdvanced import RobotControllerAdvanced

scrap_prefabs = [
    'scrap1.prefab',
    'scrap2.prefab',
    'scrap3.prefab',
    'scrap4.prefab',
    'scrap5.prefab',
    'scrap6.prefab'
]

class WorkerBehaviour(Behaviour):
    def __init__(self,workspace:str,supply_pos:tuple[int,int],trash_pos:tuple[int,int],finished_pos:tuple[int,int],dialogue_path:str|None=None):
        self.state = 'get_part'
        self.supply_pos = glm.vec2(supply_pos)
        self.trash_pos = glm.vec2(trash_pos)
        self.finished_pos = glm.vec2(finished_pos)
        self.work_time = 5
        self.workspace_name = workspace
        if dialogue_path is not None:
            with open(dialogue_path,'r',encoding='utf-8') as file:
                self.dialogue:dict = json.load(file)
        else:
            self.dialogue = None
        self.box = None
        self.player_coro = None
        self.player = None

    def start(self, gameObject, game):
        self.ctrlr = gameObject.getBehaviour(RobotControllerAdvanced)
        assert self.ctrlr is not None
        self.desk_pos = glm.vec2(gameObject.pos)
        self.workspace = game.FindEntityByName(self.workspace_name)
        assert self.workspace is not None

    def update(self, gameObject, map, dt, game):
        ctrlr = self.ctrlr
        match self.state:
            case 'look-at-player':
                ctrlr.Move(glm.vec2())
                dif = self.player.pos - gameObject.pos 
                ctrlr.target_rot = math.atan2(-dif.y,dif.x)
                if glm.distance(self.player.pos,gameObject.pos) > 100:
                    self.state = self.og_state

            case 'get_part':
                if ctrlr.target_pos != self.supply_pos:
                    ctrlr.setTarget(self.supply_pos)
                    ctrlr.startWalk()
                else:
                    if not ctrlr.walking:
                        self.state = 'go_to_desk'
            case 'go_to_desk':
                if ctrlr.target_pos != self.desk_pos:
                    ctrlr.setTarget(self.desk_pos)
                    ctrlr.startWalk()
                else:
                    if not ctrlr.walking:
                        ctrlr.Move(glm.vec2())
                        if not self.box:
                            self.box = Loader.loadEntity('box.prefab')
                            self.box.pos.xy = self.workspace.pos - glm.vec2(0,5)
                            game.spawnEntity(self.box)
                        ctrlr.target_rot = -PI_OVER_TWO
                        self.work_time = 5
                        self.state = 'work'
            case 'work':
                #do nothing (ie "do work")
                self.work_time -= game.dt
                if self.work_time <= 0:
                    scrap = Loader.loadEntity(random.choice(scrap_prefabs))
                    scrap.clean()
                    dist = ctrlr.radius + max(scrap.colliders[0].rect.size)/2
                    scrap.pos = gameObject.pos + dist* glm.vec2(glm.cos(gameObject.rot),glm.sin(gameObject.rot))
                    ctrlr.grabObject(gameObject,scrap,game)
                    game.spawnEntity(scrap)
                    self.work_time = 5
                    self.state = 'deposit_trash'
            case 'deposit_trash':
                if ctrlr.target_pos != self.trash_pos:
                    ctrlr.setTarget(self.trash_pos)
                    ctrlr.startWalk()
                else:
                    if not ctrlr.walking:
                        ctrlr.releaseObject(gameObject,game)
                        self.state = 'go_to_desk_to_put_away_finished_product'
            case 'go_to_desk_to_put_away_finished_product':
                if ctrlr.target_pos != self.desk_pos:
                    ctrlr.setTarget(self.desk_pos)
                    ctrlr.startWalk()
                else:
                    if not ctrlr.walking:
                        ctrlr.Move(glm.vec2())
                        ctrlr.target_rot = -PI_OVER_TWO
                        self.work_time = 2
                        self.state = 'finishing_touches'
            case 'finishing_touches':
                self.work_time -= dt
                if self.work_time <= 0:
                    if self.box:
                        ctrlr.grabObject(gameObject,self.box,game)
                        ctrlr.setTarget(self.finished_pos + glm.diskRand(20))
                        ctrlr.startWalk()
                        self.state = 'put_product_away'
            case 'put_product_away':
                if not ctrlr.walking:
                    if self.box:
                        ctrlr.releaseObject(gameObject,game)
                        self.box = None
                    ctrlr.Move(glm.vec2())
                    ctrlr.target_rot = -PI_OVER_TWO
                    self.work_time = 2
                    self.state = 'restart'
            case 'restart':
                if ctrlr.target_pos != self.desk_pos:
                    ctrlr.setTarget(self.desk_pos)
                    ctrlr.startWalk()
                else:
                    if not ctrlr.walking:
                        ctrlr.Move(glm.vec2())
                        ctrlr.target_rot = -PI_OVER_TWO
                        self.work_time = 2
                        self.state = 'get_part'

    def onTriggerEnter(self, gameObject:EntityType, other:EntityType, game:GameType):
        if other.name == 'Player' and self.state != 'look-at-player':
            self.og_state = self.state
            self.player = other
            self.state = 'look-at-player'
            if self.dialogue:
                d = self.dialogue.get(self.og_state,None)
                if d is None:
                    d = 'Idk what to say'
                if type(d) is str:
                    d = d,20
                game.game_manager.PopDialogue(d)

    def onTriggerExit(self, gameObject:EntityType, other:EntityType, game:GameType):
        if other.name == 'Player' and self.state == 'look-at-player':
            self.state = self.og_state
            self.player = None
    # def interactive(self,player:EntityType,gameObject:EntityType,game:GameType):
    #     import math
    #     og_state = self.state
    #     self.state = 'idle'
    #     ctrlr = self.ctrlr
        
    #     if self.dialogue is None:
    #         dialogue = {
    #             '_other': ('The Developer was too lazy and theres only 13 hours left to submit so yeah..',20)
    #         }
    #     else:
    #         dialogue = self.dialogue
    #     yield
    #     game.game_manager.PopDialogue(dialogue.get(og_state,dialogue.get('_other',('This text should never show',10))))
    #     while True:

    #         yield
