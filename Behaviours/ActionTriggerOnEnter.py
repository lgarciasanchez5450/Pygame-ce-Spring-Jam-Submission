from .ActionTrigger import ActionTrigger

class ActionTriggerOnEnter(ActionTrigger):
    def onTriggerEnter(self, gameObject, other, game):
        if other.name == 'Player':
            self.action_b.Run(gameObject,game)