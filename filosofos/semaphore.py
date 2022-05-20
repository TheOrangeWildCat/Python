from multiprocessing import Process, Semaphore
import random
import time


def think(tTime):
    time.sleep(tTime)

def eat(eTime):
    time.sleep(eTime)


def diningPhil(phil,ch1,ch2,rand):
    print(ch1,ch2)
    # Start the philosopher
    print(phil, " is starting")                                 
    # Get random time for Thinking
    thinkTime = random.randint(0,rand)                             
    # Get random time for eating
    eatTime = random.randint(1,rand+1)
    #get wait time
    waitTime = random.randint(1, 5)
    # Think for random amount of time
    print(phil, " is thinking ", thinkTime, " seconds")
    think(thinkTime)
    # Ask for first chopstick
    print(phil, " is asking for chopstick 1")
    st1 = ch1.acquire(block=True, timeout=waitTime)                                                
    print(phil, " got chopstick 1", ch1)
    print(ch1,ch2)
    think(1)
    # Ask for second chopstick
    print(phil, " is asking for chopstick 2")                 
    st2 = ch2.acquire(block=True, timeout= waitTime-1)                                               
    print(phil, " got chopstick 2", ch2)
    # Once the philosopher has both chopsticks, eat
    print(ch1, ch2)
    if st1 and st2:
        print(phil, " is eating ", eatTime, " seconds")
        eat(eatTime)
    else:
        print(phil, " is not eating ")
    # When finished eating, releast both chopsticks
    print(phil, " is releasing chopsticks")
    if st1:
        ch1.release()                                               
    if st2:
        ch2.release()

    print(phil," is finished")
    
# Main Program

if __name__=='__main__':
    # Create a Semaphore that we call chopstick1
    chopstick1 = Semaphore()
    # Create another Semaphore that we call chopstick2
    chopstick2 = Semaphore()                                         
    phil1 = "Aristotle"
    phil2 = "Plato"
    # Create process for philosopher Aristotle asking for chopstick1 and then chopstick2
    proc1 = Process(target = diningPhil, 
args=(phil1,chopstick1,chopstick2,0))  
    # Create process for philosopher Plato asking for chopstick2 and then chopstick1
    proc2 = Process(target = diningPhil, 
args=(phil2,chopstick2,chopstick1,0))
    # Start process 1
    proc1.start()
    # Start process 2
    proc2.start()
    # Join all processes together to end the program
    proc1.join()                                                
    proc2.join()
    print("end of program")
