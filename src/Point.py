class Point():
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    def __eq__(self, other) -> None:
        if isinstance(other, Point):
            if (self.x == other.x) and (self.y == other.y):
                return True
        return False