from .ActionTrigger import ActionTrigger

class ActionTriggerOnLeave(ActionTrigger):
    def onTriggerLeave(self, gameObject, other, game):
        if other.name == 'Player':
            self.action_b.Run(gameObject,game)
    
    