from src.utils.expression_tree import OperatorNode, ConstantNode, VariableNode

class Substitutor:
    def __init__(self, variable, value):
        """
        Initialize substitutor with variable to replace and its value.
        
        Args:
            variable (str): The variable name to substitute
            value (float): The value to substitute for the variable
        """
        self.variable = variable
        self.value = value

    def substitute(self, node):
        """
        Substitute a value or expression for a variable in an expression tree.
        
        Args:
            node (ExpressionNode): The root node of the expression tree
            
        Returns:
            ExpressionNode: The expression tree with substitution applied
        """
        if isinstance(node, ConstantNode):
            return node
        elif isinstance(node, VariableNode):
            if node.name == self.variable:
                if isinstance(self.value, (int, float)):
                    return ConstantNode(float(self.value))
                elif isinstance(self.value, str):
                    from src.parser.parser import Parser
                    parser = Parser()
                    return parser.parse_expression(self.value)
                else:
                    return self.value  # Already an ExpressionNode
            else:
                return node
        elif isinstance(node, OperatorNode):
            return OperatorNode(
                node.operator,
                self.substitute(node.left),
                self.substitute(node.right)
            )
        else:
            raise TypeError(f"Unsupported node type for substitution: {type(node)}")

    def substitute_multiple(self, node, substitutions):
        """
        Substitute multiple variables with their values.
        
        Args:
            node (ExpressionNode): The root node of the expression tree
            substitutions (dict): Dictionary mapping variable names to values
            
        Returns:
            ExpressionNode: The expression tree with all substitutions applied
        """
        result = node
        for var, value in substitutions.items():
            substitutor = Substitutor(var, value)
            result = substitutor.substitute(result)
        return result

    def substitute_and_evaluate(self, node):
        """
        Substitute and evaluate the expression to a numerical result.
        
        Args:
            node (ExpressionNode): The root node of the expression tree
            
        Returns:
            float: The numerical result after substitution and evaluation
        """
        substituted = self.substitute(node)
        return substituted.evaluate()

    def substitute_expression(self, node, var_expr):
        """
        Substitute a variable with another expression.
        
        Args:
            node (ExpressionNode): The root node of the expression tree
            var_expr (ExpressionNode): The expression to substitute for the variable
            
        Returns:
            ExpressionNode: The expression tree with the expression substituted
        """
        if isinstance(node, ConstantNode):
            return node
        elif isinstance(node, VariableNode):
            if node.name == self.variable:
                return var_expr
            else:
                return node
        elif isinstance(node, OperatorNode):
            return OperatorNode(
                node.operator,
                self.substitute_expression(node.left, var_expr),
                self.substitute_expression(node.right, var_expr)
            )
        else:
            raise TypeError(f"Unsupported node type for expression substitution: {type(node)}")

    def check_valid_substitution(self, node):
        """
        Check if a substitution would be valid (e.g., no division by zero).
        
        Args:
            node (ExpressionNode): The expression tree to check
            
        Returns:
            bool: True if substitution is valid, False otherwise
        """
        try:
            substituted = self.substitute(node)
            # Try evaluating to catch potential runtime errors
            substituted.evaluate()
            return True
        except (ZeroDivisionError, ValueError, ArithmeticError):
            return False

    def get_variables(self, node, variables=None):
        """
        Get all variables in an expression tree.
        
        Args:
            node (ExpressionNode): The root node of the expression tree
            variables (set, optional): Set to collect variables. Defaults to None.
            
        Returns:
            set: Set of all variable names in the expression
        """
        if variables is None:
            variables = set()
            
        if isinstance(node, VariableNode):
            variables.add(node.name)
        elif isinstance(node, OperatorNode):
            self.get_variables(node.left, variables)
            self.get_variables(node.right, variables)
            
        return variables

    def requires_substitution(self, node):
        """
        Check if an expression contains the variable to be substituted.
        
        Args:
            node (ExpressionNode): The root node of the expression tree
            
        Returns:
            bool: True if the expression contains the variable, False otherwise
        """
        variables = self.get_variables(node)
        return self.variable in variables
