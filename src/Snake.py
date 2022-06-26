from Point import *
from config import *
from Directions import *
from Game import *
from pygame import Color
import numpy as np

class Snake():
    def __init__(self, starting_point: Point = Point(MIDDLE_X, MIDDLE_Y), color1: Color = GREEN, color2: Color = GREEN2) -> None:

        self.head = starting_point
        self.body = [
            starting_point, 
            Point((starting_point.x-POINT_SIZE), starting_point.y),
            Point((starting_point.x-(POINT_SIZE*2)), starting_point.y)
            ]
        self.color1 = color1
        self.color2 = color2
        self.direction = Directions.RIGHT

    def move(self, action: list) -> None:

        # [straight, right, left]

        clock_wise = [Directions.RIGHT, Directions.DOWN, Directions.LEFT, Directions.UP]
        idx = clock_wise.index(self.direction)

        if np.array_equal(action, [1, 0, 0]):
            new_direction = clock_wise[idx]
        elif np.array_equal(action, [0, 1, 0]):
            next_idx = (idx + 1) % 4
            new_direction = clock_wise[next_idx]
        else:
            next_idx = (idx - 1) % 4
            new_direction = clock_wise[next_idx]

        self.direction = new_direction

        x = self.head.x
        y = self.head.y

        if self.direction == Directions.RIGHT:
            x += POINT_SIZE
        elif self.direction == Directions.LEFT:
            x -= POINT_SIZE
        elif self.direction == Directions.DOWN:
            y += POINT_SIZE
        elif self.direction == Directions.UP:
            y -= POINT_SIZE

        # self.body.pop()    
        self.head = Point(x, y)

    def is_collision(self, pt=None) -> bool:
        if pt is None:
            pt = self.head

        #Hitting wall
        if (pt.x > (width - POINT_SIZE)) or (pt.x < 0) or (pt.y > (height - POINT_SIZE)) or (pt.y < 0):
            return True
        #Hitting self
        if (pt in self.body[1:]):
            return True

        return False