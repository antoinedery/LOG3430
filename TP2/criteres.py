def verifyIsSpam(p, h, u, g):
    return p and ((h and u) or (u and not g))

def verifyIsSpamDNF(p, h, u, g):
    return p and h and u or u and not g

def getTable():
    counter = 0
    table = {}
    for p in [False, True]:
        for h in [False, True]:
            for u in [False, True]:
                for g in [False, True]:
                    table[counter] = [p,h,u,g, verifyIsSpam(p,h,u,g)]
                    counter += 1
    return table

def get_major_clause_tests(table):
    clauses = ['p', 'h', 'u', 'g']
    cPerRow = {}
    for elem in clauses:
        cPerRow[elem] = set()

    for cIdx, clause in enumerate(clauses):
        for i, row in enumerate(table.values()):
            tmpRow = row.copy()
            tmpRow[cIdx] = not tmpRow[cIdx] # inverse le input de la clause majeure
            tmpRow[4] = not tmpRow[4]       # inverse le output du résultat
            for j, nRow in enumerate(table.values()):
                if nRow == tmpRow:
                    cPerRow[clause].add(i)
                    cPerRow[clause].add(j)
                    break
    return cPerRow

def apply_cacc(tests, table):
    pair_found = False
    retained_tests = {}
    for idx, key in enumerate(tests):
        tList = tests[key]
        for i in tList:
            fRow = table[i].copy()
            nC = not fRow[idx]
            nP = not fRow[4]
            for j in tList:
                sRow = table[j]
                if((nC == sRow[idx]) & (nP == sRow[4])):
                    retained_tests[key] = set()
                    retained_tests[key].add(i)
                    retained_tests[key].add(j)
                    pair_found = True
                    break
            if(pair_found):
                pair_found = False
                break      

    return retained_tests

def p_Table(table):
    for key in table:
        print(str(key) + ' : ' + str(table[key]))
    print('\n')

def p_rows(tests):
    for key in tests:
        output = str(key) + ' => '
        tList = tests[key]
        for idx, row in enumerate(tList):
            output += 'd' + str(row)
            if(idx < (len(tList) - 1)):
                output += ', '
        print(output)
    print('\n')


table = getTable()
p_Table(table)

################### CACC ######################

tests = get_major_clause_tests(table)
valid_pairs = apply_cacc(tests, table)
print('CACC : ')
p_rows(valid_pairs)


################### GICC ######################

def getGICC():
    clauses = ['p', 'h', 'u', 'g']
    cPerRow = {}
    for elem in clauses:
        cPerRow[elem] = set()

    for cIdx, clause in enumerate(clauses):
        for i, row in enumerate(table.values()):
            tmpRow = row.copy()
            tmpRow[cIdx] = not tmpRow[cIdx] 
            if(mapcontaine(tmpro[4]))
            else:
                for j, nRow in enumerate(table.values()):
                    if nRow == tmpRow:
                        cPerRow[clause].add(i)
                        cPerRow[clause].add(j)
                        mapPush(false)
                        break
    return cPerRow