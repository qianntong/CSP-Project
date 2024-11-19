import numpy as np
import random

n = 30 # set number of incoming containers to be stacked (must be less than 9 for this case)

H = 5 # max allowable stack height
B = 6 # number of container columns

C = np.arange(1,n+1) # generate 6 containers
random.shuffle(C) # randomly assign priorities by shuffling

#C= np.array([1, 2, 3, 8, 7, 4, 6, 5]) # bad case for 3 x 3
print(f"Incoming container priority order: {C} \n")
Clen = len(C)

State = np.zeros((Clen+1, H, B))

# define actions
Actions = np.array([H-1,0])
for b in range(1,B):
    Actions= np.vstack((Actions, np.array([H-1, b])))
print(Actions)



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
    
for t in range(0,Clen):
    V_c = np.array([])
    V_r = np.array([])
    for q in Actions:
        V_q = stack(State, q, t)
        V_c = np.append(V_c, V_q[0])
        V_r = np.append(V_r, V_q[1]) 
    V_c = np.reshape(V_c, (len(Actions),H,B))                     
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
print(f"Final yard configuration:\n{State[-1]}\n")
    
print(f"Incoming container priority order: {C}")

# bad case: [1 2 3 8 7 4 6 5] 
        
