import pyxel



class Truck:
    # Truck holds packages visually
    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.max_rows = 4
        self.max_columns = 2

        self.package_width = 15
        self.package_height = 10

        # calculate package positions inside truck
        self.package_positions = []
        for row in range(self.max_rows):
            for col in range(self.max_columns):
                px = self.x + 35 + col * self.package_width
                py = self.y + 12 - row * self.package_height
                self.package_positions.append((px, py))

        self.packages_on_truck = []
        self.is_full = False

        # delivery timer
        self.delivery_timer = 0
        self.DELIVERY_DURATION = 120

        # visibility
        self.visible = True

    # ---------------- properties ----------------
    @property
    def x(self) -> int:
        return self.__x

    @x.setter
    def x(self, val: int):
        if not isinstance(val, int):
            raise TypeError("x must be int")
        self.__x = val

    @property
    def y(self) -> int:
        return self.__y

    @y.setter
    def y(self, val: int):
        if not isinstance(val, int):
            raise TypeError("y must be int")
        self.__y = val

    @property
    def packages_on_truck(self) -> list[int]:
        return self.__packages_on_truck

    @packages_on_truck.setter
    def packages_on_truck(self, val):
        if not isinstance(val, list):
            raise TypeError("packages_on_truck must be a list")
        self.__packages_on_truck = val

    @property
    def is_full(self) -> bool:
        return self.__is_full

    @is_full.setter
    def is_full(self, val: bool):
        if not isinstance(val, bool):
            raise TypeError("is_full must be bool")
        self.__is_full = val

    @property
    def visible(self) -> bool:
        return self.__visible

    @visible.setter
    def visible(self, val: bool):
        if not isinstance(val, bool):
            raise TypeError("visible must be bool")
        self.__visible = val

    @property
    def delivery_timer(self) -> int:
        return self.__delivery_timer

    @delivery_timer.setter
    def delivery_timer(self, val: int):
        if not isinstance(val, int):
            raise TypeError("delivery_timer must be int")
        if val < 0:
            raise ValueError("delivery_timer cannot be negative")
        self.__delivery_timer = val

    # ---------------- behavior ----------------
    def add_package(self):
        """Add a package index visually; mark truck full when all positions are occupied."""
        if len(self.packages_on_truck) < len(self.package_positions):
            self.packages_on_truck.append(len(self.packages_on_truck))
        if len(self.packages_on_truck) >= len(self.package_positions):
            self.is_full = True
            self.visible = True

    def update(self):
        """Manage the delivery timer and show or hide the truck when needed."""
        if self.is_full:
            self.delivery_timer += 1

            # truck hides with packages after a short delay
            if self.delivery_timer == 60:
                self.visible = False
                self.packages_on_truck = []

            # truck returns empty after full delivery duration
            if self.delivery_timer >= self.DELIVERY_DURATION:
                self.is_full = False
                self.delivery_timer = 0
                self.visible = True

    def draw_packages(self):
        """Draw packages inside truck when visible."""
        if self.visible:
            for index in range(len(self.packages_on_truck)):
                px, py = self.package_positions[index]
                pyxel.blt(px, py, 0, 0, 117, self.package_width, self.package_height, 0)

    def draw(self):
        """Draw the truck (when visible)."""
        if self.visible:
            pyxel.blt(self.x, self.y, 2, 178, 122, 70, 38, 0)
