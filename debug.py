import utils
from time import perf_counter

if __debug__:
    class Profile:
        active = False
        def __init__(self,func):
            self.func = func

        def __call__(self, *args, **kwds):
            if self.active:
                t_start = perf_counter()
                try:
                    return self.func(*args,**kwds)
                finally:
                    t_end = perf_counter()
                    print(f'{self.func.__name__}: {utils.formatTime(t_end-t_start)}')
            else:
                return self.func(*args,**kwds)
else:
    class Profile:#type: ignore[same-name]
        active:bool = False
        def __new__(cls,func):
            return func 