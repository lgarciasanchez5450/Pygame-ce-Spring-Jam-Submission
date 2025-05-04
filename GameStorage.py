import pygame



scrap_collected_today:int = 0
scrap_collected_total:int = 0
death_messsage:str|None = None
death_font:pygame.font.Font
current_hour:int
current_minute:int



def init():
    global death_font,current_hour,current_minute
    assert pygame.get_init() is True, 'Pygame must be Initialized to call this function'
    death_font = pygame.font.SysFont('Arial',40,True)
    current_hour = 13
    current_minute = 0

