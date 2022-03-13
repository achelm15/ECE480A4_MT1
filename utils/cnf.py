import numpy as np

def bool_to_cnf(func, addition):
    l = func.split("+")
    sum = []
    out = []
    line_count, var = count_var(func)
    #For each and gate
    for x in l:
        #If it is just a single variable
        if x.find('.')==-1:
            #If the single variable is not-ed
            if x.find('~')!=-1:
                out.append(not_cnf(x, "x"+str(line_count)))
                sum.append("x"+str(line_count))
                line_count += 1
                continue
            sum.append(x)
            continue

        #For each and within the product
        while x.find('.')!=-1:
            #If one of the inputs is not-ed
            while x.find('~')!=-1:
                if x[x.find('~'):].find('.')==-1:
                    out.append(not_cnf(x[x.find('~'):],"x"+str(line_count)))
                    x = x[:x.find('~')]+"x"+str(line_count)
                else:
                    out.append(not_cnf(x[x.find('~'):][:x[x.find('~'):].find('.'):],"x"+str(line_count)))
                    x = x[:x.find('~')] + "x"+str(line_count)+x[x.find('~'):][x[x.find('~'):].find('.'):]
                line_count+=1
            #If it is a single and
            if x.count(".")==1:
                out.append(and_cnf(x,"x"+str(line_count)))
                sum.append("x"+str(line_count))
                line_count += 1
                break
            #If there are multiple ands remaining
            k = x[x.index('.')+1:].index(".")+1
            out.append(and_cnf(x[:x.index('.')+k],"x"+str(line_count)))
            x = "x"+str(line_count)+x[x.index('.')+k:]
            line_count += 1
    #For each or gate
    while len(sum):
        #For the last or gate
        if len(sum)==1:
            out.append(sum[0][1:]+"\n")
            sum = []
            break
        #Or the first two variables
        out.append(or_cnf(sum[0]+"+"+sum[1], "x"+str(line_count)))
        #Remove the first two variables from the sum, add the output variable to the sum
        temp = ["x"+str(line_count)]
        for x in sum[2:]:
            temp.append(x)
        sum = temp
        line_count += 1
    #Write the initial CNF to the outputfile
    outFile = open("cnf.cnf", "w")
    for x in out:
        outFile.write(x)
    outFile.close()
    #Count the number of clauses
    file1 = open('cnf.cnf', 'r')
    lines = file1.readlines()
    file1.close()
    clauses = len(lines)
    #Write the header to the file
    outFile = open("cnf.cnf", "w")
    outFile.write("p cnf "+str(clauses)+" "+str(line_count-1)+"\n")
    for x in range(len(lines)):
        outFile.write(lines[x][:len(lines[x])-1]+" 0\n")
    for x in addition:
        outFile.write(x)
    outFile.close()
    return var

#Function to find the number of input variables
#And determine the next highest variable number
#to use for output of gates in cnf
def count_var(func):
    #split function by ORs
    l = func.split("+")
    var = []
    #split ANDS and find unique variables
    for x in l:
        o = x.split(".")
        for j in o:
            if j.find("~")!=-1:
                j = j[1:]
            if j not in var:
                var.append(j)
    high = -1
    #Determine the highest variable number
    #ie if x1,x2,x3,x4 are used, high would be 5
    for x in var:
        if int(x[1:])>high:
            high = int(x[1:])
    return high+1, var

#Function to create and cnf in string form
def and_cnf(func, out):
    l = func.split(".")
    out = "{a} -{c}\n{b} -{c}\n-{a} -{b} {c}\n".format(a=l[0][1:],b=l[1][1:],c=out[1:])
    return out

#Function to create or cnf in string form
def or_cnf(func, out):
    l = func.split("+")
    out = "-{a} {c}\n-{b} {c}\n{a} {b} -{c}\n".format(a=l[0][1:],b=l[1][1:],c=out[1:])
    return out

#Function to create not cnf in string form
def not_cnf(func, out):
    l = func.split("~")
    out = "{a} {c}\n-{a} -{c}\n".format(a=l[1][1:],c=out[1:])
    return out

#################### XOR functions ############################################

# inverts from SoP to PoS
def invert(lst):
    new_lst = []
    
   #----for each clause, split on . invert sign and restitch--------------
    
   #iterate through clauses
    for i in range(len(lst)):
        #split on . 
        tmp = lst[i].split('.')
        
        #iterate through clause
        tmp_lst = []
        for item in tmp:
            
            #invert signs
            if item.startswith('~'):
                var = item.split('~')
                inverse = var[1]
            else:    
                inverse = '~{}'.format(item)
            # add to temp list with .
            tmp_lst.append('{}+'.format(inverse))
        #join temp list to string
        new_arg = "".join(tmp_lst)
    
        #replace in original lst
        
        new_lst.append(new_arg)
        
        #take last . off
        for i in range(len(new_lst)):
            new_lst[i] = new_lst[i].rstrip('+')
           
    return new_lst

# helper for expand, take list of form [x1.x2,x3.x4] and return 'x1.x2+x3.x4'
def format_sop(lst):
    new_lst = []
    for item in lst:
        new_lst.append('{}+'.format(item))
    sop_str  = "".join(new_lst)
    return sop_str[:len(sop_str)-1]
 
# multiply PoS clause values by eachother
# inputs are in form ['x1+x2','x3+x4'] from invert
def expand(lst):
    
    #--------- expand first 2 terms 
    # split first clause at +
    
    c0 = lst[0].split('+')
    c1 = lst[1].split('+')
    
    # make new list with combined terms
    final = []
    # iterate through first clause
    for item in c0:
        #iterate through second clause
        for var in c1:
            final.append('{}.{}'.format(item, var))
    # return final if there are only two terms
    if len(lst) <= 2:
        final = format_sop(final)
        return final
    else:
        # if there are more than 2 clauses, create terms with final
        final2 = []
        k = 2
        # iterate through list starting at lst[2]
        while k < len(lst):
            # split lst[k] at +
            cx = lst[k].split('+')
            #append term with each of cx to each of final
            for item in final:
                for var in cx:
                    final2.append('{}.{}'.format(item,var))
            k = k + 1
        final2 = format_sop(final2)
        return final2


def var_list(string):
    # split to product groups
    p_groups = string.split('+')
    
    return p_groups

# xor creates the POS version of the input by inverting and xor'ing
 
def xor(func1, func2):

    # split functions into seaprate arguments
    vars1, vars2 = var_list(func1), var_list(func2)

    #invert sign terms and return in PoS form
    inv1,inv2 = invert(vars1), invert(vars2)
       
    #expand to SoP form
    exp1,exp2 = expand(inv1) , expand(inv2)
    
    # TODO add checker for redundant and impossible terms
    
    # implement XOR by expanding exp and func
    
    in1 = [exp1,func2]
    in2 = [exp2,func1]
    
    xor1 = expand(in1)
    xor2 = expand(in2)
   
    return '{}+{}'.format(xor1,xor2)
    
# TODO change bool_to_cf to allow for different files to be written
# TODO implement bool_to_cf in xor for result 
# =============================================================================
# test1 = 'a.b+c.d'
# test2 = 'a.c+b.c'
# 
# a = xor(test1,test2)
# print(a)
# 
# bool_to_cnf('x1.x2+x1.x3')
# =============================================================================

#Function to perform XOR of two boolean expressions
def xor2(f,s):
    #split functions into array of arrays, where the outer
    #array represents ORs of elements, and the arrays represent 
    #ANDs of elements
    f = f.split("+")
    s = s.split("+")
    for i in range(len(f)):
        f[i]=f[i].split(".")
    for i in range(len(s)):
        s[i]=s[i].split(".")
    
    #Perform De Morgan's Law on the function to account
    #For negated inputs in XOR = ~A.B+A.~B
    #Remove duplicated terms
    deMorganF = removal(deMorgan(f))
    deMorganS= removal(deMorgan(s))
    #Perform the two ANDS, ~f.s, ~s.f
    temp = mult2(deMorganF,s)
    temp2 = mult2(deMorganS,f)
    #Perform the OR operation
    xor = temp + temp2
    mul = []
    for x in xor:
        mul.append(".".join(x))
    out = "+".join(mul)
    return out

#Function to perform DeMorgan's Law
def deMorgan(f):
    notf = []
    #Invert all the inputs in the AND gates
    for x in f:
        temp = []
        for j in x:
            if j.find("~")==-1: temp.append("~"+j)
            else: temp.append(j[1:])
        notf.append(temp)
    #AND the two ORs together
    return mult(notf)

#Function to AND multiple sums
def mult(notf):
    #Loop through input POS function
    while len(notf)>1:
        #Multiply the first two terms
        temp = []
        for x in notf[0]:
            for j in notf[1]:
                temp.append(x+"."+j)
        #Replace the first two terms with their product
        notf = [temp] + notf[2:]
    #Convert back to array
    notf = [x.split(".") for x in notf[0]]
    #Remove duplicate terms
    out = [sorted(np.unique(np.asanyarray(x,dtype=object)).tolist()) for x in notf]
    return out

#Used to multiply SUMs
def mult2(f,s):
    out = []
    for x in f:
        for j in s:
            temp = np.unique(x+j).tolist()
            out.append(temp)
    return removal(out)

#Used to remove duplicate terms
def removal(out):
    out2 = []
    for x in out:
        flag = False
        for j in x:
            if j[1:] in x or "~"+j in x:
                flag = True
        if not flag:
            out2.append(x)
    return out2

