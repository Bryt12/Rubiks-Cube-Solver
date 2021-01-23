from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.utils import to_categorical
import pandas as pd
import random
import numpy as np

class Solver:
    def __init__(self):
        self.X_train = []
        self.y_train = []
        self.last_two = [None, None]
        self.model = self.make_model()

    def make_model(self):
        model = Sequential()
        model.add(Dense(256, input_dim=324, activation='relu'))
        model.add(Dropout(0.4))
        model.add(Dense(512, activation='relu'))
        model.add(Dropout(0.4))
        model.add(Dense(256, activation='relu'))
        model.add(Dense(12, activation='softmax'))

        model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=["accuracy"])

        return model

    def preprocess_cube(self, c):
        c = c.reshape((1,54))
        df = pd.DataFrame(c)
        df = df.apply(lambda x: x.astype('category').cat.set_categories(['w', 'g', 'o', 'b', 'r', 'y']))
        df = pd.get_dummies(df)
        return df

    def number_to_move(self, num):
        if num == 0 or num == 1:
            return 'r', num%2 == 0
        if num == 2 or num == 3:
            return 'l', num%2 == 0
        if num == 4 or num == 5:
            return 'u', num%2 == 0
        if num == 6 or num == 7:
            return 'd', num%2 == 0
        if num == 8 or num == 9:
            return 'f', num%2 == 0
        if num == 10 or num == 11:
            return 'b', num%2 == 0

    def generate_move(self, cube):
        # Capture state before move
        init_state = cube.cube.copy()
        init_score = cube.score()

        # Preprocess cube and ask model for next move
        df = self.preprocess_cube(cube.cube)
        num = np.argmax(self.model.predict(df), axis=-1)[0]

        # Convert last move from number to move
        # If last number does not exist use -99, -99 as placeholder
        if self.last_two[1] is not None:
            last_move, last_clockwise = self.number_to_move(self.last_two[1])
        else:
            last_move, last_clockwise = -99, -99

        # Convert AI generated move
        this_move, this_clockwise = self.number_to_move(num)

        # Check if move is the reverse of the last move
        is_reverse_of_last_move = (last_move == this_move and this_clockwise != last_clockwise)
        # Check if move is the same as the last two
        three_of_same_in_row = (num == self.last_two[0] and num == self.last_two[1])
        # If either are true, generate a random move instead
        if three_of_same_in_row or is_reverse_of_last_move:
            num = random.randint(0, 11)

        # Update last two moves
        self.last_two[0] = self.last_two[1]
        self.last_two[1] = num

        # Make calculated move and get score of cube afterward
        move, clockwise = self.number_to_move(num)
        cube.make_move(move, clockwise)
        current_score = cube.score()

        # If move increased score, add it to the training data
        if current_score > init_score:
            self.X_train.append(self.preprocess_cube(init_state).iloc[0])
            self.y_train.append(to_categorical(num, num_classes=12))

        # Return if a random move was picked
        return three_of_same_in_row or is_reverse_of_last_move

    def save_data(self, X_train, y_train):
        print("saving")

        # np.save("X_data.npy", X_train)
        # np.save("y_data.npy", y_train)

    def train_model(self):
        if len(self.y_train) > 0:
            self.model = self.make_model()

            self.model.fit(np.asarray(self.X_train), np.asarray(self.y_train), epochs=30, verbose=0)

        self.save_data(self.X_train, self.y_train)
