def verifyIsSpam(p, h, u, g):
    return p and ((h and u) or (u and not g))

def verifyIsSpamDNF(p, h, u, g):
    return p and h and u or u and not g

def getTable():
    counter = 0
    table = {}
    for p in [0, 1]:
        for h in [0, 1]:
            for u in [0, 1]:
                for g in [0, 1]:
                    rtn = 0
                    if(verifyIsSpam(p,h,u,g)): rtn = 1
                    table[(p,h,u,g, rtn)] = counter
                    counter += 1
    return table

def getCACC(table):
    print('CACC : ')
    clauses = ['p', 'h', 'u', 'g']
    cPerRow = {}
    for cIdx, clause in enumerate(clauses):
        for key in table:
            l = list(key)
            l[cIdx] = not l[cIdx] 
            l[4] = not l[4]  
            t = tuple(l)
            if t in table:
                cPerRow[clause] = set()
                cPerRow[clause].add((table[key], table[t]))
                break
    return cPerRow

def getGICC(table):
    print('GICC : ')
    clauses = ['p', 'h', 'u', 'g']
    cPerRow = {}
    for elem in clauses:
        cPerRow[elem] = set()
    for i, clause in enumerate(clauses):
        foundTests = False
        nPredicate = set() 
        for row in table:
            if row[4] not in nPredicate :
                cl = not row[i] 
                for nRow in table:
                    if((cl == nRow[i]) & (row[4] == nRow[4])):
                        cPerRow[clause].add((table[row], table[nRow]))
                        nPredicate.add(row[4])
                        if len(nPredicate) >= 2: 
                            foundTests = True
                        break
            if foundTests:
                break
    return cPerRow

def p_Table(table):
    for key in table:
        print(str(key) + ' : ' + str(table[key]))
    print('\n')

def p_rows(tests):
    for key in tests:
        output = str(key) + ' => '
        tList = tests[key]
        for idx, row in enumerate(tList):
            output += 'd' + str(row[0]) + ', d' + str(row[1])
            if(idx < (len(tList) - 1)):
                output += ', '
        print(output)
    print('\n')

###############################################

table = getTable()
p_Table(table)

################### CACC ######################

testsCACC = getCACC(table)
p_rows(testsCACC)

################### GICC ######################

testsGICC = getGICC(table)
p_rows(testsGICC)