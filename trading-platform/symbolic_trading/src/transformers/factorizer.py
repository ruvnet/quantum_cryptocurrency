from sympy import sympify, factor
from src.utils.expression_tree import ExpressionNode, OperatorNode, ConstantNode, VariableNode

class Factorizer:
    def __init__(self):
        pass

    def factor_expression(self, expression_str):
        """
        Factorize a mathematical expression using SymPy.
        
        Args:
            expression_str (str): The expression to factorize as a string
            
        Returns:
            str: The factored expression as a string
        """
        try:
            # Convert to SymPy expression
            sympy_expr = sympify(expression_str)
            # Factor the expression
            factored_expr = factor(sympy_expr)
            return str(factored_expr)
        except Exception as e:
            raise ValueError(f"Failed to factorize expression: {str(e)}")

    def factor_node(self, node):
        """
        Convert ExpressionNode to string, factorize, and convert back to ExpressionNode.
        Not fully implemented - would need parser to convert string back to ExpressionNode.
        
        Args:
            node (ExpressionNode): The expression tree node to factorize
            
        Returns:
            ExpressionNode: The factored expression tree
        """
        # Convert node to string representation
        expr_str = str(node)
        # Factorize the string
        factored_str = self.factor_expression(expr_str)
        # Would need to parse factored_str back to ExpressionNode
        raise NotImplementedError("Converting factored expression back to ExpressionNode not implemented")

    def is_polynomial(self, node):
        """
        Check if an expression is a polynomial in its variables.
        
        Args:
            node (ExpressionNode): The expression tree node to check
            
        Returns:
            bool: True if the expression is a polynomial, False otherwise
        """
        if isinstance(node, ConstantNode):
            return True
        elif isinstance(node, VariableNode):
            return True
        elif isinstance(node, OperatorNode):
            if node.operator in ['+', '-', '*']:
                return self.is_polynomial(node.left) and self.is_polynomial(node.right)
            elif node.operator == '^':
                # Only allow positive integer exponents for polynomials
                return (self.is_polynomial(node.left) and 
                        isinstance(node.right, ConstantNode) and 
                        node.right.value >= 0 and 
                        node.right.value.is_integer())
            else:
                return False
        return False

    def get_degree(self, node, variable):
        """
        Get the degree of a polynomial with respect to a variable.
        
        Args:
            node (ExpressionNode): The expression tree node
            variable (str): The variable to find the degree for
            
        Returns:
            int: The degree of the polynomial in the variable
        """
        if isinstance(node, ConstantNode):
            return 0
        elif isinstance(node, VariableNode):
            return 1 if node.name == variable else 0
        elif isinstance(node, OperatorNode):
            if node.operator in ['+', '-']:
                return max(self.get_degree(node.left, variable), 
                          self.get_degree(node.right, variable))
            elif node.operator == '*':
                return (self.get_degree(node.left, variable) + 
                       self.get_degree(node.right, variable))
            elif node.operator == '^':
                if isinstance(node.right, ConstantNode):
                    return self.get_degree(node.left, variable) * node.right.value
                else:
                    raise ValueError("Variable exponent in degree calculation")
            elif node.operator == '/':
                # For f(x)/g(x), degree is deg(f) - deg(g)
                return (self.get_degree(node.left, variable) - 
                       self.get_degree(node.right, variable))
            else:
                raise ValueError(f"Unknown operator in degree calculation: {node.operator}")
        else:
            raise TypeError("Unknown node type in degree calculation")

    def get_coefficients(self, node, variable):
        """
        Get the coefficients of a polynomial in standard form.
        Not fully implemented - would need more complex polynomial manipulation.
        
        Args:
            node (ExpressionNode): The expression tree node
            variable (str): The variable to get coefficients for
            
        Returns:
            list: The coefficients of the polynomial from highest to lowest degree
        """
        if not self.is_polynomial(node):
            raise ValueError("Expression is not a polynomial")
            
        degree = self.get_degree(node, variable)
        coefficients = [0] * (degree + 1)
        
        # Would need to implement coefficient extraction logic here
        raise NotImplementedError("Coefficient extraction not implemented")
