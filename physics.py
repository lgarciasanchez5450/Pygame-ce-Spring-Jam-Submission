
import GameConstants
from pyglm import glm
from pygame import Rect
from pygame import Mask
from gametypes import *
from Colliders.MaskCollider import MaskCollider
import Utils as utils
import debug


class CollisionInfo:
    mask:Mask
    center_of_collision:glm.vec2
    set_bits:int
    __slots__ = 'mask','center_of_collision','set_bits'

class PhysicsState:
    collisions:dict[frozenset,CollisionInfo]
    triggers:set[frozenset[EntityType]]

    __slots__ = 'collisions','triggers'
    def __init__(self,collisions:dict[frozenset[EntityType],CollisionInfo],triggers:set[frozenset[EntityType]]):
        self.collisions = collisions
        self.triggers = triggers

    @classmethod
    def new(cls):
        return cls({},set())

@debug.Profile
def calc_collision_map(map:MapType,dt:float,game:GameType,lastState:PhysicsState):
    collisions:dict[frozenset,CollisionInfo] = {}
    triggers:set[frozenset[EntityType]] = set()
    for chunk in map.values():
        for collider in chunk:
            assert isinstance(collider,MaskCollider)
            _r = collider.rect
            _cr = _r.colliderect
            _w,_h = collider.mask.get_size()
            _mo = collider.mask.overlap
            _mom = collider.mask.overlap_mask
            _moa = collider.mask.overlap_area
            entity = collider.gameObject
            layers = collider.layers
            if collider.isTrigger:
                for other_collider in chunk:
                    if other_collider is collider: continue
                    if not (other_collider.layers & layers): continue
                    assert isinstance(other_collider,MaskCollider)
                    other_mask = other_collider.mask
                    other_entity = other_collider.gameObject
                    if other_entity is entity: continue
                    if _cr(other_collider.rect):
                        fs = frozenset([entity,other_entity])
                        if fs in triggers: continue
                        w,h = other_mask.get_size()
                        x = other_entity.pos.x - w//2 - (entity.pos.x - _w//2)
                        y = other_entity.pos.y - h//2 - (entity.pos.y - _h//2)
                        if _mo(other_mask,(x,y)) is not None:
                            triggers.add(fs)
            else:
                if entity.mass == float('inf'): continue
                for other_collider in chunk:
                    if other_collider is collider: continue
                    if other_collider.isTrigger: continue
                    if not (other_collider.layers & layers): continue
                    assert isinstance(other_collider,MaskCollider)
                    other_mask = other_collider.mask
                    other_entity = other_collider.gameObject
                    if other_entity is entity: continue
                    if _cr(other_collider.rect):
                        fs = frozenset([entity,other_entity])
                        if fs in collisions: continue
                        w,h = other_mask.get_size()
                        x = other_entity.pos.x - w//2 - (entity.pos.x - _w//2)
                        y = other_entity.pos.y - h//2 - (entity.pos.y - _h//2)
                        mask =_mom(other_mask,(x,y))
                        set_bits = mask.count()
                        if set_bits:
                            dx = _moa(other_mask, (x + 1, y)) - _moa(other_mask, (x - 1, y))
                            dy = _moa(other_mask, (x, y + 1)) - _moa(other_mask, (x, y - 1))
                            collision_normal = glm.vec2(dx,dy)
                            if dx != 0 or dy != 0:
                                collision_normal = glm.normalize(collision_normal)
                            info = CollisionInfo()
                            info.mask = mask
                            info.center_of_collision = glm.vec2(mask.centroid()) + _r.topleft
                            info.set_bits = set_bits
                            resolveCollision(entity,other_entity,info,collision_normal,dt)
                            entity.onCollide(other_collider,info,collision_normal)
                            other_entity.onCollide(entity,info,-collision_normal)
                            collisions[fs] = info

    for fs in triggers:
        a,b = fs
        if fs in lastState.triggers:
            a.onTriggerStay(b,game)
            b.onTriggerStay(a,game)
        else:
            a.onTriggerEnter(b,game)
            b.onTriggerEnter(a,game)
    for fs in lastState.triggers.difference(triggers):
        a,b = fs
        a.onTriggerLeave(b,game)
        b.onTriggerLeave(a,game)

    return PhysicsState(collisions,triggers)


def resolveCollision(a:EntityType,b:EntityType,info:CollisionInfo,normal:Vec2,dt:float):
    if a.mass == float('inf'):
        a,b = b,a
    Cr = a.bounciness * b.bounciness #Coefficient of Restitution [0 -> inelastic, 1 -> elastic]
    a_vel = glm.vec2(a.vel)
    b_vel = glm.vec2(b.vel)
    
    rel_vel = a_vel - b_vel
    d = glm.vec2(normal)
    dot = glm.dot(d,rel_vel)
    if dot < 0:
        d *= dot * (1 + Cr)  #type: ignore
        if b.mass == float('inf'):
            a_dv = -d
            b_dv = 0
        else:
            a_dv = -d * (b.mass / (a.mass+b.mass)) 
            b_dv = d * (a.mass / (a.mass+b.mass)) 
        a.vel += a_dv
        b.vel += b_dv
        a.pos += a_dv * dt * max(1,info.set_bits/20)
        b.pos += b_dv * dt * max(1,info.set_bits/20)
    else:
        if b.mass == float('inf'):
            a.vel += d * (1 + Cr)
        else:
            a.vel +=  d * (b.mass / (a.mass+b.mass)) * (1 + Cr)
            b.vel -=  d * (a.mass / (a.mass+b.mass)) * (1 + Cr)

    if glm.length2(normal):
        if b.mo_inertia == float('inf'):
            a_dir = a.pos - info.center_of_collision
            a_tau = utils.cross2d(a_dir,normal)
            a.rot_vel += a_tau * dt
        else:
            a_dir = a.pos - info.center_of_collision
            a_tau = utils.cross2d(a_dir,normal)
            a.rot_vel += a_tau * (b.mo_inertia / (a.mo_inertia+b.mo_inertia)) * dt

            b_dir = b.pos - info.center_of_collision
            b_tau = utils.cross2d(b_dir,-normal)
            b.rot_vel += b_tau * (a.mo_inertia / (a.mo_inertia+b.mo_inertia))  * dt
        # print('Collision Normal:',normal,)
        # print('A:')
        # print('\tname:',a.name)
        # print('\ta_dir:',a_dir)
        # print('\tmo_inertia:',a.mo_inertia)
        # print('\trot_vel:',a.rot_vel)
        # print('\tpos:',a.pos)
        # print('\trot:',a.rot)
        # print('B:')
        # print('\tname:',b.name)
        # print('\tmo_inertia:',b.mo_inertia)
        # print('\trot_vel:',b.rot_vel)
        # print('\tpos:',b.pos)
        # print('\trot:',b.rot)
    
def get_colliding(r:Rect,map:MapType,layers:int=1,collideTriggers:bool=False):
    s = set()
    _cr = r.colliderect
    for cpos in collide_chunks2d(r.left,r.top,r.right,r.bottom,GameConstants.CHUNK_SIZE):
        if cols:=map.get(cpos):
            for other in cols:
                if not (other.layers & layers): continue
                if other.isTrigger and not collideTriggers: continue
                ent = other.gameObject
                if ent not in s and _cr(other.rect):
                    s.add(ent)
                    yield ent
                    
def get_colliding_colliders(r:Rect,map:MapType,layers:int=1,collideTriggers:bool=False):
    s:set[ColliderType] = set()
    _cr = r.colliderect
    for cpos in collide_chunks2d(r.left,r.top,r.right,r.bottom,GameConstants.CHUNK_SIZE):
        if cols:=map.get(cpos):
            for other in cols:
                if not (other.layers & layers): continue
                if other.isTrigger and not collideTriggers: continue
                if other not in s and _cr(other):
                    s.add(other)
                    yield other

def get_contained(r:Rect,map:MapType,layers:int=1,collideTriggers:bool=False):
    s = set()
    _cr = r.colliderect
    _c = r.contains
    for cpos in collide_chunks2d(r.left,r.top,r.right,r.bottom,GameConstants.CHUNK_SIZE):
        if cols:=map.get(cpos):
            for other in cols:
                if not (other.layers & layers): continue
                if other.isTrigger and not collideTriggers: continue
                ent = other.gameObject
                if _cr(other.rect) and ent not in s:
                    assert isinstance(other,MaskCollider)
                    if _c(other.rect) or all(_c(rect.move(other.rect.topleft)) for rect in other.mask.get_bounding_rects()):
                        s.add(ent)
                        yield ent


def collide_chunks2d(x1:float,y1:float,x2:float,y2:float,chunk_size:int):
    cx1 = (x1 // chunk_size).__floor__()
    cy1 = (y1 // chunk_size).__floor__()
    cx2 = (x2 / chunk_size).__ceil__()
    cy2 = (y2 / chunk_size).__ceil__()
    return [(x,y) for x in range(cx1,cx2,1) for y in range(cy1,cy2,1)]


def linecast(origin:Vec2,dest:Vec2,map:MapType,subsections:int=200):
    '''This implementation is incorrect: TODO Use DDA for chunk traversal algo'''
    origin_cpos = glm.ivec2(origin // GameConstants.CHUNK_SIZE)
    dest_cpos = glm.ivec2(dest // GameConstants.CHUNK_SIZE)
    collided = set()
    if origin_cpos == dest_cpos:
        for collider in map.get(origin_cpos.to_tuple(),[]):
            ent = collider.gameObject
            if collider.rect.clipline(origin,dest) and ent not in collided:
                assert isinstance(collider,MaskCollider)
                if any(collider.mask.get_bounding_rects()):
                    collided.add(ent)
                    yield ent
    else:
        chunks_crossed = set()
        for i in range(subsections):
            i /= subsections
            p = origin * (1-i) + dest * i
            cpos = glm.ivec2(p // GameConstants.CHUNK_SIZE).to_tuple()
            if cpos in chunks_crossed: continue
            chunks_crossed.add(cpos)
            for collider in map.get(cpos,[]):
                ent = collider.gameObject
                if collider.rect.clipline(origin,dest) and ent not in collided:
                    assert isinstance(collider,MaskCollider)
                    if any(collider.mask.get_bounding_rects()):
                        collided.add(ent)
                        yield ent



def collide_line_rect(origin:Vec2,dest:Vec2,rect:Rect):
    # if not dir.x: return rect.left < origin.x < rect.right
    # if not dir.y: return rect.top < origin.y < rect.bottom
    return bool(rect.clipline(origin,dest))
    
    t_top = rect.top / dir.y
    t_bottom = rect.bottom / dir.y
    t_left = rect.left / dir.x
    t_right = rect.right / dir.x



# Initial Calculations
from pygame import Surface
from pygame import mask
def calculateMomentOfInertia(s:Surface|None,total_mass:float):
    if s is None: return total_mass
    half_size = glm.vec2(s.get_size()) / 2
    m = mask.from_surface(s,0)
    area = m.count()
    density = total_mass / area
    sum = 0
    for y in range(s.get_height()):
        for x in range(s.get_width()):
            dist = (glm.vec2(x,y) - half_size) / 10
            sum += glm.dot(dist,dist)   
    
    return sum * density
    