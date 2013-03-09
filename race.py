import pygame
import pygame.midi
from pygame.locals import *
from giantwin32 import *
from mythread import myThread
import time
pygame.init()

pygame.fastevent.init()
event_get = pygame.fastevent.get
event_post = pygame.fastevent.post

pygame.midi.init()
input_id = pygame.midi.get_default_input_id()
i = pygame.midi.Input( input_id )

pygame.display.set_caption("midi test")
screen = pygame.display.set_mode((400, 300), RESIZABLE, 32)

print "starting"

going = True

def diff(val):
        return abs(64-val)

def getCurrent(val):
        if val<64:
                return "left_arrow"
        else:
                return "right_arrow"

t = myThread(1, "Thread", 1,0,'center')
t.start()
while going:
        
        val=64            # value from pitch bender
        current="center"    # left,right,center
        
        events = event_get()
        for e in events:
                if e.type in [QUIT]:
                        going = False
                if e.type in [KEYDOWN]:
                        going = False

        if i.poll():
                midi_events = i.read(10)
                if int(midi_events[0][0][0]) in [224,225,226]:#Pitch Bender
                        newval = int(midi_events[0][0][2])
                        if val!=newval:
                                val=newval
                                t.updateSteer(diff(val),getCurrent(val))                               

                #print "full midi_events " + str(midi_events)
                    #print "my midi note is " + str(midi_events[0][0][1])
                # convert them into pygame events.
                midi_evs = pygame.midi.midis2events(midi_events, i.device_id)

                for m_e in midi_evs:
                        event_post( m_e )

print "exit button clicked."
i.close()
pygame.midi.quit()
pygame.quit()
exit()
"""
reads num_events midi events from the buffer.
Input.read(num_events): return midi_event_list
Reads from the Input buffer and gives back midi events. [[[status,data1,data2,data3],timestamp],

 [[status,data1,data2,data3],timestamp],...]
"""
