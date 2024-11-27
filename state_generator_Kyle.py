import numpy as np

B = 2
C = np.array([2, 1, 4, 3])


# i = C[-1] # current container to be placed

# prev_cont = np.sort(C[:i])[::-1] # containers in stack (already sorted)

# full_config = np.pad(prev_cont,(0,len(prev_cont))) # full elements in state, with containers and zeros
# #print(full_config)
# start_state = np.reshape(full_config,(B,-1)) # all elements, with one column of containers and other column of zeros
# #print(start_state)
# col1 = start_state[0]
# col2 = start_state[1]

def swap_elements(list_in1, list_in2, index1, index2):
  list1 = list_in1.copy()
  list2 = list_in2.copy()
  temp = list1[index1]
  list1[index1] = list2[index2]
  list2[index2] = temp
  return [np.sort(list1)[::-1].tolist(), np.sort(list2)[::-1].tolist()] # return reverse sorted lists

#list_of_feasible_states = [[col1,col2]] # add initial state

# for i in range(0,len(C)-1):
#   list_of_feasible_states.append(swap_elements(col1, col2, i, i)) # swap elements at each index and add to list of feasible states
  
#print(list_of_feasible_states) # returns all feasible states for a B = 2 configuration and n = 4 containers at i = 4

# Works for B = 2 and n = 4, will need to adjust for larger B or n (nested for loops)

list_of_feasible_states = []

for i in range(len(C))[::-1]:
  current_container = i
  print(f"Current container: {C[current_container]}")
  prev_containers = C[:current_container][::-1]
  prev_containers_sorted = np.sort(prev_containers)[::-1]
  print(f"Previous containers: {prev_containers}")
  print(f"Previous containers sorted: {prev_containers_sorted}")
  #print(C[:i+1][::-1])
  print('Generating feasible states...\n')

  full_config = np.pad(prev_containers_sorted,(0,len(prev_containers_sorted)))
  start_state = np.reshape(full_config,(B,-1))
  col1 = start_state[0]
  col2 = start_state[1]

  list_of_feasible_states.append([col1.tolist(), col2.tolist()])

  for j in range(0,len(prev_containers)):
    list_of_feasible_states.append(swap_elements(col1, col2, j, j))

print(list_of_feasible_states)