# Rubiks-Cube-Solver

This program is a Rubik's cube application written from scratch and a neural network designed to try to solve it. 
The goal is to create a network that can take any state of the Rubik's cube and be able to solve it. Currently 
it is using a very simple fully connected neural network but in the future I plan on implementing CNN's and RNN's.

## Setup

The only package outside of the data science world is arcade and it is used to display the Rubik's Cube

```bash
pip install -r requirements.txt
```

## Usage

By running main.py the application will open.
```bash
python main.py
```


## Controls

Every move will be clockwise, to turn counter-clockwise hold shift and hit the associated key.

u - up clockwise  
d - down clockwise  
r - right clockwise  
l - left clockwise  
f - front clockwise  
b - back clockwise  
t - train network  
a - toggle network going indefinitely  

## Training

In order to train the network hit the 't' key and it will begin trying to solve the cube. (it's not very smart yet so bare with it)
After every specified number of cubes it will train the network on the good moves. (moves that increased the score) It will then attempt
to solve a Rubik's cube behind the scenes and print out the maximum percent solved. It will also print out how many times it was given a
random move during training. A random move will happen if it chooses the same exact move three times or it is undoing it's last move.
