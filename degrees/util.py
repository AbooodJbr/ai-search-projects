class Node:
    """Search tree node used by frontier implementations."""

    def __init__(self, state, parent, action):
        """Create a new node.

        Summary:
            Holds a search state plus a pointer to its parent and the action
            taken from the parent to reach this state.
        Params:
            state: Hashable identifier for the search state.
            parent: Optional parent Node that led to this node.
            action: Optional action label describing the move from parent.
        Outputs:
            None; fields are stored on the instance for frontier usage.
        """
        self.state = state
        self.parent = parent
        self.action = action


class StackFrontier:
    """LIFO frontier for depth-first search strategies."""

    def __init__(self):
        """Initialize an empty frontier."""
        self.frontier = []

    def add(self, node):
        """Push a node onto the frontier."""
        self.frontier.append(node)

    def contains_state(self, state):
        """Return True if a node with the given state is already present."""
        return any(node.state == state for node in self.frontier)

    def empty(self):
        """Return True when no nodes remain in the frontier."""
        return len(self.frontier) == 0

    def remove(self):
        """Pop and return the most recently added node."""
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier[-1]
            self.frontier = self.frontier[:-1]
            return node


class QueueFrontier(StackFrontier):

    def remove(self):
        """Dequeue and return the oldest node for BFS strategies."""
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier[0]
            self.frontier = self.frontier[1:]
            return node
