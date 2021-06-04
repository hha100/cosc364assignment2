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
import time


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
            raw_input = input(f'Enter three positive integers separated by a space:\n')
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
    
    def demands(self):
        """ Creates a table of demand volumes """
        self.demands = []
        for i in range(self.X):
            self.demands.append([i+j+2 for j in range(self.Z)])
        
        print(f'Demand Volume Table:')
        for line in self.demands:
            print(line)
        print()
    
    def capacities(self):
        """ Creates arbitrary tables of link capacitances """
        self.Cik = []
        self.Dkj = []
        
        for i in range(self.X):
            self.Cik.append([10 for k in range(self.Y)])
        
        for k in range(self.Y):
            self.Dkj.append([10 for j in range(self.Z)])
    

class LP_File:
    
    def __init__(self):
        """ Initialises the variable holding the list of lines in the generated LP file """
        self.LP = []
    
    def __repr__(self):
        """ Returns a string representation of the generated LP file """
        return '\n'.join(self.LP)
    
    def generate(self, function, constraints, bounds):
        """ Generates an LP file """
        self.LP.append(f'Minimize')
        self.LP.append(f'    {function}')
        self.LP.append(f'Subject to')
        for constraint in constraints:
            self.LP.append(f'    {constraint}')
        self.LP.append(f'Bounds')
        for bound in bounds:
            self.LP.append(f'    {bound}')
        self.LP.append(f'End')

def main():
    """ Starts the program and runs support scripts """
    config = Config()
    print(f'\nInputs Accepted:\n    {config}\n')
    
    # Generate a table of demand volumes
    config.demands()
    
    # Generate an arbirary list of link capacities
    config.capacities()
    
    # Call LP file generation function here
    LP = LP_File()
    
    function = f'5 x12 + 12 x132' # Debug Variable
    constraints = ['demandflow: x12 + x132 = 17', 'capp1: x12 <= 10', 'capp2: x132 <= 12'] # Debug Variable
    bounds = ['0 <= x12', '0 <= x132'] # Debug Variable
    
    LP.generate(function, constraints, bounds)
    
    print(f'LP file is:\n{LP if LP else "    EMPTY LP FILE"}')
    
    done = 0
    while not done:
        try:
            file = open('tm.lp', 'w')
            file.write(str(LP))
            file.close()
            done = 1
        except:
            print(f'LP file failed to write, trying again...')
            time.sleep(1)
    
    start_time = time.time()
    CPLEX_done = 0 # Debug variable
    
    # Call CPLEX here
    #
    #CPLEX_done = 1
    #
    
    # Find the CPLEX execution time
    end_time = f'{time.time() - start_time:.4f}'
    print(f'\nCPLEX Execution Time is:\n    {end_time+" s" if CPLEX_done else "CPLEX not performed"}\n')

main()