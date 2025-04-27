def ease_in(t:float):
    return t*t

def ease_out(t:float):
    return 1-(t-1)*(t-1)

def smoothstep(t:float):
    tt = t*t
    return 3*tt - 2*tt*t 

def ease_out_circ(t:float):
    return ease_out(t)**0.5

def ease_in_circ(t:float):
    return 1-(1-t*t)**0.5

