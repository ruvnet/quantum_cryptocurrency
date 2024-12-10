#!/bin/bash

# =====================================================================
# SPARC Symbolic Math Engine Full Implementation Script
# =====================================================================
# This script sets up a comprehensive project structure for a Symbolic
# Mathematics Engine based on the SPARC methodology. It includes all
# necessary code files, configurations, Docker setups, unit tests,
# and deployment scripts.
# =====================================================================

# Exit immediately if a command exits with a non-zero status.
set -e

# Variables
PROJECT_NAME="symbolic_math_engine"
SRC_DIR="src"
TESTS_DIR="tests"
DOCS_DIR="docs"
SCRIPTS_DIR="scripts"
DOCKER_DIR="Docker"
VENV_DIR="venv"

# Create project directories
echo "Creating project directories..."
mkdir -p $PROJECT_NAME/$SRC_DIR/parser
mkdir -p $PROJECT_NAME/$SRC_DIR/transformers
mkdir -p $PROJECT_NAME/$SRC_DIR/utils
mkdir -p $PROJECT_NAME/$TESTS_DIR/parser
mkdir -p $PROJECT_NAME/$TESTS_DIR/transformers
mkdir -p $PROJECT_NAME/$TESTS_DIR/utils
mkdir -p $PROJECT_NAME/$DOCS_DIR
mkdir -p $PROJECT_NAME/$SCRIPTS_DIR
mkdir -p $PROJECT_NAME/$DOCKER_DIR

# Navigate to project directory
cd $PROJECT_NAME

# Initialize Git repository
echo "Initializing Git repository..."
git init

# Create README.md
echo "Creating README.md..."
cat <<EOL > README.md
# Symbolic Math Engine

## Introduction

This project implements a symbolic mathematics engine using the SPARC (Specification, Pseudocode, Architecture, Refinement, Completion) methodology. The system is designed to parse, simplify, differentiate, integrate, factorize, and substitute symbolic mathematical expressions.

## Project Structure

- \`src/\`: Source code
  - \`parser/\`: Parsing logic
  - \`transformers/\`: Transformation modules (simplify, differentiate, etc.)
  - \`utils/\`: Utility functions and classes
- \`tests/\`: Unit and integration tests
- \`docs/\`: Documentation
- \`scripts/\`: Installation and deployment scripts
- \`Docker/\`: Docker configurations
- \`requirements.txt\`: Python dependencies

## Setup and Installation

Refer to the \`scripts/install.sh\` for installation instructions.

## Usage

Refer to the \`docs/\` directory for user guides and API references.

## Testing

Run tests using the \`scripts/run_tests.sh\` script.

## Deployment

Refer to the \`Docker/\` directory for Docker deployment configurations.

## License

MIT License
EOL

# Create requirements.txt
echo "Creating requirements.txt..."
cat <<EOL > requirements.txt
# Symbolic Math Engine Dependencies
numpy
sympy
sqlalchemy
pytest
docker
python-dotenv
flask
gunicorn
EOL

# Create .gitignore
echo "Creating .gitignore..."
cat <<EOL > .gitignore
# Python
__pycache__/
*.pyc
*.pyo
*.pyd
*.env
venv/
.env

# Docker
Dockerfile
docker-compose.yml

# IDEs
.vscode/
.idea/

# Tests
htmlcov/
.coverage
EOL

# Create main application files
echo "Creating main application files..."

# src/__init__.py
touch $SRC_DIR/__init__.py

# src/parser/__init__.py
touch $SRC_DIR/parser/__init__.py

# src/parser/parser.py
cat <<EOL > $SRC_DIR/parser/parser.py
import re
from src.utils.expression_tree import ExpressionNode, OperatorNode, ConstantNode, VariableNode

class Parser:
    def __init__(self):
        self.operators = {
            '+': {'precedence': 1, 'associativity': 'L'},
            '-': {'precedence': 1, 'associativity': 'L'},
            '*': {'precedence': 2, 'associativity': 'L'},
            '/': {'precedence': 2, 'associativity': 'L'},
            '^': {'precedence': 3, 'associativity': 'R'}
        }

    def tokenize(self, expression):
        token_specification = [
            ('NUMBER',   r'\d+(\.\d*)?'),   # Integer or decimal number
            ('IDENT',    r'[A-Za-z]+'),     # Identifiers
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
                raise SyntaxError(f'Unexpected character {value}')
        return tokens

    def parse(self, expression):
        tokens = self.tokenize(expression)
        output_queue = []
        operator_stack = []

        for token in tokens:
            if token['type'] == 'NUMBER':
                output_queue.append(ConstantNode(token['value']))
            elif token['type'] == 'IDENT':
                output_queue.append(VariableNode(token['value']))
            elif token['type'] == 'OP':
                if token['value'] == '(':
                    operator_stack.append(token['value'])
                elif token['value'] == ')':
                    while operator_stack and operator_stack[-1] != '(':
                        op = operator_stack.pop()
                        right = output_queue.pop()
                        left = output_queue.pop()
                        output_queue.append(OperatorNode(op, left, right))
                    operator_stack.pop()  # Remove '('
                else:
                    while (operator_stack and operator_stack[-1] != '(' and
                           ((self.operators[token['value']]['associativity'] == 'L' and
                             self.operators[token['value']]['precedence'] <= self.operators[operator_stack[-1]]['precedence']) or
                            (self.operators[token['value']]['associativity'] == 'R' and
                             self.operators[token['value']]['precedence'] < self.operators[operator_stack[-1]]['precedence']))):
                        op = operator_stack.pop()
                        right = output_queue.pop()
                        left = output_queue.pop()
                        output_queue.append(OperatorNode(op, left, right))
                    operator_stack.append(token['value'])

        while operator_stack:
            op = operator_stack.pop()
            right = output_queue.pop()
            left = output_queue.pop()
            output_queue.append(OperatorNode(op, left, right))

        if len(output_queue) != 1:
            raise SyntaxError('Invalid expression')
        return output_queue[0]

    def parse_expression(self, expression):
        return self.parse(expression)
EOL

# src/utils/expression_tree.py
cat <<EOL > $SRC_DIR/utils/expression_tree.py
class ExpressionNode:
    def evaluate(self, variables={}):
        raise NotImplementedError("Evaluate method not implemented.")

    def __str__(self):
        raise NotImplementedError("String conversion not implemented.")

class ConstantNode(ExpressionNode):
    def __init__(self, value):
        self.value = value

    def evaluate(self, variables={}):
        return self.value

    def __str__(self):
        return str(self.value)

class VariableNode(ExpressionNode):
    def __init__(self, name):
        self.name = name

    def evaluate(self, variables={}):
        return variables.get(self.name, 0)

    def __str__(self):
        return self.name

class OperatorNode(ExpressionNode):
    def __init__(self, operator, left, right):
        self.operator = operator
        self.left = left
        self.right = right

    def evaluate(self, variables={}):
        left_val = self.left.evaluate(variables)
        right_val = self.right.evaluate(variables)
        if self.operator == '+':
            return left_val + right_val
        elif self.operator == '-':
            return left_val - right_val
        elif self.operator == '*':
            return left_val * right_val
        elif self.operator == '/':
            return left_val / right_val
        elif self.operator == '^':
            return left_val ** right_val
        else:
            raise ValueError(f"Unknown operator: {self.operator}")

    def __str__(self):
        return f"({self.left} {self.operator} {self.right})"
EOL

# src/transformers/__init__.py
cat <<EOL > $SRC_DIR/transformers/__init__.py
from .simplifier import Simplifier
from .differentiator import Differentiator
from .integrator import Integrator
from .factorizer import Factorizer
from .substitutor import Substitutor
EOL

# src/transformers/simplifier.py
cat <<EOL > $SRC_DIR/transformers/simplifier.py
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
EOL

# src/transformers/differentiator.py
cat <<EOL > $SRC_DIR/transformers/differentiator.py
from src.utils.expression_tree import OperatorNode, ConstantNode, VariableNode

class Differentiator:
    def __init__(self, variable):
        self.variable = variable

    def differentiate(self, node):
        if isinstance(node, ConstantNode):
            return ConstantNode(0)
        elif isinstance(node, VariableNode):
            if node.name == self.variable:
                return ConstantNode(1)
            else:
                return ConstantNode(0)
        elif isinstance(node, OperatorNode):
            if node.operator == '+':
                return OperatorNode('+', self.differentiate(node.left), self.differentiate(node.right))
            elif node.operator == '-':
                return OperatorNode('-', self.differentiate(node.left), self.differentiate(node.right))
            elif node.operator == '*':
                # Product rule: (f * g)' = f' * g + f * g'
                left_diff = OperatorNode('*', self.differentiate(node.left), node.right)
                right_diff = OperatorNode('*', node.left, self.differentiate(node.right))
                return OperatorNode('+', left_diff, right_diff)
            elif node.operator == '/':
                # Quotient rule: (f / g)' = (f' * g - f * g') / g^2
                numerator_left = OperatorNode('*', self.differentiate(node.left), node.right)
                numerator_right = OperatorNode('*', node.left, self.differentiate(node.right))
                numerator = OperatorNode('-', numerator_left, numerator_right)
                denominator = OperatorNode('^', node.right, ConstantNode(2))
                return OperatorNode('/', numerator, denominator)
            elif node.operator == '^':
                if isinstance(node.right, ConstantNode):
                    # Power rule: d/dx (f^n) = n * f^(n-1) * f'
                    new_exponent = ConstantNode(node.right.value - 1)
                    base_diff = self.differentiate(node.left)
                    new_base = OperatorNode('^', node.left, new_exponent)
                    return OperatorNode('*', OperatorNode('*', node.right, new_base), base_diff)
                elif isinstance(node.left, ConstantNode):
                    # d/dx (a^f(x)) = a^f(x) * ln(a) * f'(x)
                    ln_a = ConstantNode(math.log(node.left.value))
                    f_prime = self.differentiate(node.right)
                    a_f = OperatorNode('^', node.left, node.right)
                    return OperatorNode('*', OperatorNode('*', a_f, ln_a), f_prime)
                else:
                    # d/dx (f(x)^g(x)) = f(x)^g(x) * [g'(x) * ln(f(x)) + g(x) * f'(x)/f(x)]
                    f = node.left
                    g = node.right
                    f_prime = self.differentiate(f)
                    g_prime = self.differentiate(g)
                    ln_f = FunctionNode('ln', [f])
                    term1 = OperatorNode('*', g_prime, ln_f)
                    term2 = OperatorNode('/', OperatorNode('*', g, f_prime), f)
                    bracket = OperatorNode('+', term1, term2)
                    return OperatorNode('*', node, bracket)
            else:
                raise NotImplementedError(f"Differentiation for operator '{node.operator}' not implemented.")
        else:
            raise TypeError("Unsupported node type for differentiation.")
EOL

# src/transformers/integrator.py
cat <<EOL > $SRC_DIR/transformers/integrator.py
from src.utils.expression_tree import OperatorNode, ConstantNode, VariableNode
import math

class Integrator:
    def __init__(self, variable):
        self.variable = variable

    def integrate(self, node):
        if isinstance(node, ConstantNode):
            return OperatorNode('*', node, VariableNode(self.variable))
        elif isinstance(node, VariableNode):
            return OperatorNode('/', OperatorNode('^', node, ConstantNode(2)), ConstantNode(2))
        elif isinstance(node, OperatorNode):
            if node.operator == '+':
                return OperatorNode('+', self.integrate(node.left), self.integrate(node.right))
            elif node.operator == '-':
                return OperatorNode('-', self.integrate(node.left), self.integrate(node.right))
            elif node.operator == '*':
                # Integration by parts or other advanced methods needed
                raise NotImplementedError("Integration for multiplication not implemented.")
            elif node.operator == '^':
                if isinstance(node.right, ConstantNode):
                    new_exponent = node.right.value + 1
                    return OperatorNode('/', OperatorNode('^', node.left, ConstantNode(new_exponent)), ConstantNode(new_exponent))
                else:
                    raise NotImplementedError("Integration for variable exponents not implemented.")
            else:
                raise NotImplementedError(f"Integration for operator '{node.operator}' not implemented.")
        else:
            raise TypeError("Unsupported node type for integration.")
EOL

# src/transformers/factorizer.py
cat <<EOL > $SRC_DIR/transformers/factorizer.py
from sympy import sympify, factor
from src.utils.expression_tree import ExpressionNode

class Factorizer:
    def __init__(self):
        pass

    def factor_expression(self, expression_str):
        sympy_expr = sympify(expression_str)
        factored_expr = factor(sympy_expr)
        return str(factored_expr)
EOL

# src/transformers/substitutor.py
cat <<EOL > $SRC_DIR/transformers/substitutor.py
from src.utils.expression_tree import OperatorNode, ConstantNode, VariableNode

class Substitutor:
    def __init__(self, variable, value):
        self.variable = variable
        self.value = value

    def substitute(self, node):
        if isinstance(node, ConstantNode):
            return node
        elif isinstance(node, VariableNode):
            if node.name == self.variable:
                return ConstantNode(self.value)
            else:
                return node
        elif isinstance(node, OperatorNode):
            left_sub = self.substitute(node.left)
            right_sub = self.substitute(node.right)
            return OperatorNode(node.operator, left_sub, right_sub)
        else:
            raise TypeError("Unsupported node type for substitution.")
EOL

# src/transformers/function_node.py
cat <<EOL > $SRC_DIR/transformers/function_node.py
from src.utils.expression_tree import ExpressionNode, OperatorNode, ConstantNode, VariableNode

class FunctionNode(ExpressionNode):
    def __init__(self, function_name, arguments):
        self.function_name = function_name
        self.arguments = arguments

    def evaluate(self, variables={}):
        arg_values = [arg.evaluate(variables) for arg in self.arguments]
        if self.function_name == 'sin':
            return math.sin(arg_values[0])
        elif self.function_name == 'cos':
            return math.cos(arg_values[0])
        elif self.function_name == 'ln':
            return math.log(arg_values[0])
        # Add more functions as needed
        else:
            raise ValueError(f"Unknown function: {self.function_name}")

    def __str__(self):
        args_str = ', '.join(str(arg) for arg in self.arguments)
        return f"{self.function_name}({args_str})"
EOL

# src/transformers/__init__.py (updated to include FunctionNode)
cat <<EOL > $SRC_DIR/transformers/__init__.py
from .simplifier import Simplifier
from .differentiator import Differentiator
from .integrator import Integrator
from .factorizer import Factorizer
from .substitutor import Substitutor
from .function_node import FunctionNode
EOL

# src/transformers/transformer.py
cat <<EOL > $SRC_DIR/transformers/transformer.py
class Transformer:
    def __init__(self, parser):
        self.parser = parser
        self.simplifier = Simplifier()
        self.differentiator = Differentiator('x')
        self.integrator = Integrator('x')
        self.factorizer = Factorizer()
        self.substitutor = Substitutor('x', 2)

    def simplify_expression(self, expression):
        ast = self.parser.parse_expression(expression)
        simplified_ast = self.simplifier.simplify(ast)
        return str(simplified_ast)

    def differentiate_expression(self, expression):
        ast = self.parser.parse_expression(expression)
        derivative_ast = self.differentiator.differentiate(ast)
        return str(derivative_ast)

    def integrate_expression(self, expression):
        ast = self.parser.parse_expression(expression)
        integral_ast = self.integrator.integrate(ast)
        return str(integral_ast)

    def factor_expression(self, expression):
        return self.factorizer.factor_expression(expression)

    def substitute_expression(self, expression, variable, value):
        ast = self.parser.parse_expression(expression)
        substitutor = Substitutor(variable, value)
        substituted_ast = substitutor.substitute(ast)
        return str(substituted_ast)
EOL

# src/utils/__init__.py
touch $SRC_DIR/utils/__init__.py

# src/main.py
cat <<EOL > $SRC_DIR/main.py
from src.parser.parser import Parser
from src.transformers.transformer import Transformer

def main():
    parser = Parser()
    transformer = Transformer(parser)

    print("Welcome to the Symbolic Math Engine!")
    while True:
        print("\nChoose an operation:")
        print("1) Simplify Expression")
        print("2) Differentiate Expression")
        print("3) Integrate Expression")
        print("4) Factorize Expression")
        print("5) Substitute Variable")
        print("6) Exit")
        choice = input("Enter choice [1-6]: ")

        if choice == '1':
            expr = input("Enter expression to simplify: ")
            try:
                result = transformer.simplify_expression(expr)
                print(f"Simplified Expression: {result}")
            except Exception as e:
                print(f"Error: {e}")
        elif choice == '2':
            expr = input("Enter expression to differentiate: ")
            try:
                result = transformer.differentiate_expression(expr)
                print(f"Derivative: {result}")
            except Exception as e:
                print(f"Error: {e}")
        elif choice == '3':
            expr = input("Enter expression to integrate: ")
            try:
                result = transformer.integrate_expression(expr)
                print(f"Integral: {result}")
            except Exception as e:
                print(f"Error: {e}")
        elif choice == '4':
            expr = input("Enter expression to factorize: ")
            try:
                result = transformer.factor_expression(expr)
                print(f"Factorized Expression: {result}")
            except Exception as e:
                print(f"Error: {e}")
        elif choice == '5':
            expr = input("Enter expression for substitution: ")
            var = input("Enter variable to substitute: ")
            val = float(input("Enter value to substitute: "))
            try:
                substitutor = Substitutor(var, val)
                result = transformer.substitute_expression(expr, var, val)
                print(f"Substituted Expression: {result}")
            except Exception as e:
                print(f"Error: {e}")
        elif choice == '6':
            print("Exiting Symbolic Math Engine. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
EOL

# Create tests files
echo "Creating test files..."

# tests/__init__.py
touch $TESTS_DIR/__init__.py

# tests/parser/test_parser.py
cat <<EOL > $TESTS_DIR/parser/test_parser.py
import pytest
from src.parser.parser import Parser
from src.utils.expression_tree import ConstantNode, VariableNode, OperatorNode

def test_parse_simple_expression():
    parser = Parser()
    expr = "x + 2"
    ast = parser.parse_expression(expr)
    assert isinstance(ast, OperatorNode)
    assert ast.operator == '+'
    assert isinstance(ast.left, VariableNode)
    assert ast.left.name == 'x'
    assert isinstance(ast.right, ConstantNode)
    assert ast.right.value == 2

def test_parse_complex_expression():
    parser = Parser()
    expr = "x^2 + 2*x + 1"
    ast = parser.parse_expression(expr)
    assert isinstance(ast, OperatorNode)
    assert ast.operator == '+'
    # Further assertions can be added to verify the entire AST structure
EOL

# tests/transformers/test_simplifier.py
cat <<EOL > $TESTS_DIR/transformers/test_simplifier.py
import pytest
from src.transformers.simplifier import Simplifier
from src.utils.expression_tree import OperatorNode, ConstantNode, VariableNode

def test_simplify_add_zero():
    simplifier = Simplifier()
    expr = OperatorNode('+', ConstantNode(0), VariableNode('x'))
    simplified = simplifier.simplify(expr)
    assert isinstance(simplified, VariableNode)
    assert simplified.name == 'x'

def test_simplify_multiply_zero():
    simplifier = Simplifier()
    expr = OperatorNode('*', VariableNode('x'), ConstantNode(0))
    simplified = simplifier.simplify(expr)
    assert isinstance(simplified, ConstantNode)
    assert simplified.value == 0

def test_simplify_multiply_one():
    simplifier = Simplifier()
    expr = OperatorNode('*', VariableNode('x'), ConstantNode(1))
    simplified = simplifier.simplify(expr)
    assert isinstance(simplified, VariableNode)
    assert simplified.name == 'x'

def test_simplify_power_zero():
    simplifier = Simplifier()
    expr = OperatorNode('^', VariableNode('x'), ConstantNode(0))
    simplified = simplifier.simplify(expr)
    assert isinstance(simplified, ConstantNode)
    assert simplified.value == 1

def test_simplify_power_one():
    simplifier = Simplifier()
    expr = OperatorNode('^', VariableNode('x'), ConstantNode(1))
    simplified = simplifier.simplify(expr)
    assert isinstance(simplified, VariableNode)
    assert simplified.name == 'x'
EOL

# tests/transformers/test_differentiator.py
cat <<EOL > $TESTS_DIR/transformers/test_differentiator.py
import pytest
from src.transformers.differentiator import Differentiator
from src.utils.expression_tree import OperatorNode, ConstantNode, VariableNode

def test_differentiate_constant():
    differentiator = Differentiator('x')
    expr = ConstantNode(5)
    derivative = differentiator.differentiate(expr)
    assert isinstance(derivative, ConstantNode)
    assert derivative.value == 0

def test_differentiate_variable():
    differentiator = Differentiator('x')
    expr = VariableNode('x')
    derivative = differentiator.differentiate(expr)
    assert isinstance(derivative, ConstantNode)
    assert derivative.value == 1

def test_differentiate_power():
    differentiator = Differentiator('x')
    expr = OperatorNode('^', VariableNode('x'), ConstantNode(3))
    derivative = differentiator.differentiate(expr)
    assert isinstance(derivative, OperatorNode)
    assert derivative.operator == '*'
    # Further assertions can be added based on the structure of the derivative
EOL

# tests/transformers/test_integrator.py
cat <<EOL > $TESTS_DIR/transformers/test_integrator.py
import pytest
from src.transformers.integrator import Integrator
from src.utils.expression_tree import OperatorNode, ConstantNode, VariableNode

def test_integrate_constant():
    integrator = Integrator('x')
    expr = ConstantNode(5)
    integral = integrator.integrate(expr)
    assert isinstance(integral, OperatorNode)
    assert integral.operator == '*'

def test_integrate_variable():
    integrator = Integrator('x')
    expr = VariableNode('x')
    integral = integrator.integrate(expr)
    assert isinstance(integral, OperatorNode)
    assert integral.operator == '/'

def test_integrate_power():
    integrator = Integrator('x')
    expr = OperatorNode('^', VariableNode('x'), ConstantNode(2))
    integral = integrator.integrate(expr)
    assert isinstance(integral, OperatorNode)
    assert integral.operator == '/'
EOL

# tests/transformers/test_factorizer.py
cat <<EOL > $TESTS_DIR/transformers/test_factorizer.py
import pytest
from src.transformers.factorizer import Factorizer

def test_factor_simple():
    factorizer = Factorizer()
    expression = "x^2 + 2*x + 1"
    factored = factorizer.factor_expression(expression)
    assert factored == "(x + 1)**2"

def test_factor_linear():
    factorizer = Factorizer()
    expression = "x + 5"
    factored = factorizer.factor_expression(expression)
    assert factored == "x + 5"  # Already factored
EOL

# tests/transformers/test_substitutor.py
cat <<EOL > $TESTS_DIR/transformers/test_substitutor.py
import pytest
from src.transformers.substitutor import Substitutor
from src.utils.expression_tree import OperatorNode, ConstantNode, VariableNode

def test_substitute_variable():
    substitutor = Substitutor('x', 2)
    expr = OperatorNode('+', VariableNode('x'), ConstantNode(3))
    substituted = substitutor.substitute(expr)
    assert isinstance(substituted, OperatorNode)
    assert isinstance(substituted.left, ConstantNode)
    assert substituted.left.value == 2
    assert isinstance(substituted.right, ConstantNode)
    assert substituted.right.value == 3

def test_substitute_multiple():
    substitutor = Substitutor('x', 3)
    expr = OperatorNode('*', VariableNode('x'), OperatorNode('+', VariableNode('x'), ConstantNode(4)))
    substituted = substitutor.substitute(expr)
    # Further assertions can be added to verify the substituted expression
EOL

# tests/transformers/test_transformer.py
cat <<EOL > $TESTS_DIR/transformers/test_transformer.py
import pytest
from src.parser.parser import Parser
from src.transformers.transformer import Transformer

def test_transformer_simplify():
    parser = Parser()
    transformer = Transformer(parser)
    expr = "x + 0"
    simplified = transformer.simplify_expression(expr)
    assert simplified == "x"

def test_transformer_differentiate():
    parser = Parser()
    transformer = Transformer(parser)
    expr = "x^3"
    derivative = transformer.differentiate_expression(expr)
    assert derivative == "((3 * (x ^ 2)) * 1)"

def test_transformer_integrate():
    parser = Parser()
    transformer = Transformer(parser)
    expr = "x^2"
    integral = transformer.integrate_expression(expr)
    assert integral == "((x ^ 3) / 3)"

def test_transformer_factor():
    parser = Parser()
    transformer = Transformer(parser)
    expr = "x^2 + 2*x + 1"
    factored = transformer.factor_expression(expr)
    assert factored == "(x + 1)**2"

def test_transformer_substitute():
    parser = Parser()
    transformer = Transformer(parser)
    expr = "x^2 + 2*x + 1"
    substituted = transformer.substitute_expression(expr, 'x', 2)
    assert substituted == "4 + 4 + 1"
EOL

# Create scripts
echo "Creating installation and deployment scripts..."

# scripts/install.sh
cat <<'EOL' > $SCRIPTS_DIR/install.sh
#!/bin/bash

# Install Script for Symbolic Math Engine

# Exit immediately if a command exits with a non-zero status.
set -e

echo "Setting up virtual environment..."
python3 -m venv ../venv
source ../venv/bin/activate

echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "Installation complete. To activate the virtual environment, run:"
echo "source ../venv/bin/activate"
EOL

# scripts/run_tests.sh
cat <<'EOL' > $SCRIPTS_DIR/run_tests.sh
#!/bin/bash

# Run Tests for Symbolic Math Engine

# Exit immediately if a command exits with a non-zero status.
set -e

echo "Activating virtual environment..."
source ../venv/bin/activate

echo "Running pytest..."
pytest --cov=src tests/

echo "Tests completed."
EOL

# scripts/start.sh
cat <<'EOL' > $SCRIPTS_DIR/start.sh
#!/bin/bash

# Start Script for Symbolic Math Engine

echo "Choose deployment option:"
echo "1) Local Deployment"
echo "2) Docker Deployment"
read -p "Enter choice [1-2]: " choice

if [ "$choice" -eq "1" ]; then
    echo "Starting locally..."
    source ../venv/bin/activate
    python src/main.py
elif [ "$choice" -eq "2" ]; then
    echo "Starting Docker deployment..."
    docker-compose up --build
else
    echo "Invalid choice."
    exit 1
fi
EOL

# Make scripts executable
chmod +x $SCRIPTS_DIR/install.sh
chmod +x $SCRIPTS_DIR/run_tests.sh
chmod +x $SCRIPTS_DIR/start.sh

# Create Dockerfile
echo "Creating Dockerfile..."
cat <<EOL > $DOCKER_DIR/Dockerfile
# Use official Python image as base
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy project
COPY . /app/

# Expose port if needed (e.g., for web interface)
EXPOSE 8000

# Run the application
CMD ["bash", "scripts/start.sh"]
EOL

# Create docker-compose.yml
echo "Creating docker-compose.yml..."
cat <<EOL > docker-compose.yml
version: '3.8'

services:
  symbolic_math_engine:
    build: ./Docker
    container_name: symbolic_math_engine
    volumes:
      - .:/app
    ports:
      - "8000:8000"
    environment:
      - PYTHONUNBUFFERED=1
EOL

# Create docs
echo "Creating documentation files..."

# docs/README.md
cat <<EOL > $DOCS_DIR/README.md
# Symbolic Math Engine Documentation

## Getting Started

### Installation

Refer to the [Installation Guide](../scripts/install.sh) for setting up the project.

### Usage

Run the application using the start script:

\`\`\`bash
./scripts/start.sh
\`\`\`

### Available Operations

1. **Simplify Expression**
2. **Differentiate Expression**
3. **Integrate Expression**
4. **Factorize Expression**
5. **Substitute Variable**
6. **Exit**

## API Reference

*To be developed if a web interface or API is implemented.*

## Contributing

*Guidelines for contributing to the project.*

## License

MIT License
EOL

# Create Docker entrypoint script if needed
# Not necessary in this setup as start.sh handles it

# Create .env file (empty placeholder)
touch .env

# Create example scripts
echo "Creating example scripts..."

# scripts/example_simplify.py
cat <<EOL > $SCRIPTS_DIR/example_simplify.py
from src.parser.parser import Parser
from src.transformers.simplifier import Simplifier

def example_simplify():
    parser = Parser()
    simplifier = Simplifier()
    expression = "x + 0"
    ast = parser.parse_expression(expression)
    simplified_ast = simplifier.simplify(ast)
    print(f"Simplified Expression: {simplified_ast}")

if __name__ == "__main__":
    example_simplify()
EOL

# scripts/example_differentiate.py
cat <<EOL > $SCRIPTS_DIR/example_differentiate.py
from src.parser.parser import Parser
from src.transformers.differentiator import Differentiator

def example_differentiate():
    parser = Parser()
    differentiator = Differentiator('x')
    expression = "x^3"
    ast = parser.parse_expression(expression)
    derivative_ast = differentiator.differentiate(ast)
    print(f"Derivative: {derivative_ast}")

if __name__ == "__main__":
    example_differentiate()
EOL

# scripts/example_integrate.py
cat <<EOL > $SCRIPTS_DIR/example_integrate.py
from src.parser.parser import Parser
from src.transformers.integrator import Integrator

def example_integrate():
    parser = Parser()
    integrator = Integrator('x')
    expression = "x^2"
    ast = parser.parse_expression(expression)
    integral_ast = integrator.integrate(ast)
    print(f"Integral: {integral_ast}")

if __name__ == "__main__":
    example_integrate()
EOL

# scripts/example_factorize.py
cat <<EOL > $SCRIPTS_DIR/example_factorize.py
from src.transformers.factorizer import Factorizer

def example_factorize():
    factorizer = Factorizer()
    expression = "x^2 + 2*x + 1"
    factored = factorizer.factor_expression(expression)
    print(f"Factorized Expression: {factored}")

if __name__ == "__main__":
    example_factorize()
EOL

# scripts/example_substitute.py
cat <<EOL > $SCRIPTS_DIR/example_substitute.py
from src.parser.parser import Parser
from src.transformers.substitutor import Substitutor

def example_substitute():
    parser = Parser()
    substitutor = Substitutor('x', 2)
    expression = "x^2 + 3*x + 4"
    ast = parser.parse_expression(expression)
    substituted_ast = substitutor.substitute(ast)
    substituted_value = substituted_ast.evaluate()
    print(f"Substituted Expression: {substituted_ast}")
    print(f"Evaluated Value: {substituted_value}")

if __name__ == "__main__":
    example_substitute()
EOL

# Final message
echo "SPARC Symbolic Math Engine project structure has been set up successfully."
echo "Navigate to the '$PROJECT_NAME' directory and run './scripts/install.sh' to install dependencies."
