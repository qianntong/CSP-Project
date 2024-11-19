import numpy as np

def bubble_sort_count(arr):
  """Sorts a list of numbers using the bubble sort algorithm.

  Args:
    arr: The list to be sorted.

  Returns:
    The sorted list.
  """
  arr = np.array(arr)
  n = len(arr)
  swaps = 0

  # Traverse through all array elements
  for i in range(n):

    # Last i elements are already in place
    for j in range(0, n-i-1):

      # Traverse the array from 0 to n-i-1
      # Swap if the element found is greater
      # than the next element
      if arr[j] > arr[j+1] :
        arr[j], arr[j+1] = arr[j+1], arr[j]
        swaps +=1

  return swaps

# usage
#my_list = [0,12,22,5,6,13]
# num_swaps = bubble_sort_count()
# print(num_swaps)

def split_list(lst, n):
    """Splits a list into smaller lists of length n."""
    return [lst[i:i + n] for i in range(0, len(lst), n)]


# usage
# lst = [1, 2, 3, 4, 5, 6, 7, 8, 9]
# n = 3

# result = split_list(lst, n)
# print(result)