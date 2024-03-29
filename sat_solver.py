# load a file in DIMACS format
def load_dimacs(file):
    r = []
    
    with open(file) as f:
        lines = f.readlines()
    
    for line in lines:
        a = []
        l = line.split(' ')
        if l[0] != 'p' and l[0] != 'c':
            for i in range(len(l) - 1): # minus 1 for skip 0
                a.append(int(l[i]))
            r.append(a)
            
    return r

# find a satisfying assignment by running through all truth assignments
def conversion(i, v):   # [1,0,1] --> [1, -2, 3]
    if v == 1:
        return i+1
    else:
        return -(i+1)

def simple_sat_solve(sat):
    if sat == [[]]:
        return 'unsat'

    a = [] # all truth assignments
    p = -1 # the index of satisfying assignment
    N = 0
    M = len(sat)

    # find out the number of variables
    flat = sum(sat, []) # flat the array
    N = max([abs(x) for x in flat])

    # convert number to binary format to produce truth table
    for i in range(2**N):
        f = "{0:0"+str(N)+"b}" # "{0:b}".format(37)
        a.append([int(i) for i in str(f.format(i))])

    # iternate all assignments
    for i in range(len(a)):
        l = [x==1 for x in a[i]] # convert binary to True/False
        t = [] # record the status of each clause

        # evaluate each clause and record it
        for j in range(M):  # iterate every clause
            e = sat[j]    # i.e. e=[1,-1]
            
            s = False # initial status of literal
            
            for k in range(len(e)):
            # evaluate every literal, if there is any True, break the current loop
            # and that means the current clause is True; if s remains False, that
            # means this clause is false
                if e[k] < 0:    # i.e., e[0]=1
                    s = not l[abs(e[k])-1]  # abs(e[k]) is the index of the variables, -1 is because of the index
                else:
                    s = l[abs(e[k])-1]
                    
                if s:
                    break
            
            t.append(s)    # record the result of each clause
        
        if all(t):
            p = i
            break   # just find one satisfying assignment and then return

    # return the search result
    if p != -1:
        return [conversion(x,index) for x, index in enumerate(a[p])] # return one of satisfying assignment
    else:
        return 'unsat'
        
# Backtracking
import copy

def remove_e(l, e): # remove the elements from the list
    c = l.count(e)
    for i in range(c):
        l.remove(e) 

def branching_sat_solve(sat, p):    # partial_assigment (i.e., [1, -3])
    M = len(sat)        # M clauses
    P = len(p)          # N fixed variables
    t_p = p.copy()
    
    # iterate each partial assignment
    for i in range(P):
        r_c = []            # record the index of the clause that should be removed
        
        for j in range(len(sat)):
            if t_p[i] > 0:  # x is True
                if t_p[i] in sat[j]:  # remove that clause consisting x
                    if j not in r_c:
                        r_c.append(j)
                if -t_p[i] in sat[j]: # remove the literal of !x
                    remove_e(sat[j], -t_p[i])
            else:           # x is False
                if abs(t_p[i]) in sat[j]: # remove the literal of x
                    remove_e(sat[j], -t_p[i])
                if -abs(t_p[i]) in sat[j]:
                    if j not in r_c:
                        r_c.append(j)
                        
        for e in sorted(r_c, reverse = True):
            del sat[e]
                
    # if sat contains empty clause or sat is [[]]
    if [] in sat or sat == [[]]:
        return 'unsat'
    
    # if F has no clauses, return [] which means what the values of the rest of variables do not matter
    if sat == []:
        return t_p
        
    # choose the last variable x in sat that is *
    # find out the number of variables
    flat = sum(sat, []) # flat the array
    x = max([abs(e) for e in flat])
    
    # assign True to the variable x
    temp = branching_sat_solve(copy.deepcopy(sat), [x])
    if temp != 'unsat':
        return temp + t_p
    # assign False to the variable x
    temp = branching_sat_solve(copy.deepcopy(sat), [-x])
    if temp != 'unsat':
        return temp + t_p
        
    return 'unsat'
    
# Unit Propagation
def unit_propagate(clause_set):
    while True:
        l = [len(c) for c in clause_set]
        try:
            index = l.index(1)          # identify an unit clause, the length of unit clause is 1
            x = clause_set[index][0]    # read the value of that unit clause
            # if x > 0:
            #     p = x                   # to make the clause True, x need to be True
            # else:
            #     p = x
            p = [x]
            simplification(clause_set, p)
        except:                         # no unit clauses anymore
            break
    
    return clause_set
    
# Pure Literal Elimination
def pure_literal_eliminate(clause_set):
    while True:
        flat = sum(clause_set, [])          # flatten F
        flat = list(dict.fromkeys(flat))
        p = []                              # pure literals (also satisfying partial assignments)
        
        for i in range(len(flat)):
            if -flat[i] not in flat and flat[i] not in p:   # check if there is ¬x
                p.append(flat[i])
                
        if p != []:                         # if there are any literals
            simplification(clause_set, p)
        else:
            return clause_set               # return the most simplified F
            
# The DPLL Algorithm
def dpll_sat_solve(clause_set, p):
    # simiplify the set of clauses
    simplification(clause_set, p)

    # unit propagation
    u_p = []                            # partial assignments got from unit propagation
    while True:
        l = [len(c) for c in clause_set]
        try:
            index = l.index(1)          # identify an unit clause, the length of unit clause is 1
            x = clause_set[index][0]    # read the value of that unit clause
            # if x > 0:
            #     p = x                 # to make the clause True, x need to be True
            # else:
            #     p = x
            t_p = [x]                   # temp p
            u_p.append(x)
            simplification(clause_set, t_p)
        except:                         # no unit clauses anymore
            break

    # pure literal elimination
    p_p = []                            # partial assignments got from unit propagation
    while True:
        flat = sum(clause_set, [])          # flatten F
        flat = list(dict.fromkeys(flat))
        t_p = []                              # pure literals (also satisfying partial assignments)
        
        for i in range(len(flat)):
            if -flat[i] not in flat and flat[i] not in p:   # check if there is ¬x
                t_p.append(flat[i])
                
        if t_p != []:                         # if there are any literals
            p_p.extend(t_p)
            simplification(clause_set, t_p)
        else:
            break                           # return the most simplified F
            
    
    # branching sat solver
    
    # if sat contains empty clause or sat is [[]]
    if [] in clause_set:
        return 'unsat'
    
    # if F has no clauses, return [] which means what the values of the rest of variables do not matter
    if clause_set == []:
        return p + u_p + p_p
        
    # choose the last variable x in sat that is *
    # find out the number of variables
    flat = sum(clause_set, []) # flat the array
    x = max([abs(e) for e in flat])
    
    # assign True to the variable x
    temp = dpll_sat_solve(copy.deepcopy(clause_set), [x])
    if temp != 'unsat':
        return temp + p + u_p + p_p
    # assign False to the variable x
    temp = dpll_sat_solve(copy.deepcopy(clause_set), [-x])
    if temp != 'unsat':
        return temp + p + u_p + p_p
        
    return 'unsat'