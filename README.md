# ECE480A4_MT1 - SAT Solver
To run the base program enter:
`python run.py --f "boolean function"`
- The boolean function must use variables in the form xN, with N being the Nth number. The first variable must be x1. x0 cannot be used.
- The boolean function must be in SoP form
- If SAT, each combination of inputs will be stored in output.txt

To run the program with a set of inputs:
`python run.py --f "boolean function" --set "var1,var2,var3"`

To run the program to determine if two function are equal:
`python run.py --f "boolean function" --s "boolean function" --equality`
