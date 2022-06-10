#!/usr/bin/env python
# coding: utf-8

# In[2]:


class extended_WCG_node:
    conflict_state = [
        ["c","g","s","t","w"],
        ["g","s","t","w"],
        ["c","g","s","w"],
        ["c","g","t","w"],
        ["g","s","w"],
        ["g","t","w"],
        ["c","g","w"],
        ["g","w"],
        ["c","s","t", "w"],
        ["s","t","w"],
        ["c","s","w"],
        ["s","w"],
        ["g","s","t"],
        ["c","s","t"],
        ["s","t"]
    ]
    
    def __init__(self, left=["w", "g", "c", "s", "t"], right=[], boat_side=False, children=[]):
        self.left = left
        self.right = right
        self.boat_side = boat_side
        self.children = children
    
    def gen_brand(self, visited, parent_map):
        children = []
        # the boat is on the left
        if not self.boat_side:
            for i in self.left:
                new_left = self.left[:]
                new_left.remove(i)
                new_right = self.right[:]
                new_right.append(i)
                for j in new_left:
                    next_left = new_left[:]
                    next_left.remove(j)
                    next_right = new_right[:]
                    next_right.append(j)
                    # considering instance when bringing 2 things at a time
                    if sorted(next_left) not in extended_WCG_node.conflict_state and not extended_WCG_node.check_visited(visited, next_left, next_right, not self.boat_side):
                      child = extended_WCG_node(next_left, next_right, not self.boat_side, [])
                      children.append(child)
                      parent_map[child] = self
                # considering instance when bringing 1 thing at a time
                if sorted(new_left) not in extended_WCG_node.conflict_state and not extended_WCG_node.check_visited(visited, new_left, new_right, not self.boat_side):
                    child = extended_WCG_node(new_left, new_right, not self.boat_side, [])
                    children.append(child)
                    parent_map[child] = self
            # considering instance when the shepherd travel alone
            if sorted(self.left) not in extended_WCG_node.conflict_state and not extended_WCG_node.check_visited(visited, self.left[:], self.right[:], not self.boat_side):
                child = extended_WCG_node(self.left, self.right, not self.boat_side, [])
                children.append(child)
                parent_map[child] = self
        # the boat is on the right
        else:
            for i in self.right:
                new_left = self.left[:]
                new_left.append(i)
                new_right = self.right[:]
                new_right.remove(i)
                for j in new_right:
                    next_left = new_left[:]
                    next_left.append(j)
                    next_right = new_right[:]
                    next_right.remove(j)
                    if sorted(next_right) not in extended_WCG_node.conflict_state and not extended_WCG_node.check_visited(visited, next_left, next_right, not self.boat_side):
                      child = extended_WCG_node(next_left, next_right, not self.boat_side, [])
                      children.append(child)
                      parent_map[child] = self
                if sorted(new_right) not in extended_WCG_node.conflict_state and not extended_WCG_node.check_visited(visited, new_left, new_right, not self.boat_side):
                    child = extended_WCG_node(new_left, new_right, not self.boat_side, [])
                    children.append(child)
                    parent_map[child] = self
            if sorted(self.right) not in extended_WCG_node.conflict_state and not extended_WCG_node.check_visited(visited, self.left[:], self.right[:], not self.boat_side):
                child = extended_WCG_node(self.left[:], self.right[:], not self.boat_side, [])
                children.append(child)
                parent_map[child] = self
        self.children = children
        
    def __str__(self):
        return str(self.left) + "~~~" + str(self.right) + "- The boat is on the " + ("Left" if not self.boat_side else "Right")
           
    def check_visited(visited, left, right, boat_side):
        return any(
            sorted(left) == sorted(i.left) and
            sorted(right) == sorted(i.right) and
            boat_side == i.boat_side
            for i in visited
        )
    
time_complex = 0
space_complex = 1 
def seq_action(start, dfs=True):
    global time_complex
    global space_complex
    visit = [start]
    node = start
    visited = []
    parent_map = {start: None}
    while visit:
        node = visit.pop()
        time_complex = time_complex + 1 # take time when a node is taked out of the array
        if not extended_WCG_node.check_visited(visited, node.left, node.right, node.boat_side):
            visited.append(node)
        node.gen_brand(visited, parent_map)
        if dfs:
          visit = visit + node.children 
        else:
          visit = node.children + visit
        space_complex = space_complex + len(node.children) # count the space when a node is generated 
        if sorted(node.right) == sorted(["c", "g", "s", "t","w"]):
            solution = []
            while node is not None:
                solution = [node] + solution
                node = parent_map[node]
            return solution
    return "Solution not found"

if __name__ == "__main__":
    start = extended_WCG_node()

    # DFS
    RUN_DFS = seq_action(start)
    print("DFS solution : ")
    for node in RUN_DFS:
        print(node, ', ', end='')
    print("\nTime complexity: ",time_complex)
    print("Space complexity: ",space_complex)
    
    # BFS
    time_complex = 0
    space_complex = 1
    RUN_BFS = seq_action(start, dfs= False)
    print("BFS solution : ")
    for node in RUN_BFS:
        print(node, ', ', end='')
    print("\nTime complexity: ",time_complex)
    print("Space complexity: ",space_complex)


# In[ ]:




