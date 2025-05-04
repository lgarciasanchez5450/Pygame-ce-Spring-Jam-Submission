import Async
import physics
import GameStorage
from pyglm import glm
from .Action import *
from Particle import Particle
from Entities.Entity import Entity
from pygame import transform,Surface,locals

class DumpBehaviour(Action):
    def __init__(self, name, *,open_anim,close_anim, next = None):
        super().__init__(name, next=next)
        self.open_anim = open_anim
        self.close_anim= close_anim
        self.stage = 0
        self.particles:list[tuple[Particle,Surface,Async.Timer]] = []

    
    def start(self, gameObject:EntityType, game:GameType):
        self.open_anim = self.FindAction(gameObject,Action,self.open_anim)
        self.close_anim = self.FindAction(gameObject,Action,self.close_anim)
        self.collider = gameObject.colliders[0]

    def Run(self, gameObject, game, *args):
        self.running = True
        self.open_anim.Run(gameObject,game)
        self.stage = 0

    def update(self, gameObject:EntityType, map, dt, game:GameType):
        if not self.running: return
        if self.stage == 0:
            if not self.open_anim.running:
                self.timer = Async.Timer(2,game)
                self.timer.start()
                self.stage = 1
                # ents = list(physics.get_contained(self.collider.rect,map,layers=0b111))
                game.asyncCtx.StartCoroutine(self.eatAsync(game))
        elif self.stage == 1:
            if self.timer.isDone():
                self.stage = 2
                self.close_anim.Run(gameObject,game)
            else:
                timer = Async.Timer(3,game)
                timer.start()
                for ent in physics.get_contained(self.collider.rect,map,layers=0b111):
                    if ent is gameObject: continue
                    GameStorage.scrap_collected_today += 1
                    GameStorage.scrap_collected_total += 1
                    ent.dead = True
                    particle = Particle(glm.vec2(ent.pos),glm.vec2(ent.vel),ent.surf)
                    self.particles.append((particle,ent.surf,timer))
                    game.spawnParticle(particle)

        elif self.stage == 2:
            if not self.close_anim.running:
                self.running = False


    def eatAsync(self,game:GameType):
        while self.stage == 1:
            for particle,original_surf,timer in self.particles:
                t = timer.getTimePassed() 
                m = 1/(2*t*t+1)
                new_size = (glm.vec2(original_surf.get_size()) * m).to_tuple()
                particle.setSurf(transform.smoothscale(original_surf,new_size))
                particle.surf.fill((255*m,255*m,255*m),special_flags=locals.BLEND_MULT)
                particle.vel -= particle.vel * game.dt
                if glm.min(new_size) < 2 or glm.max(new_size) < 3 or int(255 * m) == 0:
                    particle.dead = True            
            yield
        
        for particle,_,_ in self.particles:
            particle.dead = True
        self.particles.clear()
        yield

            
