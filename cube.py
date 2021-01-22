import numpy as np
import random

class Cube():
    # The white face is always on top with the green face in front
    # white - 0
    # Green - 1
    # Orange - 2
    # Blue - 3
    # Red - 4
    # Yellow - 5

    # np.rot90 will rotate counter-clockwise 90, thus
    # 3 rotations are needed for one clockwise rotation

    def __init__(self):
        self.sides = []
        colors = {
            0: "w",
            1: "g",
            2: "o",
            3: "b",
            4: "r",
            5: "y"
        }
        for i in range(6):
            side = np.full((3,3), colors[i])

            self.sides.append(side)

        self.cube = np.array(self.sides)

    def u(self, clockwise=True):
        rotations = 3
        face_order = [1, 4, 3, 2]
        if not clockwise:
            rotations = 1
            face_order = [2, 3, 4, 1]

        self.cube[0] = np.rot90(self.cube[0], k=rotations)

        temp_row = self.cube[face_order[0]][0].copy()
        self.cube[face_order[0]][0] = self.cube[face_order[1]][0]
        self.cube[face_order[1]][0] = self.cube[face_order[2]][0]
        self.cube[face_order[2]][0] = self.cube[face_order[3]][0]
        self.cube[face_order[3]][0] = temp_row

    def d(self, clockwise=True):
        rotations = 3
        face_order = [1, 2, 3, 4]
        if not clockwise:
            rotations = 1
            face_order = [4, 3, 2, 1]

        self.cube[5] = np.rot90(self.cube[5], k=rotations)

        temp_row = self.cube[face_order[0]][2].copy()
        self.cube[face_order[0]][2] = self.cube[face_order[1]][2]
        self.cube[face_order[1]][2] = self.cube[face_order[2]][2]
        self.cube[face_order[2]][2] = self.cube[face_order[3]][2]
        self.cube[face_order[3]][2] = temp_row

    def r(self, clockwise=True):
        rotations = 3
        face_order = [1, 5, 3, 0]
        if not clockwise:
            rotations = 1
            face_order = [0, 3, 5, 1]

            self.cube[4] = np.rot90(self.cube[4], k=rotations)

            temp_row = self.cube[face_order[0]].T[2].copy()
            self.cube[face_order[0]].T[2] = np.flip(self.cube[face_order[1]].T[0])
            self.cube[face_order[1]].T[0] = np.flip(self.cube[face_order[2]].T[2])
            self.cube[face_order[2]].T[2] = self.cube[face_order[3]].T[2]
            self.cube[face_order[3]].T[2] = temp_row

            return

        self.cube[4] = np.rot90(self.cube[4], k=rotations)

        temp_row = self.cube[face_order[0]].T[2].copy()
        self.cube[face_order[0]].T[2] = self.cube[face_order[1]].T[2]
        self.cube[face_order[1]].T[2] = np.flip(self.cube[face_order[2]].T[0])
        self.cube[face_order[2]].T[0] = np.flip(self.cube[face_order[3]].T[2])
        self.cube[face_order[3]].T[2] = temp_row

    def l(self, clockwise=True):
        rotations = 3
        face_order = [1, 0, 3, 5]
        if not clockwise:
            rotations = 1
            face_order = [5, 3, 0, 1]

            self.cube[2] = np.rot90(self.cube[2], k=rotations)

            temp_row = self.cube[face_order[0]].T[0].copy()
            self.cube[face_order[0]].T[0] = np.flip(self.cube[face_order[1]].T[2])
            self.cube[face_order[1]].T[2] = np.flip(self.cube[face_order[2]].T[0])
            self.cube[face_order[2]].T[0] = self.cube[face_order[3]].T[0]
            self.cube[face_order[3]].T[0] = temp_row

            return

        self.cube[2] = np.rot90(self.cube[2], k=rotations)

        temp_row = self.cube[face_order[0]].T[0].copy()
        self.cube[face_order[0]].T[0] = self.cube[face_order[1]].T[0]
        self.cube[face_order[1]].T[0] = np.flip(self.cube[face_order[2]].T[2])
        self.cube[face_order[2]].T[2] = np.flip(self.cube[face_order[3]].T[0])
        self.cube[face_order[3]].T[0] = temp_row

    def f(self, clockwise=True):
        rotations = 3
        face_order = [0, 2, 5, 4]
        if not clockwise:
            rotations = 1
            face_order = [0, 4, 5, 2]

            self.cube[1] = np.rot90(self.cube[1], k=rotations)

            temp_row = np.flip(self.cube[face_order[0]][2].copy())
            self.cube[face_order[0]][2] = self.cube[face_order[1]].T[0]
            self.cube[face_order[1]].T[0] = np.flip(self.cube[face_order[2]][0])
            self.cube[face_order[2]][0] = self.cube[face_order[3]].T[2]
            self.cube[face_order[3]].T[2] = temp_row

            return

        self.cube[1] = np.rot90(self.cube[1], k=rotations)

        temp_row = self.cube[face_order[0]][2].copy()
        self.cube[face_order[0]][2] = np.flip(self.cube[face_order[1]].T[2])
        self.cube[face_order[1]].T[2] = self.cube[face_order[2]][0]
        self.cube[face_order[2]][0] = np.flip(self.cube[face_order[3]].T[0])
        self.cube[face_order[3]].T[0] = temp_row

    def b(self, clockwise=True):
        rotations = 3
        face_order = [0, 4, 5, 2]
        if not clockwise:
            rotations = 1
            face_order = [0, 2, 5, 4]

            self.cube[3] = np.rot90(self.cube[3], k=rotations)

            temp_row = self.cube[face_order[0]][0].copy()
            self.cube[face_order[0]][0] = np.flip(self.cube[face_order[1]].T[0])
            self.cube[face_order[1]].T[0] = self.cube[face_order[2]][2]
            self.cube[face_order[2]][2] = np.flip(self.cube[face_order[3]].T[2])
            self.cube[face_order[3]].T[2] = temp_row

            return
        self.cube[3] = np.rot90(self.cube[3], k=rotations)

        temp_row = np.flip(self.cube[face_order[0]][0].copy())
        self.cube[face_order[0]][0] = self.cube[face_order[1]].T[2]
        self.cube[face_order[1]].T[2] = np.flip(self.cube[face_order[2]][2])
        self.cube[face_order[2]][2] = self.cube[face_order[3]].T[0]
        self.cube[face_order[3]].T[0] = temp_row

    def make_move(self, move, clockwise=True):
        if move == 'u':
            self.u(clockwise)
        elif move == 'd':
            self.d(clockwise)
        elif move == 'r':
            self.r(clockwise)
        elif move == 'l':
            self.l(clockwise)
        elif move == 'f':
            self.f(clockwise)
        elif move == 'b':
            self.b(clockwise)

    def scramble(self, number_of_moves=20):
        moves = [random.randint(1, 6) for _ in range(number_of_moves)]
        direction = [random.randint(0, 1) for _ in range(number_of_moves)]
        scramble = ""

        for i in range(len(moves)):
            # print(c.cube)
            clockwise = direction[i] == 1
            if(moves[i] == 0):
                self.u(clockwise)
                scramble += ("u"+ ("'" if not clockwise else ""))
            elif (moves[i] == 1):
                self.d(clockwise)
                scramble += ("d" + ("'" if not clockwise else ""))
            elif (moves[i] == 2):
                self.r(clockwise)
                scramble += ("r" + ("'" if not clockwise else ""))
            elif (moves[i] == 3):
                self.l(clockwise)
                scramble += ("l" + ("'" if not clockwise else ""))
            elif (moves[i] == 4):
                self.f(clockwise)
                scramble += ("f" + ("'" if not clockwise else ""))
            elif (moves[i] == 5):
                self.b(clockwise)
                scramble += ("b" + ("'" if not clockwise else ""))
        # print(scramble)
        return scramble

    def solve(self):
        self.cube = np.array(self.sides)

    def test_state(self):
        self.solve()
        self.u()
        self.l()
        self.d()
        self.r()
        self.u()

    def score(self):
        out = 0
        for i in range(6):
            middle = self.cube[i][1][1]
            out += ((self.cube[i] == middle).sum() - 1)
        return out

# c = Cube()
# c.draw_cube()
# c.scramble()
# c.draw_cube()
# print("--------------------")
# c.u()
# c.u()
# c.d()
# c.d()
# c.r()
# c.r()
# c.l()
# c.l()
# c.f()
# c.f()
# c.b()
# c.b()
# print(c.cube)
# print("--------------------")
