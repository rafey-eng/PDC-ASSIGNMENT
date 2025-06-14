from lexer import tokenize
from parser import parse_code, show_lalr_table
from semantic import analyze
from codegen import generate_code
from visualizer import visualize_ast
from cfg import build_cfg
from error import handle
from ll1_parser import LL1Parser
import json
from colorama import Fore, init

init(autoreset=True)

def main():
    try:
        code = "x = 10 - 2 * 3"
        print("Input Code:\n", code)

        # Lexical Analysis
        tokens = tokenize(code)
        print("\nTokens:")
        for token in tokens:
            print(f"{token.type}: {token.value}")

        # Syntax Analysis
        ast = parse_code(code)
        print("\nAST generated.")

        # Semantic Analysis
        scope_info = analyze(ast)
        print("Semantic analysis passed.")

        # Code Generation
        output = generate_code(ast)
        print("\nFormatted Code:\n", output)

        # Visualization
        try:
            dot = visualize_ast(ast)
            dot.render("ast", view=True)
            print("\nAST visualization saved to ast.png")
        except Exception as e:
            print(f"{Fore.YELLOW}[Warning]{Fore.RESET} Could not generate AST visualization: {e}")

        # Save AST as JSON
        with open("ast.json", "w") as f:
            json.dump(ast.to_dict(), f, indent=2)
        print("AST saved to ast.json")

        # Control Flow Graph
        try:
            cfg = build_cfg(ast)
            cfg.render("cfg", view=True)
            print("CFG saved to cfg.png")
        except Exception as e:
            print(f"{Fore.YELLOW}[Warning]{Fore.RESET} Could not generate CFG visualization: {e}")

        # Variable Scope
        print("\nVariable Scope and Types:")
        for var, typ in scope_info.items():
            if var != 'int' and var != 'str':
                print(f"{var} : {typ}")

        # Parsing Tables
        print("\nGenerating parsing tables...")
        show_lalr_table()  # LALR table from PLY

        # LL(1) Table
        grammar = {
            'statement': [['ID', 'EQUALS', 'expression']],
            'expression': [
                ['term', 'expression_prime']
            ],
            'expression_prime': [
                ['PLUS', 'term', 'expression_prime'],
                ['MINUS', 'term', 'expression_prime'],
                ['ε']
            ],
            'term': [
                ['factor', 'term_prime']
            ],
            'term_prime': [
                ['MULTIPLY', 'factor', 'term_prime'],
                ['DIVIDE', 'factor', 'term_prime'],
                ['ε']
            ],
            'factor': [
                ['NUMBER'],
                ['ID'],
                ['STRING'],
                ['LPAREN', 'expression', 'RPAREN']
            ]
        }
        ll1 = LL1Parser(grammar)
        ll1.compute_first()
        ll1.compute_follow()
        ll1.build_table()
        ll1.visualize_table()

    except Exception as e:
        handle(e)

if __name__ == "__main__":
    main()