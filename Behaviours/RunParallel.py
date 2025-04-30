from .Action import Action

class RunParallel(Action):
    def __init__(self, name,actions:list[str]):
        super().__init__(name)
        self.actions = actions

    def Run(self, gameObject, game, *args):
        x = 0
        for action in gameObject.getBehaviours(Action):
            if action.name in self.actions:
                action.Run(gameObject,game)
                x += 1
        if x == 0:
            raise LookupError('RunParallel Could not find actions: {}'.format(repr(self.actions)))