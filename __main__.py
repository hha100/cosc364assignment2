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
        self.inputs()
        self.Pk = self.X * self.Z
        self.L = self.X * self.Y + self.Y * self.Z
        self.decision_vars()
    
    def __repr__(self):
        """ Returns a string representation of the config values """
        return f'X = {self.X}, Y = {self.Y}, Z = {self.Z}, Pk = {self.Pk}, L = {self.L}'
    
    def inputs(self):
        """ Reads and parses the users' inputs to get the X, Y, and Z values """
        done = 0
        while not done:
            raw_input = input(f'Enter three positive integers separated by a space:\n    ')
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
        self.X = X
        self.Y = Y
        self.Z = Z
    
    def decision_vars(self):
        """ Creates a list of decision variables and a dictionary of the different flows from source i to destination j """
        self.paths = dict()
        self.c_links = dict()
        self.d_links = dict()
        self.x_var_list = []
        self.u_var_list = []
        for i in range(1, self.X+1):
            for k in range(1, self.Y+1):
                for j in range(1, self.Z+1):
                    self.x_var_list.append(f'x{i}{k}{j}')
                    self.u_var_list.append(f'u{i}{k}{j}')
                    if (i, j) not in self.paths.keys():
                        self.paths[(i, j)] = [f'x{i}{k}{j}']
                    else:
                        self.paths[(i, j)] += [f'x{i}{k}{j}']
        #print(self.x_var_list)
    
    def demands(self):
        """ Creates a table of demand volumes """
        self.demands = []
        for i in range(self.X):
            self.demands.append([i+j+2 for j in range(self.Z)])
        
        print(f'Demand Volume Table:')
        for line in self.demands:
            print(f'    {line}')
        print()
    
    def capacities(self):
        """ Creates arbitrary tables of link capacitances """
        self.Cik = []
        self.Dkj = []
        
        for i in range(self.X):
            self.Cik.append([1000 for k in range(self.Y)])
        
        for k in range(self.Y):
            self.Dkj.append([1000 for j in range(self.Z)])
    

class LP_File:
    
    def __init__(self, config):
        """ Initialises the variable holding the list of lines in the generated LP file """
        self.LP = []
        self.config = config
    
    def __repr__(self):
        """ Returns a string representation of the generated LP file """
        return '\n'.join(self.LP)
    
    def generate_LP(self, function, constraints, bounds):
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

    def generate_function(self):
        
        return f'r'
    
    def generate_constraints(self):
        constraints = []
        for (i, j) in self.config.paths.keys():
            sum1 = [value for value in self.config.paths[(i, j)]]
            h_k = self.config.demands[i-1][j-1]
            constraints.append(' + '.join(sum1) + f' = {h_k}')
        
        
        
        return constraints
    
    def generate_bounds(self):
        bounds = []
        for dec_var in self.config.x_var_list:
            bounds.append(f'0 <= {dec_var}')
        
        
        
        bounds.append(f'0 <= r')
        bounds.append(f'r <= 1')
        return bounds
    
    
    
def main():
    """ Starts the program and runs support scripts """
    config = Config()
    print(f'\nInputs Accepted:\n    {config}\n')
    
    # Generate a table of demand volumes
    config.demands()
    
    # Generate an arbirary list of link capacities
    config.capacities()
    
    # Call LP file generation function here
    LP = LP_File(config)
    
    function = LP.generate_function()
    constraints = LP.generate_constraints()
    bounds = LP.generate_bounds()
    
    #function = f'5 x12 + 12 x132' # Debug Variable
    #constraints = ['demandflow: x12 + x132 = 17', 'capp1: x12 <= 10', 'capp2: x132 <= 12'] # Debug Variable
    #bounds = ['0 <= x12', '0 <= x132'] # Debug Variable
    
    LP.generate_LP(function, constraints, bounds)
    
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

main()