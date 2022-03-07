def bool_to_cnf(func):
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
    outFile.write("p cnf "+str(clauses)+" "+str(line_count)+"\n")
    for x in range(len(lines)):
        outFile.write(lines[x][:len(lines[x])-1]+" 0\n")
    outFile.close()
    return var

def count_var(func):
    l = func.split("+")
    var = []
    for x in l:
        o = x.split(".")
        for j in o:
            if j.find("~")!=-1:
                j = j[1:]
            if j not in var:
                var.append(j)
    high = -1
    for x in var:
        if int(x[1:])>high:
            high = int(x[1:])
    return high+1, var

def and_cnf(func, out):
    l = func.split(".")
    out = "{a} -{c}\n{b} -{c}\n-{a} -{b} {c}\n".format(a=l[0][1:],b=l[1][1:],c=out[1:])
    return out

def or_cnf(func, out):
    l = func.split("+")
    out = "-{a} {c}\n-{b} {c}\n{a} {b} -{c}\n".format(a=l[0][1:],b=l[1][1:],c=out[1:])
    return out

def not_cnf(func, out):
    l = func.split("~")
    out = "{a} {c}\n-{a} -{c}\n".format(a=l[1][1:],c=out[1:])
    return out

def xor(func1, func2):
    print("hi")
    return "6"

