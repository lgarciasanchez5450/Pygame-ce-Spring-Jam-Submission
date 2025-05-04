from pyglm import glm
from .Behaviour import *
from .RobotControllerAdvanced import RobotControllerAdvanced


class BehaviourTree:
    def __init__(self):
        pass
    
class WorkerBehaviour(Behaviour):
    def __init__(self,supply_pos:tuple[int,int],trash_pos:tuple[int,int]):
        self.state = 'get_part'
        self.supply_pos = glm.vec2(supply_pos)
        self.trash_pos = glm.vec2(trash_pos)
        self.work_time = 5

    def start(self, gameObject, game):
        self.ctrlr = gameObject.getBehaviour(RobotControllerAdvanced)
        assert self.ctrlr is not None
        self.desk_pos = glm.vec2(gameObject.pos)

    def update(self, gameObject, map, dt, game):
        ctrlr = self.ctrlr
        match self.state:
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
                        self.state = 'work'
            case 'work':
                #do nothing (ie "do work")
                self.work_time -= game.dt
                if self.work_time <= 0:
                    self.work_time = 5
                    self.state = 'deposit_trash'
            case 'deposit_trash':
                if ctrlr.target_pos != self.trash_pos:
                    print('despositing trash!')
                    ctrlr.setTarget(self.trash_pos)
                    ctrlr.startWalk()
                else:
                    if not ctrlr.walking:
                        print('got to trash')
                        self.state = 'go_to_desk'



    