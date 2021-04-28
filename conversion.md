# Converting from matrix to linked list

### steps
 1. create root and columns
     - loop over columns, create column object
     - creating links left
     - create links right
     - attach last column object to root
     - return root
 2. add data objects (x) 
     - loop over rows (i), if i==1 create data object (x)
         - apply U,D,L,R where applicable. Note wont beable to append L for first node in row 
         - append x as last node of column object 
     - now that row is made, apply L for the first node in row
3. apply all unconnected links
    - loop over column objects
    - loop over rows
    - make sure header had a L and R