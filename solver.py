import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.utils import to_categorical
import pandas as pd
import random
import numpy as np

class Solver:
    def __init__(self, delta_epsilon = 0.9, gamma = 0.7):
        self.X_train = []
        self.y_train = []
        self.data_start = 0

        self.last_two = [None, None]
        self.model = self.make_model()
        self.epsilon = 1
        self.delta_epsilon = delta_epsilon
        self.gamma = gamma

    def begin_training_cycle(self):
        self.data_start = len(self.y_train)

    def make_model(self):
        model = Sequential()
        model.add(Dense(256, input_dim=162, activation='relu'))
        model.add(Dropout(0.4))
        model.add(Dense(128, activation='relu'))
        model.add(Dropout(0.4))
        model.add(Dense(128, activation='relu'))
        model.add(Dense(12))

        model.compile(optimizer='adam', loss='mean_squared_error', metrics=["accuracy"])

        return model

    def preprocess_cube(self, c):
        c = c.flatten()
        out = np.empty((c.shape[0],3))

        for i in range(c.shape[0]):
            out[i] = self.letter_to_bin(c[i])
        # df = pd.DataFrame(c)
        # df = df.apply(lambda x: x.astype('category').cat.set_categories(['w', 'g', 'o', 'b', 'r', 'y']))
        # df = pd.get_dummies(df)
        return np.reshape(out, (-1, 162))

    def letter_to_bin(self, let):
        if let == 'w':
            return np.array([1, 0, 0])
        if let == 'y':
            return np.array([-1, 0, 0])

        if let == 'g':
            return np.array([0, 1, 0])
        if let == 'b':
            return np.array([0, -1, 0])

        if let == 'o':
            return np.array([0, 0, 1])
        if let == 'r':
            return np.array([0, 0, -1])

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

    def generate_move(self, cube, training = False):
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

        if not training:
            explore = False
        else:
            explore = random.random() < self.epsilon
        # If either are true, generate a random move instead
        if three_of_same_in_row or is_reverse_of_last_move or explore:
            num = random.randint(0, 11)

        # Update last two moves
        self.last_two[0] = self.last_two[1]
        self.last_two[1] = num

        # Make calculated move and get score of cube afterward
        move, clockwise = self.number_to_move(num)
        cube.make_move(move, clockwise)

        if training:
            current_score = cube.score()

            # Add move to training set
            self.X_train.insert(0, df.flatten())
            self.y_train.insert(0, to_categorical(num, num_classes=12) * current_score)

            # Update q-value of each y
            self.update_q_values(current_score)

        # Return if a random move was picked
        return three_of_same_in_row or is_reverse_of_last_move or explore

    def update_q_values(self, reward):
        if len(self.y_train) == self.data_start:
            return

        # Skip newest value so start at 1
        for i in range(1, len(self.y_train) - self.data_start):
            y_data = self.y_train[i]

            non_zero_index = [i for i, val in enumerate(y_data) if val != 0]
            non_zero_index = non_zero_index[0]
            current_value = y_data[non_zero_index]
            new_value = reward + current_value * self.gamma
            # new_value = (1-self.learning_rate) * current_value + self.learning_rate * (current_value + ((self.gamma**i)*current_value))


            self.y_train[i][non_zero_index] = new_value

    def save_data(self, X_train, y_train):
        print("saving")

        # np.save("X_data.npy", X_train)
        # np.save("y_data.npy", y_train)

    def train_model(self):
        self.epsilon *= self.delta_epsilon
        self.model = self.make_model()

        self.model.fit(np.asarray(self.X_train), np.asarray(self.y_train), epochs=30, verbose=0)

        # self.save_data(self.X_train, self.y_train)