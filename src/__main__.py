"""
COSC364 Assignment 2
Flow Planning

Authors: Henry Hay-Smith and Rory Patterson
Date: 26/05/2021

__main__.py is run by default when naming the directory in the command line, meaning you don't need to specify
which file you want to run
e.g. 'py src'
"""


import sys


class Config:
    
    def __init__(self):
        """ Initialises the X, Y, and Z values """
        self.X, self.Y, self.Z = self.inputs()
    
    def __repr__(self):
        """ Returns a string representation of the config values """
        return f'X = {self.X}, Y = {self.Y}, Z = {self.Z}'
    
    def inputs(self):
        """ Reads and parses the users' inputs to get the X, Y, and Z values """
        done = 0
        
        while not done:
            raw_input = input(f'\nEnter three positive integers separated by a space:\n')
            
            for char in raw_input:
                
                if char != ' ' and not char.isnumeric():
                    print(f'\nInvalid characters found in the input.\n')
                    break
                
            vals = raw_input.split(' ')
            
            if len(vals) != 3:
                print(f'Exactly 3 positive integers, separated by a single space, are required.\n')
                
            elif int(vals[1]) < 2:
                print(f'Y must be greater than or equal to 2.\n')
                
            else:
                X, Y, Z = int(vals[0]), int(vals[1]), int(vals[2])
                done = 1
                
        return X, Y, Z


def main():
    """ Starts the program and runs support scripts """
    config = Config()
    print(f'\n{config}')


if __name__ == "__main__":
    """ Runs the main function automatically """
    main()