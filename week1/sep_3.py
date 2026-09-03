# Goals for today:
# - Import from other files
# - Inheritance
# - Overwrite default methods
# - Tracking time

# import node
# from [name of file] import [thing you want]
from node import Node
from datetime import datetime
import time

# create a AnimalNode, it has the aspects of a node,
# and also holds the name (a string)
class AnimalNode(Node):

    '''
    def __init__(self, key, name):
        self.number = key
        self.name = name
    '''
    def __init__(self, key, name):
        # call inherited class __init__
        # don't need "self", because the obj automatically sends it
        super().__init__(key) 
        self.name = name
    def __str__(self):
        return f"[{self.number}: {self.name}]"

class LinkedNode(Node):
    def __init__(self, num):
        super().__init__(num)
        self.next = None # This is the "Null"

# keep track of the head of the linked list
head = LinkedNode(5)
cur = head
cur.next = LinkedNode(6)
cur = cur.next
cur.next = LinkedNode(10)
cur = None
cur = head
while (cur != None):
    # print self, go to next
    print(cur)
    cur = cur.next


# create an animal Node
y = AnimalNode(9, "Cat")
print(y) # What I want: [Cat: 9]
# Create a node object
x = Node(5)
print(x.number)
print(x)

numList = []
# don't need to create a variable to hold Node,
#  can immediately add it to a list.
numList.append(Node(8))

start_time = datetime.now()
print(start_time)
time.sleep(5) # do something that takes time
end_time = datetime.now()
print(f"Time taken: {end_time - start_time}")

# open file (to read)
# in a loop:
#      read a line
#       split line on ","
#       Create an animal Node with those two things.
#       Add that node to a list.