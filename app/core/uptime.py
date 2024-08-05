import time 

UPTIME=time.time()

def reset_uptime():
    global UPTIME
    UPTIME=time.time()
    return UPTIME

def get_uptime():
    global UPTIME
    return UPTIME

