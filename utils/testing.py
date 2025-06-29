"""
Testing infrastructure utilities for Advent of Code solutions.

This module provides comprehensive testing, validation, and regression testing
capabilities for Advent of Code solutions.
"""

import sys
from typing import Any, Dict, List, Optional, Callable, Tuple, Union
from dataclasses import dataclass, field
from pathlib import Path
import json
import traceback
from enum import Enum


class TestStatus(Enum):
    """Status of a test case."""
    PASSED = "PASSED"
    FAILED = "FAILED"
    ERROR = "ERROR"
    SKIPPED = "SKIPPED"


@dataclass
class TestCase:
    """
    Container for a single test case.
    """
    name: str
    input_data: str
    expected_part1: Any = None
    expected_part2: Any = None
    description: str = ""
    tags: List[str] = field(default_factory=list)
    timeout: Optional[float] = None
    
    def __str__(self) -> str:
        return f"TestCase({self.name})"


@dataclass
class TestResult:
    """
    Container for test execution results.
    """
    test_case: TestCase
    status: TestStatus
    part1_result: Any = None
    part2_result: Any = None
    part1_status: TestStatus = TestStatus.SKIPPED
    part2_status: TestStatus = TestStatus.SKIPPED
    execution_time: float = 0.0
    error_message: str = ""
    
    @property
    def passed(self) -> bool:
        """Check if the test passed completely."""
        return self.status == TestStatus.PASSED
    
    @property
    def failed(self) -> bool:
        """Check if the test failed."""
        return self.status == TestStatus.FAILED
    
    @property
    def had_error(self) -> bool:
        """Check if the test had an error."""
        return self.status == TestStatus.ERROR


class TestSuite:
    """
    Comprehensive test suite for Advent of Code solutions.
    """
    
    def __init__(self, year: int, day: int):
        """
        Initialize test suite.
        
        Args:
            year: Year of the challenge
            day: Day number
        """
        self.year = year
        self.day = day
        self.test_cases: List[TestCase] = []
        self.results: List[TestResult] = []
        
    def add_test_case(self, test_case: TestCase) -> None:
        """
        Add a test case to the suite.
        
        Args:
            test_case: TestCase to add
        """
        self.test_cases.append(test_case)
    
    def add_test(self, name: str, input_data: str, 
                expected_part1: Any = None, expected_part2: Any = None,
                description: str = "", tags: Optional[List[str]] = None) -> None:
        """
        Add a test case with individual parameters.
        
        Args:
            name: Test name
            input_data: Input data for the test
            expected_part1: Expected result for part 1
            expected_part2: Expected result for part 2
            description: Optional description
            tags: Optional tags for categorization
        """
        test_case = TestCase(
            name=name,
            input_data=input_data,
            expected_part1=expected_part1,
            expected_part2=expected_part2,
            description=description,
            tags=tags or []
        )
        self.add_test_case(test_case)
    
    def load_test_file(self, filename: str) -> None:
        """
        Load test cases from a JSON file.
        
        Args:
            filename: Path to JSON test file
            
        Expected JSON format:
        {
            "tests": [
                {
                    "name": "example_1",
                    "input": "test input data",
                    "expected_part1": 42,
                    "expected_part2": 84,
                    "description": "Test description",
                    "tags": ["example"]
                }
            ]
        }
        """
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
            
            for test_data in data.get('tests', []):
                self.add_test(
                    name=test_data['name'],
                    input_data=test_data['input'],
                    expected_part1=test_data.get('expected_part1'),
                    expected_part2=test_data.get('expected_part2'),
                    description=test_data.get('description', ''),
                    tags=test_data.get('tags', [])
                )
                
        except (FileNotFoundError, json.JSONDecodeError, KeyError) as e:
            print(f"Warning: Could not load test file {filename}: {e}")
    
    def run_tests(self, part1_func: Callable, part2_func: Callable,
                  tags: Optional[List[str]] = None, 
                  verbose: bool = True) -> List[TestResult]:
        """
        Run all test cases.
        
        Args:
            part1_func: Function for part 1
            part2_func: Function for part 2
            tags: Optional tags to filter tests
            verbose: Print detailed output
            
        Returns:
            List of test results
        """
        import time
        
        self.results.clear()
        
        # Filter tests by tags if specified
        tests_to_run = self.test_cases
        if tags:
            tests_to_run = [tc for tc in self.test_cases 
                           if any(tag in tc.tags for tag in tags)]
        
        if verbose:
            print(f"\nRunning {len(tests_to_run)} test(s) for {self.year} Day {self.day}")
            print("=" * 60)
        
        for i, test_case in enumerate(tests_to_run, 1):
            if verbose:
                print(f"Test {i}: {test_case.name}")
                if test_case.description:
                    print(f"  Description: {test_case.description}")
            
            result = self._run_single_test(test_case, part1_func, part2_func)
            self.results.append(result)
            
            if verbose:
                self._print_test_result(result)
                print()
        
        if verbose:
            self._print_summary()
        
        return self.results
    
    def _run_single_test(self, test_case: TestCase, 
                        part1_func: Callable, part2_func: Callable) -> TestResult:
        """
        Run a single test case.
        
        Args:
            test_case: Test case to run
            part1_func: Function for part 1
            part2_func: Function for part 2
            
        Returns:
            TestResult with execution details
        """
        import time
        
        result = TestResult(test_case=test_case, status=TestStatus.PASSED)
        start_time = time.time()
        
        try:
            # Test part 1
            if test_case.expected_part1 is not None:
                try:
                    result.part1_result = part1_func(test_case.input_data)
                    if result.part1_result == test_case.expected_part1:
                        result.part1_status = TestStatus.PASSED
                    else:
                        result.part1_status = TestStatus.FAILED
                        result.status = TestStatus.FAILED
                except Exception as e:
                    result.part1_status = TestStatus.ERROR
                    result.status = TestStatus.ERROR
                    result.error_message = f"Part 1 error: {str(e)}"
            
            # Test part 2
            if test_case.expected_part2 is not None:
                try:
                    result.part2_result = part2_func(test_case.input_data)
                    if result.part2_result == test_case.expected_part2:
                        result.part2_status = TestStatus.PASSED
                    else:
                        result.part2_status = TestStatus.FAILED
                        if result.status != TestStatus.ERROR:
                            result.status = TestStatus.FAILED
                except Exception as e:
                    result.part2_status = TestStatus.ERROR
                    result.status = TestStatus.ERROR
                    if result.error_message:
                        result.error_message += f"; Part 2 error: {str(e)}"
                    else:
                        result.error_message = f"Part 2 error: {str(e)}"
            
        except Exception as e:
            result.status = TestStatus.ERROR
            result.error_message = f"Test execution error: {str(e)}"
        
        result.execution_time = time.time() - start_time
        return result
    
    def _print_test_result(self, result: TestResult) -> None:
        """Print formatted test result."""
        status_symbol = {
            TestStatus.PASSED: "✅",
            TestStatus.FAILED: "❌", 
            TestStatus.ERROR: "🔥",
            TestStatus.SKIPPED: "⏭️"
        }
        
        print(f"  Overall: {status_symbol[result.status]} {result.status.value}")
        
        if result.test_case.expected_part1 is not None:
            symbol = status_symbol[result.part1_status]
            expected = result.test_case.expected_part1
            actual = result.part1_result
            print(f"  Part 1:  {symbol} Expected: {expected}, Got: {actual}")
        
        if result.test_case.expected_part2 is not None:
            symbol = status_symbol[result.part2_status]
            expected = result.test_case.expected_part2
            actual = result.part2_result
            print(f"  Part 2:  {symbol} Expected: {expected}, Got: {actual}")
        
        if result.error_message:
            print(f"  Error:   {result.error_message}")
        
        print(f"  Time:    {result.execution_time:.4f}s")
    
    def _print_summary(self) -> None:
        """Print test run summary."""
        if not self.results:
            return
        
        total = len(self.results)
        passed = sum(1 for r in self.results if r.passed)
        failed = sum(1 for r in self.results if r.failed)
        errors = sum(1 for r in self.results if r.had_error)
        
        print("=" * 60)
        print("TEST SUMMARY")
        print("=" * 60)
        print(f"Total tests: {total}")
        print(f"✅ Passed:   {passed}")
        print(f"❌ Failed:   {failed}")
        print(f"🔥 Errors:   {errors}")
        
        if failed > 0 or errors > 0:
            print(f"\nSuccess rate: {(passed/total)*100:.1f}%")
        else:
            print("\n🎉 All tests passed!")
    
    def get_failing_tests(self) -> List[TestResult]:
        """Get all failing test results."""
        return [r for r in self.results if not r.passed]
    
    def save_results(self, filename: str) -> None:
        """
        Save test results to JSON file.
        
        Args:
            filename: Output filename
        """
        results_data = {
            'year': self.year,
            'day': self.day,
            'total_tests': len(self.results),
            'passed': sum(1 for r in self.results if r.passed),
            'failed': sum(1 for r in self.results if r.failed),
            'errors': sum(1 for r in self.results if r.had_error),
            'results': []
        }
        
        for result in self.results:
            result_data = {
                'test_name': result.test_case.name,
                'status': result.status.value,
                'part1_result': result.part1_result,
                'part2_result': result.part2_result,
                'part1_status': result.part1_status.value,
                'part2_status': result.part2_status.value,
                'execution_time': result.execution_time,
                'error_message': result.error_message
            }
            results_data['results'].append(result_data)
        
        with open(filename, 'w') as f:
            json.dump(results_data, f, indent=2)


class ValidationHelper:
    """
    Helper class for solution validation and regression testing.
    """
    
    @staticmethod
    def validate_solution(part1_func: Callable, part2_func: Callable,
                         test_input: str, expected_part1: Any = None,
                         expected_part2: Any = None) -> bool:
        """
        Quick validation function for simple cases.
        
        Args:
            part1_func: Part 1 function
            part2_func: Part 2 function
            test_input: Test input data
            expected_part1: Expected part 1 result
            expected_part2: Expected part 2 result
            
        Returns:
            True if all validations pass
        """
        success = True
        
        if expected_part1 is not None:
            try:
                result1 = part1_func(test_input)
                if result1 == expected_part1:
                    print(f"✅ Part 1: {result1}")
                else:
                    print(f"❌ Part 1: expected {expected_part1}, got {result1}")
                    success = False
            except Exception as e:
                print(f"🔥 Part 1 error: {e}")
                success = False
        
        if expected_part2 is not None:
            try:
                result2 = part2_func(test_input)
                if result2 == expected_part2:
                    print(f"✅ Part 2: {result2}")
                else:
                    print(f"❌ Part 2: expected {expected_part2}, got {result2}")
                    success = False
            except Exception as e:
                print(f"🔥 Part 2 error: {e}")
                success = False
        
        return success
    
    @staticmethod
    def create_test_decorator(expected_part1: Any = None, 
                            expected_part2: Any = None,
                            test_input: str = ""):
        """
        Create a decorator for automatic test validation.
        
        Args:
            expected_part1: Expected part 1 result
            expected_part2: Expected part 2 result
            test_input: Test input data
            
        Returns:
            Decorator function
        """
        def decorator(solution_class):
            original_main = getattr(solution_class, 'main', None)
            
            def enhanced_main(self):
                # Run validation first
                if test_input:
                    print("Running validation...")
                    self.validate(expected_part1, expected_part2)
                    print()
                
                # Run original main
                if original_main:
                    original_main(self)
                else:
                    # Default main behavior
                    results = self.run()
                    print(f"Part 1: {results.get('part1', 'N/A')}")
                    print(f"Part 2: {results.get('part2', 'N/A')}")
            
            solution_class.main = enhanced_main
            return solution_class
        
        return decorator


# Convenience functions for simple testing
def quick_test(part1_func: Callable, part2_func: Callable,
              test_input: str, expected_part1: Any = None,
              expected_part2: Any = None) -> bool:
    """Quick test function for simple validation."""
    return ValidationHelper.validate_solution(
        part1_func, part2_func, test_input, expected_part1, expected_part2
    )


def test_with_examples(part1_func: Callable, part2_func: Callable,
                      examples: List[Tuple[str, Any, Any]]) -> bool:
    """
    Test with multiple examples.
    
    Args:
        part1_func: Part 1 function
        part2_func: Part 2 function
        examples: List of (input, expected_part1, expected_part2) tuples
        
    Returns:
        True if all tests pass
    """
    all_passed = True
    
    for i, (test_input, expected1, expected2) in enumerate(examples, 1):
        print(f"\nExample {i}:")
        passed = quick_test(part1_func, part2_func, test_input, expected1, expected2)
        if not passed:
            all_passed = False
    
    return all_passed