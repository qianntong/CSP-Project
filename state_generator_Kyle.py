import numpy as np

B = 2
C = np.array([2, 1, 4, 3])

i = C[-1] # current container to be placed

prev_cont = np.sort(C[:i])[::-1] # containers in stack (already sorted)

full_config = np.pad(prev_cont,(0,len(prev_cont))) # full elements in state, with containers and zeros
#print(full_config)
start_state = np.reshape(full_config,(B,-1)) # all elements, with one column of containers and other column of zeros
print(start_state)
col1 = start_state[0]
col2 = start_state[1]

def swap_elements(list_in1, list_in2, index1, index2):
  list1 = list_in1.copy()
  list2 = list_in2.copy()
  temp = list1[index1]
  list1[index1] = list2[index2]
  list2[index2] = temp
  return [np.sort(list1)[::-1], np.sort(list2)[::-1]] # return reverse sorted lists

list_of_feasible_states = [[col1,col2]] # add initial state

for i in range(0,len(C)-1):
  print(i)
  list_of_feasible_states.append(swap_elements(col1, col2, i, i)) # swap elements at each index and add to list of feasible states
  
print(list_of_feasible_states) # returns all feasible states for a B = 2 configuration and n = 4 containers at i = 4

# Works for B = 2, will need to adjust for larger B