from .ActionTrigger import ActionTrigger

class ActionTriggerInteract(ActionTrigger):
    def __init__(self, action,collider):
        self.a = 1
        super().__init__(action)