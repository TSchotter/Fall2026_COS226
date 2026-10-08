from btree_visualizer import Tree, TreeVisualizer, Bucket, DataItem


treevisualizer = TreeVisualizer()

class BucketNode(Bucket):

    def add(self, item, left_link = None):
        #check if node is a leaf node

        if self.is_leaf:
            # if node is a leaf node, we're working with a DataItem object.
            
            # find the correct index to insert the item
            index = 0
            #print(f"Adding item {item.key} to leaf node {self.keys}")
            while index < len(self.keys) and item.key > self.keys[index].key:
                #print(f"Item {item.key} is less than {self.keys[index].key}, incrementing index")
                index += 1
            self.keys.insert(index, item)
            # check if the node has reached the max number of keys
            if len(self.keys) >= self.maxdegree:
                return 1 # return 1 to indicate that the node needs to be split
        else:
            # if node is not a leaf node, we need to find the correct child node to add the item to
            print(f"Adding item {item} to internal node {self.keys}")

            index = 0
            while index < len(self.keys) and item > self.keys[index]:
                index += 1

            print(f"Adding item {item} to internal node {self.keys} at index {index}")
            print(f"Left link: {left_link}")
            self.keys.insert(index, item)
            self.links.insert(index, left_link)

            if len(self.keys) == self.maxdegree:
                return 1
        return 0

    def remove(self, key):
        #find the correct index to remove the key, will only be used for leaf nodes
        target = 0
        for item in self.keys:
            if item.key == key:
                return self.keys.pop(target)
            if item.key > key:
                return -1
            target += 1
        return -1

class BTree(Tree):
    def add(self, key, value):

        item = DataItem(key, value)
        if self.root is None:
            self.root = BucketNode(self.maxdegree)
            self.root.add(item)
            return

        current_node = self.root
        while not current_node.is_leaf:
            index = 0
            while index < len(current_node.keys) and item.key > current_node.keys[index]:
                index += 1
            current_node = current_node.links[index]
        split = current_node.add(item) # returns 1 if the node needs to be split, 0 otherwise
        if split == 1:
            self.split_leaf_node(current_node)

    def remove(self, key):
        # first, find the correct leaf node to remove the key from

        current_node = self.root
        if current_node is None:
            return -1
        
        # memory is used to store the bucket we find the key in, so we can fix it later if needed
        memory = None
        memory_index = 0

        while not current_node.is_leaf:
            target = 0
            for item in current_node.keys:
                if item > key:
                    break
                elif item == key:
                    memory = current_node
                    memory_index = target
                target += 1
            current_node = current_node.links[target]
        
        print(f"Key: {key}")
        print(f"Memory: {memory}")
        print(f"Leaf Found: {current_node}")

        #if current_node.parent == memory: # we fix this in normal operations
        #   memory = None

        if memory != None:
            print(f"Fixing memory for {key}")
            next_key = self.find_next_key(current_node, key)
            print(f"Next key was {next_key}")
            if next_key != None:
                self.fix_memory(memory, memory_index, next_key)

        # try to remove the key from the leaf node
        remove = current_node.remove(key)
        
        if remove != -1:
            print(f'Checking if removing {remove.key} from {current_node.keys} caused a underflow')
            #treevisualizer.add_to_stack(self)
            if len(current_node.keys) < current_node.maxdegree/2-1:
                self.fix_leaf_node(current_node, memory)

            return f'Key Removed: {remove.key} with value {remove.value}'
        else:
            return f'Key not found'


    def find_next_key(self, node, key): 
        # helper function to find the next key in the tree
        # will only be used on the leaf node
        target = 0
        for item in node.keys:
            if item.key == key:
                break
            target += 1

        if len(node.keys)>1:
            return node.keys[target+1].key
        elif node.next:
            return node.next.keys[0].key
        else:
            return None

    def fix_memory(self, node, index, newKey):
        # helper function to fix the remembered node
        # will only be used on internal nodes
        node.keys[index] = newKey

    def fix_leaf_node(self, node, memory):
        # Check if left is available to steal from
        print(f"Checking if nodes neighbors are available to steal from")
        left_node, right_node, link_index = self.get_siblings(node)
                
        if self.valid_steal(left_node):
            self.leaf_steal(node, 'left')
        elif self.valid_steal(right_node):
            self.leaf_steal(node, 'right')
        elif left_node != None:
            self.leaf_merge(left_node, node)
        else:
            self.leaf_merge(node, right_node)

    def get_siblings(self, node): # helper function to get the left and right siblings of a node
        left_node = None
        right_node = None

        target = 0
        for i in node.parent.links:
            if i == node:
                break
            target += 1

        if target == 0:
            left_node = None
        else:
            left_node = node.parent.links[target-1]
        
        if target == len(node.parent.keys):
            right_node = None
        else:
            right_node = node.parent.links[target+1]
        
        return left_node, right_node, target

    def valid_steal(self, node): # helper function to check if a node has enough keys to steal from
        if node is None:
            return False
        if len(node.keys) > self.maxdegree/2:
            return True
        return False

    def leaf_steal(self, node, direction):
        if direction == 'left':
            other = node.prev
            print(f"Stealing from left node {other.keys}")
            node.keys.insert(0, other.keys.pop())
        else:
            other = node.next
            print(f"Stealing from right node {other.keys}")
            node.keys.append(other.keys.pop(0))

        print(f"Node after stealing: {node.keys}")
        self.fix_internal_node_keys(node.parent)

    
    def leaf_merge(self, left_node, right_node):
        print(f"Merging left node {left_node.keys} and right node {right_node.keys}")

        # stuff all the nodes into the left node
        for key in right_node.keys:
            left_node.keys.append(key)
        
        # fix the next/prev
        left_node.next = right_node.next
        if right_node.next != None:
            right_node.next.prev = left_node

        # remove the key and link from the parent node
        parent = left_node.parent


        target = 0
        for i in parent.links:
            if i == left_node:
                break
            target += 1
        print(f"Target: {target}")
        parent.keys.pop(target)
        parent.links.pop(target+1)
        self.fix_internal_node_keys(parent)

        # Check if the parent node underflowed
        if len(parent.keys) < self.maxdegree/2-1:
            print(f"Parent node {parent.keys} underflowed")
            self.fix_internal_node(parent)
        
    def fix_internal_node(self, node): # helper function to decide how to fix an internal node
        print(f"Fixing underflow for internal node {node.keys}")
        # if root, not a problem
        if node.parent == None:
            return
    

        left_sibling, right_sibling, link_index = self.get_siblings(node)
        print(f"Left sibling: {left_sibling}")
        print(f"Right sibling: {right_sibling}")
        print(f"Link index: {link_index}")
        if self.valid_steal(left_sibling):
            self.internal_steal(node, left_sibling, link_index, 'left')
        elif self.valid_steal(right_sibling):
            self.internal_steal(node, right_sibling, link_index, 'right')
        elif left_sibling != None:
            self.internal_merge(left_sibling, node, link_index-1)
        else:
            self.internal_merge(node, right_sibling, link_index)

    def internal_steal(self, node, sibling, i, direction):
        print(f"Internal Stealing from {direction} sibling {sibling.keys}, index at parent is {i}")
        if direction == 'left':
            #rotate the key in
            node.keys.insert(0, node.parent.keys[i-1])
            node.parent.keys[i-1] = sibling.keys.pop()
            
            # move the link to the node
            node.links.insert(0, sibling.links.pop())
            # fix the parent link
            node.links[0].parent = node
        else:
            #rotate the key in
            node.keys.append(node.parent.keys[i])
            node.parent.keys[i] = sibling.keys.pop(0)
            # update the parent link
            sibling.links[0].parent = node
            # move the link to the node
            node.links.append(sibling.links.pop(0))

    def internal_merge(self, left_node, right_node, left_index):
        print(f"InternalMerging left node {left_node.keys} and right node {right_node.keys}, index at parent is {left_index}")

        #pull parent key into the left node
        left_node.keys.append(left_node.parent.keys[left_index])

        # add right_node keys to the left node
        left_node.keys.extend(right_node.keys)
        
        # fix right node links parents
        for link in right_node.links:
            link.parent = left_node
        
        # add right node links to the left node
        left_node.links.extend(right_node.links)

        # set new parent link to the left node
        left_node.parent.links[left_index+1] = left_node

        # remove the key and link from the parent node
        left_node.parent.keys.pop(left_index)
        left_node.parent.links.pop(left_index)

        # check if this pull removed the root node, and last key from the parent node
        if left_node.parent == self.root and len(left_node.parent.keys) == 0:
            self.root = left_node
            left_node.parent = None
            return

        # Check if the parent node underflowed
        if len(left_node.parent.keys) < self.maxdegree/2-1:
            print(f"Parent node {left_node.parent.keys} underflowed")
            self.fix_internal_node(left_node.parent)

        

    def fix_internal_node_keys(self, node):
        print(f"Fixing internal node keys {node.keys}")
        #treevisualizer.add_to_stack(self)
        for i in range(len(node.keys)):
            # each key needs to be checked
            link = node.links[i+1]
            print(f"Link: {link}")
            print(f"Updating key {i} to {link.keys[0].key}")
            node.keys[i] = link.keys[0].key


    def search(self, key):
        pass

    def split_leaf_node(self, node):
        #find the middle index
        middle_index = len(node.keys) // 2
        
        print(f"Splitting leaf node {node.keys}")
        print(f"Parent node: {node.parent}")
        print(f"Middle index: {middle_index}")
        
        print(f"Middle key: {node.keys[middle_index].key}")

        #create new left BucketNode (that is a leaf node)
        new_node_left = BucketNode(node.maxdegree)
        new_node_left.keys = node.keys[:middle_index]
        new_node_left.parent = node.parent

        #reassign the remaining keys to the original node
        node.keys = node.keys[middle_index:]

        #assign left and right node links
        new_node_left.next = node
        new_node_left.prev = node.prev
        node.prev = new_node_left

        if new_node_left.prev is not None:
            new_node_left.prev.next = new_node_left
        

        print(f"New left node: {new_node_left.keys}")
        print(f"Right node: {node.keys}")

        #check if this node is the root node
        if node.parent is None:
            self.root = BucketNode(node.maxdegree)
            self.root.keys = [node.keys[0].key]
            self.root.links = [new_node_left, node]
            self.root.is_leaf = False

            node.parent = self.root
            new_node_left.parent = self.root
            return

        print("About to add new node to parent node")
        #otherwise, add the new node to the parent node
        split = node.parent.add(node.keys[0].key, new_node_left)

        if split == 1:
            self.split_internal_node(node.parent)

    def split_internal_node(self, node):
        print(f"Splitting internal node {node.keys}")
        print(f"Parent node: {node.parent}")

        #find the middle index
        middle_index = len(node.keys) // 2
        middle_key = node.keys[middle_index]
        print(f"Middle key: {middle_key}")
        print(f"Splitting internal node {node.keys} at index {middle_index}")

        #create new left BucketNode (that is a internal node)
        new_node_left = BucketNode(node.maxdegree)
        new_node_left.parent = node.parent
        new_node_left.is_leaf = False
        new_node_left.keys = node.keys[:middle_index]
        new_node_left.links = node.links[:middle_index+1] # one extra link

        #go through the left links and assign the parent node
        for link in new_node_left.links:
            if link is not None:
                link.parent = new_node_left
        node.keys = node.keys[middle_index+1:] # remove the middle key from the original node
        node.links = node.links[middle_index+1:]

        #check if this node is the root node
        if node.parent is None:
            self.root = BucketNode(node.maxdegree)
            self.root.keys = [middle_key]
            self.root.links = [new_node_left, node]
            self.root.is_leaf = False
            node.parent = self.root
            new_node_left.parent = self.root
            return
        
        print("About to add new node to parent node")

        split = node.parent.add(middle_key, new_node_left)
        if split == 1:
            self.split_internal_node(node.parent)

def main():
    print("B+ Tree Example")
    tree = BTree(5)

    # Read data from file
    add_count = 1
    with open('data.txt', 'r') as file:
        lines = file.readlines()
    for line in lines:
        line = line.strip()
        key_str, data = line.split(',', 1)
        key = int(key_str.strip())
        data = data.strip()
        tree.add(key, data)
        print(f"{add_count}: Added key {key} with value '{data}'")
        #treevisualizer.add_to_stack(tree) # uncomment this to visualize the tree after every add
        if add_count % 1 == 0:
            treevisualizer.add_to_stack(tree)
        add_count += 1

    
    # uncomment this block to see each removal individually
    
    print(tree.remove(106))  # remove a key with no complications
    treevisualizer.add_to_stack(tree)
    print(tree.remove(45))  # remove a key that steals from the left sibling
    treevisualizer.add_to_stack(tree)
    print(tree.remove(37))  # remove a key that steals from the right sibling and needs to update the parent
    treevisualizer.add_to_stack(tree)
    print(tree.remove(60))  # remove a key that was spotted at the root and needs updating.
    treevisualizer.add_to_stack(tree)
    print(tree.remove(103)) # remove a key that couses a merge to the left.
    treevisualizer.add_to_stack(tree)
    print(tree.remove(34)) # remove a key that couses a merge to the right, causing an internal node steal to the right.
    treevisualizer.add_to_stack(tree)  # 6 remove checkpoint


    print(tree.remove(35)) # remove a key that was spotted at the root and needs updating.
    treevisualizer.add_to_stack(tree)
    print(tree.remove(50)) # remove a key that merges to the right, causing an internal node merge to the left. Bringing the root to be smol
    treevisualizer.add_to_stack(tree)
    print(tree.remove(85)) # remove a key that the parent needs to be updated 
    treevisualizer.add_to_stack(tree)
    print(tree.remove(50)) # attempt to remove a key that doesn't exist, should return -1
    treevisualizer.add_to_stack(tree)
    print(tree.remove(90)) # remove a key that the parent needs to be updated 
    treevisualizer.add_to_stack(tree)
    print(tree.remove(95)) # remove a key that merges to the left, causing an internal node steal from the left. 
    treevisualizer.add_to_stack(tree) # 12 remove checkpoint


    print(tree.remove(59)) # remove a key where nothing serious happens
    treevisualizer.add_to_stack(tree)
    print(tree.remove(55)) # remove a key that leaf merges to the left
    treevisualizer.add_to_stack(tree)
    print(tree.remove(20)) # remove a key where nothing serious happens
    treevisualizer.add_to_stack(tree)
    print(tree.remove(17)) # remove a key that has the leaf steal from the left 
    treevisualizer.add_to_stack(tree)
    print(tree.remove(5)) # remove a key that has the leaf merge to the right, causing an internal node merge to the right, lowering the height of the tree
    treevisualizer.add_to_stack(tree)
    print(tree.remove(100)) # remove a key where nothing serious happens
    treevisualizer.add_to_stack(tree) # 18 remove checkpoint
    '''
    
    # Read removal keys from file
    remove_keys = []
    with open('remove_data.txt', 'r') as file:
        lines = file.readlines()
    
    for line in lines:
        line = line.strip()
        if line:  # Only process non-empty lines
            key = int(line)
            remove_keys.append(key)
    
    # Perform removals
    remove_count = 1
    for i in remove_keys:
        print(f"Removal {remove_count}: {tree.remove(i)}")
        #treevisualizer.add_to_stack(tree) # uncomment this to visualize the tree after every remove

        if remove_count % 6 == 0:
            treevisualizer.add_to_stack(tree)
        remove_count += 1
    '''
    #treevisualizer.add_to_stack(tree)
    treevisualizer.visualize()

if __name__ == "__main__":
    main()