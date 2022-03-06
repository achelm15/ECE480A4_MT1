def sat(file):
    inFile = open(file, 'r')
    lines = inFile.readlines()
    header = lines[0]
    lines = lines[1:]
    header = header.split(" ")
    clauses = int(header[2])
    num_var = int(header[3])
    print(clauses, num_var)
    print(lines)
