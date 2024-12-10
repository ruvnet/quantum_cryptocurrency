from src.utils.expression_tree import OperatorNode, ConstantNode, VariableNode

class Simplifier:
    def __init__(self):
        self.rules = [
            self.simplify_add_zero,
            self.simplify_multiply_zero,
            self.simplify_multiply_one,
            self.simplify_power_zero,
            self.simplify_power_one,
            self.simplify_nested_powers,
            self.combine_like_terms,
            self.simplify_nested_operations
        ]

    def simplify(self, node):
        # First check if this is a trigonometric or exponential expression
        if isinstance(node, OperatorNode):
            if node.operator in ['sin', 'cos', 'tan']:
                raise NotImplementedError("Trigonometric pattern matching not implemented")
            elif node.operator == 'exp' or (node.operator == '^' and str(node.left) == 'e'):
                raise NotImplementedError("Exponential pattern matching not implemented")
            
            # Handle commutativity for + and *
            if node.operator in ['+', '*'] and isinstance(node.left, VariableNode) and isinstance(node.right, VariableNode):
                # Sort variables alphabetically for consistent ordering
                if node.right.name < node.left.name:
                    node = OperatorNode(node.operator, node.right, node.left)
            
            # Recursively check children for trig/exp functions first
            if node.left:
                self.simplify(node.left)
            if node.right:
                self.simplify(node.right)
            
            if node.operator in ['log', 'exp']:
                raise NotImplementedError("Transcendental function simplification not implemented")
                
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
            # First check if either operand is a ConstantNode with value 0
            left_is_zero = isinstance(node.left, ConstantNode) and node.left.value == 0
            right_is_zero = isinstance(node.right, ConstantNode) and node.right.value == 0
            
            if left_is_zero or right_is_zero:
                # Always return integer 0 for multiplication by zero
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
            if isinstance(node.left, ConstantNode) and node.left.value == 0:
                return ConstantNode(0), True
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

    def simplify_nested_powers(self, node):
        """Simplify nested power expressions like (x^n)^m -> x^(n*m)"""
        if isinstance(node, OperatorNode) and node.operator == '^':
            if isinstance(node.left, OperatorNode) and node.left.operator == '^':
                # Case: (x^n)^m -> x^(n*m)
                base = node.left.left
                inner_exp = node.left.right
                outer_exp = node.right
                # Create n*m as a parenthesized expression
                new_exp = OperatorNode('*', inner_exp, outer_exp)
                # Ensure the multiplication is properly parenthesized in the final expression
                result = OperatorNode('^', base, new_exp)
                # Force parentheses around the exponent by making it a separate node
                return result, True
        return node, False

    def simplify_nested_operations(self, node):
        # Recursively simplify child nodes
        if isinstance(node, OperatorNode):
            node.left, _ = self.simplify_nested_operations(node.left)
            node.right, _ = self.simplify_nested_operations(node.right)
        return node, False

    def format_constant(self, value):
        """Format constant values consistently."""
        if isinstance(value, (int, float)):
            if value.is_integer():
                return str(int(value))  # Return integer format for whole numbers
            return str(float(value))
        return str(value)
