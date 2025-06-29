#!/usr/bin/env python3
"""
Example solution using Enhanced Utils Module.

This demonstrates how to use the new AdventSolution base class and
enhanced utilities for a clean, maintainable solution.
"""

import sys
from pathlib import Path

# Add utils to path
sys.path.append(str(Path(__file__).parent))
from utils import AdventSolution, InputParser, timer, quick_test


class ExampleSolution(AdventSolution):
    """Example solution demonstrating enhanced utils usage."""
    
    def __init__(self):
        super().__init__(2023, 99, "Enhanced Utils Example")
    
    def part1(self, input_data: str) -> int:
        """
        Example part 1: Sum all numbers in input.
        
        Args:
            input_data: Raw input data
            
        Returns:
            Sum of all numbers
        """
        parser = InputParser(input_data)
        numbers = parser.as_integers(skip_invalid=True)
        return sum(numbers)
    
    def part2(self, input_data: str) -> int:
        """
        Example part 2: Product of all numbers in input.
        
        Args:
            input_data: Raw input data
            
        Returns:
            Product of all numbers
        """
        parser = InputParser(input_data)
        numbers = parser.as_integers(skip_invalid=True)
        
        result = 1
        for num in numbers:
            result *= num
        return result
    
    @timer
    def solve_with_timing(self) -> dict:
        """Example of using timing decorator."""
        return self.run()
    
    def validate(self, expected_part1=None, expected_part2=None) -> bool:
        """Validate solution with test cases."""
        test_input = """1
2
3
4
5"""
        
        if expected_part1 is None:
            expected_part1 = 15  # 1+2+3+4+5
        if expected_part2 is None:
            expected_part2 = 120  # 1*2*3*4*5
        
        return super().validate(expected_part1, expected_part2)
    
    def run_comprehensive_tests(self):
        """Demonstrate comprehensive testing capabilities."""
        from utils import TestSuite
        
        # Create test suite
        suite = TestSuite(self.year, self.day)
        
        # Add test cases
        suite.add_test(
            name="basic_example",
            input_data="1\n2\n3",
            expected_part1=6,
            expected_part2=6,
            description="Basic sum and product test"
        )
        
        suite.add_test(
            name="single_number",
            input_data="42",
            expected_part1=42,
            expected_part2=42,
            description="Single number test"
        )
        
        suite.add_test(
            name="empty_input",
            input_data="",
            expected_part1=0,
            expected_part2=1,
            description="Empty input test"
        )
        
        # Run tests
        results = suite.run_tests(self.part1, self.part2)
        
        return all(r.passed for r in results)


def demonstrate_enhanced_features():
    """Demonstrate various enhanced features."""
    print("🚀 Enhanced Utils Module Demonstration")
    print("=" * 50)
    
    # Create solution instance
    solution = ExampleSolution()
    
    print("\n1. Basic solution execution:")
    results = solution.run(timing=True)
    print(f"Part 1: {results.get('part1', 'N/A')}")
    print(f"Part 2: {results.get('part2', 'N/A')}")
    
    print("\n2. Validation:")
    validation_passed = solution.validate()
    print(f"Validation: {'✅ PASSED' if validation_passed else '❌ FAILED'}")
    
    print("\n3. Comprehensive testing:")
    tests_passed = solution.run_comprehensive_tests()
    print(f"All tests: {'✅ PASSED' if tests_passed else '❌ FAILED'}")
    
    print("\n4. Benchmarking:")
    benchmark_stats = solution.benchmark(iterations=10)
    print("Benchmark results:")
    for key, value in benchmark_stats.items():
        print(f"  {key}: {value:.4f}s")
    
    print("\n5. InputParser demonstration:")
    demo_input = """1 2 3
4,5,6
grid:
abc
def
ghi"""
    
    parser = InputParser(demo_input)
    print(f"Lines: {parser.as_lines()}")
    print(f"All integers: {parser.extract_integers()}")
    print(f"Groups by blank lines: {parser.split_by_blank_lines()}")
    
    print("\n🎉 Demonstration complete!")


def main():
    """Main execution function."""
    if len(sys.argv) > 1 and sys.argv[1] == "--demo":
        demonstrate_enhanced_features()
    else:
        solution = ExampleSolution()
        solution.main()


if __name__ == "__main__":
    main()