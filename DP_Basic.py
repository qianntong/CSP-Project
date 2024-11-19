import numpy as np
import random
import matplotlib.pyplot as plt
import time

start_time = time.time()

n = 10 # set number of incoming containers to be stacked (must be less than 9 for this case)

H = 4 # max allowable stack height
B = 3 # number of container columns

C = np.arange(1,n+1)    # generate n containers
random.shuffle(C)       # randomly assign priorities by shuffling
Clen = len(C)           # total number of containers

# C= np.array([1, 2, 3, 8, 7, 4, 6, 5]) # bad case for 3 x 3
print(f"Incoming container priority order: {C} \n")

# create all state variables from the beginning;
# a state represents a side profile view of the containers in a stack in the yard;
# there will be Clen+1 matrices, one for each time step AND for time t=0;
# each state has H rows; for example, if the maximum height allowed is 4, there are 4 rows;
# each state has B columns;
# all states begin as 0 and will be filled in over the time loop
State = np.zeros((Clen+1, H, B))

# define actions; the actions are arrays with two values arranged as (row, column)
Actions = np.array([H-1,0]) # begin the actions matrix; each row represents the action
Action_Set = np.array([0])  # define an action set which is useful for the print statements
for b in range(1,B):        # loop over the values of B
    Actions = np.vstack((Actions, np.array([H-1, b])))  # vertical stack with the actions for row 0
    Action_Set = np.append(Action_Set, b)               # add to action set for each cycle

def bubble_sort(cycle):
    Ylen, Ycol = cycle.shape
    swaps = 0
    for i in range (0, Ycol):
        col = cycle[:,i]
        for j in range(Ylen):
            for k in range(0, Ylen-j-1):
                if col[k] > col[k+1]:
                    col[k], col[k+1] = col[k+1], col[k]
                    swaps += 1
    return swaps

# define a function which inputs the current state and action and determines if that
# action is taken what is the future state
def stack(state, a, t):         # function of state, a, and t
    newcycle = np.zeros((H, B)) # the future state, newcycle, is a same size matrix to the current
                                # state but filled with zeros
    newcycle[a[0]][a[1]] = C[t] # the action corresponds to a container being placed in a
                                # (row, column); add that to the numpy array of zeros
    cycle = state[t] + newcycle # this will be the new state generated given state[t] and a
    cyclecopy = cycle.copy()    # copy the new state for testing in the bubble sort
    reshuffles = bubble_sort(cyclecopy) #this will return the number of reshuffles
    return cycle, reshuffles    # return new state and number of reshuffles from bubble sort
    
R_count = np.zeros(Clen+1)              # for plotting, make an array of reshuffles at each time
T_count = np.linspace(0, Clen, Clen+1)  # for plotting, make an array of each time
for t in range(0,Clen): # loop over all containers, which is essentially the times past t=0
    V_c = np.array([])  # array to store future state matrices
    V_r = np.array([])  # array to store respective reshuffles for each state
    for q in Actions:   # loop over the number of actions that can be taken at time t, call this Q
        V_q = stack(State, q, t)        # this will return a possible new state and its reshuffles
        V_c = np.append(V_c, V_q[0])    # update future state matrices array
        V_r = np.append(V_r, V_q[1])    # update respective rehuffles array
    V_c = np.reshape(V_c, (len(Actions),H,B))   # reshape the V_c array into Q HxB matrices, where
                                                # Q is the number of actions available at t
    A = int(np.argmin(V_r))                     # action A is the index that represents the action
                                                # which produces the least costly future state
    X = Action_Set[A]                           # X is the action indexed by A
    print(f"Container {C[t]} will be placed in column {X}")     # action taken for minimal cost
    print(f'Total number of reshuffles:{int(np.min(V_r))} \n')  # rehuffles for minimal cost
    State[t+1] = V_c[A]         # the state at time t+1
    R_count[t+1] = np.min(V_r)  # update the reshuffle array for graphing
    if Actions[A][0] > 0:       # if an action is taken, it needs to be changed;
                                # the initital actions all place containers in the bottom row;
                                # however, we cannot put two contaienrs in the same spot;
                                # logically, if spot j is taken, the next container must be
                                # placed in spot j+1
        Actions[A][0] -= 1      # because we are using numpy indexing, we actually will be
                                # subtracting 1 from the action; consider at the start, the bottom
                                # row of the matrix is row H-1, so to move "up" a row we go from
                                # H-1 to H-2, therefore we subtract the action taken by 1
    elif Actions[A][0] == 0:    # if we are in the top row, no more actions can be taken as this
                                # would overfill the yard
        Actions = np.delete(Actions, A, 0)      # delete the action from the array of actions
        Action_Set = np.delete(Action_Set, A)   # delete that indexed action from the action set

print("States as containers are placed:")
print(State)


print(f"\nTotal number of reshuffles to clear stack: {int(min(V_r))} \n")
print(f"Final yard configuration:\n{State[-1]}\n")

print(f"Total runtime: {round(time.time()-start_time, 5)} seconds\n")


# compute reshuffles for naive approach where incoming containers are stacked vertically until filled
from helpers import bubble_sort_count, split_list
naive_swaps = 0
for i in split_list(C, H):
    naive_swaps += int(bubble_sort_count(i[::-1])) # calculate bubble sort swaps for reverse of arrays
print(f"Number of swaps if naively stacking: {naive_swaps} \n")

print(f"Incoming container priority order: {C}") # for reference


# plot reshuffles over time
plt.plot(T_count, R_count)
plt.title("Container Reshuffles over Time")
plt.xlabel("Time Elapsed")
plt.ylabel("Number of Reshuffles")
        
