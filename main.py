import arcade
import math
from cube import Cube

sticker_width = 50

WIDTH = sticker_width*12
HEIGHT = sticker_width*9

class CubeDisplay(arcade.Window):
    scrambling = False
    scrambles = 0

    def __init__(self):
        """ Initializer """
        # Call the parent class initializer
        super().__init__(WIDTH, HEIGHT, "Cube")

        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        arcade.start_render()
        # In pixels
        if self.scrambling:
            cube.scramble(1)
            self.scrambles += 1
        if self.scrambles > 30:
            self.scrambling = False
            self.scrambles = 0

        side_offset_left = [sticker_width * 3,
                            sticker_width * 3,
                            0,
                            sticker_width * 9,
                            sticker_width * 6,
                            sticker_width * 3]

        side_offset_top = [sticker_width * 6,
                           sticker_width * 3,
                           sticker_width * 3,
                           sticker_width * 3,
                           sticker_width * 3,
                           0]
        # Sticker order
        # 0 1 2
        # 3 4 5
        # 6 7 8
        for side in range(6):
            for sticker in range(9):
                sticker_x = sticker % 3
                sticker_y = math.floor(sticker / 3)

                x = side_offset_left[side] + (sticker_width * sticker_x)
                y = side_offset_top[side] + (sticker_width * abs(2-sticker_y))

                x_center = x + (sticker_width/2)
                y_center = y + (sticker_width/2)
                col = self.get_color(cube.cube[side].T[sticker_x][sticker_y])

                arcade.draw_rectangle_filled(x_center, y_center, sticker_width, sticker_width, col)
                arcade.draw_rectangle_outline(x_center, y_center, sticker_width, sticker_width, arcade.color.BLACK)

    def on_key_release(self, symbol: int, modifiers: int):
        clockwise = not modifiers == arcade.key.MOD_SHIFT
        if symbol == arcade.key.R:
            cube.r(clockwise)
        if symbol == arcade.key.L:
            cube.l(clockwise)
        if symbol == arcade.key.U:
            cube.u(clockwise)
        if symbol == arcade.key.D:
            cube.d(clockwise)
        if symbol == arcade.key.F:
            cube.f(clockwise)
        if symbol == arcade.key.B:
            cube.b(clockwise)
        if symbol == arcade.key.S:
            if modifiers == arcade.key.MOD_SHIFT:
                self.scrambling = True
            else:
                cube.solve()

    def get_color(self, char):
        if char == 'w':
            return arcade.color.WHITE
        if char == 'g':
            return arcade.color.PASTEL_GREEN
        if char == 'o':
            return arcade.color.PASTEL_ORANGE
        if char == 'b':
            return arcade.color.PASTEL_BLUE
        if char == 'r':
            return arcade.color.PASTEL_RED
        if char == 'y':
            return arcade.color.PASTEL_YELLOW

def main():
    window = CubeDisplay()
    arcade.run()

if __name__ == "__main__":
    cube = Cube()

    main()