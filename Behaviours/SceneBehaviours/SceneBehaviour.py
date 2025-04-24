from gametypes import *
class SceneBehaviour:
    _subclasses_:dict[str,'SceneBehaviour'] = {}
    def __init_subclass__(cls):
        name = cls.__name__
        if name in SceneBehaviour._subclasses_:
            raise NameError(f'Behaviour {cls} conflicts with another. Maybe two behaviours have the same name? (<- this cannot happen)')
        SceneBehaviour._subclasses_[name] = cls
        
    def start(self,scene:SceneType,game:GameType): ...
    def update(self,scene:SceneType,game:GameType): ... 
    def preDraw(self,scene:SceneType,game:GameType): ...
