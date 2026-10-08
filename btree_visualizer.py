import turtle
import math
import copy


class DataItem:
    def __init__(self, key, value):
        self.key = key  # key is used to organize
        self.value = value  # value is the data associated with the key

    def __str__(self):
        return str(self.key)

    def __repr__(self):
        return str(self.key)


class Bucket:

    def __init__(self, maxdegree):
        self.keys = [] # A list of Keys that are used to organize the data
        self.links = [] # A list of links potential child nodes
        self.parent = None # A link to the parent node
        self.is_leaf = True # A boolean indicating if the node is a leaf node (and thus holds the data in the keys)
        self.next = None # A link to the next leaf node in the chain
        self.prev = None
        self.maxdegree = maxdegree

    def __str__(self):
        return str(self.keys)

    def __repr__(self):
        return str(self.keys)

    def add(self, item):
        pass

    def remove_key(self, key):
        pass

    
    # Important for the tree visualizer, do not touch.
    def get_data(self, key_index):
        """Get the data associated with a key at the given index"""
        if key_index < len(self.keys):
            key_data = self.keys[key_index]
            if isinstance(key_data, tuple) and len(key_data) >= 2:
                return str(key_data[1])  # Return the value part
            elif hasattr(key_data, 'value'):
                return str(key_data.value)  # Return the value attribute
            else:
                return f"{key_data}"  # Return formatted data if not a tuple
        return ""

class Tree:
    def __init__(self, maxdegree):
        self.root = None # reference to the root node
        self.maxdegree = maxdegree # the number of keys that will cause a split

    def add(self, key, value):
        pass

    def remove(self, key):
        pass

    def search(self, key):
        pass

    def split_leaf_node(self, node):
        pass

    def split_internal_node(self, node):
        pass
    
    # Important for the tree visualizer, do not touch
    def copy_tree(self):
        new_tree = Tree(self.maxdegree)
        new_tree.root = self._copy_node(self.root)
        # Create and store the leaf chain at snapshot time
        new_tree.leaf_chain = self._get_leaf_chain()
        return new_tree
    
    def _get_leaf_chain(self):
        """Get the leaf chain as a list of keys"""
        if self.root is None:
            return []
        
        # Find the leftmost leaf node
        current = self.root
        while current.links and current.links[0] is not None:
            current = current.links[0]
        
        # If we found a leaf node, traverse the chain
        if current.is_leaf:
            keys = []
            while current is not None:
                # Extract keys from current leaf node
                for key in current.keys:
                    if hasattr(key, 'key'):
                        keys.append(key.key)
                    else:
                        keys.append(key)
                current = current.next
            return keys
        return []
    
    # Important for the tree visualizer, do not touch
    def _copy_node(self, node):
        if node is None:
            return None
        
        new_node = Bucket(node.maxdegree)
        # Deep copy the keys (DataItem objects)
        new_node.keys = []
        for key in node.keys:
            if hasattr(key, 'key') and hasattr(key, 'value'):
                # Create a new DataItem object
                new_key = DataItem(key.key, key.value)
                new_node.keys.append(new_key)
            else:
                # For simple keys, just copy the value
                new_node.keys.append(key)
        
        new_node.links = [self._copy_node(link) for link in node.links]
        new_node.is_leaf = node.is_leaf  # Copy the is_leaf state
        new_node.next = node.next  # Copy the next property
        for link in new_node.links:
            if link is not None:
                link.parent = new_node
        return new_node

# Important for the tree visualizer, do not touch
class TreeVisualizer:
    def __init__(self, width=800, height=600):
        self.screen = turtle.Screen()
        self.screen.setup(width, height)
        self.screen.bgcolor("white")
        self.screen.title("B+ Tree Visualizer")
        
        # Optimize for instant drawing
        self.screen.tracer(0)  # Turn off animation completely
        
        self.turtle = turtle.Turtle()
        self.turtle.speed(0)  # Fastest drawing speed
        self.turtle.hideturtle()
        
        # Visual settings
        self.node_radius = 20
        self.level_height = 80
        self.min_width = 30
        
        # Offset variables that can be easily changed
        self.x_offset = 50  # Horizontal offset for tree positioning
        self.y_offset = 0  # Vertical offset for tree positioning
        
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
        
        # For leaf nodes or nodes with no children, return minimum width
        if not node.links or all(link is None for link in node.links):
            num_links = len(node.keys) + 1  # B+ trees have n+1 links for n keys
            return max(120, num_links * 40)  # Width based on number of links
        
        # Calculate width for each child subtree
        child_widths = []
        for link in node.links:
            if link is not None:
                child_widths.append(self.calculate_tree_width(link, level + 1))
            else:
                child_widths.append(0)
        
        # The total width is the sum of all child widths plus spacing
        num_links = len(node.keys) + 1  # B+ trees have n+1 links for n keys
        node_width = max(120, num_links * 40)
        total_width = sum(child_widths) + node_width
        
        return total_width
    
    def calculate_tree_height(self, node):
        """Calculate the height of the tree"""
        if node is None:
            return 0
        
        # For leaf nodes or nodes with no children
        if not node.links or all(link is None for link in node.links):
            return 1
        
        # Calculate height for each child and take the maximum
        child_heights = []
        for link in node.links:
            if link is not None:
                child_heights.append(self.calculate_tree_height(link))
        
        return 1 + max(child_heights) if child_heights else 1
    
    def draw_node(self, x, y, node, color="lightblue"):
        """Draw a B+ tree node with rectangular links and keys"""
        if node is None:
            return []
            
        # Calculate node width based on number of keys and links
        num_keys = len(node.keys)
        num_links = num_keys + 1  # B+ trees have n+1 links for n keys
        node_width = max(120, num_links * 40)  # Minimum width, expand for more links
        
        
        
        
        link_centers = []
        
        # Draw links and keys as rectangles
        if num_links > 0:
            # Calculate spacing for links and keys
            link_spacing = node_width / num_links
            start_x = x - node_width//2 + 10
            full_height = self.node_radius * 2  # Full height of the container
            
            
            current_x = start_x
            
            for i in range(num_links):
                
                link_width = link_spacing * 0.3  # Thin rectangles for links
                link_center_x = current_x + link_width // 2
                link_centers.append(link_center_x)
                
                
                self.turtle.penup()
                self.turtle.goto(current_x, y - self.node_radius)
                self.turtle.pendown()
                self.turtle.pencolor("black")
                self.turtle.pensize(1)
                self.turtle.fillcolor("white")
                self.turtle.begin_fill()
                for _ in range(2):
                    self.turtle.forward(link_width)
                    self.turtle.left(90)
                    self.turtle.forward(full_height)
                    self.turtle.left(90)
                self.turtle.end_fill()
                
                current_x += link_width
                
                # Draw key rectangle if we have a key for this position
                if i < num_keys:
                    key_width = link_spacing * 0.6  # Thick rectangles for keys
                    
                    # Draw key rectangle - full height
                    self.turtle.penup()
                    self.turtle.goto(current_x, y - self.node_radius)
                    self.turtle.pendown()
                    self.turtle.pencolor("black")
                    self.turtle.pensize(2)
                    self.turtle.fillcolor("lightyellow")
                    self.turtle.begin_fill()
                    for _ in range(2):
                        self.turtle.forward(key_width)
                        self.turtle.left(90)
                        self.turtle.forward(full_height)
                        self.turtle.left(90)
                    self.turtle.end_fill()
                    
                    # Draw key text
                    key_x = current_x + key_width // 2
                    self.turtle.penup()
                    self.turtle.goto(key_x, y - 5)
                    self.turtle.pendown()
                    self.turtle.pencolor("black")
                    self.turtle.pensize(1)
                    self.turtle.write(str(node.keys[i]), align="center", font=("Arial", 10, "bold"))
                    
                    # For leaf nodes, draw data squares below keys
                    if node.is_leaf and i < len(node.keys):
                        # Draw line from key to data square
                        data_y = y - self.node_radius - 50
                        self.turtle.penup()
                        self.turtle.goto(key_x, y - self.node_radius)
                        self.turtle.pendown()
                        self.turtle.pencolor("black")
                        self.turtle.pensize(1)
                        self.turtle.goto(key_x, data_y + 15)
                        
                        # Draw data square (taller rectangle)
                        data_square_width = 30
                        data_square_height = 30
                        self.turtle.penup()
                        self.turtle.goto(key_x - data_square_width//2, data_y)
                        self.turtle.pendown()
                        self.turtle.fillcolor("lightgreen")
                        self.turtle.begin_fill()
                        for _ in range(2):
                            self.turtle.forward(data_square_width)
                            self.turtle.left(90)
                            self.turtle.forward(data_square_height)
                            self.turtle.left(90)
                        self.turtle.end_fill()
                        
                        # Draw data text (smaller font to fit vertically)
                        self.turtle.penup()
                        self.turtle.goto(key_x, data_y + data_square_height//2)
                        self.turtle.pendown()
                        self.turtle.pencolor("black")
                        self.turtle.pensize(1)
                        # Get the data using the node's get_data method
                        data_value = node.get_data(i)
                        # If no data found, show the key with a prefix to indicate it's data
                        if not data_value or data_value == "":
                            data_value = f"{node.keys[i]}"
                        self.turtle.write(data_value, align="center", font=("Arial", 7, "normal"))
                    
                    current_x += key_width
        
        
        return link_centers
    
    
    def draw_leaf_chain(self, tree):
        """Display the stored leaf chain keys on the screen"""
        if tree is None or not hasattr(tree, 'leaf_chain'):
            return
        
        leaf_chain = tree.leaf_chain
        if leaf_chain:
            # Draw the chain at the bottom of the screen
            self.turtle.penup()
            self.turtle.goto(0, -self.screen.window_height() // 2 + 100)
            self.turtle.pendown()
            self.turtle.pencolor("darkblue")
            self.turtle.write("Leaf Chain:", align="center", font=("Arial", 12, "bold"))
            
            # Draw the keys
            self.turtle.penup()
            self.turtle.goto(0, -self.screen.window_height() // 2 + 80)
            self.turtle.pendown()
            self.turtle.pencolor("black")
            self.turtle.write(f"Keys: {leaf_chain}", align="center", font=("Arial", 10, "normal"))
            
            # Reset pen color
            self.turtle.pencolor("black")
    
    def _calculate_node_width(self, node):
        """Calculate the width of a node based on its keys and links"""
        if node is None:
            return 0
        num_keys = len(node.keys)
        num_links = num_keys + 1  # B+ trees have n+1 links for n keys
        return max(120, num_links * 40)
    
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
        
        # Calculate node width based on links
        num_keys = len(node.keys)
        num_links = num_keys + 1  # B+ trees have n+1 links for n keys
        node_width = max(120, num_links * 40)
        
        # If no children, return bounds of current node
        if not node.links or all(link is None for link in node.links):
            return x - node_width//2, x + node_width//2
        
        # Calculate widths for all child subtrees
        child_widths = []
        for link in node.links:
            if link is not None:
                child_widths.append(self.calculate_tree_width(link))
            else:
                child_widths.append(0)
        
        # Calculate positions for children
        total_child_width = sum(child_widths)
        start_x = x - total_child_width // 2
        
        # Get bounds from all children
        child_bounds = []
        current_x = start_x
        for i, link in enumerate(node.links):
            if link is not None:
                child_x = current_x + child_widths[i] // 2
                child_min, child_max = self.get_tree_bounds(link, child_x, level + 1)
                child_bounds.append((child_min, child_max))
                current_x += child_widths[i]
            else:
                current_x += child_widths[i]
        
        # Return overall bounds
        min_x = min([bounds[0] for bounds in child_bounds] + [x - node_width//2])
        max_x = max([bounds[1] for bounds in child_bounds] + [x + node_width//2])
        
        return min_x, max_x
    
    def draw_tree_recursive(self, node, x, y, level=0):
        """Recursively draw the B+ tree"""
        if node is None:
            return
        
        x = x + self.x_offset
        y = y + self.y_offset
        
        # Draw current node and get link center coordinates
        link_centers = self.draw_node(x, y, node)
        
        # If no children, we're done
        if not node.links or all(link is None for link in node.links):
            return
        
        # Calculate positions for children
        child_y = y - self.level_height
        
        # Calculate widths for valid child subtrees only
        valid_child_widths = []
        valid_link_indices = []
        for i, link in enumerate(node.links):
            if link is not None:
                valid_child_widths.append(self.calculate_tree_width(link))
                valid_link_indices.append(i)
        
        # Calculate total width and starting position for valid children only
        total_child_width = sum(valid_child_widths)
        # Slight left adjustment to align with parent links
        start_x = x - total_child_width // 2 - (total_child_width * 0.035)
        
        # Draw lines to children and recursively draw subtrees
        current_x = start_x
        valid_index = 0
        for i, link in enumerate(node.links):
            if link is not None:
                # Center the child node properly
                child_x = current_x + valid_child_widths[valid_index] // 2
                
                # Use the stored link center coordinates
                if i < len(link_centers):
                    link_origin_x = link_centers[i]
                else:
                    # Fallback calculation if link_centers is empty
                    link_spacing = self._calculate_node_width(node) / (len(node.keys) + 1)
                    start_x_node = x - self._calculate_node_width(node) // 2
                    link_origin_x = start_x_node + link_spacing * (i + 0.5)
                
                # Draw line from specific link rectangle to child
                self.draw_line(link_origin_x, y - self.node_radius, child_x, child_y + self.node_radius)
                
                # Recursively draw child
                self.draw_tree_recursive(link, child_x, child_y, level + 1)
                
                current_x += valid_child_widths[valid_index]
                valid_index += 1
    
    def validate_tree(self, tree):
        """Validate B+ tree structure and detect common issues"""
        if tree is None:
            return False, "Tree is None"
        
        if tree.root is None:
            return True, "Empty tree (valid)"
        
        # Check for circular references
        visited = set()
        if self._has_circular_reference(tree.root, visited):
            return False, "Circular reference detected in tree"
        
        # Check for excessive depth
        depth = self.calculate_tree_height(tree.root)
        if depth > 15:
            return False, f"Tree too deep ({depth} levels), may cause performance issues"
        
        return True, "Tree structure is valid"
    
    def _has_circular_reference(self, node, visited):
        """Check for circular references in the B+ tree"""
        if node is None:
            return False
        
        if id(node) in visited:
            return True
        
        visited.add(id(node))
        
        # Check all child links for circular references
        for link in node.links:
            if link is not None:
                if self._has_circular_reference(link, visited.copy()):
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
        
        if tree.root is None:
            print("Tree is empty - showing empty page")
            # Don't return, continue to show empty page
        
        self.turtle.clear()
        
        # Use maximum dimensions for consistent window sizing
        if self.max_width > 0 and self.max_height > 0:
            # Use the largest dimensions found across all trees
            required_width = max(800, self.max_width + 50)
            required_height = max(600, self.max_height * self.level_height + 200 + self.status_bar_height)
            print(f"Using maximum dimensions: {self.max_width}x{self.max_height}")
        else:
            # Fallback to current tree dimensions if no max dimensions set
            tree_height = self.calculate_tree_height(tree.root)
            min_x, max_x = self.get_tree_bounds(tree.root, 0)
            actual_width = max_x - min_x
            required_width = max(800, actual_width + 50)
            required_height = max(600, tree_height * self.level_height + 200 + self.status_bar_height)
            print(f"Using current tree dimensions: {actual_width}x{tree_height}")
        
        # print(f"Window size: {required_width}x{required_height}")
        
        self.screen.setup(required_width, required_height)
        
        # Simple centering: start at the center of the window (accounting for status bar)
        start_x = 200  # Start at center
        start_y = (required_height - self.status_bar_height) // 2 - 100
        
        # print(f"Starting position: x={start_x}, y={start_y}")
        
        # Draw the tree or empty message
        if tree.root is not None:
            self.draw_tree_recursive(tree.root, start_x, start_y)
            # Draw leaf node chain on screen
            self.draw_leaf_chain(tree)
        else:
            # Draw empty tree message
            self.turtle.penup()
            self.turtle.goto(0, start_y)
            self.turtle.pendown()
            self.turtle.write("Empty B+ Tree", align="center", font=("Arial", 16, "bold"))
            
            # Draw a simple empty tree representation
            self.turtle.penup()
            self.turtle.goto(0, start_y - 50)
            self.turtle.pendown()
            self.turtle.write("No nodes to display", align="center", font=("Arial", 12, "normal"))
        
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
        if tree.root is not None:
            tree_width = self.calculate_tree_width(tree.root)
            tree_height = self.calculate_tree_height(tree.root)
            
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
    
    def next_tree(self):
        """Navigate to the next tree in the stack"""
        if self.current_index < len(self.tree_stack) - 1:
            self.current_index += 1
            self.redraw_current_tree()
    
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
            if current_tree.root is not None:
                self.draw_tree_recursive(current_tree.root, 0, tree_y)
                # Draw leaf node chain on screen
                self.draw_leaf_chain(current_tree)
            else:
                # Draw empty tree message
                self.turtle.penup()
                self.turtle.goto(0, tree_y)
                self.turtle.pendown()
                self.turtle.write("Empty B+ Tree", align="center", font=("Arial", 16, "bold"))
                
                # Draw a simple empty tree representation
                self.turtle.penup()
                self.turtle.goto(0, tree_y - 50)
                self.turtle.pendown()
                self.turtle.write("No nodes to display", align="center", font=("Arial", 12, "normal"))
            
            # Draw status bar
            self.draw_status_bar(window_width, window_height)
            
            self.screen.update()


# Example usage
if __name__ == "__main__":
    # Create a B+ tree
    tree = Tree()
    
    # Create visualizer
    visualizer = TreeVisualizer()
    
    # Add empty tree to stack (will show empty page)
    visualizer.add_to_stack(tree)
    
    # Visualize the tree
    print("B+ Tree Visualizer")
    print("Use Left/Right arrow keys to navigate, 's' for info, Escape to close")
    print("This example shows an empty B+ tree")
    visualizer.visualize()

