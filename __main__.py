""" COSC364 Assignment 2
Flow Planning

Authors: Henry Hay-Smith and Rory Patterson
Date: 26/05/2021 """

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
        """ Creates a list of decision variables and dictionaries of the different flows from source i to destination j """
        self.paths, self.paths_per_node, self.x_var_list, self.u_var_list = dict(), dict(), [], []
        for i in range(1, self.X+1):
            for k in range(1, self.Y+1):
                for j in range(1, self.Z+1):
                    # Create 'x' and 'u' variables for the path
                    x_var, u_var = (f'x{i}{k}{j}', f'u{i}{k}{j}')
                    self.x_var_list.append(x_var)
                    self.u_var_list.append(f'u{i}{k}{j}')
                    # Add this path from source node to destination node to the path dictionary                    
                    if (i, j) not in self.paths.keys():
                        self.paths[(i, j)] = [(x_var, u_var)]
                    else:
                        self.paths[(i, j)] += [(x_var, u_var)]
                    # Add this paths link from source node to transit node to the d capacity dictionary                    
                    if (k) not in self.paths_per_node.keys():
                        self.paths_per_node[(k)] = [(x_var, u_var)]
                    else:
                        self.paths_per_node[(k)] += [(x_var, u_var)]
    
    def demands(self):
        """ Creates a table of demand volumes """
        self.demands = []
        for i in range(self.X):
            self.demands.append([i+j+2 for j in range(self.Z)])
        print(f'Demand Volume Table:')
        for line in self.demands:
            print(f'    {line}')
        print()







class LP_File:
    def __init__(self, config):
        """ Initialises the variable holding the list of lines in the generated LP file """
        self.LP = []
        self.config = config
    
    def __repr__(self):
        """ Returns a string representation of the generated LP file """
        return '\n'.join(self.LP)
    
    def generate_LP(self, function, constraints, bounds, binaries):
        """ Generates an LP file """
        self.LP.append(f'Minimize')
        self.LP.append(f'    {function}')
        self.LP.append(f'Subject to')
        for constraint in constraints:
            self.LP.append(f'    {constraint}')
        self.LP.append(f'Bounds')
        for bound in bounds:
            self.LP.append(f'    {bound}')
        self.LP.append(f'Binary')
        for binary in binaries:
            self.LP.append(f'    {binary}')
        self.LP.append(f'End')

    def generate_function(self):
        return f'r'
    
    def generate_constraints(self):
        constraints = []
        
        for (i, j) in self.config.paths.keys():
            x_list = [value[0] for value in self.config.paths[(i, j)]]
            h_k = self.config.demands[i-1][j-1]
            constraints.append(' + '.join(x_list) + f' = {h_k}')
        constraints.append(' ')
        
        for (i, j) in self.config.paths.keys():
            u_list = [value[1] for value in self.config.paths[(i, j)]]
            n_k = 2
            constraints.append(' + '.join(u_list) + f' = {n_k}')
        constraints.append(' ')
        
        
        
        for (i, j) in self.config.paths.keys():
            x_list = [value[0] for value in self.config.paths[(i, j)]]
            u_list = [value[1] for value in self.config.paths[(i, j)]]
            for index in range(len(x_list)):
                rhs = int(self.config.demands[i-1][j-1]) / 2
                constraints.append(f'{x_list[index]} - {rhs} {u_list[index]} = 0')
        constraints.append(' ')
        
        for (i, j) in self.config.paths.keys():
            x_list = [value[0] for value in self.config.paths[(i, j)]]
            u_list = [value[1] for value in self.config.paths[(i, j)]]
            con_list = []
            for index in range(len(x_list)):
                con_list.append(f'{x_list[index]} {u_list[index]}')
            constraints.append(' + '.join(con_list) + f' = {self.config.demands[i-1][j-1]}')
        constraints.append(' ')
        
        for (k) in self.config.paths_per_node.keys():
            x_list = [value[0] for value in self.config.paths_per_node[(k)]]
            u_list = [value[1] for value in self.config.paths_per_node[(k)]]
            con_list = []
            for index in range(len(x_list)):
                con_list.append(f'{x_list[index]} {u_list[index]}')
            constraints.append(' + '.join(con_list) + f' - r <= 0')
        constraints.append(' ')
        return constraints
    
    def generate_bounds(self):
        bounds = []
        for x_dec_var in self.config.x_var_list:
            bounds.append(f'{x_dec_var} >= 0')
        bounds.append(f'r >= 0')
        return bounds
    
    
    
    
    def generate_binaries(self):
        binaries = ""
        for u_dec_var in self.config.u_var_list:
            binaries += f'{u_dec_var} '
        return [binaries[:-1]]
    
def main():
    """ Starts the program and runs support scripts """
    config = Config()
    print(f'\nInputs Accepted:\n    {config}\n')
    config.demands()
    LP = LP_File(config)
    function = LP.generate_function()
    constraints = LP.generate_constraints()
    bounds = LP.generate_bounds()
    binaries = LP.generate_binaries()
    LP.generate_LP(function, constraints, bounds, binaries)
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