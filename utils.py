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


S_NUM = 0
S_STR1 = 1
S_STR2 = 2
S_LST = 3
S_TPL = 4
S_NUL = 5
def safeEval(s:str):

    separators = list(' [](),\'"')
    def rank(c:str):
        try:
            return s.index(c)
        except:
            return len(s)
    tokens:list[str] = []
    skip_to = None

    while s:
        if skip_to:
            index = rank(skip_to)
            skip_to = False
        else:
            index = min(map(rank,separators))
        before = s[:index].strip()
        if before: tokens.append(before)
        token = s[index:index+1].strip()
        if token == '"':
            skip_to = '"'
        elif token == "'":
            skip_to = "'"
        if token: tokens.append(token)
        s = s[index+1:]
    
    return parseTokens(tokens)
        
def parseTokens(tokens:list[str]) -> typing.Any:
    if tokens[0] == '"':
        assert tokens[-1]=='"'
        assert len(tokens) == 3
        return tokens[1]
    if tokens[0] == "'":
        assert tokens[-1]=="'"
        assert len(tokens) == 3
        return tokens[1]
    if tokens[0] == '(':
        assert tokens[-1] == ')'
        inner_ = tokens[1:-1]
        if not inner_:
            return tuple()
        s = 0
        inner:list[list[str]] = []
        sub:list[str] = []
        for token in inner_:
            if token == '(' or token == '[': s += 1
            if token == ')' or token == ']': s -= 1
            if s == 0 and token == ',':
                inner.append(sub)
                sub = []
            else:
                sub.append(token)
        if sub:
            inner.append(sub)
            return tuple([parseTokens(t) for t in inner])
    elif tokens[0] == '[':
        assert tokens[-1] == ']'
        inner_ = tokens[1:-1]
        s = 0
        inner:list[list[str]] = []
        sub:list[str] = []
        for token in inner_:
            if token == '(' or token == '[': s += 1
            if token == ')' or token == ']': s -= 1
            if s == 0 and token == ',':
                inner.append(sub)
                sub = []
            else:
                sub.append(token)
        if sub:
            inner.append(sub)

        return [parseTokens(t) for t in inner]
    else:
        token = tokens[0]
        try:
            return int(token)
        except:pass
        try:
            return float(token)
        except: pass
        if token == 'False': return False
        elif token == 'True': return True
        elif token == 'None': return None
        

        elif token.startswith('"'):
            assert token.endswith('"')
            return token[1:-1]

        elif token.startswith('\''):
            assert token.endswith('\'')
            return token[1:-1]

