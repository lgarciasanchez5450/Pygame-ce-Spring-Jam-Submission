from .ActionTrigger import *
import Loader
import Input

class ActionTriggerInteract(ActionTrigger):
    __slots__ = 'entity','offset'
    def __init__(self, action,offset = (0,0)):
        super().__init__(action)
        self.entity = Loader.loadEntity('interact_notifier.prefab')
        self.entity.dead = True
        self.offset = tuple(offset)

    def update(self, gameObject, map, dt, game):
        if not self.entity.dead:
            self.entity.pos = gameObject.pos + self.offset
            if Input.getKeyJustReleased(Input.K_DOWN):
                if not self.action_b.running:
                    self.action_b.Run(gameObject,game)

    def onTriggerEnter(self, gameObject, other, game:GameType):
        self.entity.dead = False
        game.spawnEntity(self.entity)

    def onTriggerLeave(self, gameObject, other, game):
        self.entity.dead = True