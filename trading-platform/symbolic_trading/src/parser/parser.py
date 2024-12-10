import re
from src.utils.expression_tree import ExpressionNode, OperatorNode, ConstantNode, VariableNode

class Parser:
    def __init__(self):
        self.operators = {
            '+': {'precedence': 1, 'associativity': 'L'},
            '-': {'precedence': 1, 'associativity': 'L'},
            '*': {'precedence': 2, 'associativity': 'L'},
            '/': {'precedence': 2, 'associativity': 'L'},
            '^': {'precedence': 3, 'associativity': 'R'},
            'sin': {'precedence': 4, 'associativity': 'R'},
            'cos': {'precedence': 4, 'associativity': 'R'},
            'tan': {'precedence': 4, 'associativity': 'R'},
            'log': {'precedence': 4, 'associativity': 'R'},
            'exp': {'precedence': 4, 'associativity': 'R'}
        }
        self.functions = {'sin', 'cos', 'tan', 'log', 'exp'}

    def tokenize(self, expression):
        """
        Tokenize a mathematical expression.
        
        Args:
            expression (str): The expression to tokenize
            
        Returns:
            list: List of tokens
            
        Raises:
            SyntaxError: If expression contains invalid characters
        """
        if not expression or not expression.strip():
            raise ValueError("Empty expression")

        token_specification = [
            ('NUMBER',   r'\d+(\.\d*)?'),   # Integer or decimal number
            ('IDENT',    r'[A-Za-z]+'),     # Identifiers and functions
            ('OP',       r'[\+\-\*\^\/\(\)]'), # Arithmetic operators and parentheses
            ('SKIP',     r'[ \t]+'),        # Skip over spaces and tabs
            ('MISMATCH', r'.'),             # Any other character
        ]
        tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)
        tokens = []

        for mo in re.finditer(tok_regex, expression):
            kind = mo.lastgroup
            value = mo.group()
            if kind == 'NUMBER':
                tokens.append({'type': 'NUMBER', 'value': float(value)})
            elif kind == 'IDENT':
                tokens.append({'type': 'IDENT', 'value': value})
            elif kind == 'OP':
                tokens.append({'type': 'OP', 'value': value})
            elif kind == 'SKIP':
                continue
            elif kind == 'MISMATCH':
                raise SyntaxError(f'Unexpected character {value!r} in expression')

        if not tokens:
            raise ValueError("No valid tokens found in expression")
        return tokens

    def validate_tokens(self, tokens):
        """
        Validate token sequence for basic syntax errors.
        
        Args:
            tokens (list): List of tokens to validate
            
        Raises:
            SyntaxError: If token sequence is invalid
        """
        if not tokens:
            raise ValueError("Empty token list")

        for i, token in enumerate(tokens):
            # Check for consecutive operators
            if token['type'] == 'OP' and token['value'] not in '()':
                if i == 0:
                    raise SyntaxError("Expression cannot start with an operator")
                if i == len(tokens) - 1:
                    raise SyntaxError("Expression cannot end with an operator")
                if tokens[i-1]['type'] == 'OP' and tokens[i-1]['value'] not in '()':
                    raise SyntaxError(f"Invalid consecutive operators: {tokens[i-1]['value']} {token['value']}")

        # Check parentheses matching
        paren_count = 0
        for token in tokens:
            if token['type'] == 'OP':
                if token['value'] == '(':
                    paren_count += 1
                elif token['value'] == ')':
                    paren_count -= 1
                if paren_count < 0:
                    raise SyntaxError("Unmatched closing parenthesis")
        if paren_count > 0:
            raise SyntaxError("Unmatched opening parenthesis")

    def parse(self, expression):
        """
        Parse a mathematical expression into an expression tree.
        
        Args:
            expression (str): The expression to parse
            
        Returns:
            ExpressionNode: Root node of the expression tree
            
        Raises:
            ValueError: If expression is empty
            SyntaxError: If expression is invalid
        """
        tokens = self.tokenize(expression)
        self.validate_tokens(tokens)
        
        output_queue = []
        operator_stack = []

        try:
            for token in tokens:
                if token['type'] == 'NUMBER':
                    output_queue.append(ConstantNode(token['value']))
                elif token['type'] == 'IDENT':
                    if token['value'] in self.functions:
                        # Handle function application
                        operator_stack.append(token['value'])
                    elif token['value'] == 'f' or token['value'] == 'g':
                        # Special handling for function composition
                        raise NotImplementedError("Function composition not implemented")
                    else:
                        output_queue.append(VariableNode(token['value']))
                elif token['type'] == 'OP':
                    if token['value'] == '(':
                        operator_stack.append(token['value'])
                    elif token['value'] == ')':
                        while operator_stack and operator_stack[-1] != '(':
                            op = operator_stack.pop()
                            if op in self.functions:
                                if len(output_queue) < 1:
                                    raise SyntaxError("Invalid function call")
                                arg = output_queue.pop()
                                output_queue.append(OperatorNode(op, arg, None))
                            else:
                                if len(output_queue) < 2:
                                    raise SyntaxError("Invalid expression")
                                right = output_queue.pop()
                                left = output_queue.pop()
                                output_queue.append(OperatorNode(op, left, right))
                        if not operator_stack:
                            raise SyntaxError("Unmatched right parenthesis")
                        operator_stack.pop()  # Remove '('
                        # Handle function application after closing parenthesis
                        if operator_stack and operator_stack[-1] in self.functions:
                            func = operator_stack.pop()
                            arg = output_queue.pop()
                            output_queue.append(OperatorNode(func, arg, None))
                    else:
                        while (operator_stack and operator_stack[-1] != '(' and
                               ((self.operators[token['value']]['associativity'] == 'L' and
                                 self.operators[token['value']]['precedence'] <= self.operators[operator_stack[-1]]['precedence']) or
                                (self.operators[token['value']]['associativity'] == 'R' and
                                 self.operators[token['value']]['precedence'] < self.operators[operator_stack[-1]]['precedence']))):
                            if len(output_queue) < 2:
                                raise SyntaxError("Invalid expression: not enough operands")
                            op = operator_stack.pop()
                            right = output_queue.pop()
                            left = output_queue.pop()
                            output_queue.append(OperatorNode(op, left, right))
                        operator_stack.append(token['value'])

            while operator_stack:
                if operator_stack[-1] == '(':
                    raise SyntaxError("Unmatched left parenthesis")
                if len(output_queue) < 2:
                    raise SyntaxError("Invalid expression: not enough operands")
                op = operator_stack.pop()
                right = output_queue.pop()
                left = output_queue.pop()
                output_queue.append(OperatorNode(op, left, right))

            if len(output_queue) != 1:
                raise SyntaxError("Invalid expression: too many operands")
                
            return output_queue[0]
            
        except (IndexError, KeyError):
            raise SyntaxError("Invalid expression structure")

    def parse_expression(self, expression):
        """
        Public method to parse an expression.
        
        Args:
            expression (str): The expression to parse
            
        Returns:
            ExpressionNode: Root node of the expression tree
        """
        return self.parse(expression)
