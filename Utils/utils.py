import math
import typing
import difflib
from pyglm import glm
type Vec2 = glm.vec2

def expDecay(a,b,decay:float,dt:float):
    return b+(a-b)*math.exp(-decay*dt)

def cross2d(a:Vec2,b:Vec2):
    return a.x*b.y-a.y*b.x

def splitList[T](l:list[T],v:T) -> tuple[list[T],...]:
    out:list[list[T]] = []
    while True:
        try:
            i = l.index(v)
        except:
            out.append(l)
            return out
        else:
            out.append(l[:i])

            l = l[i+1:]

def formatBytes(b:int):
    i = 0
    while b >= 1024:
        i += 1
        b >>= 10
    return f'{b} {['B','KiB','MiB','GiB'][i]}'

def formatTimeDebug(b:int,*,format = '.2f'):
    if b <= 0:
        return f'{b} s'
    i = 0
    while b < 1:
        i += 1
        b *= 1000
    return f'{{:{format}}} {['s','ms','µs','ns'][i]}'.format(b)

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


def safeEval(s:str):
    tokens = tokenize(s,{
        '[':None,
        ']':None,
        ' ':None,
        '(':None,
        ')':None,
        ',':None,
        "'":"'",
        '"':'"'
    })

    return parseTokens(tokens)

def evalArgs(s:str) -> tuple[tuple[typing.Any,...],dict[str,typing.Any]]:
    tokens = tokenize(s,{
        '[':None,
        ']':None,
        ' ':None,
        '(':None,
        ')':None,
        '{':None,
        '}':None,
        ':':None,
        ',':None,
        '=':None,
        "'":"'",
        '"':'"',
    })
    if len(tokens) == 2:
        if tokens[0] == '(' and tokens[1] == ')':
            return ((),{})
        else:
            raise SyntaxError(f'Unparsable Tokens: {repr(s)} -> {repr(tokens)}')
    assert len(tokens) > 2
    container = containerize(tokens,{'[':']','(':')','{':'}'})
    assert tokens[0]+tokens[-1]  == '()'
    return parseFuncArgsContainer(container)

def tokenize(s:str,seperators:dict[str,str|None]):
    def rank(c:str):
        try:
            return s.index(c)
        except:
            return len(s)
    out:list[str] = []
    skip_to:str|None = None
    
    while s:
        if skip_to:
            seperator = skip_to
            skip_to = None
        else:
            seperator = min(seperators.keys(),key=lambda s:rank(s))
            skip_to = seperators[seperator]

        index = rank(seperator)
        length = len(seperator)

        before = s[:index].strip()
        if before: out.append(before)
        token = s[index:index+length].strip()
        if token: out.append(token)
        s = s[index+length:]
    return out

type SContainerType = tuple[str,list[str|"SContainerType"]]

def containerize(tokens:list[str],containers:dict[str,str]) -> SContainerType:
    assert tokens[0] in containers
    i = 0
    def _containerize() -> SContainerType:
        nonlocal i
        typ = tokens[i]
        ending = containers[typ]
        inside_tokens:list[str|SContainerType] = []
        i += 1
        while True:
            cur_token = tokens[i]
            if cur_token == ending:
                return (typ,inside_tokens)
            elif cur_token in containers:
                inside_tokens.append(_containerize())
            else:
                inside_tokens.append(cur_token)
            i+=1
    try:
        return _containerize()                
    except Exception as err:
        err.add_note('Error containerizing token: {}'.format(tokens))
        raise
    
def prettyPrintContainers(container:SContainerType,tabs=0):
    typ,tokens = container
    print(f'{'   '*tabs}Container{typ}')
    
    for token in tokens:
        if type(token) is tuple:
            prettyPrintContainers(token,tabs+1)
        else:
            print(f'{'   '*(tabs+1)}{token}')
    print('   '*tabs,{'(':')','[':']','{':'}','<':'>'}[typ],sep='')


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
            return int(token,base=0)
        except:pass
        try:
            return float(token)
        except: pass
        if token == 'False': return False
        elif token == 'True': return True
        elif token == 'None': return None


def parseTokensNonContainer(tokens:list[str]) -> typing.Any:
    if tokens[0] == '"':
        assert tokens[-1]=='"'
        assert len(tokens) == 3
        return tokens[1]
    if tokens[0] == "'":
        assert tokens[-1]=="'"
        assert len(tokens) == 3
        return tokens[1]
    assert len(tokens) == 1
    tok = tokens[0]
    try:
        return int(tok)
    except ValueError: pass
    try:
        return float(tok)
    except ValueError: pass
    return {
        'False':False,
        'True':True,
        'None':None,
    }[tok]
def parseFuncArgsContainer(container:SContainerType) -> tuple[tuple[typing.Any],dict[str,typing.Any]]:
    def containerToValue(container:SContainerType) -> typing.Any:
        typ,tokens = container
        if typ == '{': #dictionary
            if not tokens:
                return {}
            out:dict[typing.Any,typing.Any] = {}
            values = splitList(tokens,',')
            for v in values:
                key,value = splitList(v,':')
                key = parseTokensNonContainer(key)
                if len(value) == 1 and type(value[0]) is tuple:
                    value = containerToValue(value[0])
                else:
                    value:str
                    value = parseTokensNonContainer(value)
                out[key] = value

            return out
        elif typ == '(':
            out:list[typing.Any] = []
            if not tokens:
                return tuple()
            values = splitList(tokens,',')
            for v in values:
                if not v: continue
                if len(v)==1 and type(v[0]) is tuple:
                    v = containerToValue(v[0])
                else:
                    v = parseTokensNonContainer(v)
                out.append(v)
            return tuple(out)
        elif typ == '[':
            if not tokens:
                return []
            out:list[typing.Any] = []
            values = splitList(tokens,',')
            for v in values:
                if not v: continue

                if len(v)==1 and type(v[0]) is tuple:
                    v = containerToValue(v[0])
                else:
                    v = parseTokensNonContainer(v)
                out.append(v)
            return out
        else:
            raise TypeError(f"Unknown Container Type: {typ}")
    typ,tokens = container
    assert typ == '('
    values = splitList(tokens,',')
    args:list[typing.Any] = []
    kwargs:dict[str,typing.Any] = {}
    doing_kwargs = False
    for v in values:
        if not doing_kwargs:
            if '=' in v:
                doing_kwargs = True
            else:
                if len(v)==1 and type(v[0]) is tuple:
                    value = containerToValue(v[0])
                else:
                    value = parseTokensNonContainer(v)
                args.append(value)
        if doing_kwargs:
            if '=' not in v:
                raise SyntaxError('positional argument follows keyword argument')
            key,value = splitList(v,'=')
            assert len(key)==1,f'Invalid Keyword Argument: {v}'
            key = key[0]
            assert type(key) is str
            if key in kwargs:
                raise SyntaxError(f"duplicate keyword: {key}")
            if type(value[0]) is tuple:
                value = containerToValue(value[0])
            else:
                value = parseTokensNonContainer(value)
            kwargs[key] = value
    return tuple(args),kwargs    


def angleDifference(target_angle:float,current_angle:float):
    d_rot = (target_angle - current_angle) % 6.283185307179586
    if d_rot > 3.141592653589793:
        d_rot -= 6.283185307179586
    return d_rot


def formatTime(hours:int,minutes:int,format:str='12'):
    if format == '12':
        h = hours-1
        meridian = 'AM' if hours < 12 else 'PM'
        h %= 12 
        h += 1

        return f'{h}:{minutes:0>2} {meridian}'
    elif format == '24':
        return f'{hours}:{minutes:0>2}'
    else:
        raise ValueError("Incorrect format: {}".format(format))
    

def walkOutWards(max:int):
    '''Yield the Sequence: 0, 1, -1, 2, -2, 3, -3, 4, -4, n-1, -(n-1)'''
    if max < 1:
        return
    yield 0
    i = 1
    while i < max:
        yield i
        yield -i
        i += 1
