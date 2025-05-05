import random
from .Action import *

class ChooseRandom(Action):
    def __init__(self, name, actions:list[str],*, next = None):
        super().__init__(name, next=next)
        self.actions = actions
    
    def Run(self, gameObject, game, *args):
        random_action_name = random.choice(self.actions)
        random_action = self.FindAction(gameObject,Action,random_action_name)
        if random_action.running: return
        random_action.Run(gameObject,game)
        self.RunNextAction(gameObject,game)
    
