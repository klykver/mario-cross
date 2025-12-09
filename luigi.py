import pyxel


class Luigi:
    def __init__(self, x: int, move_controls: bool):
        self.x = x
        # possible positions of floors
        self.floor_y_position = [210, 162, 114]
        # current floor
        self.floor = 0
        self.max_floor = len(self.floor_y_position) - 1

        # key to move Luigi
        self.move_controls = move_controls

        self.y = self.floor_y_position[0]
        self.target_y = self.y
        self.climb_speed = 3

        self.state = 'idle'
        self.busy_timer = 0

    @property
    def state(self):
        return self.__state

    @state.setter
    def state(self, value):
        if not isinstance(value, str):
            raise TypeError("state must be a string")
        elif value not in ('idle', 'busy', 'scared', 'climbing'):
            raise ValueError("State can be only 'idle', 'busy', 'scared' or 'climbing'")
        else:
            self.__state = value

    @property
    def move_controls(self):
        return self.__move_controls

    @move_controls.setter
    def move_controls(self, value):
        if not isinstance(value, bool):
            raise TypeError("move_controls must be a boolean")
        self.__move_controls = value

    # is activated when Luigi moves packages
    def set_busy(self):
        self.state = "busy"
        self.busy_timer = 10

    # it is activated when Luigi loses a package
    def set_scared(self):
        self.state = "scared"
        self.busy_timer = 60 # lasts while pause is active (approx 2s)

    # it is activated for Luigi to return to idle state and the corresponding floor
    def end_scared(self):
        self.state = "idle"
        self.busy_timer = 0
        self.y = self.floor_y_position[self.floor]

    # it is a timer for the duration of the busy state and the scared state
    def update_busy(self):
        if self.busy_timer > 0:
            self.busy_timer -= 1
        else:
            self.state = "idle"

    def update(self):
        # If Luigi is busy or scared, he ignores input and just updates the timer
        # When Luigi is busy
        if self.state == 'busy':
            self.update_busy()
            return
        # When Luigi is scared
        if self.state == 'scared':
            if self.busy_timer > 0:
                self.busy_timer -= 1
            return
        # when Luigi is moving and ready to receive a package
        # normal input
        if self.state == 'idle':
            # create some local variables to make the change of controls easier
            key_up = pyxel.KEY_W
            key_down = pyxel.KEY_S

            # if controls are inverted, change the keys
            if self.move_controls:
                key_up = pyxel.KEY_S
                key_down = pyxel.KEY_W

            # if the keys are pressed, change the floor
            if pyxel.btn(key_up) and self.floor < self.max_floor:
                self.floor += 1
                self.target_y = self.floor_y_position[self.floor]
                self.state = 'climbing'
            elif pyxel.btn(key_down) and self.floor > 0:
                self.floor -= 1
                self.target_y = self.floor_y_position[self.floor]
                self.state = 'climbing'

        # when Luigi is climbing to a floor. During the distance the climbing animation is played
        elif self.state == 'climbing':
            dist = self.target_y - self.y
            if abs(dist) <= self.climb_speed:
                self.y = self.target_y
                self.state = 'idle'
            else:
                self.y += self.climb_speed if dist > 0 else -self.climb_speed

    # Draw the Luigi sprite. The sprite changes depending on the state. The animation is also played.
    def draw(self):
        # scared state: show lying sprite shifted slightly down
        if self.state == "scared":
            pyxel.blt(self.x, self.y + 5, 0, 119, 35, 17, 29, 0)
            return

        if self.state == 'busy':
            if (pyxel.frame_count % 60) < 15:
                pyxel.blt(self.x, self.y + 11, 0, 144, 43, 24, 23, 0)
            else:
                pyxel.blt(self.x, self.y, 0, 89, 32, 23, 31, 0)
            return

        if self.state == 'idle':
            if (pyxel.frame_count % 30) < 15:
                pyxel.blt(self.x, self.y, 0, 24, 32, 14, 34, 0)
            else:
                pyxel.blt(self.x, self.y, 0, 0, 32, 16, 34, 0)
            return

        if self.state == 'climbing':
            if (pyxel.frame_count // 5) % 2 == 0:
                pyxel.blt(self.x, self.y, 0, 72, 32, 15, 30, 0)
            else:
                pyxel.blt(self.x, self.y, 0, 48, 32, 15, 33, 0)
            return
