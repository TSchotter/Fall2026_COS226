import turtle
import math
import copy

class Node:

    def __init__(self, value):
        self.data = value
        self.left = None
        self.right = None
        self.height = 1

    def __str__(self):
        return str(self.data)

    def __repr__(self):
        return str(self.data)

class BinaryTree:
    def __init__(self):
        self.head = None

    def add(self, data):
        pass

    def remove(self, data):
        pass

    def search(self, data):
        pass
    
    def copy_tree(self):
        new_tree = BinaryTree()
        new_tree.head = self._copy_node(self.head)
        return new_tree
    
    def _copy_node(self, node):
        if node is None:
            return None
        
        new_node = Node(node.data)
        new_node.left = self._copy_node(node.left)
        new_node.right = self._copy_node(node.right)
        return new_node

class TreeVisualizer:
    def __init__(self, width=800, height=600):
        self.screen = turtle.Screen()
        self.screen.setup(width, height)
        self.screen.bgcolor("white")
        self.screen.title("Binary Tree Visualizer")
        
        # Optimize for instant drawing
        self.screen.tracer(0)  # Turn off animation completely
        
        self.turtle = turtle.Turtle()
        self.turtle.speed(0)  # Fastest drawing speed
        self.turtle.hideturtle()
        
        # Visual settings
        self.node_radius = 20
        self.level_height = 80
        self.min_width = 30
        
        # Stack management
        self.tree_stack = []
        self.current_index = -1
        
        # Track maximum dimensions across all trees
        self.max_width = 0
        self.max_height = 0
        
        # Status bar settings
        self.status_bar_height = 40
        
    def calculate_tree_width(self, node, level=0):
        """Calculate the total width needed for the tree"""
        if node is None:
            return 0
        
        # For leaf nodes, return minimum width
        if node.left is None and node.right is None:
            return self.min_width
        
        left_width = self.calculate_tree_width(node.left, level + 1)
        right_width = self.calculate_tree_width(node.right, level + 1)
        
        # The total width is the sum of left and right widths plus spacing
        total_width = left_width + right_width + self.min_width
        
        return total_width
    
    def calculate_tree_height(self, node):
        """Calculate the height of the tree"""
        if node is None:
            return 0
        return 1 + max(self.calculate_tree_height(node.left), self.calculate_tree_height(node.right))
    
    def draw_node(self, x, y, value, color="lightblue"):
        """Draw a single node with its value"""
        # Optimize drawing by reducing pen movements
        self.turtle.penup()
        self.turtle.goto(x, y - self.node_radius)
        self.turtle.pendown()
        
        # Draw circle
        self.turtle.fillcolor(color)
        self.turtle.begin_fill()
        self.turtle.circle(self.node_radius)
        self.turtle.end_fill()
        
        # Draw value text
        self.turtle.penup()
        self.turtle.goto(x, y - 5)
        self.turtle.pendown()
        self.turtle.write(str(value), align="center", font=("Arial", 12, "bold"))
    
    def draw_line(self, x1, y1, x2, y2):
        """Draw a line between two points"""
        self.turtle.penup()
        self.turtle.goto(x1, y1)
        self.turtle.pendown()
        self.turtle.goto(x2, y2)
    
    def get_tree_bounds(self, node, x=0, level=0):
        """Calculate the actual horizontal bounds of the tree"""
        if node is None:
            return x, x
        
        # Calculate widths for left and right subtrees
        left_width = self.calculate_tree_width(node.left) if node.left else 0
        right_width = self.calculate_tree_width(node.right) if node.right else 0
        
        # Calculate child positions
        left_x = x - (right_width + self.min_width) / 2 if node.left else x
        right_x = x + (left_width + self.min_width) / 2 if node.right else x
        
        # Get bounds from subtrees
        left_min, left_max = self.get_tree_bounds(node.left, left_x, level + 1) if node.left else (x, x)
        right_min, right_max = self.get_tree_bounds(node.right, right_x, level + 1) if node.right else (x, x)
        
        # Return overall bounds
        min_x = min(left_min, right_min, x - self.node_radius)
        max_x = max(left_max, right_max, x + self.node_radius)
        
        return min_x, max_x
    
    def draw_tree_recursive(self, node, x, y, level=0):
        """Recursively draw the tree"""
        if node is None:
            return
        
        # Draw current node
        self.draw_node(x, y, node.data)
        
        # Calculate positions for children
        child_y = y - self.level_height
        
        # Calculate widths for left and right subtrees
        left_width = self.calculate_tree_width(node.left) if node.left else 0
        right_width = self.calculate_tree_width(node.right) if node.right else 0
        
        # Position children based on their actual widths
        if node.left is not None:
            left_x = x - (right_width + self.min_width) / 2
            self.draw_line(x, y - self.node_radius, left_x, child_y + self.node_radius)
            self.draw_tree_recursive(node.left, left_x, child_y, level + 1)
        
        if node.right is not None:
            right_x = x + (left_width + self.min_width) / 2
            self.draw_line(x, y - self.node_radius, right_x, child_y + self.node_radius)
            self.draw_tree_recursive(node.right, right_x, child_y, level + 1)
    
    def validate_tree(self, tree):
        """Validate tree structure and detect common issues"""
        if tree is None:
            return False, "Tree is None"
        
        if tree.head is None:
            return True, "Empty tree (valid)"
        
        # Check for circular references
        visited = set()
        if self._has_circular_reference(tree.head, visited):
            return False, "Circular reference detected in tree"
        
        # Check for excessive depth
        depth = self.calculate_tree_height(tree.head)
        if depth > 15:
            return False, f"Tree too deep ({depth} levels), may cause performance issues"
        
        return True, "Tree structure is valid"
    
    def _has_circular_reference(self, node, visited):
        """Check for circular references in the tree"""
        if node is None:
            return False
        
        if id(node) in visited:
            return True
        
        visited.add(id(node))
        
        if self._has_circular_reference(node.left, visited.copy()):
            return True
        if self._has_circular_reference(node.right, visited.copy()):
            return True
        
        return False
    
    def draw_status_bar(self, window_width, window_height):
        """Draw status bar at the bottom of the window"""
        # Calculate status bar position
        status_y = -window_height // 2 + self.status_bar_height // 2
        
        # Draw status bar background
        self.turtle.penup()
        self.turtle.goto(-window_width // 2, status_y - self.status_bar_height // 2)
        self.turtle.pendown()
        self.turtle.fillcolor("lightgray")
        self.turtle.begin_fill()
        self.turtle.goto(window_width // 2, status_y - self.status_bar_height // 2)
        self.turtle.goto(window_width // 2, status_y + self.status_bar_height // 2)
        self.turtle.goto(-window_width // 2, status_y + self.status_bar_height // 2)
        self.turtle.goto(-window_width // 2, status_y - self.status_bar_height // 2)
        self.turtle.end_fill()
        
        # Draw status text
        if self.tree_stack:
            current_state = self.current_index + 1
            total_states = len(self.tree_stack)
            status_text = f"State {current_state}/{total_states} | Left/Right: Navigate | 's': Info | Esc: Close"
        else:
            status_text = "No trees in stack | Add trees with add_to_stack() | Esc: Close"
        
        # Position text in status bar
        self.turtle.penup()
        self.turtle.goto(0, status_y - 5)
        self.turtle.pendown()
        self.turtle.write(status_text, align="center", font=("Arial", 10, "normal"))

    def visualize(self):
        """Main method to visualize the first tree from the stack"""
        if not self.tree_stack:
            print("No trees in stack! Add trees first using add_to_stack()")
            return
        
        # Show the first tree in the stack
        self.current_index = 0
        tree = self.tree_stack[self.current_index]
        
        # Validate tree structure
        is_valid, message = self.validate_tree(tree)
        print(f"Tree validation: {message}")
        
        if not is_valid:
            print("Warning: Tree has structural issues!")
            if "circular" in message.lower():
                print("Cannot visualize tree with circular references")
                return
            elif "too deep" in message.lower():
                print("Proceeding with deep tree (may be slow)...")
        
        if tree.head is None:
            print("Tree is empty!")
            return
        
        self.turtle.clear()
        
        # Use maximum dimensions for consistent window sizing
        if self.max_width > 0 and self.max_height > 0:
            # Use the largest dimensions found across all trees
            required_width = max(800, self.max_width + 200)
            required_height = max(600, self.max_height * self.level_height + 200 + self.status_bar_height)
            print(f"Using maximum dimensions: {self.max_width}x{self.max_height}")
        else:
            # Fallback to current tree dimensions if no max dimensions set
            tree_height = self.calculate_tree_height(tree.head)
            min_x, max_x = self.get_tree_bounds(tree.head, 0)
            actual_width = max_x - min_x
            required_width = max(800, actual_width + 200)
            required_height = max(600, tree_height * self.level_height + 200 + self.status_bar_height)
            print(f"Using current tree dimensions: {actual_width}x{tree_height}")
        
        # print(f"Window size: {required_width}x{required_height}")
        
        self.screen.setup(required_width, required_height)
        
        # Simple centering: start at the center of the window (accounting for status bar)
        start_x = 0  # Start at center
        start_y = (required_height - self.status_bar_height) // 2 - 100
        
        # print(f"Starting position: x={start_x}, y={start_y}")
        
        # Draw the tree
        self.draw_tree_recursive(tree.head, start_x, start_y)
        
        # Draw status bar
        self.draw_status_bar(required_width, required_height)
        
        # Update the screen instantly after drawing
        self.screen.update()
        
        # Set up keyboard controls
        self.screen.listen()
        self.screen.onkey(self.previous_tree, "Left")
        self.screen.onkey(self.next_tree, "Right")
        self.screen.onkey(self.show_stack_info, "s")
        self.screen.onkey(self.close_visualizer, "Escape")
        
        # Keep window open until Escape is pressed
        self.screen.mainloop()
    
    def close_visualizer(self):
        """Close the visualizer window"""
        self.screen.bye()
    
    def add_to_stack(self, tree):
        """Add a copy of the current tree to the stack"""
        tree_copy = tree.copy_tree()
        self.tree_stack.append(tree_copy)
        self.current_index = len(self.tree_stack) - 1
        
        # Calculate and update maximum dimensions
        if tree.head is not None:
            tree_width = self.calculate_tree_width(tree.head)
            tree_height = self.calculate_tree_height(tree.head)
            
            # Update maximum dimensions
            self.max_width = max(self.max_width, tree_width)
            self.max_height = max(self.max_height, tree_height)
            
            print(f"Tree state {len(self.tree_stack)} added to stack (dimensions: {tree_width}x{tree_height})")
        else:
            print(f"Tree state {len(self.tree_stack)} added to stack (empty tree)")
    
    def previous_tree(self):
        """Navigate to the previous tree in the stack"""
        if self.current_index > 0:
            self.current_index -= 1
            self.redraw_current_tree()
            print(f"Showing tree state {self.current_index + 1}")
    
    def next_tree(self):
        """Navigate to the next tree in the stack"""
        if self.current_index < len(self.tree_stack) - 1:
            self.current_index += 1
            self.redraw_current_tree()
            print(f"Showing tree state {self.current_index + 1}")
    
    def show_stack_info(self):
        """Display information about the current stack"""
        if self.tree_stack:
            print(f"Stack has {len(self.tree_stack)} states, currently viewing state {self.current_index + 1}")
            print(f"Maximum dimensions: {self.max_width}x{self.max_height}")
            print("Use Left/Right arrow keys to navigate, 's' to show this info, Escape to close")
        else:
            print("Stack is empty")
    
    def redraw_current_tree(self):
        """Redraw the current tree from the stack"""
        if 0 <= self.current_index < len(self.tree_stack):
            current_tree = self.tree_stack[self.current_index]
            # Clear and redraw instantly
            self.turtle.clear()
            
            # Calculate window dimensions for status bar
            window_width = self.screen.window_width()
            window_height = self.screen.window_height()
            
            # Draw tree (accounting for status bar)
            tree_y = (window_height - self.status_bar_height) // 2 - 100
            self.draw_tree_recursive(current_tree.head, 0, tree_y)
            
            # Draw status bar
            self.draw_status_bar(window_width, window_height)
            
            self.screen.update()

