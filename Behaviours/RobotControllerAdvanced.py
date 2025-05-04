import math
import Utils
import physics
from GameConstants import TWO_PI,PI,PI_OVER_TWO
from pyglm import glm
from gametypes import *
from Behaviours.Behaviour import Behaviour
from . RobotController import RobotController


class Path:
    def __init__(self,position:Vec2):
        self.pos = position


    def pathfindTo(self,destination:Vec2,map:MapType,ignore:set[EntityType],_built:list['Path'] = [],i:int=10) -> list['Path']:
        if not i: return
        dif = destination - self.pos
        target_angle = math.atan2(dif.y,dif.x)
        if glm.length(dif) < 20:
            return _built
        # v = glm.normalize(dif)
        walk_dist = 10
        if not _built:
            _built.append(self)
        for ent in physics.linecast(self.pos,destination,map,20):
            if ent in ignore: continue
            break
        else:
            return _built + [Path(destination)]

        for i2 in Utils.walkOutWards(8):
            angle = target_angle + i2*TWO_PI / 8
            new_pos = self.pos + walk_dist * glm.vec2(glm.cos(angle),glm.sin(angle))
            for ent in physics.linecast(self.pos,new_pos,map,20):
                if ent in ignore: continue
                break
            else:
                new_path = Path(new_pos)
                try:
                    if path:= new_path.pathfindTo(destination,map,ignore,_built+[new_path],i-1):
                        return path
                except RecursionError:
                    return 
                

class PathNode:
    m = 0.5
    __slots__ = 'pos','children','parent','dr','dd','best_child_value'
    def __init__(self,pos:Vec2):
        self.pos = pos
        self.children:list[PathNode] = []
        self.dr:float = 0
        self.dd:float = 0
        self.best_child_value = float('inf')
        self.parent = None

    def dfs_iter(self):
        yield self
        for child in self.children:
            yield from child.dfs_iter()

    def __repr__(self):
        return f'PathNode[{self.pos}]'
    
    def poshash(self):
        return glm.ivec2(self.pos//1).to_tuple()


    def value(self): return self.dd + self.dr + len(self.children)
import heapq
import random
from collections import deque
def explore(root:PathNode,destination:Vec2,map:MapType,heatmap:dict):
    # root.dd = glm.distance(root.pos,destination)
    bests = [root]
    cur = root
    while cur.children:
        best_child = min(cur.children,key=lambda x:x.best_child_value)
        bests.append(best_child)
        cur = best_child
    cur = min(bests,key=lambda x: x.value())
    step_size= 20
    if cur.dd < step_size:
        step_size = cur.dd/2
    if step_size < 0.1:
        return
    fails = 0
    while True:
        theta = random.random() * TWO_PI
        rel_pos = glm.vec2(glm.cos(theta),glm.sin(theta)) * step_size
        child = PathNode(cur.pos + rel_pos)
        ch = child.poshash()
        if ch in heatmap:
            fails += 1
            if fails > 5:
                if cur.parent:
                    cur = cur.parent
            continue
        else:
            pass
        if any(math.isinf(ent.mass) for ent in physics.linecast(cur.pos,child.pos,map,5)):
            continue#retry
        child.parent = cur
        child.dr = cur.dr + step_size
        child.dd = glm.distance(child.pos,destination)
        child.best_child_value = child.value()
        cur.children.append(child)
        break
    while cur and cur.best_child_value > child.best_child_value:
        cur.best_child_value = child.best_child_value
        child = cur
        cur = cur.parent
    

class RobotControllerAdvanced(RobotController):
    def __init__(self):
        super().__init__()
        self.target_pos = None
        self.path = None
        self.root:PathNode
        self.walking = False
        self.heatmap = {}
    
    def start(self, gameObject, game):
        super().start(gameObject, game)
        game.asyncCtx.StartCoroutine(self.drawPath(gameObject,game))

    def setTarget(self,target_pos:Vec2):
        self.target_pos = target_pos
        self.heatmap = {}
        self.path = None

    def startWalk(self):
        # assert self.path is not None
        self.walking = True

    def update(self, gameObject:EntityType, map, dt:float, game:GameType):
        super().update(gameObject,map,dt,game)

        if self.target_pos is not None and self.path is None:
            self.root = PathNode(gameObject.pos)
            self.root.dd = glm.distance(self.root.pos,self.target_pos)
            for _ in range(500):#we do a little bit of thinking
                explore(self.root,self.target_pos,map,self.heatmap)
            self.path = self.root
            
        if self.walking:
            for _ in range(5):
                explore(self.path,self.target_pos,map,self.heatmap)
            subgoal = self.path
            dist2 = glm.distance2(subgoal.pos,gameObject.pos)
            if dist2 > 20*20:
                self.Move(1*(subgoal.pos - gameObject.pos)/glm.sqrt(dist2))
            else:
                if self.path.children:
                    self.path = min(self.path.children,key=lambda x:x.best_child_value)
                else:
                    print('stop walking')
                    self.walking = False

    def drawPath(self,gameObject:EntityType,game:GameType):
        import pygame
        screen = game.window.get_surface()
        while True:
            offset = glm.vec2(screen.get_size())//2 - game.camera_pos
            if self.path:
                cur = self.path
                queue = [cur]
                while queue:
                    cur = queue.pop(0)
                    for child in cur.children:
                        pygame.draw.line(screen,'red',cur.pos+offset,child.pos+offset)
                        queue.append(child)
                # line = [self.path]
                cur = self.path
                while cur.children:
                    best_child = min(cur.children,key=lambda x:x.best_child_value)
                    pygame.draw.line(screen,'blue',cur.pos+offset,best_child.pos+offset,width=2)
                    cur = best_child
                    continue
                pygame.draw.circle(screen,'blue',gameObject.pos+ offset,3)
                pygame.draw.circle(screen,'blue',self.target_pos+ offset,3)


            yield
            



    