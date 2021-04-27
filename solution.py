import unittest,HelperFunctions
from copy import copy,deepcopy

def AlgorithumX(A):
    rangeOfRows = [i for i in range(len(A))]
    rangeOfCols = [i for i in range(len(A[0]))]
    Solutions = []
    Partial_Solution = []

    
    def solve(rowToLoop,ColToLoop,level=0,):

        if len(rowToLoop) == 0 and len(ColToLoop) == 0:
            Solutions.append(copy(Partial_Solution))
            #print(level,"good",Partial_Solution)
            return 

        for j in ColToLoop:
            colSum = 0
            for row in rowToLoop:
                    colSum += A[row][j]
            if colSum == 0:
                #print(level,"bad")
                return
        for col in ColToLoop:
            for row in rowToLoop:

                if A[row][col] == 1:
                    #print(level,row,col)
                    #print(level,rowToLoop,ColToLoop)
                    
                    Partial_Solution.append(row)
                    newRows = copy(rowToLoop)
                    newCols = copy(ColToLoop)
                    j = 0
                    while j < len(newCols):
                        if A[row][newCols[j]] == 1:
                            i = 0
                            while i < len(newRows):
                                if A[newRows[i]][newCols[j]] == 1:
                                    newRows.pop(i)
                                    i=0
                                else:
                                    i+=1
                            newCols.pop(j)
                            j=0
                        else:
                            j += 1
                    
                    #print(level,newRows,newCols)
                    k = level +1
                    solve(newRows,newCols,k)
                    Partial_Solution.pop()
    
    solve(rangeOfRows,rangeOfCols)
    return Solutions

class AlgorithumXTest(unittest.TestCase):
    Matrix = HelperFunctions.testFillFromLecture()

    def test_algorx1( self ):
        self.assertTrue( [1,3,5] in AlgorithumX(self.Matrix))



if __name__ == "__main__":
    unittest.main()
