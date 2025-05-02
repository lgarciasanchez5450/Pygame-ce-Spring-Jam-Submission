from .Action import *
import Async
import physics
from Entities.Entity import Entity

class DumpBehaviour(Action):
    def __init__(self, name, *,open_anim,close_anim, next = None):
        super().__init__(name, next=next)
        self.open_anim = open_anim
        self.close_anim= close_anim
        self.stage = 0

    
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
                self.timer = Async.Timer(0.5,game)
                self.timer.start()
                self.stage = 1
                ents = list(physics.get_contained(self.collider.rect,map,layers=0b111))
                game.asyncCtx.StartCoroutine(self.eatAsync(ents,game))


        elif self.stage == 1:
            if self.timer.isDone():
                self.stage = 2
                self.close_anim.Run(gameObject,game)
        elif self.stage == 2:
            if not self.close_anim.running:
                self.running = False


    def eatAsync(self,entities:list[EntityType],game:GameType):
        t = game.time
        for entity in entities:
            entity.dead = True
        
        game.spawnEntities()
        
            
