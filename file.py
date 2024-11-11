import pygame
from pygame.locals import * #for event MOUSE variables
import os
import RPi.GPIO as GPIO
import time
import subprocess
from collections import deque


time_lim = 300
start_time=time.time()

run_flag=True
GPIO.setmode(GPIO.BCM)   # Set for GPIO (bcm) numbering not pin numbers...
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)

GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(26, GPIO.IN, pull_up_down=GPIO.PUD_UP)


def quit_callback(channel):
    global run_flag
    run_flag=False
GPIO.add_event_detect(17,GPIO.FALLING, callback=quit_callback, bouncetime=300)

def timestamp():
    global start_time
    return int(time.time()-start_time)

os.putenv('SDL_VIDEODRIVER', 'fbcon') # Display on piTFT
os.putenv('SDL_FBDEV', '/dev/fb1')
os.putenv('SDL_MOUSEDRV', 'TSLIB') # Track mouse clicks on PiTFT
os.putenv('SDL_MOUSEDEV', '/dev/input/touchscreen')

pygame.init()
pygame.mouse.set_visible(False)
WHITE=255,255,255
BLACK=0,0,0
RED = 255,0,0
GREEN = 0,255,0
screen=pygame.display.set_mode((320,240))

my_font=pygame.font.Font(None,25)
my_buttons={'quit':(300,220), 'stop':(160,120)}
quit_size=20
stop_center=160,120
stop_radius=40
stop_flag=False
left_history=60,50
left_entries_loc=[(60,120),(60,150),(60,180)]
left_deque=deque(['Stop    0','Stop    0','Stop    0'])
right_history=250,50
right_entries_loc=[(250,120),(250,150),(250,180)]
right_deque=deque(['Stop    0','Stop    0','Stop    0'])
#'Stop    '
#'CW      '
#'CCW     '
screen.fill(BLACK)
pygame.draw.circle(screen,RED,stop_center,stop_radius)
text="STOP"
text_surface=my_font.render(text, True,WHITE)
rect=text_surface.get_rect(center=(160, 120))
screen.blit(text_surface, rect)
text='Left History'
text_surface=my_font.render(text, True,WHITE)
rect=text_surface.get_rect(center=left_history)
screen.blit(text_surface, rect)
for i in range(3):
    text=left_deque[i]
    text_surface=my_font.render(text, True,WHITE)
    rect=text_surface.get_rect(center=left_entries_loc[i])
    screen.blit(text_surface, rect)

text='Right History'
text_surface=my_font.render(text, True,WHITE)
rect=text_surface.get_rect(center=right_history)
screen.blit(text_surface, rect)
for i in range(3):
    text=right_deque[i]
    text_surface=my_font.render(text, True,WHITE)
    rect=text_surface.get_rect(center=right_entries_loc[i])
    screen.blit(text_surface, rect)
    


# Motor A
GPIO.setup(5, GPIO.OUT) # In1
GPIO.setup(6, GPIO.OUT) # In2
GPIO.setup(13, GPIO.OUT) # PWM

GPIO.output(5, GPIO.LOW)
GPIO.output(6, GPIO.LOW)
pwmA = GPIO.PWM(13,50)
pwmA.start(0)

# Motor B
GPIO.setup(20, GPIO.OUT) # In1
GPIO.setup(21, GPIO.OUT) # In2
GPIO.setup(16, GPIO.OUT) # PWM

GPIO.output(20, GPIO.LOW)
GPIO.output(21, GPIO.LOW)
pwmB = GPIO.PWM(16,50)
pwmB.start(0)



def left_stop():
    GPIO.output(5, GPIO.LOW)
    GPIO.output(6, GPIO.LOW)


def left_clockwise(dc,freq=50):
    GPIO.output(5, GPIO.HIGH)
    GPIO.output(6, GPIO.LOW)
    # pwmA.ChangeFrequency(freq)
    pwmA.ChangeDutyCycle(dc)

def left_counterclockwise(dc,freq=50):
    GPIO.output(5, GPIO.LOW)
    GPIO.output(6, GPIO.HIGH)
    # pwmA.ChangeFrequency(freq)
    pwmA.ChangeDutyCycle(dc)


def right_stop():
    GPIO.output(20, GPIO.LOW)
    GPIO.output(21, GPIO.LOW)


def right_clockwise(dc,freq=50):
    GPIO.output(20, GPIO.HIGH)
    GPIO.output(21, GPIO.LOW)
    pwmB.ChangeDutyCycle(dc)

def right_counterclockwise(dc,freq=50):
    GPIO.output(20, GPIO.LOW)
    GPIO.output(21, GPIO.HIGH)
    pwmB.ChangeDutyCycle(dc)
    
left_flag=False
right_flag=False

def left_clockwise_callback(channel):
    global left_flag
    left_flag=not left_flag
    if left_flag:
        left_clockwise(50)
        left_deque.appendleft('CW      '+str(timestamp()))
    else:
        left_stop()
        left_deque.appendleft('Stop    '+str(timestamp()))
        
GPIO.add_event_detect(22,GPIO.FALLING, callback=left_clockwise_callback, bouncetime=300)

def left_counterclockwise_callback(channel):
    global left_flag
    left_flag=not left_flag
    if left_flag:
        left_counterclockwise(50)
        left_deque.appendleft('CCW     '+str(timestamp()))
    else:
        left_stop()
        left_deque.appendleft('Stop    '+str(timestamp()))
GPIO.add_event_detect(23,GPIO.FALLING, callback=left_counterclockwise_callback, bouncetime=300)

def right_clockwise_callback(channel):
    global right_flag
    right_flag=not right_flag
    if right_flag:
        right_clockwise(50)
        right_deque.appendleft('CW      '+str(timestamp()))
    else:
        right_stop()
        right_deque.appendleft('Stop    '+str(timestamp()))
GPIO.add_event_detect(26,GPIO.FALLING, callback=right_clockwise_callback, bouncetime=300)

def right_counterclockwise_callback(channel):
    global right_flag
    right_flag=not right_flag
    if right_flag:
        right_counterclockwise(50)
        right_deque.appendleft('CCW     '+str(timestamp()))
    else:
        right_stop()
        right_deque.appendleft('Stop    '+str(timestamp()))
GPIO.add_event_detect(27,GPIO.FALLING, callback=right_counterclockwise_callback, bouncetime=300)


    
while run_flag:
    time.sleep(0.01)
    for event in pygame.event.get():
        if(event.type is MOUSEBUTTONDOWN):
            pos=pygame.mouse.get_pos()
        elif(event.type is MOUSEBUTTONUP):
            pos=pygame.mouse.get_pos()
            print(pos)

            x,y=pos
            if my_buttons['quit'][0]-quit_size<=x<=my_buttons['quit'][0]+quit_size and my_buttons['quit'][1]-quit_size<=y<=my_buttons['quit'][1]+quit_size:
                run_flag=False
            if my_buttons['stop'][0]-stop_radius<=x<=my_buttons['stop'][0]+stop_radius and my_buttons['stop'][1]-stop_radius<=y<=my_buttons['stop'][1]+stop_radius:
                stop_flag=not stop_flag
    if run_flag:
        screen.fill(BLACK)
        if stop_flag:
            # stop both wheels
            left_flag=False
            right_flag=False
            left_stop()
            right_stop()
            # draw Resume btn
            pygame.draw.circle(screen,GREEN,stop_center,stop_radius)
            text="Resume"
            text_surface=my_font.render(text, True,WHITE)
            rect=text_surface.get_rect(center=(160, 120))
            screen.blit(text_surface, rect)
        else:
            # draw STOP btn
            pygame.draw.circle(screen,RED,stop_center,stop_radius)
            text="STOP"
            text_surface=my_font.render(text, True,WHITE)
            rect=text_surface.get_rect(center=(160, 120))
            screen.blit(text_surface, rect)
        text="Quit"
        text_surface=my_font.render(text, True,WHITE)
        rect=text_surface.get_rect(center=my_buttons['quit'])
        screen.blit(text_surface, rect)
        text='Left History'
        text_surface=my_font.render(text, True,WHITE)
        rect=text_surface.get_rect(center=left_history)
        screen.blit(text_surface, rect)
        for i in range(3):
            text=left_deque[i]
            text_surface=my_font.render(text, True,WHITE)
            rect=text_surface.get_rect(center=left_entries_loc[i])
            screen.blit(text_surface, rect)
        
        text='Right History'
        text_surface=my_font.render(text, True,WHITE)
        rect=text_surface.get_rect(center=right_history)
        screen.blit(text_surface, rect)
        for i in range(3):
            text=right_deque[i]
            text_surface=my_font.render(text, True,WHITE)
            rect=text_surface.get_rect(center=right_entries_loc[i])
            screen.blit(text_surface, rect)
            
    pygame.display.flip()


pygame.quit()

