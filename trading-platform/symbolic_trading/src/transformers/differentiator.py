from src.utils.expression_tree import ConstantNode, VariableNode, OperatorNode

class Differentiator:
    def __init__(self, variable):
        """
        Initialize differentiator with respect to a variable.
        
        Args:
            variable (str): The variable to differentiate with respect to
        """
        self.variable = variable

    def differentiate(self, ast):
        """
        Differentiate an AST with respect to the variable.
        
        Args:
            ast: The abstract syntax tree to differentiate
            
        Returns:
            The differentiated AST
        """
        # Handle constant nodes
        if isinstance(ast, ConstantNode):
            return ConstantNode(0.0)
            
        # Handle variable nodes
        if isinstance(ast, VariableNode):
            return ConstantNode(1.0 if ast.name == self.variable else 0.0)
            
        # Handle operator nodes
        if isinstance(ast, OperatorNode):
            if ast.operator == '^' and isinstance(ast.left, VariableNode) and ast.left.name == self.variable:
                # Power rule: d/dx(x^n) = n * x^(n-1)
                if isinstance(ast.right, ConstantNode):
                    # Case: x^c where c is constant
                    power = ast.right.value
                    coefficient = ConstantNode(power)
                    new_power = ConstantNode(power - 1.0)
                else:
                    # Case: x^n where n is variable
                    power = ast.right
                    coefficient = power
                    new_power = OperatorNode('-', power, ConstantNode(1.0))
                power_term = OperatorNode('^', VariableNode(self.variable), new_power)
                return OperatorNode('*', coefficient, power_term)
                
            elif ast.operator == '*':
                # Product rule: d/dx(u*v) = u'v + uv'
                if isinstance(ast.left, ConstantNode):
                    # Case: c * f(x)
                    return OperatorNode('*', ast.left, self.differentiate(ast.right))
                elif isinstance(ast.right, ConstantNode):
                    # Case: f(x) * c
                    return OperatorNode('*', ast.right, self.differentiate(ast.left))
                else:
                    # Full product rule
                    left_derivative = self.differentiate(ast.left)
                    right_derivative = self.differentiate(ast.right)
                    term1 = OperatorNode('*', left_derivative, ast.right)
                    term2 = OperatorNode('*', ast.left, right_derivative)
                    return OperatorNode('+', term1, term2)
                    
            elif ast.operator in ['+', '-']:
                # Sum/difference rule
                return OperatorNode(
                    ast.operator,
                    self.differentiate(ast.left),
                    self.differentiate(ast.right)
                )
                
        return ast
