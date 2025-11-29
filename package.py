import pyxel


class Package:
    def __init__(self, conveyor_y_position: list, start_floor: int = 0):
        # conveyor_y_position: is a list of the y positions of the conveyors
        # start_floor - initial conveyor. Options (0-4)
        self.conveyor_y_position = conveyor_y_position

        self._conveyor_index = start_floor

        # Визначаємо Y (безпечно беремо зі списку)
        #y position of the package (current conveyor hight)
        if self._conveyor_index < len(self.conveyor_y_position):
            self._y = self.conveyor_y_position[self._conveyor_index]
        else:
            self._y = 0

        # --- НАПРЯМОК І СТАРТ X ---
        # Парні (0, 2, 4) -> ВПРАВО. Непарні (1, 3) -> ВЛІВО.
        if self._conveyor_index % 2 == 0:
            self._direction = 1 #rigth
            self._x = 180  # Зліва (біля труби)
        else:
            self._direction = -1 #left
            self._x = 280  # Справа (підлаштуй під ширину свого екрану 386)

        self.active = True
        self.state = 'moving'  # 'moving', 'falling'
        self.speed = 1.5

        # --- СИСТЕМА КАДРІВ (6 ШТУК) ---
        # Тут треба вписати координати для всіх 6 стадій торта:
        # (u, v, w, h)
        # after the biggest dimensions that the packages can have we are going to youse the same wight and hight for every package
        self.SPRITE_FRAMES = [
            (8, 142, 15, 7),
            (32, 140, 15, 9),
            (56, 140, 15, 9),
            (80, 140, 15, 9),
            (104, 138, 15, 11),
        ]

        self.current_frame_index = 0
        self.transfer_timer = 0

    # --- PROPERTIES ---
    @property
    def x(self) -> int:
        return self._x

    @x.setter
    def x(self, value: int):
        self._x = value

    @property
    def y(self) -> int:
        return self._y

    @y.setter
    def y(self, value: int):
        self._y = value

    @property
    def conveyor_index(self) -> int:
        return self._conveyor_index

    def update(self, mario, luigi):
        if not self.active:
            return

        if self.state == 'moving':
            self._update_position()
            self._update_animation()
            self._check_edges(mario, luigi)

        elif self.state == 'transferring':
            self._update_transferring()


        elif self.state == 'falling':
            self._update_falling()



    def _update_position(self):
        # 1. РУХ
        self._x += self.speed * self._direction

    def _update_animation(self):
        # --- ЛОГІКА ЗМІНИ КАДРУ (0-5) ---
        # Базовий індекс для поверху (Поверх 0->0, Поверх 1->2, Поверх 2->4) <- before

        """# Frame base según la cinta (0->0, 1->2, 2->4, 3->5, 4->5)
        if self._conveyor_index >= 2:
            base_frame = 5  # Cintas superiores usan el último sprite
        else:
            base_frame = self._conveyor_index * 2

        # Centro de las cintas transportadoras (aprox x=250)
        center_x = 250

        # Si pasó el centro, usa el siguiente frame
        if self._x > center_x and base_frame < 5:
            self.current_frame_index = base_frame + 1
        else:
            self.current_frame_index = base_frame """
        # dont not how to implement the uper code
        base_frame = self._conveyor_index * 2
        # Центр екрану (приблизно 386 / 2 = 193)
        center_x = 193

        passed_center = False
        if self._direction == 1 and self._x > center_x:
            passed_center = True
        elif self._direction == -1 and self._x < center_x:
            passed_center = True

        # Якщо проїхали центр, додаємо +1 до індексу кадру
        if passed_center:
            self.current_frame_index = base_frame + 1
        else:
            self.current_frame_index = base_frame
# Maks
    def _check_edges(self, mario, luigi):
        if self._direction == 1 and self._x > 250:
            if mario.floor == self.conveyor_index and mario.state != 'busy':
                self.transfer_up(mario)
            else:
                self.state = 'falling'
        elif self._direction == -1 and self._x < 180:
            if luigi.floor == self.conveyor_index and luigi.state != 'busy':
                self.transfer_up(luigi)
            else:
                self.state = 'falling'




    def _update_falling(self):
        # 2. ПАДІННЯ
        self._y += 4
        if self._y > 360:  # Низ екрану
            self.active = False
            # Тут можна віднімати життя

    # =====================================================
    #                TRANSFER TO NEXT FLOOR
    # =====================================================
    def transfer_up(self, character):
        """Переміщення на поверх вище"""
        # Тут можна додати: character.state = 'busy' (щоб він підняв руки)

        self._conveyor_index += 1

        # Перевірка на вантажівку (якщо поверхи закінчились)
        if self._conveyor_index >= len(self.conveyor_y_position):
            self.active = False  # Успіх!
            return

        # Нова висота
        self._y = self.conveyor_y_position[self._conveyor_index]

        # Змінюємо напрямок
        self._direction *= -1

        # Ставимо на початок нової стрічки
        if self._direction == 1:
            self._x = 180
        else:
            self._x = 280

    # =====================================================
    #                       DRAW
    # =====================================================
    def draw(self):
        if not self.active:
            return

        # Перевіряємо, чи індекс кадру правильний
        if 0 <= self.current_frame_index < len(self.SPRITE_FRAMES):
            u, v, w, h = self.SPRITE_FRAMES[self.current_frame_index]

            # Малюємо пакунок
            # colkey=0 означає, що чорний колір буде прозорим
            pyxel.blt(self._x, self._y, 0, u, v, w, h, 0)
