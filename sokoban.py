
#Check to see if Human, Box, and Destination are in the array and if array size is in correct bounds 
def checker(room, rows, cols):
    #check if row and columns are at MOST 5 X 6 and
    if rows > 5 or cols > 6:
        return False

    #if either row or columns is equal to 0 there wont be any space for the boxes to move
    if rows == 0 or cols == 0:
        return False 

    #first convert list of lists into 1 list 
    List = []
    for sublist in room:
        for item in sublist:
            List.append(item)
   
    #Check the array to locate if there is a '2'- human AND '3'- box AND '4'- destination in the array
    if 2 in List:
        if 3 in List:
            if 4 in List:
                return True 

    #if either are not found, return False
    return False


#get dirictions up, down, left, right based on point stored in variable
def directions(HumanOrBox):
    r,c = HumanOrBox
                #UP      ,  Down   ,  Left   , Right
    neighbors = [(r-1, c), (r+1, c), (r, c-1), (r, c+1)]
    return neighbors


#get dirictions up, down, left, right based on point NOT stored in variable 
def directions2(x, y):
    r = x
    c = y
                #UP      ,  Down   ,  Left   , Right
    neighbors = [(r-1, c), (r+1, c), (r, c-1), (r, c+1)]
    return neighbors


#BFS on the human. If its no where near the box, it will start running the algoritm and queuing all 
#the moves till it reaches teh location which is next to the box
def humanBFS(room, human, box, rows, cols, loc):
    
    #queue and visted specifically meant for Human so we can track its path
    queue = [human]
    visited = [human]

    while queue:
        x, y = queue.pop()
        
        #if a location is matched from the queue return true
        if loc == (x,y):
            return True

        #get directions of up down left right from the current position    
        UDLR = directions2(x,y)
        for r, c in UDLR:
            if r >= 0:
                if c >= 0: 
                    if r < rows:
                        if c < cols:
                            if room[r][c] != 1: # not equal to a wall
                                if (r, c) != box: #the human cannot be equal to the box 
                                    if (r, c) not in visited:  #if none of the directions are in visited, mark tham in the queue and in visted 
                                        queue.append((r, c))
                                        visited.append((r, c))
    return False


#BFS on the box, we need figure out if the box path to thhe target exists, and the same time we will run BFS on the human 
def boxBFS(room, H_2, B_3, D_4, rows, cols):
   
    start_states = (B_3, H_2)   #piazza post 
    queue = [start_states]
    visited = set([(B_3, H_2)])
    
    while queue:
        B_3, H_2 = queue.pop()
        
        #if the destination equals the box that measns a solution was found 
        if D_4 == B_3:
            return True
        
        #get r,c values from the B_3
        r, c = B_3 
        
        #if the row is greater than 0, and within the bounds, we will than check above and below of the postion and see if those
        #areas have been visited
        if r > 0:
            if r < (rows-1):
                if room[r-1][c] != 1 and room[r+1][c] != 1: #check to make sure were not accesing the wall
                
                        if ((r-1, c), (r, c)) not in visited:
                            
                            if humanBFS(room, H_2, B_3, rows, cols, (r+1, c)) == True:       
                                queue.append(((r-1, c), (r, c)))
                                visited.add(((r-1, c), (r, c)))

                        if ((r+1, c), (r, c)) not in visited:
                            
                            if humanBFS(room, H_2, B_3, rows, cols, (r-1, c)) == True:       
                                queue.append(((r+1, c), (r, c)))
                                visited.add(((r+1, c), (r, c)))
        
        #if the col is greater than 0, and within the bounds, we will than check right and left of the postion and see if those
        #areas have been visited
        if c > 0:
            if c < (cols-1):
                if room[r][c-1] != 1 and room[r][c+1] != 1: #check to make sure were not accesing the wall
                        
                        if ((r, c-1), (r, c)) not in visited:
                            
                            if humanBFS(room, H_2, B_3, rows, cols, (r, c+1)) == True:     
                                queue.append(((r, c-1), (r, c)))
                                visited.add(((r, c-1), (r, c)))
                        
                        if ((r, c+1), (r, c)) not in visited:
                            
                            if humanBFS(room, H_2, B_3, rows, cols, (r, c-1)) == True:     
                                queue.append(((r, c+1), (r, c)))
                                visited.add(((r, c+1), (r, c)))
    return False

# Do not rename this function, otherwise, the automated checks will fail.
def solve_sokoban(room):
    """
    :param room: 2-dimensional array filled with values ranging from 0 to and including 4 where
        0 = empty, 1 = obstacle, 2 = human, 3 = box, 4 = destination
    :return: YES or NO depending on whether there is a sequence of moves that terminate
    with the box at the destination
    """
    # Write your code in this method.
    
    #get information of matrix 
    rowLength = len(room)
    #print(rowLength)
    colLength = len(room[0])
    #print(colLength)

    #All checks are made here about the matrix size and if the Human, Box, and Destination exist 
    if checker(room, rowLength, colLength) == False:           
        return "NO"                 
    
    #Create variables and locate positions for Human-H_2, Box-B_3, and Destination-D_4
    for r in range(rowLength):
        for c in range(colLength):
            if room[r][c] == 2:
                H = (r,c)
            if room[r][c] == 3:
                B = (r,c)
            if room[r][c] == 4:
                D = (r,c)
    
    if boxBFS(room, H, B, D, rowLength, colLength) == True:
        return "YES"
    else:
        return "NO"
    
    return "NO"
    
#####################################################

# Feel free to modify main function
def main():
    # Example 1, expecting NO:
    test_1 = [[4, 0, 0, 0, 0, 0],
              [1, 1, 1, 1, 1, 0],
              [0, 0, 0, 2, 0, 0],
              [0, 0, 0, 3, 0, 0],
              [0, 0, 0, 0, 0, 0]]

    assert solve_sokoban(test_1) == "NO", "Test 1 failed."
    # # Example 2, expecting YES:
    test_2 = [[4, 0, 0, 0, 0, 0],
              [1, 1, 1, 1, 0, 0],
              [0, 0, 0, 2, 0, 0],
              [0, 0, 0, 3, 0, 0],
              [0, 0, 0, 0, 0, 0]]

    assert solve_sokoban(test_2) == "YES", "Test 2 failed."
    
    #exta rows
    test_3 = [[4, 0, 0, 0, 0, 0],
              [1, 1, 1, 1, 0, 0],
              [0, 0, 0, 2, 0, 0],
              [0, 0, 0, 3, 0, 0],
              [0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0]]

    #exta cols[0]
    test_4 = [[4, 0, 0, 0, 0, 0, 0],
              [1, 1, 1, 1, 0, 0],
              [0, 0, 0, 2, 0, 0],
              [0, 0, 0, 3, 0, 0],
              [0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0]]
    
    #exta cols[5] 
    test_5 = [[4, 0, 0, 0, 0, 0],
              [1, 1, 1, 1, 0, 0],
              [0, 0, 0, 2, 0, 0],
              [0, 0, 0, 3, 0, 0],
              [0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0]]
    
    #missing either 2, 3, or 4 or ALL
    test_6 = [[0, 0, 0, 0, 0, 0],    #missing 4 1,1
              [1, 1, 1, 1, 0, 0],
              [0, 0, 0, 2, 0, 0],
              [0, 0, 0, 3, 0, 0],
              [0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0]]

    test_7 = [[4, 0, 0, 0, 3, 2]]
    assert solve_sokoban(test_7) == "YES", "Test 2 failed."
 

if __name__ == "__main__":
    main()
