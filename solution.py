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
    filtered = []
    filter = lambda x,y: [y.append(i) for i in x if i not in y]
    filter(Solutions,filtered)
    #print(filtered)
    return filtered

class AlgorithumXTest(unittest.TestCase):
    Matrix = HelperFunctions.testFillFromLecture()

    def test_algorx_solution_in_solutions( self ):
        self.assertTrue( [1,3,5] in AlgorithumX(self.Matrix))
    def test_algorx_length_of_solutions( self ):
        self.assertTrue(len(AlgorithumX(self.Matrix)) == 6)

class MaxtrixToLinkedListsTest(unittest.TestCase):
    Matrix = HelperFunctions.testFillFromLecture()

    def test_linklists_converter_test( self ):
        #if we use the matrix from lecture there should be 24, I counted manually, if algorithum is made and test doesnt pass count again @michael
        #self.assertTrue(len(MaxtirxToList(Matrix)) == 24)
        pass
    def test_linklist_converter_createColumnHeaders_testcircularlist(self):
        root = HelperFunctions.createColumnHeaders(self.Matrix)
        self.assertEqual(root.N, "root")
        self.assertEqual(root.L.N, 7) #last column
        self.assertEqual(root.R.N, 0) # first column

    def test_linklist_converter_1(self):
        pass

if __name__ == "__main__":
    unittest.main()
