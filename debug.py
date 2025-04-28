import typing
import Utils.utils as utils
from time import perf_counter
import functools
F = typing.TypeVar('F',bound=typing.Callable)
P = typing.ParamSpec('P')
V = typing.TypeVar('V')
if __debug__:
   
    class Profile:
        active = False
        __slots__ = 'func','last_timed'
        def __init__(self,func:typing.Callable[P,V]):
            self.func = func

        def __call__(self, *args:P.args, **kwds:P.kwargs):
            if self.active:
                t_start = perf_counter()
                try:
                    return self.func(*args,**kwds)
                finally:
                    t_end = perf_counter()
                    self.last_timed = t_end-t_start
            else:
                return self.func(*args,**kwds)
else:
    class Profile:#type: ignore[same-name]
        active:bool = False
        last_timed:float
        def __new__(cls,func:typing.Callable[P,V]) -> 'Profile': #type: ignore
            return func 

        def __call__(self,*args:P.args,**kwds:P.kwargs) -> V: ...

    