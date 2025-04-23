import math
import typing
import difflib
from pyglm import glm
from gametypes import *

def expDecay(a,b,decay:float,dt:float):
    return b+(a-b)*math.exp(-decay*dt)

def cross2d(a:Vec2,b:Vec2):
    return a.x*b.y-a.y*b.x


def formatBytes(b:int):
    i = 0
    while b >= 1024:
        i += 1
        b >>= 10
    return f'{b} {['B','KiB','MiB','GiB'][i]}'
def formatTime(b:int,*,decimals:int=2):
    if b <= 0:
        return f'{b} s'
    i = 0
    while b < 1:
        i += 1
        b *= 1000
    return f'{{:.{decimals}f}} {['s','ms','µs','ns'][i]}'.format(b)

def rotateAbout(a:Vec2,b:Vec2):
    return glm.vec2(
        a.x * b.x - a.y * b.y,
        a.x * b.y + a.y * b.x
    )

def vecFromPolar(x:float):
    return glm.vec2(
        glm.cos(x),
        glm.sin(x)
    )


def sortBySimilarity(s:str,l:typing.Iterable[str]):
    m = difflib.SequenceMatcher(False,'',s)
    def rank(other:str):
        m.set_seq1(other)
        return m.ratio()
    return sorted(l,key=rank,reverse=True)