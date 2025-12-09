import pyxel

class Truck:
    def __init__(self, x, y):
        # position of the truck on the screen
        self.x = x
        self.y = y
        # some private attributes that are used only inside the class
        self.__max_rows = 1
        self.__max_columns = 2

        self.__package_width = 15
        self.__package_height = 10

        # Establish the position of the packages in the truck.
        self.package_positions = []
        for row in range(self.__max_rows):
            for col in range(self.__max_columns):
                px = self.x+35 + col * self.__package_width
                py = self.y+12 - row * self.__package_height
                self.package_positions.append((px, py))

        self.packages_on_truck = []
        self.is_full = False

        # delivery timer
        self.delivery_timer = 0
        self.DELIVERY_DURATION = 120  # the duration of the pause. 4 seconds at 30 FPS

        # If the truck is visible
        self.visible = True

    @property
    def x(self):
        return self.__x

    @x.setter
    def x(self, value):
        if not isinstance(value, int):
            raise TypeError("X must be an integer.")
        if value < 0:
            raise ValueError("X cannot be negative.")

        self.__x = value

    @property
    def y(self):
        return self.__y

    @y.setter
    def y(self, value):
        if not isinstance(value, int):
            raise TypeError("Y must be an integer.")
        if value < 0:
            raise ValueError("Y cannot be negative.")
        self.__y = value

    # this method only add packages to the list, for us know how many packages are in the truck
    def add_package(self):
        if len(self.packages_on_truck) < len(self.package_positions):
            #the index of the package is related to the index of the position in the truck
            self.packages_on_truck.append(len(self.packages_on_truck))

        # also it checks if the truck is full. If it is, it sets the truck to visible
        if len(self.packages_on_truck) >= len(self.package_positions):
            self.is_full = True


    def update(self):
        if self.is_full:
            self.delivery_timer += 1

            #truck disappears after 60 frames amount of time
            if self.delivery_timer == 60:
                self.visible = False
                self.packages_on_truck = []

            # truck returns empty after the delivery duration
            if self.delivery_timer >= self.DELIVERY_DURATION:
                self.is_full = False
                self.delivery_timer = 0
                self.visible = True  # only the truck is visible

    # this method draws packages on the truck, by the index of the package in the list
    def draw_packages(self):
        if self.visible:
            for index in range(len(self.packages_on_truck)):
                px, py = self.package_positions[index]
                pyxel.blt(px, py, 0, 0, 117, self.__package_width, self.__package_height, 0)
    # draws the truck
    def draw(self):
        if self.visible:
            pyxel.blt(self.x, self.y, 2, 178, 122, 70, 38, 0)