import sys
from tkinter import E
from utils.cnf import bool_to_cnf, xor, xor2
from utils.sat import sat, remove_set, minimum
import argparse

def main():
    input = parser()
    if input:
        #If checking satisfiabiltiy 
        if not input.equality:
            #If no set of inputs given
            if not input.set:
                #Create the cnf in cnf.cnf
                bool_to_cnf(input.f, [])
                tot = []
                #Loop to find all satisfied inputs
                while True:
                    returned = sat("cnf.cnf")
                    if returned:
                        tot.append(returned)
                    else:
                        break
                #If none found, unsat
                if len(tot)==0:
                    print("UNSAT")
                    return
                #If sat, write all possible inputs to output.txt, along with smallest input
                else:
                    outFile = open("output.txt","w")
                    for x in tot:
                        outFile.write(x)
                    outFile.write("\n\nSmallest set of input variables: "+minimum(input.f, ""))
                    outFile.close()
            #If set of inputs given
            else:
                #Store given inputs in cnf form in addition
                addition = remove_set(input.set)
                #Create the cnf in cnf.cnf
                bool_to_cnf(input.f, addition)
                tot = []
                #Loop to find all satisfied inputs
                while True:
                    returned = sat("cnf.cnf")
                    if returned:
                        tot.append(returned)
                    else:
                        break
                #If none found, unsat
                if len(tot)==0:
                    print("UNSAT")
                    return
                #If sat, write all possible inputs to output.txt, along with smallest input
                else:
                    outFile = open("output.txt","w")
                    for x in tot:
                        outFile.write(x)
                    outFile.write("\n\nSmallest set of input variables: "+minimum(input.f, input.set))
                    outFile.close()
        #if checking equality
        else:
            #Xor the funcitons and then simplify
            xorred = xor2(input.f, input.s)
            #If nothing remains, the inputs are equal
            if not xorred:
                print("Functions are equal") 
                return 
            #convert output to cnf stored in cnf.cnf
            bool_to_cnf(xorred, [])
            returned = sat("cnf.cnf")
            #if the xorred function is SAT the funcions are unequal
            if returned:
                print("Fuctions are not equal")
            else:
                print("Functions are equal")            

#Used to parse and check inputs - Assumes functions given in proper SOP form as stated in README
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

if __name__ == "__main__":
    main()