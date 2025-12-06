import pyxel

class Truck:
    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.max_rows = 4
        self.max_columns = 2

        self.package_width = 15
        self.package_height = 10

        # calcular posiciones de paquetes en el truck
        self.package_positions = []
        for row in range(self.max_rows):
            for col in range(self.max_columns):
                px = self.x+35 + col * self.package_width
                py = self.y+12 - row * self.package_height
                self.package_positions.append((px, py))

        self.packages_on_truck = []
        self.is_full = False

        # temporizador de entrega
        self.delivery_timer = 0
        self.DELIVERY_DURATION = 120  # duración de pausa en frames

        # visibilidad del camión y paquetes
        self.visible = True

    def add_package(self):
        if len(self.packages_on_truck) < len(self.package_positions):
            #the index of the package is the same as the position. The index is stored.W
            self.packages_on_truck.append(len(self.packages_on_truck))
        if len(self.packages_on_truck) >= len(self.package_positions):
            self.is_full = True
            self.visible = True

    def update(self):
        if self.is_full:
            self.delivery_timer += 1

            # camión desaparece con paquetes después de cierto tiempo
            if self.delivery_timer == 60:  # por ejemplo, a los 60 frames desaparece
                self.visible = False
                self.packages_on_truck = []

            # camión vuelve vacío después de la duración total
            if self.delivery_timer >= self.DELIVERY_DURATION:
                self.is_full = False
                self.delivery_timer = 0
                self.visible = True  # reaparece vacío

    def draw_packages(self):
        if self.visible:
            for index in range(len(self.packages_on_truck)):
                px, py = self.package_positions[index]
                pyxel.blt(px, py, 0, 0, 117, self.package_width, self.package_height, 0)

    def draw(self):
        if self.visible:
            pyxel.blt(self.x, self.y, 2, 178, 122, 70, 38, 0)