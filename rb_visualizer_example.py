

from rb_visualizer import BinaryTree, Node, TreeVisualizer

# create a BST class that inherits from BinaryTree
class BST(BinaryTree):

    # adds a node to the tree, loop method
    def add(self, data):
        if (self.head == None):
            self.head = Node(data)
            return
        
        newNode = Node(data)

        currentNode = self.head
        while(currentNode != None):
            if (data < currentNode.data):
                if (currentNode.left == None):
                    currentNode.left = newNode
                    return
                else:
                    currentNode = currentNode.left
            else:
                if (currentNode.right == None):
                    currentNode.right = newNode
                    return
                else:
                    currentNode = currentNode.right
        return

    # searches for a node in the tree, if it can't be found return -1
    def search(self, data):
        if (self.head == None):
            return -1
        
        currentNode = self.head
        while(currentNode != None):
            if (data == currentNode.data):
                return currentNode
            elif (data < currentNode.data):
                if (currentNode.left == None):
                    return -1
                else:
                    currentNode = currentNode.left
            else:
                if (currentNode.right == None):
                    return -1
                else:
                    currentNode = currentNode.right
        return -1

    def remove(self, target):
        if (self.head == None): # no tree yet
            return -1
        
        if (self.head.data == target): # if what we're looking for is the head
            self.head = self.realRemove(self.head)
            return f"Successfully deleted {target}"

        curNode = self.head

        while(curNode != None):
            # things we know at this time
            # - target != curNode.data
            # - curNode != None

            # things that we don't know
            # - if we want to go left or right
            # - if left or right exists

            if (target > curNode.data):
                # look right
                
                if curNode.right == None:
                    return -1
                
                # we now know that right exists and we want to look right

                # found it, we want it to be replaced with either None or another node
                if curNode.right.data == target:
                    curNode.right = self.realRemove(curNode.right)
                    return f"Successfully deleted {target}"
                else:
                    curNode = curNode.right
            else:
                # look left
                if curNode.left == None:
                    return -1
                
                # we now know that right exists and we want to look right

                # found it, we want it to be replaced with either None or another node
                if curNode.left.data == target:
                    curNode.left = self.realRemove(curNode.left)
                    return f"Successfully deleted {target}"
                else:
                    curNode = curNode.left

        # was never in the tree
        return -1


    # Handle no child, one child, two child. Return new node (or None) that takes its place
    def realRemove(self, node):
        # no child
        if node.left == None and node.right == None:
            return None
        
        # one child
        if node.left == None or node.right == None:
            if node.left != None:
                return node.left
            else:
                return node.right
        
        #two child

        parentNode = node

        # find next highest
        travNode = node.right
        while(travNode.left != None):
            parentNode = travNode  #drag parentNode behind travNode
            travNode = travNode.left
        
        # swap data
        node.data, travNode.data = travNode.data, node.data

        #need to change parentNode
        
        #if parentNode is still just node
        if parentNode == node:
            parentNode.right = travNode.right
        else:
            parentNode.left = travNode.right
        
        return node



        

def printTree(node):
    # in-order print 
    if (node == None):
        return
    printTree(node.left)
    print(f"[ {node.data} ] ", end="")
    printTree(node.right)
def main():
    newBST = BST()

    # Create the visualizer
    visualizer = TreeVisualizer() 

    visualizer.add_to_stack(newBST)
    # Add the nodes to the tree
    newBST.add(50)
    newBST.add(25)
    newBST.add(20)
    newBST.add(10)
    newBST.add(100)
    newBST.add(120)
    newBST.add(200)
    newBST.add(75)
    newBST.add(60)
    newBST.add(80)
    #Add snapshot of the tree to the visualizer
    visualizer.add_to_stack(newBST)

    # change color of root node to black
    newBST.head.color = "BLACK"
    print("Root node color changed to BLACK")
    visualizer.add_to_stack(newBST)
    
    # perform some removals, add a snapshot to the visualizer after each remove
    newBST.remove(50)
    visualizer.add_to_stack(newBST)
    newBST.remove(25)
    visualizer.add_to_stack(newBST)
    newBST.remove(20)
    visualizer.add_to_stack(newBST)
    newBST.remove(10)
    visualizer.add_to_stack(newBST)


    # Start the visualizer
    visualizer.visualize()

if __name__ == "__main__":
    main()