# this is continuing from the visualizer_example.py

from binarytreeVisualizer import BinaryTree, Node, TreeVisualizer

def getHeight(curNode):
    if curNode == None:
        return 0
    return curNode.height

def getBalance(curNode): # should only return -2 to 2
    return getHeight(curNode.right)-getHeight(curNode.left)

def calcHeight(curNode): # calculate + update height of node
    curNode.height = max(getHeight(curNode.left), 
                         getHeight(curNode.right))+1

# rotate with curNode the root of the subtree we are rotating
def rightRotate(curNode):
    newRoot = curNode.left
    curNode.left = newRoot.right
    newRoot.right = curNode
    calcHeight(curNode) # old root got moved down, recalc height
    return newRoot

# same as right rotate but directions flipped
def leftRotate(curNode):
    newRoot = curNode.right
    curNode.right = newRoot.left
    newRoot.left = curNode
    calcHeight(curNode) # old root got moved down, recalc height
    return newRoot

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

        # check if out of balance
        balance = getBalance(curNode)
        if balance < -1: # left heavy, we need to...
            if getBalance(curNode.left) == 1: # slight right bend
                # straighten the bend
                curNode.left = leftRotate(curNode.left)
            
            # rotate, set curNode to new subTree root
            curNode = rightRotate(curNode)
        elif balance > 1: # right heavy
            if getBalance(curNode.right) == -1: #slight bend
                # straighten the bend
                curNode.right = rightRotate(curNode.right)
            curNode = leftRotate(curNode)
        
        # calculate the new height
        calcHeight(curNode)

        return curNode

    


    # searches for a node in the tree, if it can't be found return -1
    def search(self, data):
        searchPtr = self.head
        while(searchPtr != None): # iterative search
            if searchPtr.data == data:
                print("We found it")
                return 1
            if searchPtr.data < data:
                searchPtr = searchPtr.right
            else:
                searchPtr = searchPtr.left
        return -1

    def remove(self, curNode, target): 
        # needs to return the new root of the sub tree.

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
        elif curNode.data > target:
            curNode.left = self.remove(curNode.left, target)
        else:
            curNode.right = self.remove(curNode.right, target)

        # check if out of balance
        balance = getBalance(curNode)
        if balance < -1: # left heavy, we need to...
            if getBalance(curNode.left) == 1: # slight right bend
                # straighten the bend
                curNode.left = leftRotate(curNode.left)
            
            # rotate, set curNode to new subTree root
            curNode = rightRotate(curNode)
        elif balance > 1: # right heavy
            if getBalance(curNode.right) == -1: #slight bend
                # straighten the bend
                curNode.right = rightRotate(curNode.right)
            curNode = leftRotate(curNode)

        # update height
        calcHeight(curNode)
        # return new root (curNode) up the recursion chain
        return curNode


def main():
    newBST = BST()

    # Create the visualizer
    visualizer = TreeVisualizer() 

    newBST.head = newBST.add(newBST.head, 20)
    visualizer.add_to_stack(newBST)
    newBST.head = newBST.add(newBST.head, 10)
    visualizer.add_to_stack(newBST)
    newBST.head = newBST.add(newBST.head, 30)
    visualizer.add_to_stack(newBST)
    newBST.head = newBST.add(newBST.head, 5)
    visualizer.add_to_stack(newBST)
    newBST.head = newBST.add(newBST.head, 15)
    visualizer.add_to_stack(newBST)
    newBST.head = newBST.add(newBST.head, 40)
    visualizer.add_to_stack(newBST)
    newBST.head = newBST.add(newBST.head, 50)
    visualizer.add_to_stack(newBST)
    newBST.head = newBST.add(newBST.head, 2)
    visualizer.add_to_stack(newBST)
    newBST.head = newBST.add(newBST.head, 3)
    visualizer.add_to_stack(newBST)

    newBST.head = newBST.remove(newBST.head, 50)
    visualizer.add_to_stack(newBST)
    newBST.head = newBST.remove(newBST.head, 30)
    visualizer.add_to_stack(newBST)
    newBST.head = newBST.remove(newBST.head, 20)
    visualizer.add_to_stack(newBST)
    # Start the visualizer
    visualizer.visualize()

if __name__ == "__main__":
    main()