import sys
class NodeObject():
    def __init__(self,L=None,R=None,U=None,D=None,C=None,I="default"):
        self.L=L
        self.R=R
        self.D=D
        self.U=U
        self.C=C
        self.I=I

    def printSelf(self):
        print(str(f"L:{self.L},R:{self.R},U:{self.R},D:{self.D},C:{self.C},I:{self.I}"))
    
    #def __str__(self):
    #    return f"L:{self.L},R:{self.R},U:{self.R},D:{self.D},C:{self.C},I:{self.I}"

class ColumnNode( NodeObject ):
    def __init__(self,N="defaultName",S=-1):
        super().__init__(U=self,D=self)
        self.N=N
        self.S=S
    #def __str__(self):
    #    return str(self.N)

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
            #return ColumnNode(N=n,S=0)
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
                name = int(str(row) + str(i))
                rowArray[i] = NodeObject(I=name)
        
        #link them up horizontally
        connectRowsFromRowArray(rowArray)

        #link them to column headers
        for i in range(len(rowArray)):
            if rowArray[i] != 0:
                #find column of this node, i.e i
                columnHeader = rootNode
                
                for x in range(i+1):
                    columnHeader = columnHeader.R
                
                """while columnHeader:
                    if columnHeader.N == i:
                        break
                    columnHeader = columnHeader.L"""
                
                

                #bottom element in a column
                #set 'up' fields

                rowArray[i].U = columnHeader.U
                columnHeader.U = rowArray[i]
                

                #set 'down' fields
                
                if columnHeader.D == columnHeader:
                    columnHeader.D = rowArray[i]

                rowArray[i].D = columnHeader

                if rowArray[i].U != columnHeader and rowArray[i].U != rowArray[i]:
                    rowArray[i].U.D = rowArray[i]

                #rowArray[i].C = columnHeader.D
                rowArray[i].C = columnHeader
                columnHeader.S += 1
def printObject(obj):
    for key in obj.__dict__:
        value = key + ":" + obj.__dict__[key].__str__()
        sys.stdout.write(value + " ")
    print()
def printLinkedLists(rootNode):
    """
    param rootNode: ColumnNode object
    
    :return: Node count
    :rtype: int
    """
    nxt = rootNode.R
    while nxt != rootNode:
        printObject(nxt)
        nxt = nxt.R   
def ConvertMatrixToList(Matrix):
    """Converts a 2d python array into a structure of linked lists based on Donal E. Knuths paper "Dancing Links"

    :param Matrix: 2d python array of 1's and 0's
    
    :return: the root element of the linked list structure
    :rtype: ColumnNode
    """
    rootHeader = createColumnHeaders(Matrix)
    createRows(rootHeader,Matrix)

    #printLinkedLists(rootHeader) 
    return rootHeader
def coverColumn(c):
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
def countOnesInMatrix(Matrix):
    count = 0
    for row in Matrix:
        for col in row:
            if col == 1:
                count +=1 
    return count
def printSolutionFromDict(solutionDict):
    
    for key in solutionDict:
        obj = solutionDict[key]
        sys.stdout.write(obj.C.N)
        nxt = obj.R
        while nxt != obj:
            sys.stdout.write(nxt.C.N)
            nxt = nxt.R
        print()
if __name__ == "__main__":
    #Used for testing
    A = testFillFromLecture()
    ones = countOnesInMatrix(A)

    root = ConvertMatrixToList(A)
    c = root.R
    coverColumn(c)
    


#cock