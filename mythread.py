from giantwin32 import *
import threading
import time
class myThread (threading.Thread):
    def __init__(self, threadID, name, counter,steer_value,current):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
        self.steer_value = steer_value
        if steer_value<10:#Too less for any input
            self.should_steer=False
        else:
            self.should_steer=True
        self.delay = (64-steer_value)/100.0
        self.current = current

    def run(self):
        print "Starting " + self.name

        while True:
            if self.should_steer:
                if self.steer_value>60:
                    pressAndHold(self.current)
                else:
                    release('left_arrow','right_arrow')
                    press(self.current)
                threading.Event().wait(self.delay)
        print "Exiting " + self.name
        
    def updateSteer(self,steer_value,current):
        release('left_arrow','right_arrow')
        if steer_value<5:#Too less for any input
            self.should_steer=False
        else:
            self.should_steer=True
#        print self.steer_value,self.current,self.delay,self.should_steer            
        self.steer_value = steer_value
        self.delay = (64-steer_value)/64.0
        self.current = current
        
if __name__=="__main__":
    thread1 = myThread(1, "Thread-1", 1,15,'a')
    thread1.start()
    time.sleep(5)
    thread1.updateSteer(50,'b')
    time.sleep(5)
    thread1.updateSteer(5,'c')
    time.sleep(5)
    thread1.updateSteer(20,'p')
    '''
    Please kill the thread from task manager (if you can, sorry)
    '''
