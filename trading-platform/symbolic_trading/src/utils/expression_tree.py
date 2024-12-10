# Define operator precedence levels
operator_precedence = {
    '+': 1,
    '-': 1,
    '*': 2,
    '/': 2,
    '^': 3
}

class ExpressionNode:
    """Base class for all expression tree nodes."""
    
    def evaluate(self, variables=None):
        """
        Evaluate the expression with given variable values.
        
        Args:
            variables (dict, optional): Dictionary mapping variable names to values.
            
        Returns:
            float: The evaluated result
        """
        raise NotImplementedError("Evaluate method not implemented")

    def __str__(self):
        """Convert the expression to a string representation."""
        raise NotImplementedError("String conversion not implemented")

    def get_variables(self):
        """Get set of variables in the expression."""
        raise NotImplementedError("Get variables not implemented")

class ConstantNode(ExpressionNode):
    """Node representing a constant numerical value."""
    
    def __init__(self, value):
        """
        Initialize constant node with a value.
        
        Args:
            value (float): The constant value
        """
        self.value = float(value)

    def evaluate(self, variables=None):
        """Return the constant value."""
        return self.value

    def __str__(self):
        """Convert constant to string."""
        return str(self.value)

    def get_variables(self):
        """Constants have no variables."""
        return set()

class VariableNode(ExpressionNode):
    """Node representing a variable."""
    
    def __init__(self, name):
        """
        Initialize variable node with a name.
        
        Args:
            name (str): The variable name
        """
        self.name = name

    def evaluate(self, variables=None):
        """
        Evaluate variable with given values.
        
        Args:
            variables (dict): Dictionary mapping variable names to values
            
        Returns:
            float: The value of the variable
            
        Raises:
            KeyError: If variable value not provided
        """
        if variables is None:
            variables = {}
        if self.name not in variables:
            raise KeyError(f"No value provided for variable '{self.name}'")
        return float(variables[self.name])

    def __str__(self):
        """Convert variable to string."""
        return self.name

    def get_variables(self):
        """Return set containing this variable."""
        return {self.name}

class OperatorNode(ExpressionNode):
    """Node representing a mathematical operator."""
    
    # Define supported functions
    functions = {'sin', 'cos', 'tan', 'log', 'exp'}
    
    def __init__(self, operator, left, right):
        """
        Initialize operator node.
        
        Args:
            operator (str): The operator symbol (+, -, *, /, ^) or function name
            left (ExpressionNode): Left operand or function argument
            right (ExpressionNode): Right operand (None for functions)
        """
        self.operator = operator
        self.left = left
        self.right = right
        self.precedence = operator_precedence.get(self.operator, 0)

    def evaluate(self, variables=None):
        """
        Evaluate the operation.
        
        Args:
            variables (dict, optional): Dictionary mapping variable names to values
            
        Returns:
            float: Result of the operation
            
        Raises:
            ZeroDivisionError: If dividing by zero
            ValueError: If operation is invalid
        """
        if variables is None:
            variables = {}
            
        left_val = self.left.evaluate(variables)
        right_val = self.right.evaluate(variables)

        if self.operator == '+':
            return left_val + right_val
        elif self.operator == '-':
            return left_val - right_val
        elif self.operator == '*':
            return left_val * right_val
        elif self.operator == '/':
            if right_val == 0:
                raise ZeroDivisionError("Division by zero")
            return left_val / right_val
        elif self.operator == '^':
            return left_val ** right_val
        else:
            raise ValueError(f"Unknown operator: {self.operator}")

    def __str__(self):
        """
        Convert operation to string with proper parentheses.
        
        Returns:
            str: String representation of the operation
        """
        if self.operator in OperatorNode.functions:
            # Handle function application
            return f"{self.operator}({self.left})"
            
        # Handle binary operators
        left_str = str(self.left)
        right_str = str(self.right)

        # Add parentheses around the left operand if needed
        if isinstance(self.left, OperatorNode):
            if (self.left.precedence < self.precedence) or \
               (self.left.precedence == self.precedence and self.operator in ('+', '-', '/')):
                left_str = f'({left_str})'

        # Add parentheses around the right operand if needed
        if isinstance(self.right, OperatorNode):
            if (self.right.precedence < self.precedence) or \
               (self.right.precedence == self.precedence and self.operator in ('+', '-', '/', '^')):
                right_str = f'({right_str})'

        return f'{left_str} {self.operator} {right_str}'

    def get_variables(self):
        """Get set of all variables in the operation."""
        return self.left.get_variables().union(self.right.get_variables())

    def is_commutative(self):
        """Check if the operation is commutative."""
        return self.operator in ['+', '*']

    def is_associative(self):
        """Check if the operation is associative."""
        return self.operator in ['+', '*']

    def precedence(self):
        """Get operator precedence level."""
        if self.operator in ['+', '-']:
            return 1
        elif self.operator in ['*', '/']:
            return 2
        elif self.operator == '^':
            return 3
        else:
            raise ValueError(f"Unknown operator: {self.operator}")
