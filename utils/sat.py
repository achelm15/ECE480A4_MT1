import copy

def sat(file):
    inFile = open(file, 'r')
    lines = inFile.readlines()
    header = []
    count = 0
    for x in lines:
        if x[0]=='c':
            count+=1
            continue
        if x[0]=='p':
            header = x
            count+=1
            break
    lines = lines[count:]
    header = header.split()
    num_clauses = int(header[2])
    num_var = int(header[3])
    formula = create_formula(lines)
    global true, false
    true, false = [], []
    if dpll(formula):
        print("SAT")
        print("Solution:")
        print("\tTrue variables: ", true)
        print("\tFalse variables: ", false)
    else:
        print("UNSAT")

def dpll(formula):
    res = []
    [res.append(x) for x in formula if x not in res]
    formula = res
    formula, new_true, new_false = unit_propogate(formula)
    formula, new_true, new_false = pure_literal(formula, new_true, new_false)
    if len(formula)==0:
        return True
    null = False
    new_var = []
    for x in formula:
        if len(x)==0:
            null = True
        else:
            for j in x:
                if abs(j) not in new_var:
                    new_var.append(abs(j))
    new_var = sorted(new_var)
    if null:
        for i in new_true:
            true.remove(i)
        for i in new_false:
            false.remove(i)
        return False
    pos = copy.deepcopy(formula)
    neg = copy.deepcopy(formula)
    pos.append([new_var[0]])
    neg.append([-new_var[0]])
    if dpll(pos):
        return True
    elif dpll(neg):
        return True
    else:
        for i in new_true:
            true.remove(i)
        for i in new_false:
            false.remove(i)
        return False

def create_formula(lines):
    formula = []
    count = 1
    for x in lines:
        var_list = []
        for j in x[:len(x)-3].split():
            var_list.append(int(j))
        formula.append(var_list)
        count += 1
    return formula

def unit_propogate(formula):
    unit = [j[0] for j in formula if len(j)==1]
    new_true = []
    new_false = []
    if len(unit)!=0:
        for u in unit:
            if u<0:
                false.append(-u)
                new_false.append(-u)
                i = 0
                while True:
                    if u in formula[i]:
                        formula.remove(formula[i])
                        i -= 1
                    elif -u in formula[i]:
                        formula[i].remove(-u)
                    i += 1
                    if i==len(formula):
                        break
            else:
                true.append(u)
                new_true.append(u)
                i = 0
                while True:
                    if u in formula[i]:
                        formula.remove(formula[i])
                        i -= 1
                    elif -u in formula[i]:
                        formula[i].remove(-u)
                    i += 1
                    if i==len(formula):
                        break
    return formula, new_true, new_false

def pure_literal(formula, new_true, new_false):
    if len(formula)==0:
        return formula, new_true, new_false
    falser = []
    truer = []
    for x in formula:
        for j in x:
            if j>0: truer.append(j)
            else: falser.append(j)
    true_only = []
    false_only = []
    for x in truer:
        if -x not in falser and x not in true_only:
            true_only.append(x)
            true.append(x)
    for x in falser:
        if -x not in truer and x not in false_only:
            false_only.append(x)
            false.append(-x)
    new_true += true_only
    new_false += false_only
    i = 0
    while True:
        removal = False
        for j in formula[i]:
            if j in new_true or j in new_false:
                removal = True
        if removal:
            formula.remove(formula[i])
            i -= 1
        i += 1
        if i == len(formula):
            break
    return formula, new_true, new_false