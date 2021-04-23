import unittest,sys,random,math

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

def testfillFromPaper():
    return [
        [0,0,1,0,1,1,0],
        [1,0,0,1,0,0,1],
        [0,1,1,0,0,1,0],
        [1,0,0,1,0,0,0],
        [0,1,0,0,0,0,1],
        [0,0,0,1,1,0,1]
    ]

def testFillFromLecture():
    return [
        [1,0,0,1,0,0,1],
        [1,0,0,1,0,0,0],
        [0,0,0,1,1,0,1],
        [0,0,1,0,1,1,0],
        [0,1,1,0,0,1,1],
        [0,1,0,0,0,0,1]
    ]

def removeColumn(A,j):
    for row in A:
        row.pop(j)
    #print("-"*30)
    #print(j)
    #pprint(A)
    #print("-"*30)


def SingleSolve(matrix):

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

def ColumnWithLeast1s(A):
    map = {}
    for col in range(len(A[0])):
        count =0
        for row in A:
            if row[col] == 1:
                count +=1
        map[col] = count
    large = math.inf
    smallest = None
    for key in map:
        if map[key] == 0:
            return None
        if map[key] < large:
            large = map[key]
            smallest = key
        
    #print(f"map: {map}")
    return smallest

def allSolutions(matrix):
    
    Solutions=[]
    Partial_solution = []
    def algorX(A):

        pprint(A)
        print(Partial_solution)

        if len(A) == 0:
            Solutions.append(Partial_solution)
            return

        c = ColumnWithLeast1s(A)
        if c is not None:
            for row in range(len(A)):
                if A[row][c] == 1:
                    r = row
                    break
            Partial_solution.append(r)
            j = 0
            while j < len(A[0]):
                if A[r][j]==1:
                    removeColumn(A,j)
                    j =0
                    i = 0
                    while i < len(A):
                        if A[i][j]==1:
                            A.pop(i)
                            i=0
                        else:
                            i+=1
                else:
                    j += 1  
        else:
            #no further to go we must back track
            Partial_solution.pop()
        
            
        algorX(A)

    algorX(matrix)

    return Solutions

def reduceMatrixAtRow(A,row):
    j = 0
    while j < len(A[0]):
        if A[row][j]==1:
            removeColumn(A,j)
            j =0
            i = 0
            while i < len(A):
                if A[i][j]==1:
                    A.pop(i)
                    i=0
                else:
                    i+=1
        else:
            j += 1 
    

def test(A):

    Solutions = []
    Partial_Solution = []
    
    def solve(matrix):
        pprint(matrix)
        print(Partial_Solution)
        if len(matrix) == 0:
            Solutions.append(Partial_Solution)
            print("good")
            return 
        if ColumnWithLeast1s(matrix) is None:
            Partial_Solution.pop()
            print("bad")
            return
        
        for col in range(len(matrix[0])):
            for row in range(len(matrix)):
                #print(row,col)
                if matrix[row][col] == 1:
                    Partial_Solution.append(row)

                    nextMatrix = list(map(list,matrix))
                    reduceMatrixAtRow(nextMatrix,row)
                    #TODO return to using array to store bad values
                    solve(nextMatrix)
                    pprint(matrix)
                    
                    
            
    return solve(A)




def main():
    #matrix = [[ 0 for i in range(0,8) ] for j in range(0,1)]
    #randomFill(matrix)
    matrix = testFillFromLecture()
    
    a = test(matrix)
    print(a)
    



if __name__ == '__main__':
    main()
