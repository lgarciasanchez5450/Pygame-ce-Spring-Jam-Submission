from .Input import Input
from ..utils.Event import Event
from pygame import Surface,Rect
# from Utils.YoutubeParsers.types import Image
from typing import Any, Protocol, Callable, Literal, TypeAlias,Final, Generic,TypeVar,ParamSpec, Iterable,Optional,MutableSequence, Hashable,Sequence

P = ParamSpec("P")
T = TypeVar("T")

BorderDirecton:TypeAlias = Literal['top','bottom','left','right']
ColorType:TypeAlias = tuple[int,int,int] | tuple[int,int,int,int]
EventHook = Callable[[],None|Any]
EventHookAny = Callable[[],Any]
EventHookInt = Callable[[int],Any]

class SupportsResize(Protocol):
  def onResize(self,size:tuple[int,int]): ...

class SupportsUpdate(Protocol):
  def update(self,input:Input): ...
  
class SupportsDraw(Protocol):
  order_in_layer:int
  def draw(self,surf:Surface): ...

class SupportsQuit(Protocol):
  def onQuit(self): ...

class HasRect(Protocol):
  @property
  def rect(self) -> Rect:...
  order_in_layer:int
  def draw(self,surf:Surface): ...

class HasFullRect(Protocol):
  @property
  def rect(self) -> Rect:...
  @rect.setter
  def rect(self,rect): ...
  order_in_layer:int
  def draw(self,surf:Surface): ...

class SupportsAll(SupportsUpdate,HasRect,Protocol): ...

class SelectionLike(Protocol):
  @property
  def fullHeight(self) -> int: ...
  size_change_event:Event
  max_y:int
  rect:Rect
  order_in_layer:int
  def getScrollPercent(self) -> float: ... 
  def setScrollPercent(self,percent:float): ...
  def setYScroll(self,y:int): ...
  def update(self,input:Input): ...
  def draw(self,surf:Surface): ...


class SelectionProtocol(Protocol):
  pos:tuple[int,int]
  rect:Rect
  def setYOffset(self,y:int): ...
  def getYOffSet(self) -> int: ...
  def setToUp(self): ...
  def update(self,input:Input): ...
  def draw(self,surf:Surface): ...

class Runnable(Protocol):
  def run(self): ...
  def stop(self): ...

class WrapperObject(Protocol):
  def get(self): ...
  def set(self,value): ...

# class ItunesResult:
#   title:str
#   album:str
#   artist:str
#   thumbnail:Image
#   duration:int
#   release_date:str
#   explicit:bool
#   genre:str
#   __slots__ = 'title','album','artist','thumbnail','duration','release_date','explicit','genre'
#   def __repr__(self) -> str:
#       return f'ItunesSong[{self.title}, {self.artist}, {self.album}]'


UIElement = TypeVar('UIElement',SupportsDraw,SupportsUpdate)
