import numpy as np
import random

n = 8 # set number of incoming containers to be stacked (must be less than 9 for this case)

C = np.arange(1,n+1) # generate 6 containers
random.shuffle(C) # randomly assign priorities by shuffling
print(f"Incoming container priority order: {C} \n")
Clen = len(C)

State = np.zeros((Clen+1, 3, 3))
Actions = np.array([[2, 0],
                    [2, 1],
                    [2, 2]]) #first entry is height, second entry is stack

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
    newcycle = np.zeros((3, 3))
    newcycle[a[0]][a[1]] = C[t]
    cycle = state[t] + newcycle
    cyclecopy = cycle.copy()
    reshuffles = bubble_sort(cyclecopy)
    return cycle, reshuffles
    
for t in range(0,Clen):
    V_c = np.array([])
    V_r = np.array([])
    for q in Actions:
        V_q = stack(State, q, t)
        V_c = np.append(V_c, V_q[0])
        V_r = np.append(V_r, V_q[1]) 
    V_c = np.reshape(V_c, (len(Actions),3,3))                     
    A = int(np.argmin(V_r))
    print(f"Container {C[t]} will be placed in column {A}")
    print(f'Total number of reshuffles:{int(np.min(V_r))} \n')
    State[t+1] = V_c[A]
    if Actions[A][0] > 0:
        Actions[A][0] -= 1
    elif Actions[A][0] == 0:
        Actions = np.delete(Actions, A, 0)
    #print(C[t], V_r)

print("States as containers are placed:")
print(State)


print(f"\nTotal number of reshuffles to clear stack: {int(min(V_r))} \n")
print(f"Final yard configuration:\n{State[-1]}")
    
    

# bad case: [1 2 3 8 7 4 6 5] 
        
        
