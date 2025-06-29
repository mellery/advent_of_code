#!/usr/bin/env python3
"""
Test compatibility of enhanced utils with existing solution patterns.
"""

import sys
from pathlib import Path

# Add utils to path
sys.path.append(str(Path(__file__).parent))
from utils import AdventSolution, InputParser, timer, quick_test


class CompatibilityTestSolution(AdventSolution):
    """Test solution to verify enhanced utils compatibility."""
    
    def __init__(self):
        super().__init__(2023, 98, "Compatibility Test")
    
    def part1(self, input_data: str) -> int:
        """Test basic input parsing."""
        parser = InputParser(input_data)
        numbers = parser.extract_integers()
        return sum(numbers)
    
    def part2(self, input_data: str) -> int:
        """Test grid parsing."""
        parser = InputParser(input_data)
        lines = parser.as_lines()
        return len(lines)
    
    @timer
    def solve_with_timing(self) -> dict:
        """Test timing decorator."""
        return self.run()


def test_legacy_functions():
    """Test that legacy functions still work."""
    print("Testing legacy compatibility...")
    
    # Test InputParser backwards compatibility
    test_input = "123\n456\n789"
    parser = InputParser(test_input)
    
    # Test that new methods work
    assert parser.as_integers() == [123, 456, 789]
    assert len(parser.as_lines()) == 3
    assert parser.extract_integers() == [123, 456, 789]
    
    print("✅ Legacy compatibility verified")


def main():
    """Test enhanced utils compatibility."""
    print("🧪 Enhanced Utils Compatibility Test")
    print("=" * 50)
    
    # Test legacy functions
    test_legacy_functions()
    
    # Create test data
    test_data = """100 200 300
400,500,600
abc
def
ghi"""
    
    with open("day98_input.txt", "w") as f:
        f.write(test_data)
    
    # Test solution
    solution = CompatibilityTestSolution()
    
    print("\n1. Testing basic execution:")
    results = solution.run()
    print(f"Part 1: {results['part1']}")  # Should be 2100 (sum of all numbers)
    print(f"Part 2: {results['part2']}")  # Should be 5 (number of lines)
    
    print("\n2. Testing validation:")
    validation_passed = quick_test(
        solution.part1, 
        solution.part2,
        test_data,
        2100,  # Expected part 1
        5      # Expected part 2
    )
    print(f"Quick validation: {'✅ PASSED' if validation_passed else '❌ FAILED'}")
    
    print("\n3. Testing timing:")
    timed_results = solution.solve_with_timing()
    
    print("\n🎉 Compatibility test complete!")
    
    # Cleanup
    import os
    os.remove("day98_input.txt")


if __name__ == "__main__":
    main()