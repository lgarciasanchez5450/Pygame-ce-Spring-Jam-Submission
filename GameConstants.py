import debug
import pygame
from pyglm import glm
from gametypes import *

PI = 3.1415926535897932384626
TWO_PI = 2*3.1415926535897932384626
PI_OVER_TWO = 3.1415926535897932384626 / 2
RAD_TO_DEG = 180 / 3.1415926535897932384626
DEG_TO_RAD =  3.1415926535897932384626 / 180


NULL_SURF = pygame.Surface((0,0))


CHUNK_SIZE = 800
BG_CHUNK_SIZE = 800

SCENE_FOLDER = './Scenes'

# def build_map(entities:list[EntityType]):
#     #first hash everything
#     map:MapType = {}
#     for ent in entities:
#         assert type(ent.pos) is glm.vec2, f'Ship:{ent}'
#         cpos = glm.ivec2(ent.pos // CHUNK_SIZE).to_tuple()
#         if cpos not in map:
#             map[cpos] = [ent]
#         else:
#             map[cpos].append(ent)
#     return map




@debug.Profile
def build_map_better(entities:list[EntityType]):
    '''
    Build a map of chunks where each chunk is a list of entities that are in that chunk.
    Keep in mind that entities may be in multiple chunks at once, depending on their size and position.
    '''
    #first hash everything
    map:MapType = {}
    for ent in entities:
        for col in ent.colliders:
            r = col.rect
            cx1 = (r.left // CHUNK_SIZE).__floor__()
            cy1 = (r.top // CHUNK_SIZE).__floor__()
            cx2 = (r.right / CHUNK_SIZE).__ceil__()
            cy2 = (r.bottom / CHUNK_SIZE).__ceil__()
            for y in range(cy1,cy2,1):
                for x in range(cx1,cx2,1):
                    cpos = x,y
                    if cpos not in map:
                        map[cpos] = [col]
                    else:
                        map[cpos].append(col)
        # else:
        #     cpos = ent.pos.x//CHUNK_SIZE,ent.pos.y//CHUNK_SIZE
        #     if cpos not in map:
        #         map[cpos] = [ent]
        #     else:
        #         map[cpos].append(ent)
    return map



    

