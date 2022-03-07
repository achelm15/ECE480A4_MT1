import sys
from utils.cnf import bool_to_cnf
from utils.sat import sat

def main():
    input = parser()
    if input:
        bool_to_cnf(input)
        sat("testt.cnf")
    

def parser():
    if len(sys.argv)!=2:
        print("Please enter a boolean function in proper format.")
        return False
    func = sys.argv[1]
    return func

if __name__ == "__main__":
    main()