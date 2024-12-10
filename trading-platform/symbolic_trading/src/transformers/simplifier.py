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
        # Placeholder for combining like terms
        return node, False

    def simplify_nested_operations(self, node):
        # Recursively simplify child nodes
        if isinstance(node, OperatorNode):
            node.left, _ = self.simplify_nested_operations(node.left)
            node.right, _ = self.simplify_nested_operations(node.right)
        return node, False
