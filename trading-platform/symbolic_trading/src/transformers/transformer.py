from src.parser.parser import Parser
from src.transformers.simplifier import Simplifier
from src.transformers.differentiator import Differentiator
from src.transformers.integrator import Integrator
from src.transformers.factorizer import Factorizer
from src.transformers.substitutor import Substitutor

class Transformer:
    def __init__(self, parser=None):
        """
        Initialize transformer with optional parser.
        Creates new parser if none provided.
        """
        self.parser = parser if parser else Parser()
        self.simplifier = Simplifier()
        self.differentiator = None  # Created when needed with specific variable
        self.integrator = None      # Created when needed with specific variable
        self.factorizer = Factorizer()

    def parse_expression(self, expression):
        """Parse an expression string into an AST."""
        return self.parser.parse_expression(expression)

    def simplify_expression(self, expression):
        """
        Simplify a mathematical expression.
        
        Args:
            expression (str): The expression to simplify
            
        Returns:
            str: The simplified expression
        """
        if not expression or not expression.strip():
            raise ValueError("Empty expression")
            
        ast = self.parser.parse_expression(expression)
        simplified_ast = self.simplifier.simplify(ast)
        return str(simplified_ast)

    def differentiate_expression(self, expression, variable='x'):
        """
        Differentiate a mathematical expression.
        
        Args:
            expression (str): The expression to differentiate
            variable (str): The variable to differentiate with respect to
            
        Returns:
            str: The derivative expression
        """
        if not expression or not expression.strip():
            raise ValueError("Empty expression")
            
        if not variable:
            raise ValueError("Variable name cannot be empty")
            
        self.differentiator = Differentiator(variable)
        ast = self.parser.parse_expression(expression)
        derivative_ast = self.differentiator.differentiate(ast)
        simplified = self.simplifier.simplify(derivative_ast)
        return str(simplified)

    def integrate_expression(self, expression, variable='x'):
        """
        Integrate a mathematical expression.
        
        Args:
            expression (str): The expression to integrate
            variable (str): The variable to integrate with respect to
            
        Returns:
            str: The integral expression
        """
        if not expression or not expression.strip():
            raise ValueError("Empty expression")
            
        if not variable:
            raise ValueError("Variable name cannot be empty")
            
        self.integrator = Integrator(variable)
        ast = self.parser.parse_expression(expression)
        integral_ast = self.integrator.integrate(ast)
        simplified = self.simplifier.simplify(integral_ast)
        return str(simplified)

    def factor_expression(self, expression):
        """
        Factor a mathematical expression.
        
        Args:
            expression (str): The expression to factor
            
        Returns:
            str: The factored expression
        """
        if not expression or not expression.strip():
            raise ValueError("Empty expression")
            
        return self.factorizer.factor_expression(expression)

    def substitute_expression(self, expression, variable, value):
        """
        Substitute a value for a variable in an expression.
        
        Args:
            expression (str): The expression to perform substitution in
            variable (str): The variable to substitute
            value (float): The value to substitute for the variable
            
        Returns:
            str: The expression with substitution applied
        """
        if not expression or not expression.strip():
            raise ValueError("Empty expression")
            
        if not variable:
            raise ValueError("Variable name cannot be empty")
            
        ast = self.parser.parse_expression(expression)
        substitutor = Substitutor(variable, value)
        substituted_ast = substitutor.substitute(ast)
        return str(substituted_ast)

    def substitute_and_evaluate(self, expression, variable, value):
        """
        Substitute a value and evaluate the resulting expression.
        
        Args:
            expression (str): The expression to evaluate
            variable (str): The variable to substitute
            value (float): The value to substitute for the variable
            
        Returns:
            float: The numerical result
        """
        if not expression or not expression.strip():
            raise ValueError("Empty expression")
            
        if not variable:
            raise ValueError("Variable name cannot be empty")
            
        ast = self.parser.parse_expression(expression)
        substitutor = Substitutor(variable, value)
        return substitutor.substitute_and_evaluate(ast)

    def transform_chain(self, expression, transformations):
        """
        Apply a chain of transformations to an expression.
        
        Args:
            expression (str): The initial expression
            transformations (list): List of (method, args) tuples defining transformations
            
        Returns:
            str: The final transformed expression
        """
        if not expression or not expression.strip():
            raise ValueError("Empty expression")
            
        result = expression
        for method, args in transformations:
            if hasattr(self, method):
                transform_func = getattr(self, method)
                result = transform_func(result, *args)
            else:
                raise ValueError(f"Unknown transformation method: {method}")
        return result

    def analyze_expression(self, expression):
        """
        Analyze an expression and return various properties.
        
        Args:
            expression (str): The expression to analyze
            
        Returns:
            dict: Dictionary containing expression properties
        """
        if not expression or not expression.strip():
            raise ValueError("Empty expression")
            
        ast = self.parser.parse_expression(expression)
        variables = ast.get_variables()
        simplified = self.simplifier.simplify(ast)
        
        return {
            'variables': variables,
            'is_polynomial': self.factorizer.is_polynomial(ast),
            'degree': self.factorizer.get_degree(ast, 'x') if variables else 0,
            'simplified': str(simplified)
        }
