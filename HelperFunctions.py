class NodeObject():
    def __init__(self,L=None,R=None,U=None,D=None,C=None):
        self.L=L
        self.R=R
        self.D=D
        self.U=U
        self.C=C

class ColumnObject( NodeObject ):
    def __init__(self,N="defaultName",S=-1):
        super().__init__()
        self.N=N
        self.S=S


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


def createColumnHeaders(Matrix):
    def makeColumnObject(n):
        if n == 0:
            return ColumnObject(N=n,S=0)
        a = ColumnObject(N=n,S=0) 
        a.L = makeColumnObject( n-1 )
        return a

    columnCount = len(Matrix[0])
    root = ColumnObject(N="root")
    a = makeColumnObject(columnCount)
    #returns the last column object linked only to the left
    #now we link to the right
    nxt = a
    while nxt.L:
        nxt.L.R = nxt
        nxt = nxt.L
    #append root
    root.L = a
    root.R = nxt 
    return root




def ConvertMatrixToList(Matrix):
    rootHeader = createColumnHeaders(Matrix)
    nxt = rootHeader
    
    


if __name__ == "__main__":
    #Used for testing
    A = testFillFromLecture()
    node = NodeObject(L=22)
    col = ColumnObject(N="bob")
