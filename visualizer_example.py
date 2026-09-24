

from binarytreeVisualizer import BinaryTree, Node, TreeVisualizer

# create a BST class that inherits from BinaryTree
class BST(BinaryTree):

    # adds a node to the tree
    def add(self, curNode, data):
        # start of the recursion
        if curNode == None:
            return Node(data) # ground state, return the node
        # look at data of node, compare it to incoming data
        if curNode.data == data:
            return curNode # if it's the same, just stop and return up
        if curNode.data > data:
            # recursive add
            curNode.left = self.add(curNode.left, data)
        else:
            curNode.right = self.add(curNode.right, data)
        return curNode

    


    # searches for a node in the tree, if it can't be found return -1
    def search(self, data):
        return -1

    def remove(self, curNode, target):

        # ground state, curNode = None, which means we couldn't find it
        if curNode == None:
            return None
        if curNode.data == target:
            # No child situation
            if curNode.left == None and curNode.right == None:
                return None
            # One child (no left)
            if curNode.left == None:
                # let parent know, the new node here is the right node
                return curNode.right 
            elif curNode.right == None:
                # let parent know the left child will take its place
                return curNode.left
            # two child
            # aim for next largest.
            # curNode = thing we want to swap with next seq
            swapTarget = curNode.right # step right once
            while(swapTarget.left != None): # go as far left as we can
                swapTarget = swapTarget.left
            # place the value of sT into cN
            curNode.data = swapTarget.data

            # find the duplicate data and remove it.
            curNode.right = self.remove(curNode.right, curNode.data)

        # didn't find it, search left or right
        if curNode.data > target:
            curNode.left = self.remove(curNode.left, target)
        else:
            curNode.right = self.remove(curNode.right, target)


def main():
    newBST = BST()

    # Create the visualizer
    visualizer = TreeVisualizer() 

    # Add the nodes to the tree
    # this is an example of adding them manually (not how you should do it)
    x = Node(5)
    x.right = Node(10)
    x.left = Node(2)
    newBST.head = x

    y = Node(12)
    newBST.head.right.right = y #manually adding nodes

    newBST.add(newBST.head, 1)

    #Add snapshot of the tree to the visualizer
    visualizer.add_to_stack(newBST)

    newBST.add(newBST.head, 100)
    visualizer.add_to_stack(newBST)

    newBST.add(newBST.head, 6)
    visualizer.add_to_stack(newBST)
    newBST.add(newBST.head, 70)
    visualizer.add_to_stack(newBST)
    newBST.add(newBST.head, 18)
    visualizer.add_to_stack(newBST)
    newBST.add(newBST.head, 2)
    visualizer.add_to_stack(newBST)
    newBST.add(newBST.head, 120)
    visualizer.add_to_stack(newBST)


    newBST.remove(newBST.head, 5)
    visualizer.add_to_stack(newBST)
    
    # perform some removals, add a snapshot to the visualizer after each remove
    


    # Start the visualizer
    visualizer.visualize()

if __name__ == "__main__":
    main()