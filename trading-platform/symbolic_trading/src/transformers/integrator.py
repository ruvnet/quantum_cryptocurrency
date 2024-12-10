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
                elif isinstance(node.left, VariableNode) and node.left.name == self.variable:
                    # Special case for x*f(x)
                    # Use u-substitution with u = f(x)
                    return self._integrate_variable_product(node)
                else:
                    # For other cases, try u-substitution
                    return self._integrate_by_substitution(node)
            elif node.operator == '/':
                if isinstance(node.right, ConstantNode):
                    # ∫ (f/c) dx = (1/c)*∫f dx
                    return OperatorNode('*',
                        OperatorNode('/', ConstantNode(1), node.right),
                        self.integrate(node.left))
                else:
                    # For non-constant denominators, try standard integration
                    return self.integrate(
                        OperatorNode('*', node.left, 
                            OperatorNode('^', node.right, ConstantNode(-1)))
                    )
            elif node.operator == '^':
                if isinstance(node.left, VariableNode) and node.left.name == self.variable:
                    # Handle x^n where n is any expression
                    if isinstance(node.right, ConstantNode):
                        # Standard power rule: ∫ x^n dx = x^(n+1)/(n+1)
                        new_power = ConstantNode(node.right.value + 1)
                        numerator = OperatorNode('^', node.left, new_power)
                        return OperatorNode('/', numerator, new_power)
                    else:
                        # For variable exponent, use the same rule but with expressions
                        new_power = OperatorNode('+', node.right, ConstantNode(1))
                        numerator = OperatorNode('^', node.left, new_power)
                        return OperatorNode('/', numerator, new_power)
                else:
                    # For other cases, try standard integration
                    return self.integrate(
                        OperatorNode('*', node.left,
                            OperatorNode('^', node.right, ConstantNode(-1)))
                    )
            else:
                raise ValueError(f"Unknown operator: {node.operator}")
        else:
            raise TypeError("Unsupported node type for integration")

    def _integrate_variable_product(self, node):
        """Handle integration of x*f(x) type expressions"""
        if node.left.name == self.variable:
            f = node.right
        else:
            f = node.left
            
        # For x*f(x), use u = f(x)
        # Then du = f'(x)dx
        from src.transformers.differentiator import Differentiator
        differentiator = Differentiator(self.variable)
        du = differentiator.differentiate(f)
        
        # Result is (1/2)*f(x)^2
        return OperatorNode('/', 
            OperatorNode('^', f, ConstantNode(2)),
            ConstantNode(2))

    def _integrate_by_substitution(self, node):
        """Use u-substitution for integration"""
        # Choose the more complex part as u
        if isinstance(node.left, OperatorNode):
            u = node.left
            dv = node.right
        else:
            u = node.right
            dv = node.left
            
        # Get du/dx
        from src.transformers.differentiator import Differentiator
        differentiator = Differentiator(self.variable)
        du = differentiator.differentiate(u)
        
        # Get v by integrating dv
        v = self.integrate(dv)
        
        # Result is u*v - ∫v*du
        return OperatorNode('-',
            OperatorNode('*', u, v),
            self.integrate(OperatorNode('*', v, du)))

    def integrate_with_bounds(self, node, lower_bound, upper_bound):
        """
        Definite integration between bounds.
        Not fully implemented - would need evaluation capabilities.
        """
        indefinite_integral = self.integrate(node)
        # Would need to evaluate indefinite_integral at bounds
        # and return upper_eval - lower_eval
        raise NotImplementedError("Definite integration not implemented")
