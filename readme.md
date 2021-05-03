
# Dancing Links by Donald Knuth
### michael knudsen 2021

# Files
`solution.py`: entry point and tests

`HelperFunctions.py`: library of functions for debugging and printing, includes code to convert 
from a Matrix to a node structure

## AlgoithumX
### functions
AlgorithumX(A)

 - `A`: A 2d python array of 1's and 0's

solve(rowToLoop,ColToLoop,level=0)

 - `rowToLoop`: is a list of rows to loop over

 - `ColToLoop`: is a list of columns to loop over

 - `level`: a debug varible for printing out the recursion level

### logic
We initialize two arrays `rangeOfRows` and `rangeOfCols` which is a list (`0,1,2 ... n`) of all 
the indices of the rows and columns. Then in order to back track we create copies of these arrays
were we remove the covered rows and columns indices. These copies are passed recursivly to 
the solve function as rowToLoop and ColToLoop. This lets us easily back track by simply ignoring
the copies once we have returned and leave them to garbage collection

### return 
a python list of solutions

## DancingLinks
### functions
dancingLinks(root)

 - `root`: A ColumnObject

search(k)

 - `k`: our starting index


### logic
The logic follows directly from Donald Knuths paper. However in order to keep track of 
our Data Objects (`NodeObjects` in our code) we use a dictionary. where the key is the `k` value
and the value is the `NodeObjects`

### return 
A dictionary containing `NodeObjects` for each row of the solution

# Classess

`NodeObject`: represents the Data Object from the paper. 

`ColumnNode`: represents the column header Objects, inherits from `NodeObject`

# Notes
the solution columns can be printed by calling `printSolutionFromDict(solutionDict)`
on the return value of `dancingLinks(root)` 

# Examples 

```Python
root = ConvertMatrixToList(Matrix)
SolutionDict = dancingLinks(root)
SolutionArray = AlgoithumX(Matrix)
```
