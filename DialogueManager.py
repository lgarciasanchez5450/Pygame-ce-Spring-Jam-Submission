from Utils import TextRenderer
from pygame.font import Font
from pygame import Surface

class DialogueState:
    canceled:bool
    running:bool
    done:bool
    time_running:float
    def __init__(self):
        self.canceled = False
        self.running = False
        self.done = False
        self.time_running = 0

class DialogueManager:
    current_dialogue:None|str
    current_speed:float
    _cached_text_surf:Surface
    def __init__(self):
        self.current_dialogue = None
        self._renderer = TextRenderer(Font('./font/Pixeltype.ttf',40),'white')
        self.last_chars = None
        self.current_state = DialogueState()
        

    def setCurrentDialogue(self,dialogue:None|tuple[str,int]):
        if not dialogue:
            self.current_dialogue = None
        else:
            self.current_dialogue,self.current_speed = dialogue
        if not self.current_state.done:
            self.current_state.canceled = True
            self.current_state.running = False
        next_state = DialogueState()
        next_state.running = True
        self.current_state = next_state
        return next_state

    def getText(self,dt:float):
        state = self.current_state
        if self.current_dialogue is None: return 
        if state.canceled: return
        if state.running:
            state.time_running += dt
        if state.done:
            chars = len(self.current_dialogue)
        else:
            chars = min(int(state.time_running * self.current_speed),len(self.current_dialogue))
            
        if chars != self.last_chars:
            text = self.current_dialogue[:chars]
            self._cached_text_surf = self._renderer.render_align(text)
            if chars == len(self.current_dialogue):
                state.done = True
                state.running = False

        return self._cached_text_surf

        