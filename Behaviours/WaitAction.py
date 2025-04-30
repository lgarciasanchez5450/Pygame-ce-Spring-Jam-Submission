from .Action import *
import Async
class WaitAction(Action):
    __slots__ = 'time',
    def __init__(self, name:str,time:float, *, next = None):
        super().__init__(name, next=next)
        self.time = time

    def Run(self, gameObject, game:GameType, *args):
        game.asyncCtx.StartCoroutine(self.waitAsync(gameObject,game))
        
    def waitAsync(self,gameObject,game:GameType):
        timer = Async.Timer(self.time,game)
        timer.start()
        while timer.isRunning():
            yield
        self.RunNextAction(gameObject,game)