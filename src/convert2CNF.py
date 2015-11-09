'''
#################################################
Name - Vinayak Mittal
NET ID - VMITTAL
SBU ID - 110385943

Name - Alpit Gupta
NET ID - ALGUPTA
SBU ID - 110451714
#################################################
'''

import sys
from itertools import product, combinations
from copy import deepcopy

'''
Reference:
https://en.wikipedia.org/wiki/Conjunctive_normal_form#Conversion_into_CNF
'''
def parse_file(filepath):
    # read the layout file to the board array
    board = []
    fin = open(filepath)
    
    row, col = fin.readline().split()
    row = int(row)
    col = int(col)
    x_cnt = 0
    
    line =  fin.readline()
    while line:
        line=line.strip('\n')
        board.append(line.split(','))
        line = fin.readline();        
    
    #Reversed the board to match input specifications
    board.reverse()
    
    #Storing board hints and negative value in place of X.        
    for i in range(0,row):
        for j in range(0,col):
            if board[i][j] == 'X':
                x_cnt += 1
                board[i][j] = -x_cnt
            else:
                board[i][j] = int(board[i][j]) 
                    
    fin.close()
    return board, row, col, x_cnt

'''
convert2CNF finds the CNF equivalent across all the hint positions on the board.
We have learnt of introducing the new variables from WIKI to reduce exponential time
to linear time.
Link: https://en.wikipedia.org/wiki/Conjunctive_normal_form#Conversion_into_CNF
'''
def convert2CNF(board, row, col, x_cnt, output):
    # interpret the number constraints

    hints = getBoardHints(board, row, col) 
    cnf = [] #holds the final CNF of the board
    total_variables = x_cnt
    
    for hint in hints:
        r,c = hint
        val = board[r][c]
        '''Finding all neigbours for the cell'''
        nbr_list = findNeighbours(board,hint,row,col)

        
        '''Checking if the input board is invalid'''        
        if (val > len(nbr_list)):
            print "Invalid Board Passed!"
            exit(-1)
        
        if val>0:
            '''Finding all possible combinations.'''
            comb = list(combinations(nbr_list, val)) 
                        
            dnf = [] 
            
            #Finding DNF                      
            for i in range(len(comb)):
                domain = deepcopy(nbr_list)                
                domain[:] = [-1*l for l in domain]                                    
                
                temp = list(comb[i])
                
                for k in range(len(domain)):
                    if -1*domain[k] in temp:
                        domain[k] = domain[k] * -1
                         
                if domain not in dnf:
                    dnf.append(domain)
                                                            
            
            tmp_cnf = []                 
            
            if len(dnf) == 1:
                for i in range(len(dnf[0])):
                    if [dnf[0][i]] not in cnf:
                        cnf.append([dnf[0][i]])
            else:
                dnf_count = len(dnf)
                new_var = []
                
                for i in range(1, dnf_count+1):
                    new_var.append(x_cnt + i)
                    total_variables = total_variables + 1                                                
                
                tmp_cnf.append(new_var)

                                
                for y in range(0,len(new_var)):
                    elem = new_var[y]*-1;                    
                    local_dnf = dnf[y]
                    
                    for i in range(len(local_dnf)):
                        local_cnf = []
                        local_cnf.append(elem)
                        local_cnf.append(local_dnf[i])                           
                        tmp_cnf.append(local_cnf)
                
                for y in range(0, len(tmp_cnf)):                    
                    if tmp_cnf[y] not in cnf:
                        cnf.append(tmp_cnf[y])
                          
    print "CNF",cnf
    fout = open(output, 'w')
    fout.write("p cnf %d %d\n" %(total_variables,len(cnf)))
    for i in range(0, len(cnf)):
        for j in range(0, len(cnf[i])):
                fout.write(str(cnf[i][j]) + " ");

        fout.write("0 \n");

    fout.close()

'''
Finding neighbours for all possible board hints.
'''
def findNeighbours(board,hint,row,col):
    nbr_list = []
    r,c = hint   
     
    if r+1 >= 0 and r+1 < row:
        if board[r+1][c] < 0:
            nbr_list.append(-1*board[r+1][c])
        
    if r-1 >= 0 and r-1 < row:
        if board[r-1][c] < 0:
            nbr_list.append(-1*board[r-1][c])
        
    if c+1 >=0 and c+1 < col:
        if board[r][c+1] < 0:
            nbr_list.append(-1*board[r][c+1])
        
    if c-1 >=0 and c-1 < col:
        if board[r][c-1] < 0:
            nbr_list.append(-1*board[r][c-1])
        
    if r+1 >= 0 and r+1 < row and c-1 >=0 and c-1 < col:
        if board[r+1][c-1] < 0:
            nbr_list.append(-1*board[r+1][c-1])
        
    if r-1 >= 0 and r-1 < row and c-1 >=0 and c-1 < col:
        if board[r-1][c-1] < 0:
            nbr_list.append(-1*board[r-1][c-1])
        
    if r+1 >= 0 and r+1 < row and c+1 >=0 and c+1 < col:
        if board[r+1][c+1] < 0:
            nbr_list.append(-1*board[r+1][c+1])
        
    if r-1 >= 0 and r-1 < row and c+1 >=0 and c+1 < col:
        if board[r-1][c+1] < 0:
            nbr_list.append(-1*board[r-1][c+1])  
         
    return nbr_list

'''
Finding board hints
'''
def getBoardHints(board, row, col):
    hints = []
    cells = product(xrange(row), xrange(col))
        
    for cell in cells:
        i,j = cell
        if board[i][j] >= 0 :
            hints.append(cell)
            
    return hints

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print 'Layout or output file not specified.'
        exit(-1)
    board, row, col, x_cnt = parse_file(sys.argv[1])
    convert2CNF(board, row, col, x_cnt, sys.argv[2])