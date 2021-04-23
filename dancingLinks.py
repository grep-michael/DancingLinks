import unittest,sys,random

class Node():
    def __init__(self, right=None, left=None,value=None):
        self.right = right
        self.left = left
        self.value = value
    def printNodes(self):
        nxt = self
        while nxt is not None:
            print(nxt.value)
            nxt = nxt.right
    
    def removeX(self,x):
        x.left.right = x.right 
        x.right.left = x.left

    def replaceX(self,x):
        x.left.right = x 
        x.right.left = x

def makeList():
    array = []
    a = Node(value=1)
    b = Node(left=a,value=2)
    c = Node(left=b,value=3)
    d = Node(left=c,value=4)
    a.right = b
    b.right = c
    c.right = d
    array.extend((a,b,c,d))
    return array

def pprint(matrix):
    #print column count
    sys.stdout.write(f"  ")
    for i in range(0,len(matrix[0])):
        sys.stdout.write(f" {i} ")
    sys.stdout.write("\n")
    for i in range(0,len(matrix[0])+1):
        sys.stdout.write(f" - ")
    sys.stdout.write("\n")

    #print rows
    rows = list(range(0,len(matrix)))
    rowcount = 0
    for row in matrix:
        sys.stdout.write(f"{rows[rowcount]}|")
        for col in row:
            sys.stdout.write(f" {col} ")
        sys.stdout.write("\n")
        rowcount += 1

def randomFill(A):
    rows = len(A)
    columns = len(A[0])
    for i in range(rows+1):
        con = True
        while con:
            c = random.randint(0,columns-1)
            r = random.randint(0,rows-1)
            if A[r][c] == 0:
                A[r][c] = 1
                con = False

def testfill():
    A = [
        [0,0,1,0,1,1,0],
        [1,0,0,1,0,0,1],
        [0,1,1,0,0,1,0],
        [1,0,0,1,0,0,0],
        [0,1,0,0,0,0,1],
        [0,0,0,1,1,0,1]
    ]
    return A


def removeColumn(A,j):
    for row in A:
        row.pop(j)
    #print("-"*30)
    #print(j)
    #pprint(A)
    #print("-"*30)


def XDriver(matrix):

    Solution=[]
    badCols = []
    badRows = []
    def algorX(A,startCol=0):
        #pprint(A)
        #print(Solution)

        if len(A) == len(badRows) and len(A[0]) == len(badCols): 
            return
        #todo make random
        for row in range(len(A)):
            if A[row][startCol] == 1:
                startCol+=1
                r = row
                break
        
        Solution.append(r)

        for j in range(len(A[0])):
            if A[r][j]==1 and j not in badCols:
                badCols.append(j)
                for i in range(len(A)):
                    if A[i][j]==1 and i not in badRows:
                        badRows.append(i)
            
        algorX(A,startCol=startCol)

    algorX(matrix)

    return Solution

def main():
    #matrix = [[ 0 for i in range(0,8) ] for j in range(0,1)]
    #randomFill(matrix)
    matrix = testfill()
    
    a = XDriver(matrix)
    print(a)
    



if __name__ == '__main__':
    main()
