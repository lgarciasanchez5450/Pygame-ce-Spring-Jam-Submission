'''This class is for game input not to be confused with the GUI library input class'''
from pygame.constants import *
from pygame import key
_kp:key.ScancodeWrapper
_kd:key.ScancodeWrapper
_kr:key.ScancodeWrapper

def _update():
    global _kp,_kd,_kr
    _kp = key.get_pressed()
    _kd = key.get_just_pressed()
    _kr = key.get_just_released()


def getKeyPressed(key:int):
    global _kp
    return _kp[key]

def getKeyJustPressed(key:int):

    global _kd
    return _kd[key]

def getKeyJustReleased(key:int):
    global _kr
    return _kr[key]


