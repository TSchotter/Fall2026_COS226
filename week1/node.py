class Node:
    def __init__(self, number):
        self.number = number
    # when we treat the obj as a string, call this
    def __str__(self):
        # make sure it returns a str
        return str(self.number)

    