import arcade
import math
from cube import Cube
from solver import Solver
import matplotlib.pyplot as plt

sticker_width = 50

WIDTH = sticker_width * 12
HEIGHT = sticker_width * 9

NUMBER_FOR_SCRAMBLE = 30

NUMBER_OF_CUBES_TO_TRAIN = 100
NUMBER_OF_TURNS_PER_CUBE = 30
NUMBER_OF_TRAINS = 20


class CubeDisplay(arcade.Window):
    scrambling = False
    scrambles = 0

    collecting_data = False
    collections = 0
    trains = 0
    cubes_scrambled = 0

    solving = False

    max_scores = []
    rand_counts = []

    def __init__(self):
        """ Initializer """
        # Call the parent class initializer
        super().__init__(WIDTH, HEIGHT, "Cube")
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        arcade.start_render()

        # Scramble one move at a time to add animation
        if self.scrambling:
            cube.scramble(1)
            self.scrambles += 1
        if self.scrambles >= NUMBER_FOR_SCRAMBLE:
            self.scrambling = False
            self.scrambles = 0

        # Let AI make move and if move increases score add to train data
        if self.collecting_data:
            self.collect_data()

        # If done training
        if self.trains >= NUMBER_OF_TRAINS:
            self.finish_training()

        # Let AI solve indefinity
        if self.solving:
            solver.generate_move(cube)

        # Draw cube
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
                y = side_offset_top[side] + (sticker_width * abs(2 - sticker_y))

                x_center = x + (sticker_width / 2)
                y_center = y + (sticker_width / 2)
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
        if symbol == arcade.key.T:
            self.collecting_data = True
        if symbol == arcade.key.A:
            self.solving = not self.solving

    def get_color(self, char):
        if char == 'w':
            return arcade.color.WHITE
        if char == 'g':
            return arcade.color.PASTEL_GREEN
        if char == 'o':
            return arcade.color.PASTEL_ORANGE
        if char == 'b':
            return arcade.color.BLUEBERRY
        if char == 'r':
            return arcade.color.PASTEL_RED
        if char == 'y':
            return arcade.color.PASTEL_YELLOW

    def test_model(self):
        # Test model
        cube.scramble(NUMBER_FOR_SCRAMBLE)
        max_score = 0
        random_moves = 0
        for _ in range(20):
            random_move = solver.generate_move(cube)
            if cube.score() > max_score:
                max_score = cube.score()
            if random_move:
                random_moves += 1

        # Print results
        print("Generation Stats")
        print(str(int(self.collections / (NUMBER_OF_CUBES_TO_TRAIN * NUMBER_OF_TURNS_PER_CUBE))) + "/" + str(
            NUMBER_OF_TRAINS))
        print("Max completion:" + str((max_score / 48) * 100) + "%")
        print("Percent Random:" + str((random_moves / NUMBER_OF_TURNS_PER_CUBE) * 100) + "%")

        return max_score, random_moves

    def finish_training(self):
        # Reset variables
        self.trains = 0
        self.collecting_data = False
        self.collections = 0

        # Display results
        fig, axs = plt.subplots(2)
        axs[0].plot(self.max_scores)
        axs[0].set_ylabel('Percent Complete')
        axs[1].plot(self.rand_counts)
        axs[1].set_ylabel('Random Count')
        plt.show()

        # Solve cube
        cube.solve()

    def collect_data(self):
        # After the number of turns per cube is up re-scramble
        if self.collections % NUMBER_OF_TURNS_PER_CUBE == 0:
            # Solve cube first to allow the scramble to get more and more
            # as time goes on
            cube.solve()
            cube.scramble(int(NUMBER_FOR_SCRAMBLE * (self.cubes_scrambled / NUMBER_OF_CUBES_TO_TRAIN)))
            self.cubes_scrambled += 1

        solver.generate_move(cube)
        self.collections += 1

        # If at end of training cycle
        if self.collections % (NUMBER_OF_CUBES_TO_TRAIN * NUMBER_OF_TURNS_PER_CUBE) == 0:
            self.trains += 1
            self.cubes_scrambled = 0

            solver.train_model()

            max_score, random_moves = self.test_model()

            self.max_scores.append(max_score / 48)
            self.rand_counts.append(random_moves)

def main():
    window = CubeDisplay()
    arcade.run()


if __name__ == "__main__":
    cube = Cube()
    solver = Solver()
    main()
