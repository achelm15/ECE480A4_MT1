import sys
from tkinter import E
from utils.cnf import bool_to_cnf, xor
from utils.sat import sat, remove_set
import argparse

def main():
    input = parser()
    if input:
        if not input.equality:
            if not input.set:
                print(input.f)
                in_var_list = bool_to_cnf(input.f)
                sat("cnf.cnf", in_var_list, ([],[]))
            else:
                removed_formula = remove_set(input.f, input.set)
                if removed_formula:
                    if removed_formula == True:
                        # print("SAT")
                        # print("Solution:")
                        # print("\tTrue input variables: ", get_set_var(input.set)[0])
                        # print("\tFalse input variables: ", get_set_var(input.set)[1])
                        return
                    in_var_list = bool_to_cnf(removed_formula)
                    sat("cnf.cnf", in_var_list, get_set_var(input.set))
                else:
                    print("UNSAT")
                    return 
        else:
            xor(input.f, input.s)

def parser():
    parser = argparse.ArgumentParser(description='Python Satisfiability Solver')
    parser.add_argument('--equality', default=False, action=argparse.BooleanOptionalAction, help='flag to choose equality')
    parser.add_argument('--single', default=False, type=bool, help='flag to choose equality')
    parser.add_argument('--f', default=False, type=str, help='flag to choose equality')
    parser.add_argument('--s', default=False, type=str, help='flag to choose equality')
    parser.add_argument('--set', default=False, type=str, help='flag to choose set of inputs')
    args = parser.parse_args()
    if args.equality==False:
        if args.f==False:
            print("Please enter a boolean function after the flag \'--f\'")
            return False
        if args.s!=False:
            print("Please remove the boolean function after the flag \'--s\' and the flag itself")
            return False
    else:
        if args.f==False or args.s==False:
            print("Please enter two boolean functions")
            return False
        else:
            if args.set!=False:
                print("Please remove the --set option")
                return False
    return args
        
    
def get_set_var(input):
    falser = []
    truer = []
    l = input.split(",")
    for x in l:
        if x.find("~")==-1:
            truer.append(int(x[1:]))
        else:
            falser.append(int(x[2:]))
                
    return truer, falser


if __name__ == "__main__":
    main()