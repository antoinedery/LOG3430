# def createTruthTable():
#     counter = 0
#     table = {}
#     for p in [0, 1]:
#         for h in [0, 1]:
#             for u in [0, 1]:
#                 for g in [0, 1]:
#                     table[counter] = [p,h,u,g, verifyIsSpam(p,h,u,g)]
#                     counter += 1
#     return table

def verifyIsSpam(p, h, u, g):
    return p and ((h and u) or (u and not g))


def verifyIsSpamDNF(p, h, u, g):
    return p and h and u or u and not g

def createTruthTable():
    counter = 0
    table = {}
    for p in [False, True]:
        for h in [False, True]:
            for u in [False, True]:
                for g in [False, True]:
                    table[counter] = [p,h,u,g, verifyIsSpam(p,h,u,g)]
                    counter += 1
    return table

def printTruthTable():
    table = createTruthTable()
    for key in table:
        print(str(key) + ' : ' + str(table[key]))

printTruthTable()

def find_major_clause():
    clauses = ['p', 'h', 'u', 'g']
    table = createTruthTable()

    cPerRow = {}
    for elem in clauses:
        cPerRow[elem] = set()

    for cIdx, clause in enumerate(clauses):
        # foundPair = False
        for row in table.values():
            tmpRow = row.copy()
            tmpRow[cIdx] = not tmpRow[cIdx] # inverse le input de la clause majeure
            tmpRow[4] = not tmpRow[4]       # inverse le output du résultat
            for nRow in table.values():
                # si les clauses mineures sont égales pour un résultat et une clause majeure différents, RACC est respecté
                if nRow == tmpRow:
                    cPerRow[clause].add(tuple(row))
                    cPerRow[clause].add(tuple(nRow))
                    break
    return cPerRow

def print_valid_tests(tests):
    for key in tests:
        print(str(key) + ' : ')
        tList = tests[key]
        for row in tList:
            print(str(row))

tests = find_major_clause()
print_valid_tests(tests)

def find_cacc(tests):
    for idx, key in enumerate(tests):
        tList = tests[key]
        for row in tList:
            tmpRow = row.copy()
            nC = not tmpRow[idx]
            nP = not tmpRow[4]
            for nRow in tList:
                if((nC == nRow[idx]) & (nP == nRow[4])):
                    
