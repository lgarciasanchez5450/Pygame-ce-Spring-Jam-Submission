import typing
from gametypes import *

class Timer:
    def __init__(self,time:float,game:GameType):
        self.time = time
        self.game = game
        self.start_time = None
    
    def start(self):
        self.start_time = self.game.time
        self.stop_time = self.game.time + self.time

    @property
    def running(self):
        return self.isRunning()

    def isRunning(self):
        return self.game.time <= self.stop_time
    
    def isDone(self):
        if self.start_time is None: return False
        return self.game.time > self.stop_time
    
    def getTimePassed(self):
        return self.game.time - self.start_time #type: ignore

    def getTimePassedPercent(self):
        return self.getTimePassed() / self.time
    
    def getTimeLeft(self):
        return self.stop_time - self.game.time
    
    def getTimeLeftPercent(self):
        return self.getTimeLeft() / self.time
    
    
    

class Delay:
    __slots__ = ()
    def isDone(self,curr_time:float,curr_frame:int) -> bool: ...
    def start(self,curr_time:float,curr_frame:int) -> None: ...

class WaitForSeconds(Delay):
    __slots__ = 'end_time',
    def __init__(self,delay:float):
        self.end_time = delay

    def start(self,curr_time:float,curr_frame:int):
        self.end_time += curr_time

    def isDone(self,curr_time:float,curr_frame:int) -> bool:
        return self.end_time <= curr_time
    
class WaitForFrames(Delay):
    __slots__ = 'end_frames',
    def __init__(self,delay:int):
        self.end_frames = delay
    
    def start(self,curr_time:float,curr_frame:int):
        self.end_frames += curr_frame
    def isDone(self,curr_time:float,curr_frame:int):
        return self.end_frames <= curr_frame
    
    
type Coroutine[T] = typing.Generator[None|Delay,typing.Any,T]

class Context:
    def __init__(self) -> None:
        self.coros:list[Coroutine] = []
        self.waiting:dict[Delay,Coroutine] = {}

    def update(self,curr_time:float,curr_frame:int) -> tuple[Coroutine,typing.Any]|None:
        for delay in list(self.waiting.keys()):
            if delay.isDone(curr_time,curr_frame):
                self.coros.append(self.waiting.pop(delay))

        to_wait:list[int] = []
        for i,coro in enumerate(self.coros):
            try:
                delay = next(coro)
            except StopIteration:
                pass
            else:
                if delay:
                    to_wait.append(i)
                    delay.start(curr_time,curr_frame)
                    self.waiting[delay] = coro
    
        for i in reversed(to_wait):
            self.coros.pop(i)

    def StartCoroutine(self,coro:Coroutine):
        self.coros.append(coro)
        return True

    def StopCoroutine(self,coro:Coroutine):
        try:
            self.coros.remove(coro)
        except ValueError:
            for key,value in self.waiting.items():
                if value is coro:
                    break
            else:
                return False
            del self.waiting[key]
        return True
    def getNumCoros(self):
        return len(self.coros)