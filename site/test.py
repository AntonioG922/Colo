from time import sleep

conv_dist = 0

DPS = 5/200

def move_conveyor(final_pos):
    global conv_dist
    delay = 0.005/5
    print(final_pos)
    while conv_dist < final_pos:
        sleep(delay)
        sleep(delay)
        conv_dist+=DPS
        print(conv_dist)
    return