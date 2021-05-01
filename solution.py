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
    """
    Paper Matrix comes from the example matrix in Donal knuth paper
    Lacture Matrix comes from the example matrix from class
    """
    LecutreMatrix = HelperFunctions.testFillFromLecture()
    PaperMatrix = HelperFunctions.testfillFromPaper()

    def test_algorx_solution_in_solutions_fromLectureMatrix( self ):
        self.assertTrue( [1,3,5] in AlgorithumX(self.LecutreMatrix))
    def test_algorx_length_of_solutions_fromLectureMatrix( self ):
        self.assertTrue(len(AlgorithumX(self.LecutreMatrix)) == 6)
    def test_algorx_solution_in_solutions_fromPaperMatrix( self ):
        self.assertTrue( [0,3,4] in AlgorithumX(self.PaperMatrix))
    def test_algorx_length_of_solutions_fromPaperMatrix( self ):
        self.assertTrue(len(AlgorithumX(self.PaperMatrix)) == 6)

class DancingLinksTest(unittest.TestCase):
    """
    you can print the solution by column using the printSolutionFromDict function from HelperFunctions
    Paper Matrix comes from the example matrix in Donal knuth paper
    Lacture Matrix comes from the example matrix from class
    """
    LectureMatrix = HelperFunctions.testFillFromLecture()
    PaperMatrix = HelperFunctions.testfillFromPaper()
    def getSolution(Os):
        """
        gets the solution from a dict of NodeObjects
        This works because the 'I' field of the NodeObjects is set to a two digit string of row and column
        
        :param Os: solution dict produced from dancingLinks
        :type Os: dict 
        """
        solution = ""
        for key in Os:
            solution += Os[key].I[0]
        return solution
    
    def test_dancingLinks_LectureMatrix(self):  
        root = HelperFunctions.ConvertMatrixToList(self.LectureMatrix)  
        Os = dancingLinks(root)
        self.assertTrue( getSolution(Os) == "153")

    def test_dancingLinks_PaperMatrix(self):
        root = HelperFunctions.ConvertMatrixToList(self.PaperMatrix)  
        Os = dancingLinks(root)
        self.assertTrue( getSolution(Os) == "340")

class MaxtrixToLinkedListsTest(unittest.TestCase):
    """
    Paper Matrix comes from the example matrix in Donal knuth paper
    Lacture Matrix comes from the example matrix from class
    """
    LectureMatrix = HelperFunctions.testFillFromLecture()
    PaperMatrix = HelperFunctions.testfillFromPaper()

    def test_linklist_converter_createColumnHeaders_testcircularlist_LectureMaxtrix(self):
        root = HelperFunctions.createColumnHeaders(self.LectureMatrix)
        self.assertEqual(root.N, "root")
        self.assertEqual(root.L.N, 'g') #last column
        self.assertEqual(root.R.N, 'a') # first column
    
    def test_linklist_converter_creatRows_testAllRowsExist_LectureMaxtrix(self):
        root = HelperFunctions.createColumnHeaders(self.LectureMatrix)
        HelperFunctions.createRows(root,self.LectureMatrix)
        #the size of each row from the lecture Matrix
        sizes = [2,2,2,3,2,2,4]
        r = root.R
        for i in sizes:
            self.assertEqual(r.S,i)
            r = r.R

    def test_linklist_converter_createColumnHeaders_testcircularlist_PaperMatrix(self):
        root = HelperFunctions.createColumnHeaders(self.PaperMatrix)
        self.assertEqual(root.N, "root")
        self.assertEqual(root.L.N, 'g') #last column
        self.assertEqual(root.R.N, 'a') # first column
    
    def test_linklist_converter_creatRows_testAllRowsExist_PaperMatrix(self):
        root = HelperFunctions.createColumnHeaders(self.PaperMatrix)
        HelperFunctions.createRows(root,self.PaperMatrix)
        #the size of each row from the paper Matrix
        sizes = [2,2,2,3,2,2,3]
        r = root.R
        for i in sizes:
            self.assertEqual(r.S,i)
            r = r.R


if __name__ == "__main__":
    unittest.main()
    