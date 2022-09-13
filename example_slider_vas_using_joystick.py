from psychopy import visual, event, core, data
from psychopy.visual.slider import Slider
from psychopy.visual.window import Window

import pygame

#initialise window
myscreen = {}
myscreen['hight'] = 1000
myscreen['width'] = 1000
#win   = visual.Window([myscreen['width'],myscreen['hight']], fullscr=False, units='pix', color=(1,1,1))
win = visual.Window( [1920, 1080], fullscr = False, monitor="testMonitor", units="deg", color=(1, 1, 1), useFBO=False)

#function to reverse text
def reverse(text):
    return reverse(text[1:]) + text[0]


#initialise vas slider
vas = Slider(win,
             ticks=(1, 100),
             labels=('אל ללכ', 'בר בשק'),
             granularity=0,
             color='black',
             fillColor='black',
             borderColor='black',
             startValue=50, 
             labelHeight=None,
             size=(20,1.5))

#initialise pygame joystick 
pygame.init() 
myjoystick = pygame.joystick.Joystick(0)
myjoystick.init()

#initial flip of slide
question = visual.TextStim(win, ('הלטמל תובישקו זוכירה תגרד המ'),color=(-1, -1, -1), colorSpace='rgb',pos=(0,100))

vas.draw()
question.draw()
win.flip()
x=50
while True:
                    events = pygame.event.poll()
                    #check joystick input
                    
                    # get joysticks axes
                    x=x+myjoystick.get_axis(4)
                    if (x>100): x=100
                    if (x<1): x=1
                    #print circles according to the joystick, adjusted with the screen size    
                    print(x)       
                    vas.markerPos=(x)
                    vas.draw()
                    question.draw()
                    win.flip()
                    #check to see if the button 'A' in the controller was pressed to stop the program    
                    if(events.type == pygame.JOYBUTTONDOWN):
                        if(events.button == 0):
                            coordinates = x
                            vas.markerPos=(x)
                            question.draw()
                            vas.draw()
                            win.update()
                            core.wait(1)
                            break
