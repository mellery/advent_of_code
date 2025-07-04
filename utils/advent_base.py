"""
Base class for Advent of Code solutions.

This module provides the AdventSolution base class that standardizes
the structure and execution of Advent of Code solutions.
"""

import time
import argparse
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict, List, Optional, Union, Callable
import sys
import os

class AdventSolution(ABC):
    """
    Base class for all Advent of Code solutions.
    
    This class provides:
    - Automatic input file discovery
    - Standardized execution patterns
    - Built-in timing and validation
    - Command-line argument handling
    - Consistent output formatting
    """
    
    def __init__(self, year: int, day: int, title: str = ""):
        """
        Initialize the solution.
        
        Args:
            year: Year of the challenge (e.g., 2019, 2020)
            day: Day number (1-25)
            title: Optional descriptive title for the challenge
        """
        self.year = year
        self.day = day
        self.title = title
        self._input_file: Optional[str] = None
        self._test_file: Optional[str] = None
        self._timing_enabled = False
        self._results: Dict[str, Any] = {}
        
    @property
    def input_file(self) -> str:
        """Get the input file path, discovering it if not already set."""
        if self._input_file is None:
            self._input_file = self._discover_input_file()
        return self._input_file
    
    @input_file.setter
    def input_file(self, path: str) -> None:
        """Set a custom input file path."""
        self._input_file = path
    
    @property
    def test_file(self) -> Optional[str]:
        """Get the test file path, discovering it if not already set."""
        if self._test_file is None:
            self._test_file = self._discover_test_file()
        return self._test_file
    
    def _discover_input_file(self) -> str:
        """
        Auto-discover the input file using standard naming patterns.
        
        Returns:
            Path to the discovered input file
            
        Raises:
            FileNotFoundError: If no input file is found
        """
        patterns = [
            f"day{self.day}_input.txt",
            f"day{self.day}input.txt",
            f"input{self.day}.txt",
            f"day{self.day}.txt",
            "input.txt",
            "part1.txt"
        ]
        
        for pattern in patterns:
            if Path(pattern).exists():
                return pattern
        
        # If not found in current directory, check parent directories
        current_dir = Path.cwd()
        for parent in [current_dir] + list(current_dir.parents)[:3]:
            for pattern in patterns:
                file_path = parent / pattern
                if file_path.exists():
                    return str(file_path)
        
        raise FileNotFoundError(
            f"No input file found for {self.year} Day {self.day}. "
            f"Tried patterns: {', '.join(patterns)}"
        )
    
    def _discover_test_file(self) -> Optional[str]:
        """
        Auto-discover the test file using standard naming patterns.
        
        Returns:
            Path to the discovered test file, or None if not found
        """
        patterns = [
            f"day{self.day}_test.txt",
            f"day{self.day}_example.txt",
            f"day{self.day}_sample.txt",
            f"test{self.day}.txt",
            f"example{self.day}.txt"
        ]
        
        for pattern in patterns:
            if Path(pattern).exists():
                return pattern
        
        return None
    
    @abstractmethod
    def part1(self, input_data: str) -> Any:
        """
        Solve part 1 of the challenge.
        
        Args:
            input_data: Raw input data as a string
            
        Returns:
            Solution for part 1
        """
        pass
    
    @abstractmethod
    def part2(self, input_data: str) -> Any:
        """
        Solve part 2 of the challenge.
        
        Args:
            input_data: Raw input data as a string
            
        Returns:
            Solution for part 2
        """
        pass
    
    def _load_input(self, filename: Optional[str] = None) -> str:
        """
        Load input data from file.
        
        Args:
            filename: Optional custom filename, defaults to discovered input file
            
        Returns:
            Raw input data as string
            
        Raises:
            FileNotFoundError: If the input file is not found
        """
        file_path = filename or self.input_file
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            raise FileNotFoundError(f"Input file not found: {file_path}")
        except Exception as e:
            raise RuntimeError(f"Error reading input file {file_path}: {e}")
    
    def run(self, use_test: bool = False, part: Optional[int] = None, 
            timing: bool = False, validate: bool = False) -> Dict[str, Any]:
        """
        Execute the solution with specified options.
        
        Args:
            use_test: Use test input instead of real input
            part: Run only specific part (1 or 2), or both if None
            timing: Enable execution timing
            validate: Run validation if test data is available
            
        Returns:
            Dictionary containing results and metadata
        """
        self._timing_enabled = timing
        
        # Determine input file
        if use_test:
            if self.test_file is None:
                raise FileNotFoundError("No test file found for validation")
            input_file = self.test_file
        else:
            input_file = self.input_file
        
        # Load input data
        input_data = self._load_input(input_file)
        
        results = {
            'year': self.year,
            'day': self.day,
            'title': self.title,
            'input_file': input_file,
            'use_test': use_test
        }
        
        # Run part 1
        if part is None or part == 1:
            start_time = time.time()
            try:
                result1 = self.part1(input_data)
                results['part1'] = result1
                results['part1_time'] = time.time() - start_time
                
                if timing:
                    print(f"Part 1 completed in {results['part1_time']:.4f} seconds")
                    
            except Exception as e:
                results['part1_error'] = str(e)
                print(f"Error in part 1: {e}")
        
        # Run part 2
        if part is None or part == 2:
            start_time = time.time()
            try:
                result2 = self.part2(input_data)
                results['part2'] = result2
                results['part2_time'] = time.time() - start_time
                
                if timing:
                    print(f"Part 2 completed in {results['part2_time']:.4f} seconds")
                    
            except Exception as e:
                results['part2_error'] = str(e)
                print(f"Error in part 2: {e}")
        
        self._results = results
        return results
    
    def validate(self, expected_part1: Any = None, expected_part2: Any = None) -> bool:
        """
        Validate solution against expected results using test input.
        
        Solutions should override this method to provide internal  
        validation with hardcoded test cases.
        
        Args:
            expected_part1: Expected result for part 1
            expected_part2: Expected result for part 2
            
        Returns:
            True if all validations pass
        """
        print("❌ VALIDATION FAILURE: validate() method must be overridden in solution class")
        return False
        
    
    def benchmark(self, iterations: int = 5) -> Dict[str, float]:
        """
        Benchmark the solution by running it multiple times.
        
        Args:
            iterations: Number of iterations to run
            
        Returns:
            Dictionary with timing statistics
        """
        print(f"Benchmarking {self.year} Day {self.day} ({iterations} iterations)...")
        
        part1_times = []
        part2_times = []
        
        for i in range(iterations):
            results = self.run(timing=False)
            
            if 'part1_time' in results:
                part1_times.append(results['part1_time'])
            if 'part2_time' in results:
                part2_times.append(results['part2_time'])
        
        stats = {}
        
        if part1_times:
            stats['part1_avg'] = sum(part1_times) / len(part1_times)
            stats['part1_min'] = min(part1_times)
            stats['part1_max'] = max(part1_times)
        
        if part2_times:
            stats['part2_avg'] = sum(part2_times) / len(part2_times)
            stats['part2_min'] = min(part2_times)
            stats['part2_max'] = max(part2_times)
        
        if part1_times and part2_times:
            total_times = [p1 + p2 for p1, p2 in zip(part1_times, part2_times)]
            stats['total_avg'] = sum(total_times) / len(total_times)
            stats['total_min'] = min(total_times)
            stats['total_max'] = max(total_times)
        
        # Print results
        for key, value in stats.items():
            print(f"{key}: {value:.4f}s")
        
        return stats
    
    def setup_args(self) -> argparse.Namespace:
        """
        Set up command line arguments with standard options.
        
        Returns:
            Parsed command line arguments
        """
        parser = argparse.ArgumentParser(
            description=f'Advent of Code {self.year} Day {self.day}'
                       f'{": " + self.title if self.title else ""}'
        )
        
        parser.add_argument(
            '--input', '-i',
            help='Custom input file path'
        )
        parser.add_argument(
            '--test', '-t',
            action='store_true',
            help='Use test input'
        )
        parser.add_argument(
            '--part', '-p',
            type=int,
            choices=[1, 2],
            help='Run only specific part (1 or 2)'
        )
        parser.add_argument(
            '--time',
            action='store_true',
            help='Show execution timing'
        )
        parser.add_argument(
            '--validate',
            action='store_true',
            help='Run validation against test cases'
        )
        parser.add_argument(
            '--benchmark',
            type=int,
            metavar='N',
            help='Benchmark with N iterations'
        )
        
        return parser.parse_args()
    
    def main(self) -> None:
        """
        Main entry point that handles command line arguments and execution.
        
        This method should be called from the solution's main block.
        """
        args = self.setup_args()
        
        # Set custom input file if provided
        if args.input:
            self.input_file = args.input
        
        try:
            if args.benchmark:
                self.benchmark(args.benchmark)
            elif args.validate:
                # For validation, you would typically override this
                # to provide expected values
                self.validate()
            else:
                results = self.run(
                    use_test=args.test,
                    part=args.part,
                    timing=args.time
                )
                
                # Display results
                print(f"\n=== {self.year} Day {self.day}" + 
                      (f": {self.title}" if self.title else "") + " ===")
                
                if 'part1' in results:
                    print(f"Part 1: {results['part1']}")
                if 'part2' in results:
                    print(f"Part 2: {results['part2']}")
                
        except Exception as e:
            print(f"Error: {e}")
            sys.exit(1)
    
    def __str__(self) -> str:
        """String representation of the solution."""
        return f"AdventSolution({self.year}, {self.day}" + \
               (f", '{self.title}'" if self.title else "") + ")"
    
    def __repr__(self) -> str:
        """Developer representation of the solution."""
        return self.__str__()