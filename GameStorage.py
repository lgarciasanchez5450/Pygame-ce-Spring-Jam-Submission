import pygame



user_input_index = -1


scrap_collected_today:int = 0
scrap_collected_total:int = 0
death_messsage:str|None = None
death_font:pygame.font.Font
current_hour:int
current_minute:int
found_spatial:bool
boss_favorability:int
told_player_quota:bool
told_player_how_to_play_safe:bool


def init():
    global death_font,current_hour,current_minute,found_spatial,boss_favorability,told_player_quota,told_player_how_to_play_safe
    assert pygame.get_init() is True, 'Pygame must be Initialized to call this function'
    death_font = pygame.font.SysFont('Arial',40,True)
    current_hour = 13
    current_minute = 0
    found_spatial = False
    told_player_quota = False
    boss_favorability = 0
    told_player_how_to_play_safe = False