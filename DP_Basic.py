import numpy as np
import random
import matplotlib.pyplot as plt
import time

start_time = time.time()

n = 10 # set number of incoming containers to be stacked (must be less than 9 for this case)

H = 4 # max allowable stack height
B = 3 # number of container columns

C = np.arange(1,n+1) # generate containers
random.shuffle(C) # randomly assign priorities by shuffling

#C= np.array([1, 2, 3, 8, 7, 4, 6, 5]) # bad case for 3 x 3
print(f"Incoming container priority order: {C} \n")
Clen = len(C)

State = np.zeros((Clen+1, H, B))

# define actions
Actions = np.array([H-1,0])
Action_Set = np.array([0])
for b in range(1,B):
    Actions = np.vstack((Actions, np.array([H-1, b])))
    Action_Set = np.append(Action_Set, b)
print(Action_Set)



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

def stack(state, a, t):
    newcycle = np.zeros((H, B))
    newcycle[a[0]][a[1]] = C[t]
    cycle = state[t] + newcycle
    cyclecopy = cycle.copy()
    reshuffles = bubble_sort(cyclecopy)
    return cycle, reshuffles
    
R_count = np.zeros(Clen+1)
T_count = np.linspace(0, Clen, Clen+1)
for t in range(0,Clen):
    V_c = np.array([])
    V_r = np.array([])
    for q in Actions:
        V_q = stack(State, q, t)
        V_c = np.append(V_c, V_q[0])
        V_r = np.append(V_r, V_q[1]) 
    V_c = np.reshape(V_c, (len(Actions),H,B))                     
    A = int(np.argmin(V_r))
    Q = Action_Set[A]
    print(f"Container {C[t]} will be placed in column {Q}")
    print(f'Total number of reshuffles:{int(np.min(V_r))} \n')
    State[t+1] = V_c[A]
    R_count[t+1] = np.min(V_r)
    if Actions[A][0] > 0:
        Actions[A][0] -= 1
    elif Actions[A][0] == 0:
        Actions = np.delete(Actions, A, 0)
        Action_Set = np.delete(Action_Set, A)

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
plt.show()
