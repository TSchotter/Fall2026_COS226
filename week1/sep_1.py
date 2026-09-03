class Node:
    def __init__(self, num): # constructor
        self.num = num # set num to internal value
    def get(self):
        return self.num
    def setNum(self, num):
        self.num = num

x = Node(5)
x.setNum(10)
print(x.get())