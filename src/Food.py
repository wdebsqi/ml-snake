from pygame import Color
from Point import *
from config import *

class Food():
    def __init__(self, position: Point = Point(MIDDLE_X + 3 * POINT_SIZE, MIDDLE_Y + 3 * POINT_SIZE), color: Color = RED) -> None:
        self.position = position
        self.color = color