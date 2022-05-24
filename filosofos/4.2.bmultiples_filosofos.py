from collections import namedtuple
from datetime import datetime
import enum
import multiprocessing as mp
import random
import time


Chopstick = namedtuple("Chopstick", "semaforo name")  # * crear un objeto tipo chopstick


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


class Philosopher:
    def __init__(
        self, name, color: C, right_chopstick: Chopstick, left_chopstick: Chopstick
    ):
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
        x = self.right_chopstick.semaforo.acquire()
        self.log(f"right chpstick {self.right_chopstick.name} {x}")
        # TODO: Get the left chopstick or release the right one.
        y = self.left_chopstick.semaforo.acquire()
        self.log(f"left chopstick {self.left_chopstick.name} , {y}")
        if x and y:  # * si se asignaron los dos palillos retorna True
            return True

    def _release_chopsticks(self):
        self.log("Releasing chopsticks")
        # TODO: Release both chopsticks.
        self.right_chopstick.semaforo.release()
        self.log(f"Releasing {self.right_chopstick.name}")
        self.left_chopstick.semaforo.release()
        self.log(f"Releasing {self.left_chopstick.name}")
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
        print(
            f"{self.color.value}{datetime.utcnow().isoformat(sep=' ', timespec='microseconds')}|{self.name}|{msg}{C.Reset.value}"
        )


if __name__ == "__main__":
    print("START OF PROGRAM")

    n = int(input("ingresa un numero: \n"))

    Chopsticks = [Chopstick(mp.Semaphore(), f"chopstick {i}") for i in range(n)]

    filosofos = []

    for i in range(n):
        r = i
        if (
            i == len(Chopsticks) - 1
        ):  # * evalua si el palillo izquierdo es el ultimo de la lista, y lo toma como el primero
            l = 0
        else:
            l = i + 1  # * si no le asigna el siguiente
            print(f"left {l}, right {r}")
        phil = Philosopher(
            f"P{i+1}",
            list(C)[i],
            right_chopstick=Chopsticks[r],
            left_chopstick=Chopsticks[l],
        )
        proc = mp.Process(target=phil.run)
        filosofos.append(proc)
        proc.start()

    for i in filosofos:
        i.join()

    print("END OF PROGRAM")
