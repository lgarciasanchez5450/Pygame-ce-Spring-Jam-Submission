from Utils import TextRenderer
from pygame.font import Font
from pygame import Surface
class DialogueManager:
    current_dialogue:None|str
    current_speed:float
    _cached_text_surf:Surface
    def __init__(self):
        self.current_dialogue = None
        self._renderer = TextRenderer(Font('./font/Pixeltype.ttf',40),'white')
        self.last_chars = None
        

    def setCurrentDialogue(self,dialogue:None|tuple[str,int],time:float):
        if not dialogue:
            self.current_dialogue = None
        else:
            self.current_dialogue,self.current_speed = dialogue
        self.time = time

    def getText(self,time:float):
        if self.current_dialogue is None: return 
        t = time - self.time
        chars = min(int(t * self.current_speed),len(self.current_dialogue))
        if chars != self.last_chars:
            text = self.current_dialogue[:chars]
            self._cached_text_surf = self._renderer.render_align(text)
        return self._cached_text_surf

        