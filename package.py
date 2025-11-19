class Package:
    def __init__(self, x: int, y: int, conveyor_index: int):
        self.x = x
        self.y = y
        self.conveyor_index = conveyor_index  # Which conveyor it's on

    @property
    def x(self) -> int:
        return self.__x

    @x.setter
    def x(self, value: int):
        if not isinstance(value, int):
            raise TypeError("Position x must be an integer")
        self.__x = value

    @property
    def y(self) -> int:
        return self.__y

    @y.setter
    def y(self, value: int):
        if not isinstance(value, int):
            raise TypeError("Position y must be an integer")
        self.__y = value

    @property
    def conveyor_index(self) -> int:
        return self.__conveyor_index

    @conveyor_index.setter
    def conveyor_index(self, value: int):
        if not isinstance(value, int):
            raise TypeError("Conveyor index must be an integer")
        elif value < 0:
            raise ValueError("Conveyor index cannot be negative")
        else:
            self.__conveyor_index = value
            # When a package moves to a new conveyor,
            # its x/y position should be updated here