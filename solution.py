import unittest
from copy import copy,deepcopy
class NodeObject():
    """
    Represents a data Object as highlighted in Donald Knuths paper "dancing links"
    The I field indicates an identifier for the NodeObject, In our case we use a 2 digit number corresponding to the row and column
    """
    def __init__(self,L=None,R=None,U=None,D=None,C=None,I="default"):
        self.L=L
        self.R=R
        self.D=D
        self.U=U
        self.C=C
        self.I=I

    def printSelf(self):
        print(str(f"L:{self.L},R:{self.R},U:{self.R},D:{self.D},C:{self.C},I:{self.I}"))

class ColumnNode( NodeObject ):
    """
    Represents a Columnheader as highlighted in Donald Knuths paper "dancing links"
    """
    def __init__(self,N="defaultName",S=-1):
        super().__init__(U=self,D=self)
        self.N=N
        self.S=S


def testfillFromPaper():
    """returns the matrix used as an example in the paper
    :return: matrix
    :rtype: 2d array
    """
    return [
        [0,0,1,0,1,1,0],
        [1,0,0,1,0,0,1],
        [0,1,1,0,0,1,0],
        [1,0,0,1,0,0,0],
        [0,1,0,0,0,0,1],
        [0,0,0,1,1,0,1]
    ]

def testFillFromLecture():
    """
    returns matrix used in lecture 
    :return: maxtix
    :rtype: 2d array
    """

    return [
        [1,0,0,1,0,0,1],
        [1,0,0,1,0,0,0],
        [0,0,0,1,1,0,1],
        [0,0,1,0,1,1,0],
        [0,1,1,0,0,1,1],
        [0,1,0,0,0,0,1]
    ]

def createColumnHeaders(Matrix):
    """ from 2d array create column headers for the link list structure

    :param Matrix: 2d python array of 1's and 0's
    
    :return: the root element of the linked list structure
    :rtype: ColumnNode
    """

    def makeColumnNodes(n):
        if n == 0:
            return ColumnNode(N=chr(97+n),S=0)
        a = ColumnNode(N=chr(97+n),S=0) 
        a.L = makeColumnNodes( n-1 )
        return a

    columnCount = len(Matrix[0])-1
    root = ColumnNode(N="root")
    a = makeColumnNodes(columnCount)
    
    nxt = a
    while nxt.L:
        nxt.L.R = nxt
        nxt = nxt.L
    #append root
    root.L = a
    a.R = root
    root.R = nxt 
    nxt.L = root
    return root

def connectRowsFromRowArray(rowArray):
    """connects rows based on rowArray

    :param rowArray: Array of zeros and NodeObjects 
    
    :return: None
    """
    First = None
    prev = None
    for i in rowArray:
        if i != 0:
            #sets Right value of current element
            i.R = prev
            prev = i
            #set left Node
            if i.R != None:
                i.R.L = i
            if First == None:
                First =i
    First.R = prev
    prev.L = First

def createRows(rootNode,Matrix):
    """Loops over matrix adding nodes for each one"

    :param rootNode: ColumnNode 
    :param Matrix: 2d python array of 1's and 0's
    
    :return: None
    """

    for row in range(len(Matrix)):
        #generate the nessacary Node objects
        #storing them in an array lets us generate them and keep track of their column number
        rowArray = [0 for i in Matrix[row]]
        for i in range(len(Matrix[row])):
            if Matrix[row][i] == 1:
                name = (str(row) + str(i))
                rowArray[i] = NodeObject(I=name)
        
        #link them up horizontally
        connectRowsFromRowArray(rowArray)

        #link them to column headers

        for i in range(len(rowArray)):
            if rowArray[i] != 0:
                columnHeader = rootNode
                
                for x in range(i+1):
                    columnHeader = columnHeader.R
                
                """while columnHeader:
                    if columnHeader.N == i:
                        break
                    columnHeader = columnHeader.L"""
                
                

                
                #set 'up' fields
                rowArray[i].U = columnHeader.U
                columnHeader.U = rowArray[i]
                

                #set 'down' fields
                if columnHeader.D == columnHeader:
                    columnHeader.D = rowArray[i]

                rowArray[i].D = columnHeader

                if rowArray[i].U != columnHeader and rowArray[i].U != rowArray[i]:
                    rowArray[i].U.D = rowArray[i]

                rowArray[i].C = columnHeader
                columnHeader.S += 1

def ConvertMatrixToList(Matrix):
    """Converts a 2d python array into a structure of linked lists based on Donal E. Knuths paper "Dancing Links"

    :param Matrix: 2d python array of 1's and 0's
    
    :return: the root element of the linked list structure
    :rtype: ColumnNode
    """
    rootHeader = createColumnHeaders(Matrix)
    createRows(rootHeader,Matrix)
    return rootHeader

def coverColumn(c):
    """
    Disconnects a given column from the rest of a linked list matrix

    :param c: The column to remove
    :type c: ColumnObject
    """
    c.R.L = c.L
    c.L.R = c.R
    
    i = c.D
    while i != c:

        j = i.R
        while j != i:
            j.D.U = j.U
            j.U.D = j.D
            j.C.S = j.C.S - 1

            j = j.R
        i = i.D

def uncoverColumn(c):
    """
    Reconnects a given column

    :param c: The column to reconnect
    :type c: ColumnObject
    """
    i = c.U
    while i != c:
        j = i.L
        while j != i:
            j.C.S = j.C.S + 1
            j.D.U = j
            j.U.D = j
            j = j.L
        i=i.U
    c.R.L = c
    c.L.R = c

def printSolutionFromDict(solutionDict):
    """
    Prints the solution given a dictionary of solutions

    :param solutionDict: soultion dictionary created by solution.dancingLinks
    :type solutionDict: dict
    """
    for key in solutionDict:
        obj = solutionDict[key]
        sys.stdout.write(obj.C.N)
        nxt = obj.R
        while nxt != obj:
            sys.stdout.write(nxt.C.N)
            nxt = nxt.R
        print()

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
        coverColumn(c)

        r = c.D
        while r != c:
            O[k] = r
            j = r.R
            while j != r:
                coverColumn(j.C)
                j = j.R
            search(k+1)
            r = O[k]
            c = r.C
            j = r.L
            while j != r:
                uncoverColumn(j.C)
                j = j.L
            r = r.D
        uncoverColumn(c)
        return
    search(0)
    return O

class AlgorithumXTest(unittest.TestCase):
    """
    Paper Matrix comes from the example matrix in Donal knuth paper
    Lacture Matrix comes from the example matrix from class
    """
    LecutreMatrix = testFillFromLecture()
    PaperMatrix = testfillFromPaper()

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
    you can print the solution by column using the printSolutionFromDict
    Paper Matrix comes from the example matrix in Donal knuth paper
    Lacture Matrix comes from the example matrix from class
    """
    LectureMatrix = testFillFromLecture()
    PaperMatrix = testfillFromPaper()
    def getSolution(self,Os):
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
        root = ConvertMatrixToList(self.LectureMatrix)  
        Os = dancingLinks(root)
        self.assertTrue( self.getSolution(Os) == "153")

    def test_dancingLinks_PaperMatrix(self):
        root = ConvertMatrixToList(self.PaperMatrix)  
        Os = dancingLinks(root)
        self.assertTrue( self.getSolution(Os) == "340")

class MaxtrixToLinkedListsTest(unittest.TestCase):
    """
    Paper Matrix comes from the example matrix in Donal knuth paper
    Lacture Matrix comes from the example matrix from class
    """
    LectureMatrix = testFillFromLecture()
    PaperMatrix = testfillFromPaper()

    def test_linklist_converter_createColumnHeaders_testcircularlist_LectureMaxtrix(self):
        root = createColumnHeaders(self.LectureMatrix)
        self.assertEqual(root.N, "root")
        self.assertEqual(root.L.N, 'g') #last column
        self.assertEqual(root.R.N, 'a') # first column
    
    def test_linklist_converter_creatRows_testAllRowsExist_LectureMaxtrix(self):
        root = createColumnHeaders(self.LectureMatrix)
        createRows(root,self.LectureMatrix)
        #the size of each row from the lecture Matrix
        sizes = [2,2,2,3,2,2,4]
        r = root.R
        for i in sizes:
            self.assertEqual(r.S,i)
            r = r.R

    def test_linklist_converter_createColumnHeaders_testcircularlist_PaperMatrix(self):
        root = createColumnHeaders(self.PaperMatrix)
        self.assertEqual(root.N, "root")
        self.assertEqual(root.L.N, 'g') #last column
        self.assertEqual(root.R.N, 'a') # first column
    
    def test_linklist_converter_creatRows_testAllRowsExist_PaperMatrix(self):
        root = createColumnHeaders(self.PaperMatrix)
        createRows(root,self.PaperMatrix)
        #the size of each row from the paper Matrix
        sizes = [2,2,2,3,2,2,3]
        r = root.R
        for i in sizes:
            self.assertEqual(r.S,i)
            r = r.R


if __name__ == "__main__":
    unittest.main()
    