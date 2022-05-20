from collections import namedtuple
from datetime import datetime
import enum
import multiprocessing as mp
import random
import time


class C(enum.Enum):
    Green = "\u001b[32m"
    Magenta = "\u001b[35m"
    Yellow = "\u001b[33m"
    Cyan = "\u001b[36m"
    Blue = "\u001b[34m"
    Red = "\u001b[31m"
    White = "\u001b[37m"
    Reset = "\u001b[0m"
    # Black = "\u001b[30m"
class Chopstick():
    
    def semaforo():
        return mp.Semaphore()

class Philosopher():
    

    def __init__(self, name, color: C, right_chopstick: Chopstick, left_chopstick: Chopstick):
        self.name = name
        self.color = color
        self.right_chopstick = right_chopstick
        self.left_chopstick = left_chopstick
        self.eating_time = random.randint(2, 5)
        self.thinking_time = random.randint(2, 5)

    def think(self):
        self.log(f"START Thinking for {self.thinking_time} seconds")
        time.sleep(self.thinking_time)
        self.log("END   Thinking")

    def _acquire_chopsticks(self) -> bool:
        # TODO: Wait for right chopstick.
        x = self.right_chopstick.acquire(block=True)
        print(self.right_chopstick, x)
        # TODO: Get the left chopstick or release the right one.
        y = self.left_chopstick.acquire()
        print(self.left_chopstick, y)
        if x and y:
            return True
        else:
            self.right_chopstick.release()
            return False

       
        

    def _release_chopsticks(self):
        self.log("Releasing chopsticks")
        # TODO: Release both chopsticks.
        self.right_chopstick.release()
        self.left_chopstick.release()
        self.log("Released chopsticks")

    def eat(self):
        while not self._acquire_chopsticks():
            self.waiting()
            time.sleep(1)

        self.log(f"START Eating for {self.eating_time} seconds")
        time.sleep(self.eating_time)
        self.log("END   Eating")

        self._release_chopsticks()

    def waiting(self):
        self.log("START Waiting")
        time.sleep(1)  # Everyone waits the same.
        self.log("END   Waiting")

    def run(self):
        while True:
            self.think()
            self.eat()

    def log(self, msg):
        print(f"{self.color.value}{datetime.utcnow().isoformat(sep=' ', timespec='microseconds')}|{self.name}|{msg}{C.Reset.value}")

    
    

# TODO: Define Chopstick type (like Semaphore or BoundedSemaphore).
# https://docs.python.org/3/library/multiprocessing.html#multiprocessing.Semaphore
# https://docs.python.org/3/library/multiprocessing.html#multiprocessing.BoundedSemaphore


if __name__ == '__main__':
    print("START OF PROGRAM")

    c1 = Chopstick.semaforo()
    c2 = Chopstick.semaforo()

    phil1 = Philosopher("P1", C.Green, right_chopstick=c1, left_chopstick=c2)
    # TODO: start phil1.
    proc1 = mp.Process(target = phil1.run)
     
    
    phil2 = Philosopher("P2", C.Magenta, right_chopstick=c2, left_chopstick=c1)
    # TODO: start phil2.
    proc2 = mp.Process(target = phil2.run)
    proc2.start()
    proc1.start()
    
    # TODO: wait for all to finish.
    proc1.join()
    proc2.join()
    

    print("END OF PROGRAM")