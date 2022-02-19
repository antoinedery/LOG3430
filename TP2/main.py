from criteres import getCACC, getGICC, getIC, getTable, p_Table, p_implicant_tests, p_tests

###############################################

table = getTable()
print('\n')
print("Table: \n")
print(" p  h  u  g  z ")
print(" ............. ")
p_Table(table[0])
print("Implicants: \n")
print("    P          ")
print(" P  U     -    ")
print(" H  -  -  H  - ")
print(" U  G  P  G  U ")
print(" ............. ")
p_Table(table[1])

################### CACC ######################

testsCACC = getCACC(table[0])
p_tests(testsCACC)

################### GICC ######################

testsGICC = getGICC(table[0])
p_tests(testsGICC)

################### GICC ######################
testsGICC = getIC(table[1])
p_implicant_tests(testsGICC)