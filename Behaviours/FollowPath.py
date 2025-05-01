from pyglm import glm
from .Action import *
from .RobotController import RobotController

class FollowPath(Action):
    def __init__(self, name,points:list[tuple[int,int]],threshold:float = 20, *, next = None):
        super().__init__(name, next=next)
        self.points = points
        self.threshold = threshold
        
    def Run(self,gameObject,game:GameType):
        game.asyncCtx.StartCoroutine(self.RunImplAsync(gameObject,game))

    def RunImplAsync(self,gameObject:EntityType,game):
        controller = gameObject.getBehaviour(RobotController)
        if not controller:
            raise LookupError('Could not find robot controller')
        for target in self.points:
            d = target - gameObject.pos
            while (l:=glm.length(d)) > self.threshold:
                d /= l
                controller.Move(d)
                yield
                d = target - gameObject.pos
            controller.Move(glm.vec2())
        self.RunNextAction(gameObject,game)
