from collections import deque
from dataclasses import dataclass
from enum import Enum
from random import randint
import os

from utils import GameOverException


class Facing(Enum):
    UP = 'Up'
    DOWN = 'Down'
    LEFT = 'Left'
    RIGHT = 'Right'


@dataclass
class Position:
    x: int
    y: int


@dataclass
class Snake:
    length: int
    head_at: Position
    body_at: deque
    facing: Facing = Facing.UP


class Scenario:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self) -> None:
        self.speed = 6
        self.height = 10
        self.width = 64
        self.snake = Snake(
            length=4,
            head_at=Position(self.width // 2, self.height // 2),
            body_at=deque([
                Position(self.width // 2, self.height // 2 - x - 1)
                for x in range(3)
            ])
        )
        self.food_at = self.set_food()
        self.display_frame()

    def check_legal_position(self):
        if (self.snake.head_at.x > self.width or self.snake.head_at.x <= 0 or
                self.snake.head_at.y > self.height or self.snake.head_at.y <= 0
                or self.snake.head_at in self.snake.body_at):
            raise GameOverException()

    def move_snake(self, direction: Facing):
        self.snake.body_at.appendleft(self.snake.head_at)
        if direction == Facing.UP:
            self.snake.head_at = Position(
                x=self.snake.head_at.x,
                y=self.snake.head_at.y + 1
            )
        elif direction == Facing.DOWN:
            self.snake.head_at = Position(
                x=self.snake.head_at.x,
                y=self.snake.head_at.y - 1
            )
        elif direction == Facing.LEFT:
            self.snake.head_at = Position(
                x=self.snake.head_at.x - 1,
                y=self.snake.head_at.y
            )
        elif direction == Facing.RIGHT:
            self.snake.head_at = Position(
                x=self.snake.head_at.x + 1,
                y=self.snake.head_at.y
            )
        if self.snake.head_at == self.food_at:
            self.food_at = self.set_food()
            self.speed += 0.5
        else:
            self.snake.body_at.pop()
        self.check_legal_position()

    def next_frame(self):
        self.move_snake(self.snake.facing)
        self.display_frame()

    def get_char_at(self, x, y) -> str:
        char = ' '
        if Position(x, y) == self.snake.head_at:
            char = 'O'
        elif Position(x, y) in self.snake.body_at:
            char = 'X'
        elif Position(x, y) == self.food_at:
            char = '#'
        return char

    def get_screen_string(self) -> str:
        string = ''.join(['_' for x in range(self.width + 2)])
        for line in range(self.height):
            string += '\n|'
            string += ''.join(
                [self.get_char_at(x, self.height - line)
                 for x in range(self.width)]
            )
            string += '|'
        string += '\n'
        string += ''.join(['_' for x in range(self.width + 2)])
        return string

    def clean_terminal(self):
        command = 'clear'
        if os.name in ['nt', 'dos']:
            command = 'cls'
        os.system(command)

    def display_frame(self):
        self.clean_terminal()
        print(self.get_screen_string())

    def set_food(self) -> Position:
        ball_position = None
        while ball_position is None or ball_position == self.snake.head_at \
                or ball_position in self.snake.body_at:
            x = randint(1, self.width)
            y = randint(1, self.height)
            ball_position = Position(x, y)
        return ball_position
