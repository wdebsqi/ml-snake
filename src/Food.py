from pygame import Color
from src.Point import *
from src.config import *

class Food():
    def __init__(self, position: Point = Point(MIDDLE_X + 3 * POINT_SIZE, MIDDLE_Y + 3 * POINT_SIZE), color: Color = RED):
        self.position = position
        self.color = color