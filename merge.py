import itertools as it
import numpy as np
import time

start_time = time.time()

C = np.array([2, 4, 3, 1])
C_next = np.array([2, 1])  # stacking container 3
print("Container sequence:", C)


def bubble_sort(col):
    Ylen = len(col)
    swaps = 0
    for j in range(Ylen):
        for k in range(0, Ylen - j - 1):
            if col[k] < col[k + 1]:
                col[k], col[k + 1] = col[k + 1], col[k]
                swaps += 1
    return swaps


def zero_delete(arr):
    N = len(arr)
    new_arr = np.array([])
    for i in range(0, N):
        if arr[i] != 0:
            new_arr = np.append(new_arr, arr[i])
    while len(new_arr) > N:
        new_arr = np.append(new_arr, 0)
    return new_arr


def main(Containers, B):
    Clen = len(Containers)
    C_next = Containers[-1]
    Containers_1 = np.delete(Containers, Clen - 1)
    Sort_cons = np.sort(Containers_1)
    Slen = len(Sort_cons)
    Iter_combos = {}
    for i in range(1, Slen + 1):
        Iter_combos[i] = it.combinations(Sort_cons, r=i)
    Stack_combos = {}
    j = 0
    for i in range(1, Slen + 1):
        for IC in Iter_combos[i]:
            IC_array = np.array(IC)
            Stack_combos[j] = IC_array
            j += 1
    N = len(Stack_combos)
    N1 = int(N - 1)
    N12 = int(N1 / 2)
    Stack_pairs = {}
    for i in range(0, N12):
        for j in range(N12, N1):
            if len(np.intersect1d(Stack_combos[i], Stack_combos[j])) == 0:
                Stack_pairs[i] = Stack_combos[i], Stack_combos[j]
    Stack_pairs[N12] = np.zeros(Slen), Stack_combos[N - 1]
    NSP = len(Stack_pairs)
    states = [0] * (NSP)
    for i in Stack_pairs:
        couple = Stack_pairs[i]
        L = len(couple)
        new_couple = [0] * B
        for j in range(0, L):
            element = np.sort(couple[j])[::-1]
            while len(element) < Slen:
                element = np.append(element, 0)
            new_couple[j] = element
        # print(f" State {i} has {B} columns: column 0 is {new_couple[0]} and column 1 is {new_couple[1]}")
        states[i] = new_couple
    shuffles = np.zeros((NSP, B))
    for i in range(0, NSP):
        for j in range(0, B):
            column = states[i][j]
            column = np.append(column, C_next)
            column = zero_delete(column)
            value = bubble_sort(column.copy())
            # print(f"If you place container {C_next} in column {j} of state {i} there will be {value} reshuffles")
            shuffles[i][j] = value
    return shuffles, states


def matx_gen(listarr):
    matx_list = [0] * len(listarr)
    i = 0
    for L in listarr:
        matx_list[i] = np.column_stack((L[0][::-1], L[1][::-1]))
        i += 1
    return matx_list


def min_finder(matx):
    baseline = np.inf
    Mlen = len(matx)
    for i in range(0, Mlen):
        if np.min(matx[i]) < baseline:
            baseline = np.min(matx[i])
    for i in range(0, Mlen):
        if np.min(matx[i]) == baseline:
            print(np.argmin(matx[i]), i)


def removal(matx, r):
    row, col = matx.shape
    for i in range(0, row):
        for j in range(0, col):
            if matx[i, j] == r:
                matx[i, j] = 0
    for j in range(0, col):
        matx[:, j] = np.sort(matx[:, j])
    if matx[row - 1][0] > matx[row - 1][1]:
        matx = np.flip(matx, axis=1)
    return matx


def dict_gen(matx, count):
    nodes = {}
    Mlen = len(matx)
    for i in range(0, Mlen):
        nodes[count] = matx[i]
        count -= 1
    return nodes, count


def equivalency(MX1, MX2):
    L1 = len(MX1)
    L2 = len(MX2)
    if L2 > L1:
        MX2 = np.delete(MX2, 0, 0)
    elif L1 > L2:
        MX1 = np.delete(MX1, 0, 0)
    else:
        MX1 = MX1
    if np.array_equal(MX1, MX2) == True:
        return True
    elif np.array_equal(np.flip(MX1, axis=1), MX2) == True:
        return True
    else:
        return False


# q = np.array([2, 1, 4, 3])
# r = np.array([2, 1, 4])
# s = np.array([2, 1])

q = C
r = q[:-1]
s = r[:-1]
print("r, s are:", r, s)

qshuffs, qstats = main(q, 2)
rshuffs, rstats = main(r, 2)
sshuffs, sstats = main(s, 2)

count = 7
qnodes, qcount = dict_gen(matx_gen(qstats), count)
rnodes, rcount = dict_gen(matx_gen(rstats), qcount)
snodes, scount = dict_gen(matx_gen(sstats), rcount)

shuff_list = [qshuffs, rshuffs, sshuffs]
print(shuff_list)


def gen_tree_links(shuff_list):
    temp_tree_links = {}
    a = 15
    b = 7
    for i in shuff_list:
        for j in i:
            temp_tree_links[b] = {(a - 1): j[0], a: j[1]}
            a -= 2
            b -= 1
    return temp_tree_links


tree_links = gen_tree_links(shuff_list)
print("Cost dictionary:", tree_links)


def reverse_min_path_sum(tree):
    """
    Calculate the minimum path sum from leaf nodes to the root node by dynamic programming.
    :param tree: A nested dictionary representing the binary tree.
    :return: Minimum path sum and the optimal path from a given leaf to the root.
    """
    dp = {}  # dp[node] stores the minimum path sum to any leaf.
    reverse_tree = {}  # Reverse mapping: child -> parent
    parent_link = {}  # Track the cost for each child -> parent link

    # Build the reverse mapping (child -> parent)
    for parent, children in tree.items():
        for child, cost in children.items():
            reverse_tree[child] = parent
            parent_link[(parent, child)] = cost
        if parent not in reverse_tree:
            reverse_tree[parent] = None  # Mark root node with no parent

    # Initialize dp for all nodes
    all_nodes = set(tree.keys()).union(*[children.keys() for children in tree.values()])
    dp = {node: float('inf') for node in all_nodes}

    # Initialize dp for all nodes
    for node in all_nodes:
        if node not in tree or not tree[node]:  # If the node has no children, it's a leaf node
            if node in reverse_tree:  # If the node has a parent
                parent = reverse_tree[node]
                dp[node] = parent_link.get((parent, node), float('inf'))
            else:
                dp[node] = 0  # For isolated nodes
        else:
            dp[node] = float('inf')  # Default for non-leaf nodes
        # print(f"Initial dp[{node}] = {dp[node]}")

    # Bottom-up dynamic programming
    for child in sorted(reverse_tree.keys(), reverse=True):  # Process from leaves upwards
        if child in reverse_tree and reverse_tree[child] is not None:
            parent = reverse_tree[child]
            cost = parent_link[(parent, child)]
            dp[parent] = min(dp[parent], dp[child] + cost)

    # Reconstruct the path from any leaf to the root
    def reconstruct_path(leaf):
        path = [leaf]
        while reverse_tree[leaf] is not None:
            parent = reverse_tree[leaf]
            path.append(parent)
            leaf = parent
        return list(reversed(path))  # Reverse to get root-to-leaf order

    # Find the optimal leaf with the minimum path
    optimal_leaf = min(dp, key=lambda x: dp[x] if x not in tree or not tree[x] else float('inf'))
    return dp[optimal_leaf], reconstruct_path(optimal_leaf)


print("----Dynamic Programming Result----")
min_sum, optimal_path = reverse_min_path_sum(tree_links)
end_time = time.time()
print("Minimum reshuffle sum:", min_sum)
print("Optimal move:", optimal_path)
print("Total running time:", end_time - start_time)