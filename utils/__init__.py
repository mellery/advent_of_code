"""
Enhanced utils module for Advent of Code solutions.

This module provides a comprehensive set of utilities for creating, testing,
and optimizing Advent of Code solutions.

Key Components:
- AdventSolution: Base class for structured solutions
- InputParser: Advanced input parsing capabilities
- Performance utilities: Timing, profiling, and benchmarking
- Testing framework: Comprehensive test suite support

Example Usage:
    # Using the base class
    from utils import AdventSolution
    
    class Day1Solution(AdventSolution):
        def __init__(self):
            super().__init__(2023, 1, "Trebuchet?!")
        
        def part1(self, input_data: str) -> int:
            # Your solution here
            pass
        
        def part2(self, input_data: str) -> int:
            # Your solution here
            pass
    
    # Using input parsing
    from utils import InputParser
    
    parser = InputParser.from_file("day1_input.txt")
    numbers = parser.as_integers()
    grid = parser.as_grid()
    
    # Using performance monitoring
    from utils import timer, benchmark
    
    @timer
    def my_function():
        # Function will be automatically timed
        pass
"""

# Core components
from .advent_base import AdventSolution
from .input_parsing import (
    InputParser,
    get_lines, get_integers, get_grid, get_digit_grid,
    extract_all_integers, split_by_blank_lines, parse_coordinate_pairs,
    get_list_of_numbers  # Legacy compatibility
)
from .timing import (
    PerformanceProfiler, TimingResult, BenchmarkStats,
    timer, benchmark, time_block, measure_memory_usage,
    profile_solution, print_performance_report,
    get_profiler, clear_profiler, print_profiler_summary
)
from .testing import (
    TestCase, TestResult, TestSuite, TestStatus, ValidationHelper,
    quick_test, test_with_examples
)
from .ascii_art_parser import (
    AsciiArtParser, parse_ascii_letters
)

# Algorithm libraries for reusable components
try:
    from .algorithms import (
        pathfinding, grid, vm, parsing, math_utils
    )
    from .algorithms.pathfinding import (
        dijkstra_grid, bfs_shortest_path, a_star_search, find_path
    )
    from .algorithms.grid import (
        Grid, Direction, parse_grid, neighbors_4, neighbors_8,
        manhattan_distance, euclidean_distance
    )
    from .algorithms.vm import (
        IntcodeVM, SimpleAssemblyVM, run_intcode_program
    )
    from .algorithms.parsing import (
        ExpressionEvaluator, PatternMatcher, parse_numbers,
        parse_coordinate_pairs as algo_parse_coords, extract_patterns
    )
    from .algorithms.math_utils import (
        gcd, lcm, is_prime, prime_factors, fibonacci,
        manhattan_distance as math_manhattan_distance
    )
    ALGORITHMS_AVAILABLE = True
except ImportError:
    ALGORITHMS_AVAILABLE = False

# Legacy compatibility - import from original utils.py
import sys
from pathlib import Path

# Add parent directory to path to import original utils
parent_dir = Path(__file__).parent.parent
if str(parent_dir) not in sys.path:
    sys.path.insert(0, str(parent_dir))

try:
    from utils import (
        get_digit, timing_decorator, setup_day_args, find_input_file,
        validate_solution, run_solution
    )
except ImportError:
    # If original utils.py doesn't exist or has import issues, define fallbacks
    def get_digit(number: int, n: int) -> int:
        """Get the nth digit from the right of a number (0-indexed)."""
        return number // 10**n % 10
    
    timing_decorator = timer  # Use new timer decorator
    
    def setup_day_args(*args, **kwargs):
        """Legacy function - use AdventSolution.setup_args() instead."""
        raise NotImplementedError("Use AdventSolution.setup_args() instead")
    
    def find_input_file(*args, **kwargs):
        """Legacy function - use AdventSolution input discovery instead."""
        raise NotImplementedError("Use AdventSolution input discovery instead")
    
    def validate_solution(*args, **kwargs):
        """Legacy function - use TestSuite or ValidationHelper instead."""
        return ValidationHelper.validate_solution(*args, **kwargs)
    
    def run_solution(*args, **kwargs):
        """Legacy function - use AdventSolution.run() instead."""
        raise NotImplementedError("Use AdventSolution.run() instead")


# Version information
__version__ = "2.0.0"
__author__ = "Advent of Code Utils"

# Public API
__all__ = [
    # Core classes
    'AdventSolution',
    'InputParser',
    'PerformanceProfiler',
    'TestSuite',
    'TestCase',
    'TestResult',
    'ValidationHelper',
    
    # Input parsing functions
    'get_lines',
    'get_integers', 
    'get_grid',
    'get_digit_grid',
    'extract_all_integers',
    'split_by_blank_lines',
    'parse_coordinate_pairs',
    'get_list_of_numbers',  # Legacy
    
    # Performance utilities
    'timer',
    'benchmark',
    'time_block',
    'measure_memory_usage',
    'profile_solution',
    'print_performance_report',
    'get_profiler',
    'clear_profiler',
    'print_profiler_summary',
    
    # Testing utilities
    'quick_test',
    'test_with_examples',
    'TestStatus',
    'TimingResult',
    'BenchmarkStats',
    
    # ASCII Art Parsing
    'AsciiArtParser',
    'parse_ascii_letters',
    
    # Legacy compatibility
    'get_digit',
    'timing_decorator',
    'setup_day_args',
    'find_input_file', 
    'validate_solution',
    'run_solution'
]

# Add algorithm library components if available
if ALGORITHMS_AVAILABLE:
    __all__.extend([
        # Algorithm modules
        'pathfinding',
        'grid',
        'vm',
        'parsing',
        'math_utils',
        
        # Pathfinding algorithms
        'dijkstra_grid',
        'bfs_shortest_path', 
        'a_star_search',
        'find_path',
        
        # Grid utilities
        'Grid',
        'Direction',
        'parse_grid',
        'neighbors_4',
        'neighbors_8',
        'manhattan_distance',
        'euclidean_distance',
        
        # Virtual machine components
        'IntcodeVM',
        'SimpleAssemblyVM',
        'run_intcode_program',
        
        # Parsing utilities
        'ExpressionEvaluator',
        'PatternMatcher',
        'parse_numbers',
        'extract_patterns',
        
        # Mathematical utilities
        'gcd',
        'lcm',
        'is_prime',
        'prime_factors',
        'fibonacci',
        'math_manhattan_distance'
    ])


def create_solution_template(year: int, day: int, title: str = "") -> str:
    """
    Generate a template for a new solution using the enhanced utilities.
    
    Args:
        year: Year of the challenge
        day: Day number
        title: Optional title for the challenge
        
    Returns:
        String containing the complete solution template
    """
    template = f'''#!/usr/bin/env python3
"""
Advent of Code {year} Day {day}{": " + title if title else ""}

{title}
"""

import sys
from pathlib import Path

# Add utils to path
sys.path.append(str(Path(__file__).parent.parent))
from utils import AdventSolution, InputParser
# Optional: Import algorithm libraries for advanced problems
# from utils import Grid, dijkstra_grid, IntcodeVM, gcd, fibonacci


class Day{day}Solution(AdventSolution):
    """Solution for {year} Day {day}."""
    
    def __init__(self):
        super().__init__({year}, {day}, "{title}")
    
    def part1(self, input_data: str) -> int:
        """
        Solve part 1 of the puzzle.
        
        Args:
            input_data: Raw input data
            
        Returns:
            Solution for part 1
        """
        parser = InputParser(input_data)
        lines = parser.as_lines()
        
        # TODO: Implement part 1 solution
        return 0
    
    def part2(self, input_data: str) -> int:
        """
        Solve part 2 of the puzzle.
        
        Args:
            input_data: Raw input data
            
        Returns:
            Solution for part 2
        """
        parser = InputParser(input_data)
        lines = parser.as_lines()
        
        # TODO: Implement part 2 solution
        return 0
    
    def validate(self, expected_part1=None, expected_part2=None) -> bool:
        """
        Validate solution with test cases.
        
        Override this method to provide test validation.
        """
        # Example test case
        test_input = ""\"
        # TODO: Add test input here
        ""\"
        
        if expected_part1 is None:
            expected_part1 = None  # TODO: Add expected result
        if expected_part2 is None:
            expected_part2 = None  # TODO: Add expected result
        
        return super().validate(expected_part1, expected_part2)


def main():
    """Main execution function."""
    solution = Day{day}Solution()
    solution.main()


if __name__ == "__main__":
    main()
'''
    return template


def migration_guide() -> str:
    """
    Provide a guide for migrating from legacy utils to enhanced utils.
    
    Returns:
        String containing migration instructions
    """
    return """
=== Migration Guide: Legacy Utils → Enhanced Utils ===

OLD WAY (Legacy):
    from utils import get_list_of_numbers, run_solution
    
    def part1(filename):
        numbers = get_list_of_numbers(filename)
        return sum(numbers)
    
    def part2(filename):
        numbers = get_list_of_numbers(filename)
        return max(numbers)
    
    if __name__ == "__main__":
        run_solution(part1, part2, "day1_input.txt")

NEW WAY (Enhanced):
    from utils import AdventSolution, InputParser
    
    class Day1Solution(AdventSolution):
        def __init__(self):
            super().__init__(2023, 1, "Example Challenge")
        
        def part1(self, input_data: str) -> int:
            parser = InputParser(input_data)
            numbers = parser.as_integers()
            return sum(numbers)
        
        def part2(self, input_data: str) -> int:
            parser = InputParser(input_data)
            numbers = parser.as_integers()
            return max(numbers)
    
    if __name__ == "__main__":
        solution = Day1Solution()
        solution.main()

BENEFITS:
✅ Automatic input file discovery
✅ Built-in timing and benchmarking
✅ Comprehensive testing framework
✅ Better error handling
✅ Command-line argument parsing
✅ Performance profiling
✅ Validation capabilities

MIGRATION STEPS:
1. Replace function-based solutions with class-based solutions
2. Use InputParser instead of direct file reading
3. Update part1/part2 signatures to accept input_data string
4. Use solution.main() instead of run_solution()
5. Add validation and testing as needed
"""


# Print helpful information when module is imported
def _on_import():
    """Print helpful information about the enhanced utils."""
    import os
    
    # Only print if not in test mode or if explicitly requested
    if os.getenv('ADVENT_UTILS_QUIET') != '1':
        pass  # Could add helpful startup message here


_on_import()