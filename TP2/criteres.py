def verifyIsSpam(p, h, u, g):
	return p and ((h and u) or (u and not g))

# s = PHU | PU-G
def DNF(p, h, u, g):
	return p and h and u or p and u and not g

# s = -P | -HG | -U
def inverseDNF(p, h, u, g):
	return not p or not h and g or not u

def getTable():
	counter = 0
	table1 = {}
	table2 = {}
	for p in [0, 1]:
		for h in [0, 1]:
			for u in [0, 1]:
				for g in [0, 1]:
					table1[(p,h,u,g, verifyIsSpam(p,h,u,g)*1)] = counter
					val = (
							(p and h and u) * 1, 
							(p and u and not g) * 1,
							(not p) * 1,
							(not h and g) * 1,
							(not u) * 1
					)
					if val not in table2: table2[val] = counter
					counter += 1
	return [table1, table2]

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

def getIC(table):
	print('IC : ')
	implicant = ["PHU", "PU-G", "-P", "-HG", "-U"]
	isValid = False
	cPerRow = set()
	tmpRow = getHighestRow(table)
	cPerRow.add(tmpRow)
	for i in range(4):
		if tmpRow[i] == 0:
			for elem in table:
				if elem[i] == 1:
					cPerRow.add(elem)
					tmpRow = (tmpRow or elem) * 1
					if rowIsValid(tmpRow) == True:
						isValid = True
						break
		if isValid == True:
			break

	dic = {}
	
	for elem in cPerRow:
		dic[table[elem]] = set()
		for i, j in enumerate(elem):
			if j == 1: dic[table[elem]].add(implicant[i])

	return dic



def getHighestRow(table):
	rtnRow = (0,0,0,0,0)
	ctr = 0
	for row in table:
		res = sum(list(row))
		if ctr < res: 
			ctr = res
			rtnRow = row
	return rtnRow

def rowIsValid(row):
	for elem in row:
		if elem is False: return False
	return True

def p_Table(table):
	for key in table:
		print(str(key) + ' : ' + str(table[key]))
	print('\n')

def p_tests(tests):
	for key in tests:
		output = str(key) + ' => '
		tList = tests[key]
		for idx, row in enumerate(tList):
			output += 'd' + str(row[0]) + ', d' + str(row[1])
			if(idx < (len(tList) - 1)):
				output += ', '
		print(output)
	print('\n')

def p_implicant_tests(tests):
	for key, value in tests.items():
		output = ''
		for i, impl in enumerate(value):
			output += impl 
			if(i < (len(value) - 1)):
				output += " ; "
		print(output + ' => d' + str(key) )
	print('\n')

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