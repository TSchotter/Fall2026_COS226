from rb_visualizer import Node, BinaryTree, TreeVisualizer

def getColor(n):  # Helper function to get the color of a node (or a None node)
    if n == None:
        return "BLACK"
    return n.color

def LeftRotate(oldRoot):
    # assuming that oldRoot is the root of this subtree

    print(f"Left rotating {oldRoot.data}...")
    newRoot = None # Placeholder for the new root

    # THIS IS HW to make the Left Rotate


    return newRoot

def RightRotate(oldRoot):
    # assuming that oldRoot is the root of this subtree
    print(f"Right rotating {oldRoot.data}...")
    newRoot = None # Placeholder for the new root

    # THIS IS HW to make the Right Rotate
    
    return newRoot

class RBTree(BinaryTree):


    def fix_add(self, n):
        parentColor = getColor(n.parent)

        
        if parentColor == "BLACK":
            return
        
        print(f"Fixing add for {n.data}...")

        # THIS IS HW. Check the uncle/aunt node from here and fix the situation
        # by this point we know we have a double red node chain that needs to be fixed.

    def fix_remove(self, node, parent, removedData):
        

        if parent == None: # double black node is the root, we're done
            return

        print(f"Fixing remove for {removedData}...")

        # THIS IS HW. Check the sibling node from here and fix the situation
        # by this point we know that (as long as add was working) that "node" is a db node.



    def add(self, data):

        newNode = Node(data)

        # Check if head is null
        if self.head == None:
            self.head = newNode
            self.head.color = "BLACK"
            return 

        currentNode = self.head
        
        # find the spot and add it to the tree
        while currentNode != None:
            if data < currentNode.data:
                if currentNode.left == None:
                    currentNode.left = newNode
                    newNode.parent = currentNode
                    break
                else:
                    currentNode = currentNode.left
            else:
                if currentNode.right == None:
                    currentNode.right = newNode
                    newNode.parent = currentNode
                    break
                else:
                    currentNode = currentNode.right

        # Check if adding needs to be fixed
        self.fix_add(newNode)




        self.head.color = "BLACK"

    def remove(self, data):
        if self.head == None:
            return -1
        
        # Normal BST remove
        curNode = self.head

        
        while(curNode != None):
            if curNode.data == data:
                self.realRemove(curNode)
                break
            elif curNode.data > data:
                curNode = curNode.left
            else:
                curNode = curNode.right
        
        if curNode == None:
            return -1
        
    def realRemove(self, node):

        print(f"Removing {node.data}...")
        # We'll handle first the two child case.
        if node.left != None and node.right != None:
            # find the next highest
            travNode = node.right
            while(travNode.left != None):
                travNode = travNode.left
            # swap data (though we don't care about the new location)
            
            node.data = travNode.data
            node = travNode # update node variable to new location

        # note the removed color
        removedColor = node.color
        removedData = node.data
        parent = node.parent


        
        # one child or no child
        if node.left != None:
            
            # have the left child take its place
            if node.parent == None: # we removed the head node
                self.head = node.left
            elif node.data >= node.parent.data:
                node.parent.right = node.left
            else:
                node.parent.left = node.left
            node.left.parent = parent
            node = node.left # keep track of child node that took its place
        else: # right child takes its place
        
            if node.parent == None: # we removed the head node
                self.head = node.right
            elif node.data >= node.parent.data:
                node.parent.right = node.right
            else:
                node.parent.left = node.right
            if node.right != None:
                node.right.parent = parent
            node = node.right # keep track of child node that took its place
        

        if parent == None: # we removed the head node
            self.head = node

        # Time to check if we need to fix the tree
        if removedColor == "RED": # red node removed, no worries
            return
        if getColor(node) == "RED": # red child took place, change it to black
            node.color = "BLACK"
            return
        
        # black node child took place
        self.fix_remove(node, parent, removedData) # parent is passed in case the node is None



    def search(self, data):
        pass

visualizer = TreeVisualizer()

def main():
    nodes = []


    # Read from nodes.txt
    with open('nodes.txt', 'r') as file:
        nodes = file.readlines()
    
    # Create the tree
    tree = RBTree()
    
    # Add the nodes to the tree
    for node in nodes:
        print(f"Adding {node}...")
        tree.add(int(node))
        
    #visualizer.add_to_stack(tree)
    tree.remove(1)
    visualizer.add_to_stack(tree)
    tree.remove(44)
    visualizer.add_to_stack(tree)
    tree.remove(45)
    visualizer.add_to_stack(tree)
    tree.remove(17)
    visualizer.add_to_stack(tree)
    tree.remove(20)
    visualizer.add_to_stack(tree)
    tree.remove(74)
    visualizer.add_to_stack(tree)
    tree.remove(56)
    visualizer.add_to_stack(tree)
    tree.remove(6)
    visualizer.add_to_stack(tree)
    tree.remove(4)
    visualizer.add_to_stack(tree)
    
    # Visualize the tree
    visualizer.visualize()


if __name__ == "__main__":
    main()

