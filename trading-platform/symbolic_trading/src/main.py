from src.parser.parser import Parser
from src.transformers.transformer import Transformer
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class SymbolicMathEngine:
    def __init__(self):
        """Initialize the Symbolic Math Engine with parser and transformer."""
        self.parser = Parser()
        self.transformer = Transformer(self.parser)
        self.openrouter_api_key = os.getenv('OPENROUTER_API_KEY')
        self.trading_mode = os.getenv('TRADING_MODE', 'simulation')

    def process_command(self, command, expression, *args):
        """
        Process a command on a mathematical expression.
        
        Args:
            command (str): The operation to perform
            expression (str): The mathematical expression
            *args: Additional arguments for the operation
            
        Returns:
            str: Result of the operation
        """
        try:
            if command == 'simplify':
                return self.transformer.simplify_expression(expression)
            elif command == 'differentiate':
                variable = args[0] if args else 'x'
                return self.transformer.differentiate_expression(expression, variable)
            elif command == 'integrate':
                variable = args[0] if args else 'x'
                return self.transformer.integrate_expression(expression, variable)
            elif command == 'factor':
                return self.transformer.factor_expression(expression)
            elif command == 'substitute':
                if len(args) < 2:
                    raise ValueError("Substitute requires variable and value")
                return self.transformer.substitute_expression(expression, args[0], float(args[1]))
            else:
                raise ValueError(f"Unknown command: {command}")
        except Exception as e:
            return f"Error: {str(e)}"

def main():
    """Main function to run the Symbolic Math Engine."""
    engine = SymbolicMathEngine()
    
    print("\nWelcome to the Symbolic Math Trading Platform!")
    print("============================================")
    
    if engine.trading_mode == 'simulation':
        print("Running in simulation mode")
    elif engine.trading_mode == 'live':
        print("WARNING: Running in live trading mode!")
    
    while True:
        print("\nChoose an operation:")
        print("1) Simplify Expression")
        print("2) Differentiate Expression")
        print("3) Integrate Expression")
        print("4) Factorize Expression")
        print("5) Substitute Variable")
        print("6) Exit")
        
        try:
            choice = input("\nEnter choice [1-6]: ")
            
            if choice == '6':
                print("\nExiting Symbolic Math Engine. Goodbye!")
                break
                
            expression = input("Enter expression: ")
            
            if choice == '1':
                result = engine.process_command('simplify', expression)
                print(f"\nSimplified Expression: {result}")
                
            elif choice == '2':
                variable = input("Enter variable to differentiate with respect to [default: x]: ").strip() or 'x'
                result = engine.process_command('differentiate', expression, variable)
                print(f"\nDerivative: {result}")
                
            elif choice == '3':
                variable = input("Enter variable to integrate with respect to [default: x]: ").strip() or 'x'
                result = engine.process_command('integrate', expression, variable)
                print(f"\nIntegral: {result}")
                
            elif choice == '4':
                result = engine.process_command('factor', expression)
                print(f"\nFactorized Expression: {result}")
                
            elif choice == '5':
                variable = input("Enter variable to substitute: ")
                try:
                    value = float(input("Enter value: "))
                    result = engine.process_command('substitute', expression, variable, value)
                    print(f"\nSubstituted Expression: {result}")
                except ValueError:
                    print("\nError: Please enter a valid numerical value")
                    
            else:
                print("\nInvalid choice. Please try again.")
                
        except KeyboardInterrupt:
            print("\n\nOperation cancelled by user.")
            continue
            
        except Exception as e:
            print(f"\nError: {str(e)}")
            continue

if __name__ == "__main__":
    main()
