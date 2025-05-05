from .Action import *
from .RobotControllerAdvanced import RobotControllerAdvanced
class GoToPosition(Action):
    def __init__(self, name, pos:tuple[int,int],*, next = None):
        super().__init__(name, next=next)
        self.pos = pos
        
    def start(self, gameObject, game):
        ctrlr = gameObject.getBehaviour(RobotControllerAdvanced)
        assert ctrlr
        self.ctrlr = ctrlr

    def update(self, gameObject, map, dt, game):
        if self.running:
            if not self.ctrlr.walking:
                self.running = False
                self.RunNextAction(gameObject,game)
    def Run(self, gameObject:EntityType, game, *args):
        self.running = True
        self.ctrlr.setTarget(self.pos)
        self.ctrlr.startWalk()
