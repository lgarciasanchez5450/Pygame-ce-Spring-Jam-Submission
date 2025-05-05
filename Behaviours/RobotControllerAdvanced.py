import math
import Utils
import physics
from pyglm import glm
from pygame import Rect
from gametypes import *
from Behaviours.Behaviour import Behaviour
from . RobotController import RobotController
from Colliders.MaskCollider import MaskCollider


def calc_path(pos:Vec2,rad:float,dest:Vec2,obstacles:list[Rect]):
    pos = glm.vec2(pos)
    dest = glm.vec2(dest)

    def isValidLine(a:Vec2|tuple,b:Vec2|tuple):
        return not any(bo.clipline(a,b) for bo in inflated)
    def isValidPoint(a:tuple[int,int],/):
        return Rect(a[0],a[1],1,1).collidelist(inflated) == -1
    
    inflated = [b.inflate(2*rad,2*rad) for b in obstacles]
    corners:list[glm.vec2] = []
    for b in inflated:
        for point in [glm.vec2(b.topleft)-1, glm.vec2(b.topright)+glm.vec2(1,-1), b.bottomleft+glm.vec2(-1,1), glm.vec2(b.bottomright)+1]:
            if isValidPoint(point):
                corners.append(point)
    for box in inflated:
        while box.collidepoint(pos) or box.collidepoint(dest):
            box.inflate_ip(-2,-2)

    dist_to_dest_cache = {}
    valid_line_to_dest_cache = {}

    best_path:list[Vec2] = []
    best_path_length = float('inf')
    i = 25
    def explore(pos:Vec2,path:list[glm.vec2],length_so_far:int):
        nonlocal best_path,best_path_length,i
        i-= 1
        if not i:
            i = 25
            yield best_path
        if (distance_to_dest:=dist_to_dest_cache.get(pos)) is None:
            dist_to_dest_cache[pos] = distance_to_dest = glm.distance(pos,dest)
        if distance_to_dest + length_so_far >= best_path_length: return 
        if (_isValidLine:=valid_line_to_dest_cache.get(pos)) is None:
            valid_line_to_dest_cache[pos] = _isValidLine = isValidLine(pos,dest)
        if _isValidLine:
            best_path = path + [pos,dest]
            # assert length_so_far + distance_to_dest < best_path_length
            best_path_length = length_so_far + distance_to_dest
        else:
            for point in corners:
                if point == pos: continue
                if point in path: continue
                if not isValidLine(pos,point): continue
                dist = glm.distance(pos,point)
                yield from explore(point,path + [pos],length_so_far+dist)
    yield from explore(pos,[],0)
    return best_path


class RobotControllerAdvanced(RobotController):
    def __init__(self):
        super().__init__()
        self.target_pos = None
        self.path = None
        self.path_gen = None
        self.walking = False
        self.holding_object = None
        self.holding_object_colliders = []
        self.holding_object_dist = 0
    
    def start(self, gameObject, game):
        super().start(gameObject, game)
        # game.asyncCtx.StartCoroutine(self.drawPath(gameObject,game))
        self.radius = max(max(c.rect.w,c.rect.h) for c in gameObject.colliders if not c.isTrigger)/2

    def releaseObject(self,gameObject:EntityType,game:GameType):
        assert self.holding_object is not None
        obj = self.holding_object
        gameObject.mass -= obj.mass * 5
        gameObject.mo_inertia -= 10 * obj.mass
        obj.colliders = self.holding_object_colliders
        self.holding_object_colliders = []
        obj.clean()
        self.holding_object = None


    def grabObject(self,gameObject:EntityType,grab:EntityType,game:GameType):
        assert self.holding_object is None
        self.holding_object = grab
        gameObject.mass += grab.mass * 5
        gameObject.mo_inertia += 10*grab.mass
        self.holding_object_colliders = grab.colliders
        grab.colliders = []
        standin = MaskCollider(True,0b10,0)
        standin.gameObject = grab
        grab.colliders.append(standin)
        self.holding_object_dist = glm.distance(gameObject.pos,grab.pos)
        grab.clean()


    def setTarget(self,target_pos:Vec2):
        self.target_pos = target_pos
        self.heatmap = {}
        self.path = None
        self.path_gen = None

    def startWalk(self):
        #this will mean it will start walking when the path is full done being loaded
        self.walking = True
    def update(self, gameObject:EntityType, map:MapType, dt:float, game:GameType):
        super().update(gameObject,map,dt,game)
        
        if self.target_pos is not None and self.path is None:

            # size =glm.abs(self.target_pos - gameObject.pos)
            # r = Rect(glm.min(gameObject.pos,self.target_pos),size)  
            # r.union_ip(radrect)
            # r = Rect(0,0,1000,1000)

            colliders:set[ColliderType] = set()
            for cpos in map:
                for collider in map.get(cpos,[]):
                    if collider.isTrigger: continue
                    if not (collider.layers & 0b11): continue
                    if math.isinf(collider.gameObject.mass):
                        colliders.add(collider)
            colliders = [c for c in colliders]
            self.path_gen =calc_path(gameObject.pos,self.radius,self.target_pos,[c.rect for c in colliders])
            try:
                for _ in range(2):#we do a little bit of thinking
                    next(self.path_gen)
            except StopIteration as stop:
                self.path:list[glm.vec2] = stop.value
                self.path_gen = None
                        
        if self.path_gen:
            try:
                next(self.path_gen)
            except StopIteration as stop:
                self.path:list[glm.vec2] = stop.value
                self.path_gen = None
        if self.walking:
            if not self.path: return
            subgoal = self.path[0]
            dist2 = glm.distance2(subgoal,gameObject.pos)
            if dist2 > 20*20:
                self.Move(1*(subgoal - gameObject.pos)/glm.sqrt(dist2))
            else:
                self.path.pop(0)
                if not self.path:
                    self.walking = False
                    self.Move(glm.vec2())
        if self.holding_object is not None:
            self.holding_object.rot = rot = gameObject.rot
            self.holding_object.dirty = True
            self.holding_object.pos = gameObject.pos + glm.vec2(glm.cos(-rot),glm.sin(-rot)) * self.holding_object_dist


    def drawPath(self,gameObject:EntityType,game:GameType):
        import pygame
        screen = game.window.get_surface()
        while True:
            offset = glm.vec2(screen.get_size())//2 - game.camera_pos
            if self.path:
                if len(self.path)> 2:
                    pygame.draw.lines(screen,'blue',False,[point + offset for point in self.path],width=2)
                for point in self.path:
                    pygame.draw.circle(screen,'red',point+offset,2)
                pygame.draw.circle(screen,'blue',gameObject.pos+ offset,3)
                if self.target_pos:
                    pygame.draw.circle(screen,'blue',self.target_pos+ offset,3)
            yield
            



    