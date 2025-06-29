"""
Shared utilities for Advent of Code solutions.

This module provides common functions used across multiple solutions
to reduce code duplication and improve maintainability.

ENHANCED VERSION: This module now integrates with the enhanced utils
package while maintaining full backward compatibility.
"""

from typing import List, Union, Optional, Any, Callable
import time
import argparse
import os
from pathlib import Path

# Import enhanced utilities if available
try:
    # Try importing from the utils package subdirectory
    import sys
    from pathlib import Path
    utils_dir = Path(__file__).parent / 'utils'
    if utils_dir.exists():
        sys.path.insert(0, str(Path(__file__).parent))
        from utils.advent_base import AdventSolution
        from utils.input_parsing import InputParser
        from utils.timing import timer
        from utils.testing import quick_test
        ENHANCED_UTILS_AVAILABLE = True
    else:
        ENHANCED_UTILS_AVAILABLE = False
except ImportError:
    ENHANCED_UTILS_AVAILABLE = False


def get_list_of_numbers(filename: str) -> List[int]:
    """
    Read a file and return a list of integers, one per line.
    
    Args:
        filename: Path to the input file
        
    Returns:
        List of integers from the file
        
    Raises:
        FileNotFoundError: If the file doesn't exist
        ValueError: If a line can't be converted to an integer
    """
    try:
        with open(filename, 'r') as f:
            return [int(line.strip()) for line in f if line.strip()]
    except FileNotFoundError:
        raise FileNotFoundError(f"Input file '{filename}' not found")
    except ValueError as e:
        raise ValueError(f"Invalid number format in file '{filename}': {e}")


def get_lines(filename: str, strip_whitespace: bool = True) -> List[str]:
    """
    Read a file and return a list of lines.
    
    Args:
        filename: Path to the input file
        strip_whitespace: Whether to strip whitespace from each line
        
    Returns:
        List of strings, one per line
        
    Raises:
        FileNotFoundError: If the file doesn't exist
    """
    try:
        with open(filename, 'r') as f:
            lines = f.readlines()
            if strip_whitespace:
                return [line.strip() for line in lines]
            return lines
    except FileNotFoundError:
        raise FileNotFoundError(f"Input file '{filename}' not found")


def get_grid(filename: str) -> List[List[str]]:
    """
    Read a file and return a 2D grid of characters.
    
    Args:
        filename: Path to the input file
        
    Returns:
        2D list representing the grid
        
    Raises:
        FileNotFoundError: If the file doesn't exist
    """
    lines = get_lines(filename)
    return [list(line) for line in lines if line]


def get_digit(number: int, n: int) -> int:
    """
    Get the nth digit from the right of a number (0-indexed).
    
    Args:
        number: The number to extract from
        n: Position from right (0 = rightmost)
        
    Returns:
        The digit at position n
        
    Example:
        get_digit(12345, 0) returns 5
        get_digit(12345, 2) returns 3
    """
    return number // 10**n % 10


def timing_decorator(func: Callable) -> Callable:
    """
    Decorator to time function execution.
    
    Args:
        func: Function to time
        
    Returns:
        Wrapped function that prints execution time
    """
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"{func.__name__} executed in {end_time - start_time:.4f} seconds")
        return result
    return wrapper


def setup_day_args(day: str, year: Optional[str] = None) -> argparse.Namespace:
    """
    Set up command line arguments for a day's solution.
    
    Args:
        day: Day number (e.g., "1", "12")
        year: Year directory (optional, inferred from current directory if not provided)
        
    Returns:
        Parsed arguments namespace
    """
    parser = argparse.ArgumentParser(description=f'Advent of Code Day {day} Solution')
    
    # If year not provided, try to infer from current directory
    if year is None:
        current_dir = Path.cwd().name
        if current_dir.isdigit() and len(current_dir) == 4:
            year = current_dir
        else:
            year = "unknown"
    
    parser.add_argument(
        '--input', '-i',
        default=f'day{day}_input.txt',
        help=f'Input file (default: day{day}_input.txt)'
    )
    parser.add_argument(
        '--test', '-t',
        default=f'day{day}_test.txt',
        help=f'Test input file (default: day{day}_test.txt)'
    )
    parser.add_argument(
        '--use-test',
        action='store_true',
        help='Use test input instead of real input'
    )
    parser.add_argument(
        '--part',
        type=int,
        choices=[1, 2],
        help='Run only specific part (1 or 2)'
    )
    parser.add_argument(
        '--time',
        action='store_true',
        help='Show execution time'
    )
    
    return parser.parse_args()


def find_input_file(day: str, year: Optional[str] = None, 
                   patterns: Optional[List[str]] = None) -> Optional[str]:
    """
    Find the input file for a given day, trying multiple naming patterns.
    
    Args:
        day: Day number
        year: Year (optional)
        patterns: Custom patterns to try (optional)
        
    Returns:
        Path to the input file if found, None otherwise
    """
    if patterns is None:
        patterns = [
            f'day{day}_input.txt',
            f'day{day}input.txt', 
            f'input{day}.txt',
            f'day{day}.txt',
            f'part1.txt'  # Some solutions use this
        ]
    
    for pattern in patterns:
        if os.path.exists(pattern):
            return pattern
            
    return None


def validate_solution(part1_func: Callable, part2_func: Callable,
                     test_input: str, expected_part1: Any = None, 
                     expected_part2: Any = None) -> bool:
    """
    Validate solution against expected results.
    
    Args:
        part1_func: Function for part 1
        part2_func: Function for part 2  
        test_input: Test input file path
        expected_part1: Expected result for part 1
        expected_part2: Expected result for part 2
        
    Returns:
        True if all provided expected results match
    """
    success = True
    
    if expected_part1 is not None:
        result1 = part1_func(test_input)
        if result1 != expected_part1:
            print(f"Part 1 test failed: expected {expected_part1}, got {result1}")
            success = False
        else:
            print(f"Part 1 test passed: {result1}")
    
    if expected_part2 is not None:
        result2 = part2_func(test_input)
        if result2 != expected_part2:
            print(f"Part 2 test failed: expected {expected_part2}, got {result2}")
            success = False
        else:
            print(f"Part 2 test passed: {result2}")
            
    return success


def run_solution(part1_func: Callable, part2_func: Callable, 
                input_file: str, args: Optional[argparse.Namespace] = None) -> None:
    """
    Run the solution with proper timing and output formatting.
    
    Args:
        part1_func: Function for part 1
        part2_func: Function for part 2
        input_file: Input file path
        args: Parsed command line arguments (optional)
    """
    if args and args.time:
        part1_func = timing_decorator(part1_func)
        part2_func = timing_decorator(part2_func)
    
    if args is None or args.part is None or args.part == 1:
        print("Part 1:")
        result1 = part1_func(input_file)
        print(f"Result: {result1}")
        print()
    
    if args is None or args.part is None or args.part == 2:
        print("Part 2:")
        result2 = part2_func(input_file)
        print(f"Result: {result2}")


# Enhanced utilities integration
def get_enhanced_parser(input_data: str):
    """
    Get an enhanced InputParser if available, otherwise use basic parsing.
    
    Args:
        input_data: Input data as string
        
    Returns:
        InputParser instance if enhanced utils available, None otherwise
    """
    if ENHANCED_UTILS_AVAILABLE:
        return InputParser(input_data)
    return None


def create_enhanced_solution(year: int, day: int, title: str = ""):
    """
    Create an enhanced AdventSolution if available.
    
    Args:
        year: Year of the challenge
        day: Day number  
        title: Optional title
        
    Returns:
        AdventSolution instance if enhanced utils available, None otherwise
    """
    if ENHANCED_UTILS_AVAILABLE:
        return AdventSolution(year, day, title)
    return None


def enhanced_validate_solution(part1_func: Callable, part2_func: Callable,
                              test_input: str, expected_part1: Any = None,
                              expected_part2: Any = None) -> bool:
    """
    Use enhanced validation if available, otherwise fallback to legacy.
    
    Args:
        part1_func: Part 1 function
        part2_func: Part 2 function
        test_input: Test input data
        expected_part1: Expected part 1 result
        expected_part2: Expected part 2 result
        
    Returns:
        True if validation passes
    """
    if ENHANCED_UTILS_AVAILABLE:
        return quick_test(part1_func, part2_func, test_input, expected_part1, expected_part2)
    else:
        return validate_solution(part1_func, part2_func, test_input, expected_part1, expected_part2)


def enhanced_timer(func: Callable) -> Callable:
    """
    Use enhanced timer if available, otherwise fallback to legacy.
    
    Args:
        func: Function to time
        
    Returns:
        Wrapped function with timing
    """
    if ENHANCED_UTILS_AVAILABLE:
        return timer(func)
    else:
        return timing_decorator(func)


# Migration helper functions
def suggest_enhanced_migration(solution_file: str):
    """
    Print suggestions for migrating to enhanced utils.
    
    Args:
        solution_file: Path to the solution file being analyzed
    """
    if not ENHANCED_UTILS_AVAILABLE:
        print("Enhanced utils package not available.")
        return
        
    print(f"\n🔄 Enhanced Utils Migration Suggestions for {solution_file}:")
    print("=" * 60)
    print("1. Replace function-based approach with class-based AdventSolution")
    print("2. Use InputParser for flexible input handling")
    print("3. Add comprehensive testing with TestSuite")
    print("4. Enable performance monitoring with built-in timing")
    print("5. Use enhanced validation and benchmarking")
    print("\nRun 'from utils import create_solution_template' for boilerplate generation.")


def print_enhanced_status():
    """Print the status of enhanced utilities."""
    if ENHANCED_UTILS_AVAILABLE:
        print("✅ Enhanced utilities are available")
        print("   - AdventSolution base class")
        print("   - Advanced InputParser") 
        print("   - Performance profiling")
        print("   - Comprehensive testing framework")
    else:
        print("⚠️  Enhanced utilities not available - using legacy functions only")
        print("   Consider installing the enhanced utils package for:")
        print("   - Better input parsing")
        print("   - Automatic timing and benchmarking") 
        print("   - Comprehensive testing capabilities")


# Legacy compatibility notice
def _show_legacy_notice():
    """Show notice about enhanced utilities availability."""
    import os
    if os.getenv('ADVENT_UTILS_QUIET') != '1' and not ENHANCED_UTILS_AVAILABLE:
        print("💡 Legacy utils mode. Enhanced features available in utils/ package.")


# Show notice on import
_show_legacy_notice()