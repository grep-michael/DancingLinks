#!/bin/python3

import unittest,sys,random,math
from copy import copy,deepcopy

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



def removeColumn(A,j):
    for row in A:
        row.pop(j)
    #print("-"*30)
    #print(j)
    #pprint(A)
    #print("-"*30)


def UseArraysToStoreBadRowsAndColumns(matrix):

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
    """
    For use when physically shrinking the matrix
    """
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

def ColumnWithLeast1sArrays(A,columns,rows):
    """
    For use when storing columns and rows in arrays
    """
    map = {}
    for col in columns:
        count =0
        for row in rows:
            if A[row][col] == 1:
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

def RemoveMatrixRowsAndColumns(A):
    
    Solutions=[]
    Partial_Solution = []
    goodColumns = [i for i in range(len(A[0]))]
    def solve(matrix):
        pprint(matrix)

        if len(matrix) == 0:
            Solutions.append(Partial_Solution)
            print("good")
            return 

        if ColumnWithLeast1s(matrix) is None:
            Partial_Solution.pop()
            print("bad")
            return
        
        for col in goodColumns:
            for row in range(len(matrix)):
                
                #print(row,col)
                if matrix[row][col] == 1 :
                    
                    Partial_Solution.append(row)

                    nextMatrix = list(map(list,matrix))
                    removeAllSimilarRows(nextMatrix,matrix[row])
                    for i in range(len(matrix[row])):
                        if matrix[row][i] == 1:
                            try:
                                goodColumns.remove(i)
                            except:
                                pass
                    #solve is called on the smaller matrix
                    solve(nextMatrix)
                    #once solve returns we are back again working on our larger matrix
        
        
            
        

    solve(A)

    return Solutions
def removeAllSimilarRows(A,rowToRemove):
    A.remove(rowToRemove)
    #print(A)
    #print(rowToRemove)
    i = 0
    while i < len(A):
        for index in range(len(A[i])):
            #print(i,A[i],index,A[i][index] == 1 and rowToRemove[index] == 1)
            if A[i][index] == 1 and rowToRemove[index] == 1:
                try:
                    A.pop(i)
                    i = 0
                except:
                    pass
        i+=1
    #print(A)

def removeAllSimilarRowsBack(A,row):
    print(A)
    i = 0
    while i < len(A):
        for index in range(len(row)):
            if A[i][index] == row[i]:
                A.pop(i)
                i = -1
                break
        i+=1
    print(f"removeAllSimilar {A}")
        

def reduceMatrixAtRow(A,row):
    removedRows = []
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
    rangeOfRows = [i for i in range(len(A))]
    rangeOfCols = [i for i in range(len(A[0]))]
    Solutions = []
    Partial_Solution = []

    
    def solve(rowToLoop,ColToLoop,level=0,):

        if len(rowToLoop) == 0 and len(ColToLoop) == 0:
            Solutions.append(copy(Partial_Solution))
            print(level,"good",Partial_Solution)
            return 

        #ensure all remaining columns have at least one 1
        # #if not failed 
        for j in ColToLoop:
            colSum = 0
            for row in rowToLoop:
                    colSum += A[row][j]
            if colSum == 0:
                print(level,"bad")
                return
        for col in ColToLoop:
            for row in rowToLoop:

                if A[row][col] == 1:
                    print(level,row,col)
                    print(level,rowToLoop,ColToLoop)
                    
                    Partial_Solution.append(row)
                    newRows = copy(rowToLoop)
                    newCols = copy(ColToLoop)

                    #'remove' rows and columns
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
                    
                    print(level,newRows,newCols)
                    k = level +1
                    solve(newRows,newCols,k)
                    Partial_Solution.pop()
        """ can not brute force all possible solutions without looping over columns, this will create duplicate answers
        col = ColumnWithLeast1sArrays(A,ColToLoop,rowToLoop)
        for row in rowToLoop:
            #if level ==1:
            #    print(row,col,A[row][col])
            if A[row][col] == 1:
                print(level,row,col)
                print(level,rowToLoop,ColToLoop)
                    
                Partial_Solution.append(row)
                newRows = copy(rowToLoop)
                newCols = copy(ColToLoop)
                #'remove' rows

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
                print(level,newRows,newCols)
                k = level +1
                solve(newRows,newCols,k)
                Partial_Solution.pop()"""
        

                                   
            
    solve(rangeOfRows,rangeOfCols)
    return Solutions




def main():

    matrix = testFillFromLecture()
    a = test(matrix)
    b = []
    filter = lambda x,y: [y.append(i) for i in x if i not in y]
    filter(a,b)
    print(b)
    #removeAllSimilarRows(test,test[0])
    #pprint(test)



if __name__ == '__main__':
    main()
