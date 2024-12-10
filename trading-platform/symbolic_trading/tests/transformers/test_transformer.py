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
    assert derivative == "3.0 * x ^ 2.0"  # Updated format

def test_transformer_integrate():
    parser = Parser()
    transformer = Transformer(parser)
    expr = "x^2"
    integral = transformer.integrate_expression(expr)
    assert integral == "x ^ 3.0 / 3.0"

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
    assert substituted == "((2.0 ^ 2.0 + 2.0 * 2.0) + 1.0)"

def test_transformer_chain():
    parser = Parser()
    transformer = Transformer(parser)
    expr = "x^2 + 2*x + 1"
    transformations = [
        ('simplify_expression', []),
        ('differentiate_expression', ['x']),
        ('substitute_expression', ['x', 2])
    ]
    result = transformer.transform_chain(expr, transformations)
    assert isinstance(result, str)

def test_transformer_analyze():
    parser = Parser()
    transformer = Transformer(parser)
    expr = "x^2 + 2*x + 1"
    analysis = transformer.analyze_expression(expr)
    assert isinstance(analysis, dict)
    assert 'variables' in analysis
    assert 'is_polynomial' in analysis
    assert 'degree' in analysis
    assert 'simplified' in analysis

@pytest.mark.parametrize("expr,expected", [
    ("x + 0", "x"),
    ("x * 1", "x"),
    ("x * 0", "0.0"),
    ("x ^ 1", "x"),
    ("x ^ 0", "1.0"),
])
def test_transformer_simplify_cases(expr, expected):
    parser = Parser()
    transformer = Transformer(parser)
    simplified = transformer.simplify_expression(expr)
    assert simplified == expected

@pytest.mark.parametrize("expr,var,expected", [
    ("x", "x", "1.0"),
    ("x^2", "x", "2.0 * x ^ 1.0"),  # Updated format
    ("2*x", "x", "2.0"),  # Updated format
])
def test_transformer_differentiate_cases(expr, var, expected):
    parser = Parser()
    transformer = Transformer(parser)
    derivative = transformer.differentiate_expression(expr, var)
    assert derivative == expected

def test_transformer_error_handling():
    parser = Parser()
    transformer = Transformer(parser)
    
    with pytest.raises(ValueError):
        transformer.differentiate_expression("", "x")
        
    with pytest.raises(ValueError):
        transformer.integrate_expression("", "x")
        
    with pytest.raises(ValueError):
        transformer.substitute_expression("x + 1", "", 1)

@pytest.mark.parametrize("expr,var,value,expected", [
    ("x", "x", 2, "2.0"),
    ("x^2", "x", 3, "9.0"),
    ("2*x + 1", "x", 4, "9.0"),
])
def test_transformer_substitute_cases(expr, var, value, expected):
    parser = Parser()
    transformer = Transformer(parser)
    result = transformer.substitute_and_evaluate(expr, var, value)
    assert str(result) == expected

def test_transformer_invalid_expression():
    parser = Parser()
    transformer = Transformer(parser)
    
    with pytest.raises(ValueError):
        transformer.simplify_expression("")
        
    with pytest.raises(ValueError):
        transformer.analyze_expression("")
        
    with pytest.raises(ValueError):
        transformer.transform_chain("", [])
