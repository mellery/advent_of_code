#!/usr/bin/env python3
"""
Advent of Code 2020 Day 18: Operation Order
Enhanced solution with object-oriented design and comprehensive analysis.
"""

import sys
import os
from typing import Dict, List, Tuple, Optional, Set, Any
from dataclasses import dataclass
from collections import deque
import time
import re

# Add project root to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.advent_base import AdventSolution


@dataclass
class Token:
    """Represents a token in a mathematical expression."""
    type: str  # 'number', 'operator', 'lparen', 'rparen'
    value: str
    position: int
    
    def __str__(self) -> str:
        return f"{self.type}({self.value})"


@dataclass
class ExpressionResult:
    """Represents the result of evaluating an expression."""
    value: int
    steps: List[str]
    original: str
    
    def __str__(self) -> str:
        return f"{self.original} = {self.value}"


class ExpressionTokenizer:
    """
    Advanced tokenizer for mathematical expressions.
    
    This class provides efficient tokenization of mathematical expressions
    containing numbers, operators, and parentheses.
    """
    
    def __init__(self):
        self.tokens: List[Token] = []
        self.position = 0
    
    def tokenize(self, expression: str) -> List[Token]:
        """
        Tokenize a mathematical expression.
        
        Args:
            expression: Mathematical expression as string
            
        Returns:
            List of tokens representing the expression
        """
        self.tokens = []
        self.position = 0
        
        # Remove all whitespace for easier parsing
        cleaned = expression.replace(' ', '')
        
        i = 0
        while i < len(cleaned):
            char = cleaned[i]
            
            if char.isdigit():
                # Parse multi-digit numbers
                num_str = ''
                while i < len(cleaned) and cleaned[i].isdigit():
                    num_str += cleaned[i]
                    i += 1
                self.tokens.append(Token('number', num_str, len(self.tokens)))
                continue
            elif char in ['+', '*']:
                self.tokens.append(Token('operator', char, len(self.tokens)))
            elif char == '(':
                self.tokens.append(Token('lparen', char, len(self.tokens)))
            elif char == ')':
                self.tokens.append(Token('rparen', char, len(self.tokens)))
            
            i += 1
        
        return self.tokens


class ExpressionEvaluator:
    """
    Advanced expression evaluator with configurable precedence rules.
    
    This class provides efficient evaluation of mathematical expressions
    with different operator precedence rules and comprehensive analysis.
    """
    
    def __init__(self):
        self.tokenizer = ExpressionTokenizer()
        self.evaluation_steps: List[str] = []
    
    def evaluate_left_to_right(self, tokens: List[Token]) -> int:
        """
        Evaluate tokens with left-to-right precedence (equal precedence).
        
        Args:
            tokens: List of tokens to evaluate
            
        Returns:
            Result of evaluation
        """
        if not tokens:
            return 0
        
        # Start with first number
        result = int(tokens[0].value)
        i = 1
        
        while i < len(tokens):
            if i + 1 < len(tokens):
                operator = tokens[i].value
                operand = int(tokens[i + 1].value)
                
                if operator == '+':
                    result += operand
                elif operator == '*':
                    result *= operand
                
                self.evaluation_steps.append(f"  {result} (after {operator} {operand})")
                i += 2
            else:
                break
        
        return result
    
    def evaluate_addition_first(self, tokens: List[Token]) -> int:
        """
        Evaluate tokens with addition having higher precedence.
        
        Args:
            tokens: List of tokens to evaluate
            
        Returns:
            Result of evaluation
        """
        if not tokens:
            return 0
        
        # Create a working copy
        working_tokens = tokens.copy()
        
        # First pass: handle all additions
        i = 0
        while i < len(working_tokens):
            if (i + 2 < len(working_tokens) and 
                working_tokens[i + 1].type == 'operator' and 
                working_tokens[i + 1].value == '+'):
                
                left_val = int(working_tokens[i].value)
                right_val = int(working_tokens[i + 2].value)
                result = left_val + right_val
                
                self.evaluation_steps.append(f"  {left_val} + {right_val} = {result}")
                
                # Replace the three tokens with one result token
                new_token = Token('number', str(result), working_tokens[i].position)
                working_tokens = working_tokens[:i] + [new_token] + working_tokens[i + 3:]
            else:
                i += 1
        
        # Second pass: handle multiplications left-to-right
        return self.evaluate_left_to_right(working_tokens)
    
    def find_innermost_parentheses(self, tokens: List[Token]) -> Tuple[int, int]:
        """
        Find the innermost parentheses in the token list.
        
        Args:
            tokens: List of tokens to search
            
        Returns:
            Tuple of (start_index, end_index) or (-1, -1) if no parentheses
        """
        depth = 0
        start = -1
        
        for i, token in enumerate(tokens):
            if token.type == 'lparen':
                if depth == 0:
                    start = i
                depth += 1
            elif token.type == 'rparen':
                depth -= 1
                if depth == 0 and start != -1:
                    return start, i
        
        return -1, -1
    
    def evaluate_with_parentheses(self, expression: str, addition_precedence: bool = False) -> ExpressionResult:
        """
        Evaluate expression with parentheses support.
        
        Args:
            expression: Mathematical expression string
            addition_precedence: Whether addition has higher precedence than multiplication
            
        Returns:
            ExpressionResult containing value and evaluation steps
        """
        self.evaluation_steps = []
        self.evaluation_steps.append(f"Evaluating: {expression}")
        
        tokens = self.tokenizer.tokenize(expression)
        
        # Handle parentheses by finding innermost and evaluating
        while any(token.type in ['lparen', 'rparen'] for token in tokens):
            start, end = self.find_innermost_parentheses(tokens)
            
            if start == -1:
                break
            
            # Extract tokens inside parentheses
            inner_tokens = tokens[start + 1:end]
            
            # Evaluate the inner expression
            if addition_precedence:
                inner_result = self.evaluate_addition_first(inner_tokens)
            else:
                inner_result = self.evaluate_left_to_right(inner_tokens)
            
            # Replace parentheses group with result
            result_token = Token('number', str(inner_result), start)
            tokens = tokens[:start] + [result_token] + tokens[end + 1:]
            
            self.evaluation_steps.append(f"  Parentheses resolved: {inner_result}")
        
        # Evaluate remaining tokens
        if addition_precedence:
            final_result = self.evaluate_addition_first(tokens)
        else:
            final_result = self.evaluate_left_to_right(tokens)
        
        return ExpressionResult(
            value=final_result,
            steps=self.evaluation_steps.copy(),
            original=expression
        )
    
    def get_evaluation_statistics(self, expressions: List[str], addition_precedence: bool = False) -> Dict[str, any]:
        """
        Get comprehensive statistics about expression evaluation.
        
        Args:
            expressions: List of expressions to analyze
            addition_precedence: Whether to use addition precedence
            
        Returns:
            Dictionary containing evaluation statistics
        """
        results = []
        total_steps = 0
        
        for expr in expressions:
            result = self.evaluate_with_parentheses(expr, addition_precedence)
            results.append(result)
            total_steps += len(result.steps)
        
        values = [r.value for r in results]
        
        return {
            'total_expressions': len(expressions),
            'sum_of_results': sum(values),
            'min_result': min(values) if values else 0,
            'max_result': max(values) if values else 0,
            'avg_result': sum(values) / len(values) if values else 0,
            'total_evaluation_steps': total_steps,
            'avg_steps_per_expression': total_steps / len(expressions) if expressions else 0,
            'precedence_mode': 'addition_first' if addition_precedence else 'left_to_right'
        }


class Day18Solution(AdventSolution):
    """Enhanced solution for Advent of Code 2020 Day 18: Operation Order."""
    
    def __init__(self):
        super().__init__(year=2020, day=18, title="Operation Order")
    
    def part1(self, input_data: str) -> int:
        """
        Evaluate expressions with equal precedence (left-to-right).
        
        Args:
            input_data: Mathematical expressions, one per line
            
        Returns:
            Sum of all expression results
        """
        expressions = [line.strip() for line in input_data.strip().split('\n')]
        evaluator = ExpressionEvaluator()
        
        total = 0
        for expression in expressions:
            result = evaluator.evaluate_with_parentheses(expression, addition_precedence=False)
            total += result.value
        
        return total
    
    def part2(self, input_data: str) -> int:
        """
        Evaluate expressions with addition precedence higher than multiplication.
        
        Args:
            input_data: Mathematical expressions, one per line
            
        Returns:
            Sum of all expression results
        """
        expressions = [line.strip() for line in input_data.strip().split('\n')]
        evaluator = ExpressionEvaluator()
        
        total = 0
        for expression in expressions:
            result = evaluator.evaluate_with_parentheses(expression, addition_precedence=True)
            total += result.value
        
        return total
    
    def analyze(self, input_data: str) -> None:
        """
        Provide comprehensive analysis of expression evaluation.
        
        Args:
            input_data: Mathematical expressions, one per line
        """
        expressions = [line.strip() for line in input_data.strip().split('\n')]
        evaluator = ExpressionEvaluator()
        
        print("=== Operation Order Analysis ===\n")
        
        print(f"Input Statistics:")
        print(f"  Total expressions: {len(expressions)}")
        print(f"  Average expression length: {sum(len(e) for e in expressions) / len(expressions):.1f} characters")
        print(f"  Expressions with parentheses: {sum(1 for e in expressions if '(' in e)}")
        print(f"  Expressions with only addition: {sum(1 for e in expressions if '+' in e and '*' not in e)}")
        print(f"  Expressions with only multiplication: {sum(1 for e in expressions if '*' in e and '+' not in e)}")
        print(f"  Mixed operation expressions: {sum(1 for e in expressions if '+' in e and '*' in e)}")
        
        # Part 1 analysis
        print(f"\nPart 1 Analysis (left-to-right precedence):")
        start_time = time.time()
        stats1 = evaluator.get_evaluation_statistics(expressions, addition_precedence=False)
        part1_result = stats1['sum_of_results']
        time1 = time.time() - start_time
        
        print(f"  Sum of results: {part1_result}")
        print(f"  Min result: {stats1['min_result']}")
        print(f"  Max result: {stats1['max_result']}")
        print(f"  Average result: {stats1['avg_result']:.2f}")
        print(f"  Total evaluation steps: {stats1['total_evaluation_steps']}")
        print(f"  Average steps per expression: {stats1['avg_steps_per_expression']:.2f}")
        print(f"  Evaluation time: {time1:.4f} seconds")
        
        # Part 2 analysis
        print(f"\nPart 2 Analysis (addition precedence):")
        start_time = time.time()
        stats2 = evaluator.get_evaluation_statistics(expressions, addition_precedence=True)
        part2_result = stats2['sum_of_results']
        time2 = time.time() - start_time
        
        print(f"  Sum of results: {part2_result}")
        print(f"  Min result: {stats2['min_result']}")
        print(f"  Max result: {stats2['max_result']}")
        print(f"  Average result: {stats2['avg_result']:.2f}")
        print(f"  Total evaluation steps: {stats2['total_evaluation_steps']}")
        print(f"  Average steps per expression: {stats2['avg_steps_per_expression']:.2f}")
        print(f"  Evaluation time: {time2:.4f} seconds")
        
        # Comparison analysis
        print(f"\nPrecedence Comparison:")
        if part1_result != 0:
            ratio = part2_result / part1_result
            print(f"  Part 2 vs Part 1 result ratio: {ratio:.2f}")
        
        step_ratio = stats2['avg_steps_per_expression'] / stats1['avg_steps_per_expression']
        print(f"  Part 2 vs Part 1 step complexity ratio: {step_ratio:.2f}")
        
        time_ratio = time2 / time1 if time1 > 0 else 1
        print(f"  Part 2 vs Part 1 time ratio: {time_ratio:.2f}")
        
        # Example evaluations
        print(f"\nExample Evaluations:")
        if expressions:
            # Show detailed evaluation of first few expressions
            for i, expr in enumerate(expressions[:3]):
                print(f"\n  Expression {i+1}: {expr}")
                
                # Part 1 evaluation
                result1 = evaluator.evaluate_with_parentheses(expr, addition_precedence=False)
                print(f"    Part 1 result: {result1.value}")
                
                # Part 2 evaluation
                result2 = evaluator.evaluate_with_parentheses(expr, addition_precedence=True)
                print(f"    Part 2 result: {result2.value}")
                
                if result1.value != result2.value:
                    print(f"    Difference: {abs(result2.value - result1.value)}")
        
        # Validation with known examples
        print(f"\nValidation with Known Examples:")
        test_cases = [
            ('1 + 2 * 3 + 4 * 5 + 6', 71, 231),
            ('1 + (2 * 3) + (4 * (5 + 6))', 51, 51),
            ('2 * 3 + (4 * 5)', 26, 46),
            ('5 + (8 * 3 + 9 + 3 * 4 * 3)', 437, 1445),
            ('5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))', 12240, 669060),
            ('((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2', 13632, 23340)
        ]
        
        for expr, expected1, expected2 in test_cases:
            result1 = evaluator.evaluate_with_parentheses(expr, addition_precedence=False)
            result2 = evaluator.evaluate_with_parentheses(expr, addition_precedence=True)
            
            status1 = "✓" if result1.value == expected1 else "✗"
            status2 = "✓" if result2.value == expected2 else "✗"
            
            print(f"  {expr}")
            print(f"    Part 1: {status1} {result1.value} (expected {expected1})")
            print(f"    Part 2: {status2} {result2.value} (expected {expected2})")
        
        print(f"\nResults:")
        print(f"  Part 1: {part1_result}")
        print(f"  Part 2: {part2_result}")


# Legacy functions for test runner compatibility
def part1(filename: str) -> int:
    """Legacy part1 function for test runner compatibility."""
    try:
        with open(filename, 'r') as f:
            input_data = f.read()
    except FileNotFoundError:
        return -1
    
    solution = Day18Solution()
    return solution.part1(input_data)


def part2(filename: str) -> int:
    """Legacy part2 function for test runner compatibility."""
    try:
        with open(filename, 'r') as f:
            input_data = f.read()
    except FileNotFoundError:
        return -1
    
    solution = Day18Solution()
    return solution.part2(input_data)


if __name__ == "__main__":
    solution = Day18Solution()
    solution.main()