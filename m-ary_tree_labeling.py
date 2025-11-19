# Format: {
#           level 0: [
#                       Root Node
#                    ]
#           level 1: [
#                       Node
#                       Node
#                       Node
#                    ]
#           }

import math
from collections import deque

class Node:
    def __init__(self, key=0):
        self.key = key
        self.children = []
        self.edge_weight = 0

class Tree:
    def __init__(self, m, h):
        self.m = m
        self.h = h
        self.current_edge_weight = 2
        self.edge_weights_used = []
        self.tree = {}
        self.root = Node(key=1)
        self.tree[0] = [self.root]
        self.build_tree(self.root, 1)
        self.label_verticies()
        self.label_edges_that_have_keys()
        self.lebel_edges_forward()
        self.label_edges_reverse()
        self.label_remaining_keys()

    def set_next_edge_weight(self, node):
        if node.edge_weight == 0:
            while self.current_edge_weight in self.edge_weights_used:
                self.current_edge_weight += 1
            node.edge_weight = self.current_edge_weight
            self.edge_weights_used.append(self.current_edge_weight)
            self.current_edge_weight += 1

    def set_edge_weight(self, node, edge_weight):
        if node.edge_weight == 0:
            node.edge_weight = edge_weight
            self.edge_weights_used.append(edge_weight)

    def build_tree(self, parent_node, current_level):
        if current_level > self.h:
            return
        if current_level not in self.tree:
            self.tree[current_level] = []
        for _ in range(self.m):
            child = Node()
            parent_node.children.append(child)
            self.tree[current_level].append(child)
            self.build_tree(child, current_level + 1)

    def label_verticies(self):
        v = ((self.m ** (self.h + 1)) - 1) // (self.m - 1)
        self.root.key = 1
        d = math.floor((math.ceil(v / 2)) / (self.m - 1))
        self.tree[1][1].key = d
        for j in range(2, self.m):
            new_key = self.tree[1][j-1].key + d
            self.tree[1][j].key = new_key
        self.tree[1][0].key = 1
        self.tree[2][0].key = 2
        self.tree[1][-1].key = math.ceil(v / 2)

    def label_edges_that_have_keys(self, parent_node=None):
        if parent_node is None:
            parent_node = self.root
        for child in parent_node.children:
            if child.key and parent_node.key:
                self.set_edge_weight(child, (child.key + parent_node.key))
            self.label_edges_that_have_keys(child)

    def lebel_edges_forward(self, parent_node=None):
        if parent_node is None:
            parent_node = self.root
        for child in parent_node.children:
            if parent_node is self.root and child is parent_node.children[-1]:
                continue
            self.set_next_edge_weight(child)
            self.lebel_edges_forward(child)

    def label_edges_reverse(self, parent_node=None):
        if parent_node is None:
            parent_node = self.root.children[-1]
        for child in parent_node.children:
            self.label_edges_reverse(child)
            self.set_next_edge_weight(child)

    def label_remaining_keys(self, parent_node=None):
        if parent_node is None:
            parent_node = self.root
        for child in parent_node.children:
            child.key = child.edge_weight - parent_node.key
            self.label_remaining_keys(child)

    def find_max_key(self, root=None):
        if root is None:
            root = self.root
        max_key = root.key
        queue = deque([root])
        while queue:
            node = queue.popleft()
            if node.key > max_key:
                max_key = node.key
            for child in node.children:
                queue.append(child)
        return max_key

    def print_tree(self):
        for level, nodes in self.tree.items():
            indent = "    " * level
            for node in nodes:
                print(f"{indent}| key: {node.key}, edge_weight: {node.edge_weight}")

def has_duplicates(lst):
    return len(lst) != len(set(lst))


m = 3
h = 3
tree = Tree(m, h)

#tree.print_tree()

v = ((m ** (h + 1)) - 1) // (m - 1)
actual_max_key = tree.find_max_key()
max_key_can_be = math.ceil(v / 2)
print(f"v = {v}")
print(f"m = {m}")
print(f"h = {h}")
print(f"Number of vertices = {v}")
print(f"Max key can be = {max_key_can_be}")
print(f"Max key found = {actual_max_key}")
print(f"K condition met? = {max_key_can_be >= actual_max_key}")
print(f"Any duplicate edges? = {has_duplicates(tree.edge_weights_used)}")

'''
for i in range(2,10):
  for j in range(2, 10):
    m = i
    h = j
    tree = Tree(m, h)
    #tree.print_tree()

    v = ((m ** (h + 1)) - 1) // (m - 1)
    actual_max_key = tree.find_max_key()
    max_key_can_be = math.ceil(v / 2)
    print(f"m = {m} | h = {h} | K condition met? = {max_key_can_be >= actual_max_key} | Any duplicate edges? = {has_duplicates(tree.edge_weights_used)} | Number of vertices = {v} | Max key can be = {max_key_can_be} | Max key found = {actual_max_key}")
'''