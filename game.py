import sys
import gui
import time
import Input
import Utils
import debug
import Async
import pygame
import random
import physics

from EntityTags import *
from GameConstants import * 

from pygame import Window
from Particle import Particle
from Entities.Entity import Entity
from GameManager import GameManager


class Game:
    def __init__(self,window:Window):
        self.background = {}
        self.entities:list[Entity] = []
        self.particles:list[Particle] = []
        self.clock = pygame.time.Clock()
        self.window = window
        self.half_screen_size = glm.vec2(window.size) / 2

        self.camera_pos = glm.vec2()

        self.dt = 0
        self.frame = 0
        self.to_spawn:list[Entity] = []
        self.asyncCtx = Async.Context()

    def spawnEntity(self,entity:Entity):
        if entity.dirty:
            entity.clean()
            entity.dirty = False
        self.to_spawn.append(entity)


    def spawnEntities(self, entities:list[Entity]):
        for entity in entities:
            if entity.dirty:
                entity.clean()
                entity.dirty = False
        self.to_spawn.extend(entities)

    def spawnParticle(self,particle:Particle):
        self.particles.append(particle)

    def toWorldCoords(self,screen_cords:glm.vec2|tuple[int,int]):
        return screen_cords + self.camera_pos - self.half_screen_size
    
    def run(self):
        if __debug__:
            f3_mode = False
            dbg_font = pygame.font.SysFont('Arial',18)
        self.game_manager = GameManager(self,self.window)
        self.game_manager.start_game()
        self.screen_rect = pygame.Rect(0,0,self.window.size[0],self.window.size[1])
        screen = self.window.get_surface()
        physics_last_state = physics.PhysicsState.new()
        while True:
            if __debug__:
                if debug.Profile.active:
                    debug.Profile.active = False
            t_start = time.perf_counter()
            self.time = time.perf_counter()
            Input._update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    code = int(event.dict.get('code',0))
                    sys.exit(code)
                if event.type == pygame.KEYDOWN: #TODO move some of this logic to player class and 
                    if event.key == pygame.K_ESCAPE:
                        sys.exit(0)
                    if __debug__:
                        if event.key == pygame.K_F3:
                            f3_mode = not f3_mode
                        if event.key == pygame.K_F4:
                            print('#########')
                            debug.Profile.active = True
                     
            self.game_manager.pre_update()
            self.entities.extend(self.to_spawn)
            for ent in self.to_spawn:
                ent.start(self)
            self.to_spawn.clear()
            map = build_map_better(self.entities)
            ### Update All Entities ###
            if __debug__ and debug.Profile.active:
                t_a = time.perf_counter()
            for e in self.entities:
                e.update(map, self.dt, self)
            self.game_manager.update()
            if __debug__ and debug.Profile.active:
                t_b = time.perf_counter()
            self.game_manager.post_update(map)
            if __debug__ and debug.Profile.active:
                t_c = time.perf_counter()
            for e in self.entities:
                if e.dirty:
                    e.clean()
                    e.dirty = False
            if __debug__ and debug.Profile.active:
                t_d = time.perf_counter()
            ### Calculate Collisions ###
            physics_last_state = physics.calc_collision_map(map,self.dt,self,physics_last_state)
            #remove dead entities
            for i in range(len(self.entities)-1,-1,-1):
                if self.entities[i].dead:
                    self.entities[i].onDeath(map,self.dt,self)
                    del self.entities[i]    

            ### Draw Routine ###
            if __debug__ and debug.Profile.active:
                t_e = time.perf_counter()
            self.game_manager.pre_draw()
            if __debug__ and debug.Profile.active:
                t_f = time.perf_counter()
            # Draw All Behind Entities #
            
            # Draw All Entities #
            for e in physics.get_colliding(self.screen_rect,map,layers=0b111,collideTriggers=True):
                for col in e.colliders:
                    if e.surf:
                        s = glm.vec2(e.surf.get_size())//2
                        screen.blit(e.surf,glm.floor(e.pos-s-(self.camera_pos)+self.half_screen_size))
                    if __debug__ and f3_mode:
                        olist = col.mask.outline()
                        if len(olist) > 1:
                            pygame.draw.lines(screen,(200,150,150),1,[(glm.floor(col.rect.topleft - self.camera_pos + self.half_screen_size + (x,y))) for x,y in olist])
                        pygame.draw.rect(screen,(200,150,150),col.rect.move(glm.floor(-self.camera_pos+self.half_screen_size)),1)
            for i in range(len(self.particles)-1,-1,-1):
                p = self.particles[i]
                if p.dead:
                    self.particles.pop(i)
                else:
                    screen.blit(p.surf,glm.floor(p.pos-p.offset-(self.camera_pos)+self.half_screen_size))
                    p.pos += p.vel * self.dt    

            if __debug__ and debug.Profile.active:
                t_g = time.perf_counter()
            self.game_manager.ui_draw()
            if __debug__ and debug.Profile.active:
                t_h = time.perf_counter()
            ### Update Coroutines ###
            self.asyncCtx.update(self.time,self.frame)
            t_end = time.perf_counter()
            self.window.flip()
            t_final = time.perf_counter()
            dt = self.clock.tick(120) 
            self.dt  = dt / 1000
            self.frame += 1

            if __debug__:
                if debug.Profile.active:
                    tot = t_end-t_start
                    print(f'Input+Pre Update:   {Utils.formatTimeDebug(t_a-build_map_better.last_timed-t_start,format='6.2f')} ({100*(t_a-build_map_better.last_timed-t_start)/tot:.1f}%)',)
                    print(f'Building Map:       {Utils.formatTimeDebug(build_map_better.last_timed,format='6.2f')} ({100*(build_map_better.last_timed)/tot:.1f}%)',)
                    print(f'Update Entities:    {Utils.formatTimeDebug(t_b-t_a,format='6.2f')} ({100*(t_b-t_a)/tot:.1f}%)',)
                    print(f'Post Update:        {Utils.formatTimeDebug(t_c-t_b,format='6.2f')} ({100*(t_c-t_b)/tot:.1f}%)',)
                    print(f'Cleaning:           {Utils.formatTimeDebug(t_d-t_c,format='6.2f')} ({100*(t_d-t_c)/tot:.1f}%)',)
                    print(f'Physics:            {Utils.formatTimeDebug(physics.calc_collision_map.last_timed,format='6.2f')} ({100*(physics.calc_collision_map.last_timed)/tot:.1f}%)',)
                    print(f'Pre Draw:           {Utils.formatTimeDebug(t_f-t_e,format='6.2f')} ({100*(t_f-t_e)/tot:.1f}%)',)
                    print(f'Draw:               {Utils.formatTimeDebug(t_g-t_f,format='6.2f')} ({100*(t_g-t_f)/tot:.1f}%)',)
                    print(f'UI Draw:            {Utils.formatTimeDebug(t_h-t_g,format='6.2f')} ({100*(t_h-t_g)/tot:.1f}%)',)
                    print(f'Frame Build:        {Utils.formatTimeDebug(t_end-t_start,format='6.2f')} ({100*(t_end-t_start)/tot:.1f}%)',)
                    print(f'Frame Display:      {Utils.formatTimeDebug(t_final-t_end,format='6.2f')} ({100*(t_final-t_end)/(tot+t_final-t_end):.1f}%)',)
                    print(f'Total Frame Time:   {Utils.formatTimeDebug(t_final-t_start,format='6.2f')} ({100*(t_final-t_start)/(tot+t_final-t_end):.1f}%)',)
                    print(f'Size of Global Entity Cache:',len(Entity._global_cache))

    #### Utility Functions for Behaviours ####
    def FindEntityByName(self,name:str,search_through_unspawned:bool = False):
        for e in self.entities:
            if e.name == name:
                return e
        if search_through_unspawned:
            for e in self.to_spawn:
                if e.name == name:
                    return e
    def FindEntitiesByName(self,name:str,search_through_unspawned:bool = False):
        ents:list[EntityType] = []
        for e in self.entities:
            if e.name == name:
                ents.append(e)
        if search_through_unspawned:
            for e in self.to_spawn:
                if e.name == name:
                    ents.append(e)
        return ents



if __name__ == '__main__':
    print('!!Debug Only!!')
    pygame.init()
    # win = pygame.Window('game test',(900,600))#(1920,1080))
    win = pygame.Window('game test',(1920,1080))
    game = Game(win)
    game.run()
