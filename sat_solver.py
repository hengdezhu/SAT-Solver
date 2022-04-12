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