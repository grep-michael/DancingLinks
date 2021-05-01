import unittest,HelperFunctions
from copy import copy,deepcopy

def AlgorithumX(A):

    """brute forces all solutions to the exact cover problem
        I realized after finishing this all solutions are the same, just reordered.
    :param Matrix: 2d python array of 1's and 0's
    
    :return: array of all solutions
    :rtype: Array
    """

    rangeOfRows = [i for i in range(len(A))]
    rangeOfCols = [i for i in range(len(A[0]))]
    Solutions = []
    Partial_Solution = []

    
    def solve(rowToLoop,ColToLoop,level=0,):
        """
        preforms algorithumX on given rows and columns

        :param rowToLoop: list of rows to loop over
        :param type: list
        :param ColToLoop: list of columns to loop over
        :param type: list
        :param level: prints the level of recursion, was used for testing
        :param type: int

        """
        if len(rowToLoop) == 0 and len(ColToLoop) == 0:
            Solutions.append(copy(Partial_Solution))
            return 
        for j in ColToLoop:
            colSum = 0
            for row in rowToLoop:
                    colSum += A[row][j]
            if colSum == 0:
                return
        for col in ColToLoop:
            for row in rowToLoop:
                if A[row][col] == 1:
 
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
                    
                    k = level +1
                    solve(newRows,newCols,k)
                    Partial_Solution.pop()
    
    solve(rangeOfRows,rangeOfCols)
    filtered = []
    filter = lambda x,y: [y.append(i) for i in x if i not in y]
    filter(Solutions,filtered)
    return filtered

def dancingLinks(root):

    """
    Preformed the dancing links algorithum on a root node

    :param root: The root node
    :type root: ColumnObject
    :return O: Dictionary containg the solution NodeObjects
    :return type: Dict
    """
    
    O = {}
    
    def search(k):

        """
        The search function as outlined by Donald Knuth in "dancing links"

        :param k: the index of the search
        :param type: int 
        """

        if root.R == root:
            return
        c = root.R
        HelperFunctions.coverColumn(c)

        r = c.D
        while r != c:
            O[k] = r
            j = r.R
            while j != r:
                HelperFunctions.coverColumn(j.C)
                j = j.R
            search(k+1)
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

    def test_search_solution(self):
        
        """
        you can print the solution by column using the printSolutionFromDict function from HelperFunctions
        """
        Os = dancingLinks(self.root)
        solution = ""
        for key in Os:
            solution += Os[key].I[0]

        self.assertTrue( solution == "153")

class MaxtrixToLinkedListsTest(unittest.TestCase):
    Matrix = HelperFunctions.testFillFromLecture()

    def test_linklist_converter_createColumnHeaders_testcircularlist(self):
        root = HelperFunctions.createColumnHeaders(self.Matrix)
        self.assertEqual(root.N, "root")
        self.assertEqual(root.L.N, 'g') #last column
        self.assertEqual(root.R.N, 'a') # first column
    def test_linklist_converter_creatRows_testAllRowsExist(self):
        root = HelperFunctions.createColumnHeaders(self.Matrix)
        HelperFunctions.createRows(root,self.Matrix)
        #the size of each row from the lecture Matrix
        sizes = [2,2,2,3,2,2,4]
        r = root.R
        for i in sizes:
            self.assertEqual(r.S,i)
            r = r.R
        
if __name__ == "__main__":
    unittest.main()
    