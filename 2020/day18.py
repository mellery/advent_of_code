#!/usr/bin/env python3
"""
Advent of Code 2020 Day 18: Operation Order
https://adventofcode.com/2020/day/18

Enhanced solution using AdventSolution base class.
Expression parsing with different precedence rules.
"""

import sys
from pathlib import Path
from typing import Any, List, Dict, Optional, Tuple

# Add utils to path
sys.path.append(str(Path(__file__).parent.parent))
from utils import AdventSolution, InputParser


class Day18Solution(AdventSolution):
    """Solution for 2020 Day 18: Operation Order."""

    def __init__(self):
        super().__init__(2020, 18, "Operation Order")

    def solve_left_to_right(self, problem: str) -> int:
        """
        Solve expression with left-to-right evaluation (equal precedence).
        
        Args:
            problem: Mathematical expression as string
            
        Returns:
            Result of evaluation
        """
        values = problem.split(' ')
        ans = int(values[0])
        op = ''
        
        for v in values[1:]:
            if v.isdigit():
                n = int(v)
                if op == '+':
                    ans = ans + n
                elif op == '*':
                    ans = ans * n
            else:
                op = v
        
        return ans

    def solve_addition_first(self, problem: str) -> int:
        """
        Solve expression with addition having higher precedence than multiplication.
        
        Args:
            problem: Mathematical expression as string
            
        Returns:
            Result of evaluation
        """
        # First, handle all addition operations
        while '+' in problem:
            values = problem.split(' ')
            plus_idx = values.index('+')
            
            # Calculate the addition
            left_val = int(values[plus_idx - 1])
            right_val = int(values[plus_idx + 1])
            result = left_val + right_val
            
            # Replace the expression with the result
            old_expr = f"{values[plus_idx - 1]} + {values[plus_idx + 1]}"
            problem = problem.replace(old_expr, str(result), 1)
        
        # Now handle multiplication (left-to-right)
        return self.solve_left_to_right(problem)

    def solve_with_parentheses_part1(self, problem: str) -> int:
        """
        Solve expression with parentheses using part 1 rules.
        
        Args:
            problem: Mathematical expression with parentheses
            
        Returns:
            Result of evaluation
        """
        while '(' in problem:
            # Find innermost parentheses
            right_paren = problem.find(')')
            left_part = problem[:right_paren]
            left_paren = left_part.rfind('(')
            inner_expr = left_part[left_paren + 1:]
            
            # Solve the inner expression
            inner_result = self.solve_left_to_right(inner_expr)
            
            # Replace the parentheses expression with the result
            problem = problem.replace(f'({inner_expr})', str(inner_result))
        
        return self.solve_left_to_right(problem)

    def solve_with_parentheses_part2(self, problem: str) -> int:
        """
        Solve expression with parentheses using part 2 rules.
        
        Args:
            problem: Mathematical expression with parentheses
            
        Returns:
            Result of evaluation
        """
        while '(' in problem:
            # Find innermost parentheses
            right_paren = problem.find(')')
            left_part = problem[:right_paren]
            left_paren = left_part.rfind('(')
            inner_expr = left_part[left_paren + 1:]
            
            # Solve the inner expression with addition precedence
            inner_result = self.solve_addition_first(inner_expr)
            
            # Replace the parentheses expression with the result
            problem = problem.replace(f'({inner_expr})', str(inner_result))
        
        return self.solve_addition_first(problem)

    def part1(self, input_data: str) -> Any:
        """
        Solve part 1: evaluate expressions with equal precedence (left-to-right).
        
        Args:
            input_data: Raw input data as string
            
        Returns:
            Sum of all expression results
        """
        lines = input_data.strip().split('\n')
        total = 0
        
        for line in lines:
            expression = line.strip()
            result = self.solve_with_parentheses_part1(expression)
            total += result
        
        return total

    def part2(self, input_data: str) -> Any:
        """
        Solve part 2: evaluate expressions with addition precedence higher than multiplication.
        
        Args:
            input_data: Raw input data as string
            
        Returns:
            Sum of all expression results
        """
        lines = input_data.strip().split('\n')
        total = 0
        
        for line in lines:
            expression = line.strip()
            result = self.solve_with_parentheses_part2(expression)
            total += result
        
        return total

    def validate_examples(self):
        """Validate against known examples."""
        # Part 1 examples
        test_cases_p1 = [
            ('1 + 2 * 3 + 4 * 5 + 6', 71),
            ('1 + (2 * 3) + (4 * (5 + 6))', 51),
            ('2 * 3 + (4 * 5)', 26),
            ('5 + (8 * 3 + 9 + 3 * 4 * 3)', 437),
            ('5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))', 12240),
            ('((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2', 13632)
        ]
        
        print("Part 1 validation:")
        for expr, expected in test_cases_p1:
            result = self.solve_with_parentheses_part1(expr)
            status = "✓" if result == expected else "✗"
            print(f"  {status} {expr} = {result} (expected {expected})")
        
        # Part 2 examples
        test_cases_p2 = [
            ('1 + 2 * 3 + 4 * 5 + 6', 231),
            ('1 + (2 * 3) + (4 * (5 + 6))', 51),
            ('2 * 3 + (4 * 5)', 46),
            ('5 + (8 * 3 + 9 + 3 * 4 * 3)', 1445),
            ('5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))', 669060),
            ('((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2', 23340)
        ]
        
        print("\nPart 2 validation:")
        for expr, expected in test_cases_p2:
            result = self.solve_with_parentheses_part2(expr)
            status = "✓" if result == expected else "✗"
            print(f"  {status} {expr} = {result} (expected {expected})")


def main():
    """Main execution function."""
    solution = Day18Solution()
    
    # Uncomment to run validation
    # solution.validate_examples()
    
    solution.main()


if __name__ == "__main__":
    main()