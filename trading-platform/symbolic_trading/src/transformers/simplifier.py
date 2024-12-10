from src.utils.expression_tree import OperatorNode, ConstantNode, VariableNode

class Simplifier:
    def __init__(self):
        self.rules = [
            self.simplify_add_zero,
            self.simplify_multiply_zero,
            self.simplify_multiply_one,
            self.simplify_power_zero,
            self.simplify_power_one,
            self.combine_like_terms,
            self.simplify_nested_operations
        ]

    def simplify(self, node):
        changed = True
        while changed:
            changed = False
            for rule in self.rules:
                node, rule_applied = rule(node)
                if rule_applied:
                    changed = True
        return node

    def simplify_add_zero(self, node):
        if isinstance(node, OperatorNode) and node.operator == '+':
            if isinstance(node.left, ConstantNode) and node.left.value == 0:
                return node.right, True
            if isinstance(node.right, ConstantNode) and node.right.value == 0:
                return node.left, True
        return node, False

    def simplify_multiply_zero(self, node):
        if isinstance(node, OperatorNode) and node.operator == '*':
            if (isinstance(node.left, ConstantNode) and node.left.value == 0) or \
               (isinstance(node.right, ConstantNode) and node.right.value == 0):
                return ConstantNode(0), True
        return node, False

    def simplify_multiply_one(self, node):
        if isinstance(node, OperatorNode) and node.operator == '*':
            if isinstance(node.left, ConstantNode) and node.left.value == 1:
                return node.right, True
            if isinstance(node.right, ConstantNode) and node.right.value == 1:
                return node.left, True
        return node, False

    def simplify_power_zero(self, node):
        if isinstance(node, OperatorNode) and node.operator == '^':
            if isinstance(node.right, ConstantNode) and node.right.value == 0:
                return ConstantNode(1), True
        return node, False

    def simplify_power_one(self, node):
        if isinstance(node, OperatorNode) and node.operator == '^':
            if isinstance(node.right, ConstantNode) and node.right.value == 1:
                return node.left, True
        return node, False

    def combine_like_terms(self, node):
        """Combine like terms in an expression."""
        if not isinstance(node, OperatorNode):
            return node, False
            
        # First simplify children
        node.left, left_changed = self.combine_like_terms(node.left)
        node.right, right_changed = self.combine_like_terms(node.right)
        
        if node.operator == '*' and isinstance(node.right, OperatorNode) and node.right.operator == '+':
            # Distribute: a * (b + c) -> (a * b) + (a * c)
            new_left = OperatorNode('*', node.left, node.right.left)
            new_right = OperatorNode('*', node.left, node.right.right)
            return OperatorNode('+', new_left, new_right), True
            
        return node, (left_changed or right_changed)

    def simplify_nested_operations(self, node):
        # Recursively simplify child nodes
        if isinstance(node, OperatorNode):
            node.left, _ = self.simplify_nested_operations(node.left)
            node.right, _ = self.simplify_nested_operations(node.right)
        return node, False

    def format_constant(self, value):
        """Format constant values consistently."""
        if value == int(value):
            return str(int(value))
        return str(value)
