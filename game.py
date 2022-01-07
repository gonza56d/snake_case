from enum import Enum
from time import sleep

from pynput import keyboard

from scenario import Scenario, Facing
from utils import GameOverException


class State(Enum):
    RUNNING = 'Running'
    PAUSE = 'Pause'
    FINISHED = 'Finished'


class Game:

    def on_press(self, key):
        if ((key == keyboard.Key.up
                and self.scenario.snake.facing == Facing.DOWN)
            or (key == keyboard.Key.down
                and self.scenario.snake.facing == Facing.UP)
            or (key == keyboard.Key.left
                and self.scenario.snake.facing == Facing.RIGHT)
            or (key == keyboard.Key.right
                and self.scenario.snake.facing == Facing.LEFT)):
            return
        if key == keyboard.Key.up:
            self.scenario.snake.facing = Facing.UP
        elif key == keyboard.Key.down:
            self.scenario.snake.facing = Facing.DOWN
        elif key == keyboard.Key.left:
            self.scenario.snake.facing = Facing.LEFT
        elif key == keyboard.Key.right:
            self.scenario.snake.facing = Facing.RIGHT

    def __init__(self):
        self.scenario = Scenario()
        self.state = State.RUNNING
        self.score = 0
        listener = keyboard.Listener(on_press=self.on_press)
        listener.start()
        self.run()

    def run(self):
        while self.state == State.RUNNING:
            try:
                sleep(1.0 / self.scenario.speed)
                self.scenario.next_frame()
                self.score = len(self.scenario.snake.body_at) * 125
            except GameOverException:
                self.state = State.FINISHED
                print('\n\n\nGAME OVER!!!\n\nThe snake crashed x.x\n\n'
                      f'Score achieved: {self.score}\n\n')


Game()
