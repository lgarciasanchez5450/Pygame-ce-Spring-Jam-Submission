import os
import random
from GameConstants import BG_CHUNK_SIZE
from pygame import Surface
from pygame import image


r_inst = random.Random()
stars = []
def loadStars():
    return stars.append(Surface((0,0)))
    for name in os.listdir('./Images/Stars'):
        fqn = os.path.join('./Images/Stars',name)
        try:
            stars.append(image.load(fqn).convert_alpha())
        except:pass
    assert stars
def generate(x:int,y:int) -> Surface:
    surf = Surface((BG_CHUNK_SIZE,BG_CHUNK_SIZE))
    s = [(x-1,y-1),
        (x+0,y-1),
        (x+1,y-1),
        (x-1,y+0),
        (x+0,y+0),
        (x+1,y+0),
        (x-1,y+1),
        (x+0,y+1),
        (x+1,y+1)
    ]
    if not stars:loadStars()
    for cpos in s:
        for star_x,star_y,star_index in get_stars(*cpos,20):
            star_surf= stars[star_index%len(stars)]
            surf.blit(star_surf,(star_x+(cpos[0]-x)*BG_CHUNK_SIZE,star_y+(cpos[1]-y)*BG_CHUNK_SIZE))
    return surf

def get_stars(x:int,y:int,stars:int) -> list[tuple[int,int,int]]:
    r_inst.seed(hash((x,y)))
    return [(r_inst.randint(0,BG_CHUNK_SIZE-1),r_inst.randint(0,BG_CHUNK_SIZE-1),r_inst.randint(0,10)) for i in range(stars)]

