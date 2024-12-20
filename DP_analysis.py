import itertools as it
import numpy as np
import time
import random
import pandas as pd
import matplotlib.pyplot as plt

###########################################
#####        DEFINE FUNCTIONS         #####
###########################################

# The bubble sort algorithm is what we are basing our reshuffles upon. It determines the process where, if the containers are removed in 
# priority order, how many additional moves would need to be made.
def bubble_sort(col):   # input: column of the container stacking bay
    Ylen = len(col)     # length of column  
    swaps = 0           # initialize swaps
    for j in range(Ylen):   # loop over column
        for k in range(0, Ylen-j-1):    # loop over future elements in the column
            if col[k] < col[k+1]:       # if there is a container otu of order...
                col[k], col[k+1] = col[k+1], col[k] #swap it...
                swaps += 1              # and count the swap necessary
    return swaps                        # return the number of swaps, which we refer to as reshuffles

# This array is for the creation of states. It deletes all elements in the array that are equal to 0.
def zero_delete(arr):
    N = len(arr)                # length of array
    new_arr = np.array([])      # the new array with no 0s
    for i in range (0, N):      # loop over array
        if arr[i] != 0:         # if not equal to 0...
            new_arr = np.append(new_arr, arr[i]) # new array appends the nonzero value
    while len(new_arr) > N:             # I forget what this does, but at one point in time it was relevent
        new_arr = np.append(new_arr, 0) # yeah still no clue, but I'm afraid to delete it
    return new_arr              # returns new array with no 0s

# The heart of the state generation process. It takes the order of containers and generates the possible states. 
# For use in the first iteration
def main(Containers, B):        # Inputs are containers and columns (B)
    Clen = len(Containers)      # Length of array
    C_next = Containers[-1]     # The container we are grabbing is the last one for the backwards induction
    Containers_1 = np.delete(Containers, Clen-1)    # Delete the last container from the array; states generated come from the remainder
    Sort_cons = np.sort(Containers_1)   # Sort the remaining containers
    Slen = len(Sort_cons)               # Length of the new sorted containers
    Iter_combos = {}                    # Dictionary for the combinations of containers that can go together
    for i in range (1, Slen+1):         # Loop over sorted containers
        Iter_combos[i] = it.combinations(Sort_cons, r = i)  # Itertools library to make combinations
    Stack_combos = {}   # Dictionary to store combinations of stacks
    j = 0               # Initialize stack dictionary indexing
    for i in range(1, Slen+1):      # Loop over sorted containers
        for IC in Iter_combos[i]:   # Loop over combinations
            IC_array = np.array(IC) # Turn into numpy array as these are easiest to work with
            Stack_combos[j] = IC_array  # New array for stack combinations
            j += 1                      # Add 1 to indexing
    N = len(Stack_combos)   # Length of combinations array
    N1 = int(N-1)           # Length 1 is the above length subtract 1
    N12 = int(N1/2)         # Length N12 is N1/2
    Stack_pairs = {}        # Initialize dictionary
    for i in range(0, N12): # Because we want unique solutions, only iteration through the first half of combos and...
        for j in range(N12, N1):    # Compare them to the second half of the combos
            if len(np.intersect1d(Stack_combos[i], Stack_combos[j])) == 0:  # Intersection tells if the combination is valid
                Stack_pairs[i] = Stack_combos[i], Stack_combos[j]           # Add to dictionary
    Stack_pairs[N12] = np.zeros(Slen), Stack_combos[N-1]    # Create array to store pairs
    NSP = len(Stack_pairs)  # Length of total stack pairs
    states = [0]*(NSP)      # Choices of states depends on length of state pairs
    for i in Stack_pairs:   # Loop over stack pairs
        couple = Stack_pairs[i]
        L = len(couple)
        new_couple = [0]*B
        for j in range(0, L):
            element = np.sort(couple[j])[::-1]
            while len(element) < Slen:
                element = np.append(element, 0)
            new_couple[j] = element
        states[i] = new_couple
    shuffles = np.zeros((NSP, B))
    for i in range(0, NSP):
        for j in range(0,B):
            column = states[i][j]
            column = np.append(column, C_next)
            column = zero_delete(column)        # Zero_delete helps ensure 0s are not counted in the bubble_sort
            value = bubble_sort(column.copy())  # bubble_sort returns the number of reshufles
            shuffles[i][j] = value              # Update shuffles matrix
    return shuffles, states # Return states and shuffles for the given container input
    
# The outputs from above are in terms of a list of arrays. Change this into a matrix for better data manipulation
def matx_gen(listarr):
    matx_list = [0]*len(listarr)
    i = 0
    for L in listarr:
        matx_list[i] = np.column_stack((L[0], L[1]))
        i += 1
    return matx_list

# Removes the input container from a matrix
def removal(MX, r): # Inputs are the state, MX, and the removed container, r
    matx  = MX.copy()   # Copy the matrix
    row, col = matx.shape   # Find dimensions
    for i in range(0, row): # Loop over rows
        for j in range(0, col): # Loop over columns
            if matx[i, j] == r: # If an element is equal to the containe rof interest...
                matx[i, j] = 0  # Change to 0
    for j in range(0, row):     # Loop over remaining elements
        matx[j] = np.sort(matx[j])[::-1] #Sort them to remove the new space vacated by the 0
    return matx #return new matrix with the container removed

# Creates dictionary of states to make indexing easier
def dict_gen(matx, shuffles, level): # Inputs are matrix, the corresponding shuffles, and the level in the process this state is at
    nodes = {}          # Dictionary for nodes
    Mlen = len(matx)    # Length of matrix (number of rows)
    count = 1           # Initialize indexing at 1
    for i in range (0, Mlen):   # Loop over rows
        index = str(level)+str(count)   # Create a dictionary index of level and index. For example, the first index at level 3 is "31"
        nodes[int(index)] = (matx[i].T, shuffles[i].T)  # Transpose the matrix because working with rows is easier than columns
        count += 1  # Change dictionary index by adding 1 to it; 31 -> 32
    return nodes

# Are two matrices equivalent? This tests if eithert two matrices are equal OR if the mirror image of another matrix is equal, both are
# valid solutions for the problems due to the independent nature of the columns.
def equivalency(MX1, MX2):
    if np.array_equal(MX1, MX2) == True:
        return True
    elif np.array_equal(np.flip(MX1, axis = 0), MX2) == True:
        return True
    else:
        return False

# This establishes the top nodes, i.e. the final solutions. These are assigned in numerical order, with the indexing having no significance
# other than the ability to trace the actions back
def upper(nodes, level):
    a = int(str(level+1)+"1")
    U = {}
    for i in nodes:
        u = {}
        for j in nodes[i][1]:
            u[a] = j
            a += 1
        U[i] = u
    return U

# This is for the process below the first input, calculating the next states in the sequence to find their reshuffles
def lower(state, con, col): # Inputs are current state, the container to be removed "con", and the column of interest
    stat = state.copy()     # Make a copy as to not change the base array
    choice = (stat[col]==0).argmax(axis=0)  # Find the first instance of a 0 in the state
    stat[col][choice] = con # Make it equal to the container
    count = 0
    for i in stat:          # Calculate the bubble sort
        count += bubble_sort(i)
    return count # Return the number of reshuffles

# This function finds the literal row (container stacking column) which the given container is in
def row_finder(state, con): # Search for container "con" in the state
    Tlen = len(state)
    for i in range(0, Tlen):
        if con in state[i]:
            return i
        
# This function determines the next state after the initial state defined in main
def next_state(nodes, level, con):  # Inputs are nodes, the level, and the container to be removed
    a = int(str(level-1)+"1")       # Dictionary indexing will be level-1
    S = {}  # Dictionary of states for traceback
    V = {}  # Dictionary of values for least cost path
    L = len(nodes)  # Length of nodes = number of current states
    keys = np.array([]) # Make array of the keys to sort thorugh the unique values
    for i in nodes:     # For the nodes
        keys = np.append(keys, i)   # Now dictionary can be indexed starting at 0.
                                    # For example, if the first element of nodes is 31, then keys[0] = 31.
    for i in range(0, L):       # Loop over full range of dictionary
        for j in range(i+1, L): # Loop over all remaining states after index "i"
            truth = equivalency(removal(nodes[keys[i]][0], con), removal(nodes[keys[j]][0], con))
            # The step above determines if you remove container "con" from the node[i] and node[j] (node[i] and node[j] will never
            # be equal due to the definitions in the loops) are they equal or not. We consider if the arrays match perfectly OR
            # if a flip will result in equality.
            if truth == True:   # If they are equivalent, then all of the below is executed
                nodei = nodes[keys[i]][0]           # node i is just ith the group of columns
                nodej = nodes[keys[j]][0]           # node j is the jth group of columns
                rnodei = removal(nodei, con)        # Remove container con from node i
                rnodej = removal(nodej, con)        # Remove container con from node j
                rowi = row_finder(nodei, con)       # What row is container con in node i? This is the action taken, not necessarily optimal
                rowj = row_finder(nodej, con)       # Same logic as above, except it is container con in node j
                loweri = lower(rnodei, con, rowi)   # Find the reshuffles for adding container con in group i
                lowerj = lower(rnodej, con, rowj)   # Find the reshuffles for adding container con in group j
                S[a] = removal(nodej, con), np.array([loweri, lowerj])  # States dictionary updates with states and respective reshuffles
                V[a] = {keys[i]: loweri , keys[j]: lowerj}  # Values matrix updates with sub dictionary with values of each respective state
                a += 1  # Index += 1 to create a unique next index
    return S, V         # Return states & values

# The final function. This loops over everything to arrive at a final answer.
def looper(containers, level, columns): # Inputs: list of containers to be stacked "containers", the penultimate level or sorting, and how
    order = containers[::-1]            # many columns are given. The order must be the reverse of the input containers for backward
    Clen = len(containers)              # induction. Clen is the length of the container array
    qshuffs, qstats = main(containers, columns)         # Find the penultimate shuffles and states
    qnodes = dict_gen(matx_gen(qstats), qshuffs, level) # Generate shuffles and states into a dictionary
    states = qnodes                 # Begin a master dictionary of all states for traceback
    res_dict = upper(qnodes, level) # The result dictionary will contain the full assortment of possible paths from one node to another
    current_nodes, current_shuffs = qnodes, qshuffs # "current_nodes" and "current_shuffs" will be the temp variables during the loop
    for i in range(1, Clen):        # Loop over the list of containers, EXCEPT for the first container as this has already been sorted
                                    # during the step with qnodes.
        current_nodes, current_shuffs = next_state(current_nodes, level, order[i])  # Change the temp nodes and shuffs 
        level -= 1                          # Decrease the level down 1
        for i in current_nodes:             # Loop over the temp nodes
            res_dict[i] = current_shuffs[i] # Add values to the value dictionary
            states[i] = current_nodes[i]    # Add states to state dictionary
    return res_dict, states                 # Return values and states


def find_minimum(links, index):
    path = {}
    while index in links:
        small = min(links[index], key=links[index].get)
        path[index] = links[index][small]
        index += 1
    return path     

def shortest_path(links, cons):
    Qlen = len(cons)
    a = Qlen-1
    index = int(str(a)+str(1))
    b = {}
    while a > 0:
        b = find_minimum(links, index)
        a -= 1
        index = int(str(a)+str(1))
        for i in b:
            for j in links:
                for k in links[j]:
                    if i == k:
                        links[j][k] += b[i]
    mindex = 11
    minarr = np.array([mindex])
    for i in range(0,Qlen - 1):
        mindex = min(links[mindex], key = links[mindex].get) 
        minarr = np.append(minarr, mindex)
        if i == 0:
            print("Total Cost:", links[11][mindex])
    return links, minarr

def reconstruct(states, minarr, cols, cons):
    Mlen = len(minarr)
    step = minarr[Mlen-2]
    Bay = states[step][0]
    row = np.argmin(states[step][1])
    j = 0
    i = Bay[row][j]
    while i != 0:
        j += 1
        i = Bay[row][j] 
    Bay[row][j] = cons[-1]
    col0x = -1
    col1x = -1
    Final = np.zeros((cols, Mlen))
    Shuffs_array = np.array([])
    for i in range(0, Mlen-1):
        New_Bay = removal(Bay, cons[i])
        removed = np.setdiff1d(Bay, New_Bay)
        removed_row = np.where(Bay == removed)[0][0]
        print(f"Place container {cons[i]} into column {removed_row}")
        if removed_row == 0:
            Final[removed_row][col0x] = cons[i]
            col0x -= 1
        elif removed_row == 1:
            Final[removed_row][col1x] = cons[i]
            col1x -= 1
        Bay = New_Bay
        print(Final.T)
        F0 = Final[0]
        F1 = Final[1]
        Shuffs0 = bubble_sort(zero_delete(F0.copy())[::-1])
        Shuffs1 = bubble_sort(zero_delete(F1.copy())[::-1])
        print(f"There are {Shuffs0+Shuffs1} reshuffles at this state.")
        print("~~~")
        Shuffs_array = np.append(Shuffs_array, Shuffs0+Shuffs1)
    print(f"Place container {cons[-1]} into column {row}")
    if row == 0:
        Final[row][col0x] = cons[-1]
        col0x -= 1
    elif row == 1:
        Final[row][col1x] = cons[-1]
        col1x -= 1
    print(Final.T)
    F0 = Final[0]
    F1 = Final[1]
    Shuffs0 = bubble_sort(zero_delete(F0.copy())[::-1])
    Shuffs1 = bubble_sort(zero_delete(F1.copy())[::-1])
    print(f"There are {Shuffs0+Shuffs1} reshuffles at this state.")
    Shuffs_array = np.append(Shuffs_array, Shuffs0+Shuffs1)
    return Shuffs_array

def function(q):
    start_time = time.time()
    l = len(q)-1
    c = 2
    links, states = looper(q, l, c) # Input containers, level, and columns
    new_links, mins = shortest_path(links, q)   
    #print(f"The reshuffle over time is{reconstruct(states, mins, c, q)}")  
    end_time = time.time()
    runtime = end_time - start_time
    #print(runtime)
    result = reconstruct(states, mins, c, q)
    return result[-1], result, runtime


# function that generates a number of unique permutations for input containers to be stacked
def generate_unique_permutations(N, n):
    """Generates N unique permutations of the digits 1 to n.

    Args:
        N: The number of unique permutations to generate.
        n: The number of digits to permute.

    Returns:
        A list of N unique permutations.
    """

    digits = list(range(1, n + 1))
    permutations = []

    while len(permutations) < N:
        random.shuffle(digits)
        permutation = tuple(digits)
        if permutation not in permutations:
            permutations.append(permutation)
    #print(permutations)
    return permutations


###########################################
##### CHANGE INPUTS BELOW TO RUN CODE #####
###########################################

N = 24
n = 4


# run multiple iterations
def run_analysis(N, n):
    # N is the number of runs
    # n is the number of containers

    permutations = generate_unique_permutations(N, n)

    results = []
    for permutation in permutations:
        result = function(permutation)
        results.append(result)

    df = pd.DataFrame(results, columns=['NumReshuffs','ReshuffleCount','Runtime(s)'])
    print(df)
    return df

df = run_analysis(N,n)

print(f"Average number of reshuffles for DP: {round(df['NumReshuffs'].mean(), 2)}")
print(f"Average runtime: {round(df['Runtime(s)'].mean(), 8)} seconds")


###########################################
#####    PLOT RESHUFFLES OVER TIME    #####
###########################################

# Extract the lists of arrays from the DataFrame
data_lists = df['ReshuffleCount'].tolist()

# Calculate the mean, standard deviation, min, and max for each position
means = np.mean(data_lists, axis=0)
stds = np.std(data_lists, axis=0)
mins = np.min(data_lists, axis=0)
maxs = np.max(data_lists, axis=0)

# Create a plot
plt.figure(figsize=(10, 6))

# Plot the mean values
plt.plot(means, label='Mean')

# Plot the standard deviation bands
plt.fill_between(range(len(means)), means - stds, means + stds, alpha=0.2, label='Std Dev')

# Plot the min and max lines
plt.plot(mins, linestyle='--', color='gray', label='Min')
plt.plot(maxs, linestyle='--', color='gray', label='Max')

# Customize the plot
plt.xlabel('Time Elapsed (# iterations)')
plt.ylabel('Number of Reshuffles')
plt.title(f'Reshuffles over time for 2 container bay\nwith 4 incoming containers, 24 iterations')
plt.legend()
plt.grid(True)
plt.show()