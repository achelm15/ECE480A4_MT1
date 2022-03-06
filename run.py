import sys
from utils.cnf import bool_to_cnf

def main():
    bool_to_cnf(parser())

def parser():
    if len(sys.argv)!=2:
        print("Please enter a boolean function in proper format.")
        return
    func = sys.argv[1]
    return func

if __name__ == "__main__":
    main()