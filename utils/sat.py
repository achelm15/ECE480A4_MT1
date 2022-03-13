import copy


def sat(file):
    #read cnf file
    inFile = open(file, "r")
    lines = inFile.readlines()
    header = []
    count = 0
    #ignore comments and find header line
    for x in lines:
        if x[0] == "c":
            count += 1
            continue
        if x[0] == "p":
            header = x
            count += 1
            break
    #put body of cnf in lines
    lines = lines[count:]
    #store header
    header = header.split()
    num_clauses = int(header[2])
    num_var = int(header[3])
    #store cnf in AND array of OR arrays
    formula = create_formula(lines)
    #store the global True and False variables
    #for each run through dpll these will hold the true and false variables
    global true, false
    true, false = [], []
    #call function implementing Davis Putnam Logemann Loveland Algorithm
    if dpll(formula):
        #remove duplicates in True and False variables
        false = sim_dupl(false)
        true = sim_dupl(true)
        #Pint output
        print("SAT")
        print("Solution:")
        print("\tTrue input variables: ", sorted(true))
        print("\tFalse input variables: ", sorted(false))
        #Store input combination in output, append inverse to
        #the cnf file in order to find another solution
        addition = ""
        output = ""
        #temp holds an array full of the True and False
        #values in order of magnitude
        temp = [0] * num_var
        for x in true:
            temp[abs(x) - 1] = x
        for x in false:
            temp[abs(x) - 1] = -x
        #if there is a 0 in temp, the variable was unset
        #It does not matter if it is true or false
        #So set to true
        for i,x in enumerate(temp):
            if abs(x)!=i+1:
                temp[i] = i+1
        #Put the inverse combination of inputs in the
        #Proper form to add to the cnf file
        for x, i in enumerate(temp):
            if abs(x) != i:
                x = i
            addition += str(-x) + " "
            output += str(x) + " "
        addition += "0\n"
        output += "0\n"
        #Add the addition to the cnf file
        inFile = open(file, "a")
        inFile.write(addition)
        inFile.close()
        #return the found combination of inputs
        return output
    else:
        return False

#Function to implement the Davis Putnam Logemann Lovland Algorithm
def dpll(formula):
    #Remove duplicates in the current cnf array
    res = []
    [res.append(x) for x in formula if x not in res]
    formula = res
    #Call unit propogate on the current cnf, store the new cnf, and true and false variables
    formula, new_true, new_false = unit_propogate(formula)
    #Call pure literal on the current cnf, store the new cnf, and true and false variables
    formula, new_true, new_false = pure_literal(formula, new_true, new_false)
    #If no clauses remain, the cnf is SAT
    if len(formula) == 0:
        return True
    null = False
    
    new_var = []
    for x in formula:
        #Checks for empty clause
        if len(x) == 0:
            null = True
        #Get all variables in the current cnf to choose a new variable
        else:
            for j in x:
                if abs(j) not in new_var:
                    new_var.append(abs(j))
    #Will choose the lowest magnitude variable
    new_var = sorted(new_var)

    #If an empty clause remains within the cnf, it is UNSAT
    if null:
        for i in new_true:
            true.remove(i)
        for i in new_false:
            false.remove(i)
        return False
    #Choose a new variable for next call of DPLL, append to cnf
    pos = copy.deepcopy(formula)
    neg = copy.deepcopy(formula)
    pos.append([new_var[0]])
    neg.append([-new_var[0]])
    #Call DPLL with the cnf with both both the true and false new variable ANDed
    if dpll(pos):
        return True
    elif dpll(neg):
        return True
    else:
        #If both the cnf with the positive and negative ANDed are false, 
        #This branch does will not SAT, clear true and false
        for i in new_true:
            true.remove(i)
        for i in new_false:
            false.remove(i)
        return False

#Converts input file string to AND array of OR arrays
# 1 -5 0
# 2 -5 0
# -1 -2 5 0 --> [[1,-5],[2,-5],[-1,-2,5]]
def create_formula(lines):
    formula = []
    count = 1
    for x in lines:
        var_list = []
        for j in x[: len(x) - 3].split():
            var_list.append(int(j))
        formula.append(var_list)
        count += 1
    return formula

#Function to implement unit propogate
def unit_propogate(formula):
    #Find all single variable clauses in the cnf
    unit = [j[0] for j in formula if len(j) == 1 and j[0]]
    #Arrays to hold new variables that are set to true or false
    new_true = []
    new_false = []
    if len(unit) != 0:
        #For each unit variable
        for u in unit:
            #Append variable to proper true or false
            if u < 0:
                false.append(-u)
                new_false.append(-u)
            else:
                true.append(u)
                new_true.append(u)
            #For the cnf
            i = 0
            while True:
                #If a unit variable occurs in a clause
                #Remove the clause because it it True
                if u in formula[i]:
                    formula.remove(formula[i])
                    i -= 1
                #If the inverse of a unit variable occurs
                #In a clause remove the inverse from the clause
                elif -u in formula[i]:
                    formula[i].remove(-u)
                i += 1
                if i == len(formula):
                    break
    #return the modified cnf and new true and false variables
    return formula, new_true, new_false

#Function to implement pure literal assignment
def pure_literal(formula, new_true, new_false):
    #If the length of the cnf is zero, no work can be done
    if len(formula) == 0:
        return formula, new_true, new_false
    #Lists to hold all true and all false variables
    falser = []
    truer = []
    #find and store all true and false variables
    for x in formula:
        for j in x:
            if j > 0:
                truer.append(j)
            else:
                falser.append(j)
    #list to hold only true variables and only false variables
    true_only = []
    false_only = []
    #find and store all only true variables and only false variables
    for x in truer:
        if -x not in falser and x not in true_only:
            true_only.append(x)
            true.append(x)
    for x in falser:
        if -x not in truer and x not in false_only:
            false_only.append(-x)
            false.append(-x)
    #Set these variables to true or false in the branch
    new_true += true_only
    new_false += false_only
    i = 0
    #For the cnf
    while True:
        removal = False
        for j in formula[i]:
            #If an only true or only false variables is in a clause
            #Remove the clause
            if j in new_true or -j in new_false:
                removal = True
        if removal:
            formula.remove(formula[i])
            i -= 1
        i += 1
        if i == len(formula):
            break
    for x in true_only:
        formula.append([x])
    for x in false_only:
        formula.append([-x])
    return formula, new_true, new_false

#Append the opposite of the input set to the cnf
#forcing the input set to be true
def remove_set(input):
    input = input.split(",")
    var = []
    for x in input:
        if x.find("~") == -1:
            var.append((x[1:]) + " 0\n")
        else:
            var.append(str(-int(x[2:])) + " 0\n")
    return var

#Used to remove duplicates
def sim_dupl(form):
    sum = []
    for x in form:
        if x not in sum:
            sum.append(x)
    return sum


#Used to find the minimum input set that makes a function true
def minimum(formula, inset):
    #split the input set and find the opposite of it
    inset = inset.split(",")
    oppo = [x[1:] if x.find("~")!=-1 else "~"+x for x in inset ]

    #split the function by OR, then AND
    form = formula.split("+")
    form = [k.split(".") for k in form]
    removal = []
    #Delete elements of function with an opposite of the input set
    for x in form:
        rem = False
        for k in x:
            if k in oppo:
                rem = True
        if not rem: removal.append(x)
    #find the shortest of the remaining AND operations
    smallest = [0] * 10000000
    for x in removal:
        if len(x) < len(smallest):
            smallest = x
    sm = ""
    #send to output string in cnf form
    for x in smallest:
        if x.find("~") != -1:
            sm += "-" + x[2:] + " "
        else:
            sm += x[1:] + " "
    print("Smallest set of input Variables: ", sm + " 0")
    return sm[: len(sm) - 1]



if __name__ == "__main__":
    sat("out.cnf")
