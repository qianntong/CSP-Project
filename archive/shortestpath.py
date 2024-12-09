def tree_index(n):   # tree index for each node
    tree_indices = {}
    index = 1
    for i in range(1, n + 1):
        nodes_in_level = 2 ** (i - 1)
        tree_indices[i] = list(range(index, index + nodes_in_level))
        index += nodes_in_level
    return tree_indices


n = 4   # numbers of containers
# States: generate tree levels
print("Tree index:", tree_index(n))
indexes = tree_index(n)
for level, nodes in indexes.items():
    print(f"Level {level}: {nodes}")

# Links: required input data structure:
# From parent node 1 to other 2^n options
tree_links = {
    1: {2: 0, 3: 0},  # parent node 1: subnodes are 2 & 3，with reshuffle times (values) of 0 and 0
    2: {4: 2, 5: 4},
    3: {6: 2, 7: 0},
    4: {8: 1, 9: 1},
    5: {10: 2, 11: 0},
    6: {12: 1, 13: 1},
    7: {14: 1, 15: 1},
}


def reverse_min_path_sum(tree):
    """
    Calculate the minimum path sum from leaf nodes to the root node by dynamic programming.
    :param tree: A nested dictionary representing the binary tree.
    :return: Minimum path sum and the optimal path from a given leaf to the root.
    """
    dp = {}         # dp[node]: the minimum path sum to any leaf
    reverse_tree = {}  # Reverse mapping: child -> parent
    parent_link = {}   # Track the cost for each child -> parent link

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
        print(f"Initial dp[{node}] = {dp[node]}")

    # Bottom-up dynamic programming
    for child in sorted(reverse_tree.keys(), reverse=True):  # Process from leaves upwards
        if child in reverse_tree and reverse_tree[child] is not None:
            parent = reverse_tree[child]
            cost = parent_link[(parent, child)] # reshuffle times on this state
            dp[parent] = min(dp[parent], dp[child] + cost)  # bellman equation

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
print("Minimum reshuffle sum:", min_sum)
print("Optimal move:", optimal_path)
