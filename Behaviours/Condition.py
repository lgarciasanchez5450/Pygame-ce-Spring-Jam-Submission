import Utils
import typing
from .Action import *
import GameStorage

def quickdirty_parse(s:str,/,globals:dict[str,typing.Any]):
    if '||' in s:
        all_ = s.split('||')
        return any(quickdirty_parse(s,globals) for s in all_)
    if '&&' in s:
        all_ = s.split('&&')
        return all(quickdirty_parse(s,globals) for s in all_)
    if '<=' in s:
        a,b = s.split('<=',1)
        return quickdirty_parse(a,globals) <= quickdirty_parse(b,globals)
    if '>=' in s:
        a,b = s.split('>=',1)
        return quickdirty_parse(a,globals) >= quickdirty_parse(b,globals)
    if '<' in s:
        a,b = s.split('<',1)
        return quickdirty_parse(a,globals) < quickdirty_parse(b,globals)
    if '>' in s:
        a,b = s.split('>',1)
        return quickdirty_parse(a,globals) > quickdirty_parse(b,globals)
    if '==' in s:
        a,b = s.split('==',1)
        return quickdirty_parse(a,globals) == quickdirty_parse(b,globals)
    if '+' in s:
        a,b = s.split('+',1)
        return quickdirty_parse(a,globals)+ quickdirty_parse(b,globals)
    if '-' in s:
        a,b = s.split('-',1)
        return quickdirty_parse(a,globals)-quickdirty_parse(b,globals)
    s = s.strip()
    if s in globals:
        return globals[s]
    else:
        try:
            return Utils.safeEval(s)
        except:
            raise SyntaxError(f'Unable to Parse: {s}')


class Condition(Action):
    def __init__(self,name:str,conditionals:dict[str,str],*,short_circuit:bool=True,next:str|None=None):
        super().__init__(name,next=next)
        self.conditionals = conditionals
        self.short_circuit = short_circuit
        
    def Run(self,gameObject:EntityType,game:EntityType,*args):
        for condition,associated_action in self.conditionals.items():
            value =quickdirty_parse(condition,GameStorage.__dict__)
            if value:
                action =self.FindAction(gameObject,Action,associated_action)
                if not action.running:
                    action.Run(gameObject,game)
                if self.short_circuit:
                    break


