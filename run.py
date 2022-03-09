import sys
from tkinter import E
from utils.cnf import bool_to_cnf, xor
from utils.sat import sat, remove_set, minimum
import argparse

def main():
    input = parser()
    if input:
        if not input.equality:
            if not input.set:
                bool_to_cnf(input.f, [])
                tot = []
                while True:
                    returned = sat("cnf.cnf")
                    if returned:
                        tot.append(returned)
                    else:
                        break
                if len(tot)==0:
                    print("UNSAT")
                    return
                else:
                    outFile = open("output.txt","w")
                    for x in tot:
                        outFile.write(x)
                    outFile.write("\n\nSmallest set of input variables: "+minimum(input.f))
                    outFile.close()
                    

            else:
                addition = remove_set(input.set)
                bool_to_cnf(input.f, addition)
                tot = []
                while True:
                    returned = sat("cnf.cnf")
                    if returned:
                        tot.append(returned)
                    else:
                        break
                if len(tot)==0:
                    print("UNSAT")
                    return
                else:
                    outFile = open("output.txt","w")
                    for x in tot:
                        outFile.write(x)
                    outFile.close()
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