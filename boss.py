import pyxel


class Boss:
    # Boss appears at doors to punish the guilty worker for a short time.
    def __init__(self):
        self.active = False
        self.timer = 0
        self.side = "left"  # "left" or "right"

        # door coordinates
        self.left_x = 486
        self.left_y = 145

        self.right_x = 7
        self.right_y = 233

    # ---------------- properties ----------------
    @property
    def active(self) -> bool:
        return self.__active

    @active.setter
    def active(self, val: bool):
        if not isinstance(val, bool):
            raise TypeError("active must be bool")
        self.__active = val

    @property
    def timer(self) -> int:
        return self.__timer

    @timer.setter
    def timer(self, val: int):
        if not isinstance(val, int):
            raise TypeError("timer must be int")
        if val < 0:
            raise ValueError("timer cannot be negative")
        self.__timer = val

    @property
    def side(self) -> str:
        return self.__side

    @side.setter
    def side(self, val: str):
        if not isinstance(val, str):
            raise TypeError("side must be str")
        if val not in ("left", "right"):
            raise ValueError("side must be 'left' or 'right'")
        self.__side = val

    # ---------------- behavior ----------------
    def appear(self, side: str):
        """Show boss on given side for a short time."""
        self.active = True
        self.side = side
        self.timer = 60

    def update(self):
        """Count boss timer and hide when finished."""
        if not self.active:
            return
        self.timer -= 1
        if self.timer <= 0:
            self.active = False

    def draw(self):
        """Draw boss sprite at the appropriate door."""
        if not self.active:
            return
        if self.side == "right":
            pyxel.blt(self.left_x, self.left_y, 2, 80, 168, 23, 33, 0)
        if self.side == "left":
            pyxel.blt(self.right_x, self.right_y, 2, 81, 128, 20, 33, 0)