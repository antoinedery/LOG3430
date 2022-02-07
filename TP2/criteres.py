def verifyIsSpam(p, h, u, g):
    return p and ((h and u) or (u and not g))


def verifyIsSpamDNF(p, h, u, g):
    return p and h and u or u and not g

# def createTruthTable():
#     counter = 0
#     table = {}
#     for p in [False, True]:
#         for h in [False, True]:
#             for u in [False, True]:
#                 for g in [False, True]:
#                     table[counter] = [p,h,u,g, verifyIsSpam(p,h,u,g)]
#                     counter += 1
#     return table

def createTruthTable():
    counter = 0
    table = {}
    for p in [0, 1]:
        for h in [0, 1]:
            for u in [0, 1]:
                for g in [0, 1]:
                    table[counter] = [p,h,u,g, verifyIsSpam(p,h,u,g)]
                    counter += 1
    return table

def printTruthTable():
    table = createTruthTable()
    for key in table:
        print(str(key) + ' : ' + str(table[key]))

printTruthTable()