import unittest,HelperFunctions
from copy import copy,deepcopy

def AlgorithumX(A):

    """brute forces all solutions to the exact cover problem 

    :param Matrix: 2d python array of 1's and 0's
    
    :return: array of all solutions
    :rtype: Array
    """

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

def dancingLinks(root):
    
    O = {}
    
    def search(k):
        if root.R == root:
            return
        c = root.R
        HelperFunctions.coverColumn(c)
        #TODO remove print statments
        r = c.D
        while r != c:

            #set Ok to r
            O[k] = r
            

            j = r.R
            while j != r:
                HelperFunctions.coverColumn(j.C)
                j = j.R
            search(k+1)

            #set r=Ok and c=r.C
            r = O[k]
            c = r.C

            j = r.L
            while j != r:
                HelperFunctions.uncoverColumn(j.C)
                j = j.L
            r = r.D
        HelperFunctions.uncoverColumn(c)
        return

    search(0)
    return O

class AlgorithumXTest(unittest.TestCase):
    Matrix = HelperFunctions.testFillFromLecture()

    def test_algorx_solution_in_solutions( self ):
        self.assertTrue( [1,3,5] in AlgorithumX(self.Matrix))
    def test_algorx_length_of_solutions( self ):
        self.assertTrue(len(AlgorithumX(self.Matrix)) == 6)

class testSearch(unittest.TestCase):
    Matrix = HelperFunctions.testFillFromLecture()
    root = HelperFunctions.ConvertMatrixToList(Matrix)

    """
    troulbeshooting : make sure the c field of each node is correct
    """

    def test_search_solution_in_solutions(self):
        self.assertTrue( [1,3,5] in dancingLinks(self.root) )


class MaxtrixToLinkedListsTest(unittest.TestCase):
    Matrix = HelperFunctions.testFillFromLecture()

    def test_linklists_converter_test( self ):
        #if we use the matrix from lecture there should be 24, I counted manually, if algorithum is made and test doesnt pass count again @michael
        #self.assertTrue(len(MaxtirxToList(Matrix)) == 24)
        pass
    def test_linklist_converter_createColumnHeaders_testcircularlist(self):
        root = HelperFunctions.createColumnHeaders(self.Matrix)
        self.assertEqual(root.N, "root")
        self.assertEqual(root.L.N, 6) #last column
        self.assertEqual(root.R.N, 0) # first column
    def test_linklist_converter_creatRows_testAllRowsExist(self):
        #HelperFunctions.pprint(self.Matrix)
        root = HelperFunctions.createColumnHeaders(self.Matrix)
        HelperFunctions.createRows(root,self.Matrix)
        #the size of each row from he lecture Matrix
        sizes = [2,2,2,3,2,2,4]
        r = root.R
        for i in sizes:
            self.assertEqual(r.S,i)
            r = r.R
        
        
    def test_linklist_converter_1(self):
        pass

if __name__ == "__main__":
    #unittest.main()
    Matrix = HelperFunctions.testFillFromLecture()
    root = HelperFunctions.ConvertMatrixToList(Matrix)
    Os = dancingLinks(root)
    HelperFunctions.printSolutionFromDict(Os)