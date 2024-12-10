from src.utils.expression_tree import OperatorNode, ConstantNode, VariableNode
import math

class Integrator:
    def __init__(self, variable):
        self.variable = variable

    def integrate(self, node):
        if isinstance(node, ConstantNode):
            # ∫ c dx = cx
            return OperatorNode('*', node, VariableNode(self.variable))
        elif isinstance(node, VariableNode):
            if node.name == self.variable:
                # ∫ x dx = x^2/2
                return OperatorNode('/', 
                    OperatorNode('^', node, ConstantNode(2)), 
                    ConstantNode(2))
            else:
                # ∫ c dx = cx where c is another variable
                return OperatorNode('*', node, VariableNode(self.variable))
        elif isinstance(node, OperatorNode):
            if node.operator == '+':
                # ∫ (f + g) dx = ∫f dx + ∫g dx
                return OperatorNode('+', 
                    self.integrate(node.left), 
                    self.integrate(node.right))
            elif node.operator == '-':
                # ∫ (f - g) dx = ∫f dx - ∫g dx
                return OperatorNode('-', 
                    self.integrate(node.left), 
                    self.integrate(node.right))
            elif node.operator == '*':
                if isinstance(node.left, ConstantNode):
                    # ∫ c*f dx = c*∫f dx
                    return OperatorNode('*', 
                        node.left, 
                        self.integrate(node.right))
                elif isinstance(node.right, ConstantNode):
                    # ∫ f*c dx = c*∫f dx
                    return OperatorNode('*', 
                        node.right, 
                        self.integrate(node.left))
                else:
                    # Integration by parts needed
                    raise NotImplementedError("Integration by parts not implemented")
            elif node.operator == '/':
                if isinstance(node.right, ConstantNode):
                    # ∫ (f/c) dx = (1/c)*∫f dx
                    return OperatorNode('/', 
                        self.integrate(node.left), 
                        node.right)
                else:
                    # Complex rational function integration
                    raise NotImplementedError("Integration of rational functions not implemented")
            elif node.operator == '^':
                if isinstance(node.left, VariableNode) and node.left.name == self.variable and isinstance(node.right, ConstantNode):
                    # ∫ x^n dx = x^(n+1)/(n+1)
                    new_power = ConstantNode(node.right.value + 1)
                    numerator = OperatorNode('^', node.left, new_power)
                    return OperatorNode('/', numerator, new_power)
                else:
                    # Other cases of power integration
                    raise NotImplementedError("Integration of general powers not implemented")
            else:
                raise ValueError(f"Unknown operator: {node.operator}")
        else:
            raise TypeError("Unsupported node type for integration")

    def integrate_with_bounds(self, node, lower_bound, upper_bound):
        """
        Definite integration between bounds.
        Not fully implemented - would need evaluation capabilities.
        """
        indefinite_integral = self.integrate(node)
        # Would need to evaluate indefinite_integral at bounds
        # and return upper_eval - lower_eval
        raise NotImplementedError("Definite integration not implemented")