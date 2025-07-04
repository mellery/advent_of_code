#!/usr/bin/env python3
"""
Enhanced Test Runner for Advent of Code Solutions

This is an enhanced version of the test runner that implements milestone 4A features:
- Performance integration and benchmarking
- Parallel execution capabilities  
- Migration support for auto-detecting enhanced vs legacy solutions
- Regression detection for performance and correctness monitoring
- Memory monitoring with enhanced timing utilities
- Comprehensive test reporting and visualization
"""

import os
import sys
import time
import asyncio
import concurrent.futures
import importlib.util
import traceback
import json
import statistics
import psutil
from pathlib import Path
from typing import Dict, List, Tuple, Any, Optional, Callable, Union
from dataclasses import dataclass, field
from datetime import datetime, timedelta
import threading
import queue

try:
    from colorama import init, Fore, Style
    init()
    COLORS_AVAILABLE = True
except ImportError:
    COLORS_AVAILABLE = False
    class Fore:
        GREEN = RED = YELLOW = BLUE = CYAN = MAGENTA = WHITE = RESET = ""
    class Style:
        BRIGHT = DIM = RESET_ALL = ""

try:
    from tabulate import tabulate
    TABULATE_AVAILABLE = True
except ImportError:
    TABULATE_AVAILABLE = False

# Add utils to path for AdventSolution detection
sys.path.append(str(Path(__file__).parent))

# Try to import AdventSolution for type checking
try:
    from utils import AdventSolution
    ADVENT_SOLUTION_AVAILABLE = True
except ImportError:
    try:
        from utils.advent_base import AdventSolution
        ADVENT_SOLUTION_AVAILABLE = True
    except ImportError:
        ADVENT_SOLUTION_AVAILABLE = False
        AdventSolution = None


@dataclass
class PerformanceMetrics:
    """Detailed performance metrics for a solution."""
    execution_time: float = 0.0
    memory_peak: Optional[float] = None  # MB
    memory_delta: Optional[float] = None  # MB
    cpu_percent: Optional[float] = None
    iterations_run: int = 1
    mean_time: Optional[float] = None
    median_time: Optional[float] = None
    std_dev: Optional[float] = None
    min_time: Optional[float] = None
    max_time: Optional[float] = None


@dataclass
class ValidationResult:
    """Result of solution validation."""
    status: str = "UNKNOWN"  # PASS, FAIL, UNKNOWN, ERROR
    expected: Any = None
    actual: Any = None
    error_message: str = ""


@dataclass
class SolutionType:
    """Information about solution architecture type."""
    is_enhanced: bool = False
    is_legacy: bool = False
    has_advent_solution: bool = False
    has_validation: bool = False
    architecture_version: str = "unknown"


@dataclass
class EnhancedTestResult:
    """Comprehensive test result with enhanced metrics."""
    year: str = ""
    day: str = ""
    file_path: str = ""
    solution_type: SolutionType = field(default_factory=SolutionType)
    
    # Execution results
    success: bool = True
    error: str = ""
    
    # Solution results
    part1_result: Any = None
    part2_result: Any = None
    
    # Performance metrics
    part1_metrics: PerformanceMetrics = field(default_factory=PerformanceMetrics)
    part2_metrics: PerformanceMetrics = field(default_factory=PerformanceMetrics)
    
    # Validation results
    part1_validation: ValidationResult = field(default_factory=ValidationResult)
    part2_validation: ValidationResult = field(default_factory=ValidationResult)
    
    # Timing details
    discovery_time: float = 0.0
    loading_time: float = 0.0
    total_time: float = 0.0
    
    # Regression data
    previous_performance: Optional[Dict] = None
    performance_regression: Optional[float] = None  # percentage change
    
    # Memory tracking
    memory_efficient: bool = True
    memory_warnings: List[str] = field(default_factory=list)


class MemoryMonitor:
    """Monitor memory usage during solution execution."""
    
    def __init__(self):
        self.process = psutil.Process()
        self.monitoring = False
        self.peak_memory = 0.0
        self.start_memory = 0.0
        self.memory_samples = []
        self._monitor_thread = None
        self._stop_event = threading.Event()
    
    def start_monitoring(self):
        """Start memory monitoring in background thread."""
        self.monitoring = True
        self.start_memory = self.process.memory_info().rss / 1024 / 1024  # MB
        self.peak_memory = self.start_memory
        self.memory_samples = [self.start_memory]
        self._stop_event.clear()
        self._monitor_thread = threading.Thread(target=self._monitor_loop)
        self._monitor_thread.daemon = True
        self._monitor_thread.start()
    
    def stop_monitoring(self) -> PerformanceMetrics:
        """Stop monitoring and return metrics."""
        self.monitoring = False
        self._stop_event.set()
        if self._monitor_thread:
            self._monitor_thread.join(timeout=0.1)
        
        end_memory = self.process.memory_info().rss / 1024 / 1024  # MB
        
        metrics = PerformanceMetrics()
        metrics.memory_peak = self.peak_memory
        metrics.memory_delta = end_memory - self.start_memory
        
        return metrics
    
    def _monitor_loop(self):
        """Background monitoring loop."""
        while not self._stop_event.is_set():
            try:
                current_memory = self.process.memory_info().rss / 1024 / 1024  # MB
                self.memory_samples.append(current_memory)
                self.peak_memory = max(self.peak_memory, current_memory)
                time.sleep(0.01)  # Sample every 10ms
            except:
                break


class SolutionAnalyzer:
    """Analyze solution files to determine their architecture type."""
    
    @staticmethod
    def analyze_solution(file_path: Path) -> SolutionType:
        """Analyze a solution file to determine its type and capabilities."""
        solution_type = SolutionType()
        
        try:
            with open(file_path, 'r') as f:
                content = f.read()
            
            # Check for enhanced features
            if 'AdventSolution' in content:
                solution_type.has_advent_solution = True
                solution_type.is_enhanced = True
                solution_type.architecture_version = "enhanced"
            
            if 'class' in content and 'Solution' in content:
                solution_type.is_enhanced = True
            
            if 'def validate(' in content or 'validate_solution' in content:
                solution_type.has_validation = True
            
            # Check for legacy patterns - but now we'll reject these
            if ('def part1(' in content or 'def part2(' in content) and not solution_type.is_enhanced:
                solution_type.is_legacy = True
                solution_type.architecture_version = "legacy_deprecated"
            
            # Check for modern legacy (has part1/part2 but no class structure)
            if ('def part1(' in content and 'def part2(' in content and 
                'class' not in content):
                solution_type.is_legacy = True
                solution_type.architecture_version = "modern_legacy_deprecated"
                
        except Exception as e:
            solution_type.architecture_version = f"error: {e}"
        
        return solution_type


class RegressionTracker:
    """Track performance regression across test runs."""
    
    def __init__(self, data_file: str = "test_performance_history.json"):
        self.data_file = Path(data_file)
        self.history = self.load_history()
    
    def load_history(self) -> Dict:
        """Load performance history from file."""
        if self.data_file.exists():
            try:
                with open(self.data_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        return {}
    
    def save_history(self):
        """Save performance history to file."""
        try:
            with open(self.data_file, 'w') as f:
                json.dump(self.history, f, indent=2)
        except Exception as e:
            print(f"Warning: Could not save performance history: {e}")
    
    def record_performance(self, year: str, day: str, part: str, execution_time: float):
        """Record performance for regression tracking."""
        key = f"{year}_day{day}_{part}"
        timestamp = datetime.now().isoformat()
        
        if key not in self.history:
            self.history[key] = []
        
        self.history[key].append({
            "timestamp": timestamp,
            "execution_time": execution_time
        })
        
        # Keep only last 10 runs
        self.history[key] = self.history[key][-10:]
    
    def check_regression(self, year: str, day: str, part: str, current_time: float) -> Optional[float]:
        """Check for performance regression. Returns percentage change if regression detected."""
        key = f"{year}_day{day}_{part}"
        
        if key not in self.history or len(self.history[key]) < 2:
            return None
        
        # Compare against median of last 5 runs
        recent_times = [entry["execution_time"] for entry in self.history[key][-5:]]
        baseline = statistics.median(recent_times)
        
        if baseline > 0:
            change_percent = ((current_time - baseline) / baseline) * 100
            
            # Consider >20% increase a regression
            if change_percent > 20:
                return change_percent
        
        return None


class EnhancedTestRunner:
    """Enhanced test runner with advanced features."""
    
    def __init__(self, root_dir: str = ".", strict_mode: bool = True):
        self.root_dir = Path(root_dir)
        self.strict_mode = strict_mode
        self.results: List[EnhancedTestResult] = []
        self.expected_answers: Dict[str, Dict[str, Dict[str, Any]]] = {}
        self.answers_file = self.root_dir / "expected_answers.json"
        self.regression_tracker = RegressionTracker()
        self.load_expected_answers()
        
        # Performance benchmarks (loaded from PERFORMANCE_BENCHMARKS.md standards)
        self.performance_targets = {
            "fast": 0.1,      # < 100ms - ⚡ Fast solutions
            "medium": 1.0,    # < 1s - 🔥 Medium solutions  
            "slow": 5.0,      # < 5s - ⏱️ Slow solutions
            "very_slow": 30.0 # < 30s - 🐌 Very slow solutions (require optimization)
        }
        
        # Memory usage thresholds (from PERFORMANCE_BENCHMARKS.md)
        self.memory_targets = {
            "efficient": 50,    # < 50MB - Efficient
            "moderate": 200,    # 50MB-200MB - Moderate
            "high": 500,        # 200MB-500MB - High
            "excessive": float('inf')  # > 500MB - Excessive (requires optimization)
        }
    
    def load_expected_answers(self) -> None:
        """Load expected answers from JSON file."""
        try:
            if self.answers_file.exists():
                with open(self.answers_file, 'r') as f:
                    self.expected_answers = json.load(f)
                print(f"Loaded expected answers from {self.answers_file}")
            else:
                self.expected_answers = {}
        except Exception as e:
            print(f"Error loading expected answers: {e}")
            self.expected_answers = {}
    
    def discover_solutions(self, year_filter: Optional[str] = None, 
                          day_filter: Optional[str] = None) -> List[Tuple[str, str, Path, SolutionType]]:
        """
        Discover all solution files with enhanced analysis.
        
        Returns:
            List of tuples (year, day, file_path, solution_type)
        """
        solutions = []
        
        for year_dir in self.root_dir.iterdir():
            if year_dir.is_dir() and year_dir.name.isdigit() and len(year_dir.name) == 4:
                year = year_dir.name
                
                if year_filter and year != year_filter:
                    continue
                
                for file_path in year_dir.glob("*.py"):
                    filename = file_path.name
                    
                    # Skip template and test files
                    if "template" in filename or "test" in filename:
                        continue
                    
                    # Extract day number
                    day = self._extract_day_number(filename)
                    if day:
                        if day_filter and day != day_filter:
                            continue
                        
                        # Analyze solution type
                        solution_type = SolutionAnalyzer.analyze_solution(file_path)
                        solutions.append((year, day, file_path, solution_type))
        
        return sorted(solutions)
    
    def _extract_day_number(self, filename: str) -> Optional[str]:
        """Extract day number from filename."""
        import re
        
        patterns = [
            r"day(\d+)\.py",
            r"advent(\d+)\.py", 
            r"(\d+)\.py"
        ]
        
        for pattern in patterns:
            match = re.match(pattern, filename)
            if match:
                return match.group(1)
        
        return None
    
    def run_solution_with_monitoring(self, solution_func: Callable, 
                                   input_data: str, iterations: int = 1) -> Tuple[Any, PerformanceMetrics]:
        """Run solution with lightweight monitoring to avoid threading issues."""
        times = []
        results = []
        final_metrics = PerformanceMetrics()
        
        # Get memory baseline before any iterations
        process = psutil.Process()
        start_memory = process.memory_info().rss / 1024 / 1024  # MB
        peak_memory = start_memory
        
        for i in range(iterations):
            # Lightweight timing - no background threads
            start_time = time.perf_counter()
            
            try:
                result = solution_func(input_data)
                end_time = time.perf_counter()
                
                # Quick memory sample after execution
                current_memory = process.memory_info().rss / 1024 / 1024  # MB
                peak_memory = max(peak_memory, current_memory)
                
                execution_time = end_time - start_time
                times.append(execution_time)
                results.append(result)
                
            except Exception as e:
                raise e
        
        # Set memory metrics (lightweight approach)
        final_metrics.memory_peak = peak_memory
        final_metrics.memory_delta = peak_memory - start_memory
        
        # Calculate statistical metrics from timing data
        if len(times) > 1:
            final_metrics.execution_time = statistics.median(times)  # Use median for most representative time
            final_metrics.mean_time = statistics.mean(times)
            final_metrics.median_time = statistics.median(times)
            final_metrics.std_dev = statistics.stdev(times)
            final_metrics.min_time = min(times)
            final_metrics.max_time = max(times)
        else:
            final_metrics.execution_time = times[0]
            final_metrics.mean_time = times[0]
            final_metrics.median_time = times[0]
            final_metrics.min_time = times[0]
            final_metrics.max_time = times[0]
            final_metrics.std_dev = 0.0
            
        final_metrics.iterations_run = iterations
        
        # Return the most common result
        if results:
            return results[0], final_metrics
        else:
            return None, final_metrics
    
    def load_and_execute_solution(self, year: str, day: str, file_path: Path, 
                                solution_type: SolutionType) -> EnhancedTestResult:
        """Load and execute a solution with enhanced monitoring."""
        result = EnhancedTestResult()
        result.year = year
        result.day = day
        result.file_path = str(file_path)
        result.solution_type = solution_type
        
        start_total = time.perf_counter()
        
        try:
            # Discovery and loading timing
            start_loading = time.perf_counter()
            
            # Load the module
            module = self._load_module(file_path)
            if not module:
                result.success = False
                result.error = "Failed to load module"
                return result
            
            result.loading_time = time.perf_counter() - start_loading
            
            # Find input data
            input_data = self._get_input_data(file_path.parent, day)
            
            # Execute based on solution type and strict mode setting
            if solution_type.is_enhanced and solution_type.has_advent_solution:
                result = self._execute_enhanced_solution(module, input_data, result)
            elif solution_type.is_legacy and not self.strict_mode:
                # Allow legacy solutions only in non-strict mode
                result = self._execute_legacy_solution(module, input_data, result)
            elif solution_type.is_legacy and self.strict_mode:
                # Fail immediately for deprecated legacy solutions in strict mode
                result.success = False
                result.error = (f"STRICT MODE VIOLATION: Solution uses deprecated legacy format "
                              f"({solution_type.architecture_version}). All solutions must now use "
                              f"AdventSolution base class. Use --no-strict to allow legacy solutions "
                              f"or migrate this solution to the enhanced format.")
                return result
            else:
                # Unknown solution type - fail with helpful message
                result.success = False
                if self.strict_mode:
                    result.error = (f"STRICT MODE VIOLATION: Solution does not use AdventSolution base class. "
                                  f"All solutions must inherit from AdventSolution. "
                                  f"Architecture detected: {solution_type.architecture_version}")
                else:
                    result.error = (f"UNKNOWN ARCHITECTURE: Cannot determine solution type. "
                                  f"Architecture detected: {solution_type.architecture_version}")
                return result
            
            # Validate results
            self._validate_results(result)
            
            # Check for regressions
            self._check_performance_regression(result)
            
        except Exception as e:
            result.success = False
            result.error = f"Execution error: {str(e)}"
            
        finally:
            result.total_time = time.perf_counter() - start_total
        
        return result
    
    def _load_module(self, file_path: Path):
        """Load a Python module from file path."""
        try:
            # Set matplotlib to non-interactive backend to prevent GUI issues in threads
            try:
                import matplotlib
                matplotlib.use('Agg')
            except ImportError:
                # matplotlib not available, ignore
                pass
            
            # Add solution directory and root to sys.path for imports
            solution_dir = str(file_path.parent.absolute())
            root_dir = str(file_path.parent.parent.absolute())
            
            if solution_dir not in sys.path:
                sys.path.insert(0, solution_dir)
            if root_dir not in sys.path:
                sys.path.insert(0, root_dir)
            
            spec = importlib.util.spec_from_file_location("solution", str(file_path.absolute()))
            if spec and spec.loader:
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                return module
                
        except Exception as e:
            print(f"Error loading {file_path}: {e}")
        
        return None
    
    def _get_input_data(self, directory: Path, day: str) -> Optional[str]:
        """Get input data for a solution."""
        patterns = [
            f"day{day}_input.txt",
            f"day{day}input.txt", 
            f"input{day}.txt",
            f"day{day}.txt"
        ]
        
        for pattern in patterns:
            file_path = directory / pattern
            if file_path.exists():
                try:
                    with open(file_path, 'r') as f:
                        return f.read().strip()
                except:
                    pass
        
        return None
    
    def _execute_enhanced_solution(self, module, input_data: str, result: EnhancedTestResult) -> EnhancedTestResult:
        """Execute enhanced AdventSolution-based solution with strict validation."""
        # Find the solution class - prefer concrete implementations over base classes
        solution_class = None
        candidate_classes = []
        for name in dir(module):
            obj = getattr(module, name)
            if (isinstance(obj, type) and 
                hasattr(obj, 'part1') and hasattr(obj, 'part2') and
                'Solution' in name):
                candidate_classes.append((name, obj))
        
        # Prefer classes that are NOT named 'AdventSolution' (i.e., concrete implementations)
        for name, obj in candidate_classes:
            if name != 'AdventSolution':
                solution_class = obj
                break
        
        # If no concrete implementation found, fall back to any solution class
        if not solution_class and candidate_classes:
            solution_class = candidate_classes[0][1]
        
        if not solution_class:
            result.success = False
            result.error = "ARCHITECTURE VIOLATION: No solution class found inheriting from AdventSolution"
            return result
        
        # Strict validation: Ensure the class actually inherits from AdventSolution
        if ADVENT_SOLUTION_AVAILABLE and AdventSolution:
            if not issubclass(solution_class, AdventSolution):
                result.success = False
                result.error = (f"ARCHITECTURE VIOLATION: Solution class '{solution_class.__name__}' does not inherit "
                              f"from AdventSolution base class. All solutions must inherit from AdventSolution.")
                return result
        else:
            # If AdventSolution is not available, check for required methods
            required_methods = ['part1', 'part2', 'run']
            missing_methods = [method for method in required_methods if not hasattr(solution_class, method)]
            if missing_methods:
                result.success = False
                result.error = (f"ARCHITECTURE VIOLATION: Solution class missing required AdventSolution methods: "
                              f"{', '.join(missing_methods)}")
                return result
        
        try:
            solution_instance = solution_class()
            
            # Execute part 1 with monitoring
            if hasattr(solution_instance, 'part1'):
                part1_result, part1_metrics = self.run_solution_with_monitoring(
                    solution_instance.part1, input_data, iterations=1
                )
                result.part1_result = part1_result
                result.part1_metrics = part1_metrics
            
            # Execute part 2 with monitoring  
            if hasattr(solution_instance, 'part2'):
                part2_result, part2_metrics = self.run_solution_with_monitoring(
                    solution_instance.part2, input_data, iterations=1
                )
                result.part2_result = part2_result
                result.part2_metrics = part2_metrics
            
            # Run validation if available
            if hasattr(solution_instance, 'validate'):
                try:
                    validation_passed = solution_instance.validate()
                    if not validation_passed:
                        result.error = "Solution validation failed"
                        # Mark validation as failed for both parts if validation method fails
                        if result.part1_result is not None:
                            result.part1_validation.status = "FAIL"
                            result.part1_validation.error_message = "Internal validation failed"
                        if result.part2_result is not None:
                            result.part2_validation.status = "FAIL"
                            result.part2_validation.error_message = "Internal validation failed"
                except Exception as e:
                    result.error = f"Validation error: {e}"
                    # Mark validation as error for both parts if validation method crashes
                    if result.part1_result is not None:
                        result.part1_validation.status = "ERROR"
                        result.part1_validation.error_message = str(e)
                    if result.part2_result is not None:
                        result.part2_validation.status = "ERROR"
                        result.part2_validation.error_message = str(e)
            
        except Exception as e:
            # Enhanced execution failed, try legacy compatibility functions
            try:
                result.success = True
                result.error = ""  # Clear the error since we're trying fallback
                result = self._execute_legacy_solution(module, input_data, result)
            except Exception as e2:
                result.success = False
                result.error = f"Enhanced execution failed: {e}, Legacy fallback failed: {e2}"
        
        return result
    
    def _execute_legacy_solution(self, module, input_data: str, result: EnhancedTestResult) -> EnhancedTestResult:
        """Execute legacy solution functions."""
        try:
            # Look for part1 and part2 functions
            part1_func = getattr(module, 'part1', None)
            part2_func = getattr(module, 'part2', None)
            
            if part1_func:
                # Try to determine if function expects filename or content
                input_arg = self._get_appropriate_input(part1_func, input_data, result)
                part1_result, part1_metrics = self.run_solution_with_monitoring(
                    part1_func, input_arg, iterations=1  # Legacy solutions might be slower
                )
                result.part1_result = part1_result
                result.part1_metrics = part1_metrics
            
            if part2_func:
                # Try to determine if function expects filename or content
                input_arg = self._get_appropriate_input(part2_func, input_data, result)
                part2_result, part2_metrics = self.run_solution_with_monitoring(
                    part2_func, input_arg, iterations=1
                )
                result.part2_result = part2_result
                result.part2_metrics = part2_metrics
                
        except Exception as e:
            result.success = False
            result.error = f"Legacy execution error: {e}"
        
        return result
    
    def _get_appropriate_input(self, func: Callable, input_data: str, result: EnhancedTestResult) -> str:
        """Determine whether to pass filename or content based on function signature and behavior."""
        import inspect
        
        try:
            # Get function signature to check parameter names
            sig = inspect.signature(func)
            param_names = list(sig.parameters.keys())
            
            # If parameter is named 'filename', 'file', 'filepath', etc., likely expects filename
            if param_names and any(name.lower() in ['filename', 'file', 'filepath', 'fname', 'path'] 
                                 for name in param_names):
                # Find the actual input file in the current directory
                return self._find_input_file_for_function(result.year, result.day)
            
            # Otherwise, assume it expects content
            return input_data
            
        except Exception:
            # If we can't determine, try content first
            return input_data
    
    def _find_input_file_for_function(self, year: str, day: str) -> str:
        """Find the input file that should be passed to legacy functions expecting filenames."""
        # Check current working directory first (should be the solution directory)
        patterns = [
            f"day{day}_input.txt",
            f"day{day}input.txt", 
            f"input{day}.txt",
            f"day{day}.txt"
        ]
        
        for pattern in patterns:
            if Path(pattern).exists():
                return pattern
        
        # If not in current directory, check the year directory
        year_dir = Path(f"/home/mike/src/advent_of_code/{year}")
        for pattern in patterns:
            file_path = year_dir / pattern
            if file_path.exists():
                return str(file_path)
        
        # If no input file found, return a default name (might cause error, but that's expected)
        return f"day{day}_input.txt"
    
    def _validate_results(self, result: EnhancedTestResult):
        """Validate solution results against expected answers."""
        if result.part1_result is not None:
            expected = self.expected_answers.get(result.year, {}).get(result.day, {}).get("part1")
            result.part1_validation = self._validate_single_result(result.part1_result, expected)
        
        if result.part2_result is not None:
            expected = self.expected_answers.get(result.year, {}).get(result.day, {}).get("part2")
            result.part2_validation = self._validate_single_result(result.part2_result, expected)
    
    def _validate_single_result(self, actual: Any, expected: Any) -> ValidationResult:
        """Validate a single result."""
        validation = ValidationResult()
        validation.actual = actual
        validation.expected = expected
        
        if expected is None:
            validation.status = "UNKNOWN"
        else:
            try:
                if actual == expected or str(actual) == str(expected):
                    validation.status = "PASS"
                else:
                    validation.status = "FAIL"
            except Exception as e:
                validation.status = "ERROR"
                validation.error_message = str(e)
        
        return validation
    
    def _get_performance_category(self, execution_time: float) -> str:
        """Classify performance into categories."""
        if execution_time < self.performance_targets["fast"]:
            return "fast"
        elif execution_time < self.performance_targets["medium"]:
            return "medium"
        elif execution_time < self.performance_targets["slow"]:
            return "slow"
        else:
            return "very_slow"
    
    def _check_performance_regression(self, result: EnhancedTestResult):
        """Check for performance regressions, but only warn if performance is concerning."""
        if result.part1_metrics.execution_time > 0:
            regression = self.regression_tracker.check_regression(
                result.year, result.day, "part1", result.part1_metrics.execution_time
            )
            if regression:
                result.performance_regression = regression
                
                # Only show regression warning if current performance is slow or very slow
                performance_category = self._get_performance_category(result.part1_metrics.execution_time)
                if performance_category in ["slow", "very_slow"]:
                    result.memory_warnings.append(f"Part 1 performance regression: {regression:.1f}% slower")
            
            # Record current performance
            self.regression_tracker.record_performance(
                result.year, result.day, "part1", result.part1_metrics.execution_time
            )
        
        if result.part2_metrics.execution_time > 0:
            regression = self.regression_tracker.check_regression(
                result.year, result.day, "part2", result.part2_metrics.execution_time
            )
            if regression:
                if result.performance_regression is None:
                    result.performance_regression = regression
                
                # Only show regression warning if current performance is slow or very slow
                performance_category = self._get_performance_category(result.part2_metrics.execution_time)
                if performance_category in ["slow", "very_slow"]:
                    result.memory_warnings.append(f"Part 2 performance regression: {regression:.1f}% slower")
            
            # Record current performance
            self.regression_tracker.record_performance(
                result.year, result.day, "part2", result.part2_metrics.execution_time
            )
    
    def run_parallel(self, max_workers: int = 4, year_filter: Optional[str] = None, 
                    day_filter: Optional[str] = None) -> None:
        """Run tests in parallel for improved performance."""
        solutions = self.discover_solutions(year_filter, day_filter)
        
        if not solutions:
            print("No solutions found matching criteria")
            return
        
        print(f"🚀 Running {len(solutions)} solutions with {max_workers} parallel workers")
        print("=" * 70)
        
        # Use ThreadPoolExecutor for parallel execution
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Submit all tasks
            future_to_solution = {
                executor.submit(self.load_and_execute_solution, year, day, path, sol_type): (year, day)
                for year, day, path, sol_type in solutions
            }
            
            # Collect results as they complete
            for future in concurrent.futures.as_completed(future_to_solution):
                year, day = future_to_solution[future]
                try:
                    result = future.result()
                    self.results.append(result)
                    self._print_result_safe(result)
                except Exception as e:
                    try:
                        print(f"❌ {year} Day {day}: Exception occurred: {e}")
                    except (BrokenPipeError, IOError):
                        # Ignore broken pipe errors when output is truncated
                        pass
        
        # Save regression data
        self.regression_tracker.save_history()
        
        # Print comprehensive summary
        try:
            self._print_enhanced_summary()
        except (BrokenPipeError, IOError):
            # Ignore broken pipe errors when output is truncated
            pass
    
    def _print_result(self, result: EnhancedTestResult):
        """Print individual test result with enhanced information."""
        status_color = Fore.GREEN if result.success else Fore.RED
        status = "PASS" if result.success else "FAIL"
        
        # Architecture info
        arch_info = f"({result.solution_type.architecture_version})"
        if result.solution_type.has_validation:
            arch_info += " ✓"
        
        print(f"{status_color}{result.year} Day {result.day}: {status}{Style.RESET_ALL} {arch_info}")
        
        if result.success:
            # Part 1 results - always show if we have timing data
            if result.part1_result is not None or result.part1_metrics.execution_time > 0:
                validation_symbol = self._get_validation_symbol(result.part1_validation.status)
                perf_info = self._format_performance_info(result.part1_metrics)
                result_display = result.part1_result if result.part1_result is not None else "?"
                print(f"  Part 1: {result_display} {validation_symbol} {perf_info}")
            
            # Part 2 results - always show if we have timing data
            if result.part2_result is not None or result.part2_metrics.execution_time > 0:
                validation_symbol = self._get_validation_symbol(result.part2_validation.status)
                perf_info = self._format_performance_info(result.part2_metrics)
                result_display = result.part2_result if result.part2_result is not None else "?"
                print(f"  Part 2: {result_display} {validation_symbol} {perf_info}")
            
            # Performance warnings
            if result.memory_warnings:
                for warning in result.memory_warnings:
                    print(f"  ⚠️  {warning}")
            
            print(f"  Total: {result.total_time:.3f}s")
        else:
            print(f"  Error: {result.error}")
        
        print("-" * 50)
    
    def _print_result_safe(self, result: EnhancedTestResult):
        """Print individual test result with protection against broken pipe errors."""
        try:
            self._print_result(result)
        except (BrokenPipeError, IOError):
            # Ignore broken pipe errors when output is truncated (e.g., with head command)
            pass
    
    def _format_performance_info(self, metrics: PerformanceMetrics) -> str:
        """Format performance information for display."""
        info_parts = [f"{metrics.execution_time:.3f}s"]
        
        if metrics.memory_peak:
            info_parts.append(f"mem:{metrics.memory_peak:.1f}MB")
            # Add memory category indicator
            if metrics.memory_peak < self.memory_targets["efficient"]:
                info_parts.append(f"{Fore.GREEN}💾{Style.RESET_ALL}")
            elif metrics.memory_peak < self.memory_targets["moderate"]:
                info_parts.append(f"{Fore.YELLOW}💾{Style.RESET_ALL}")
            elif metrics.memory_peak < self.memory_targets["high"]:
                info_parts.append(f"{Fore.RED}💾{Style.RESET_ALL}")
            else:
                info_parts.append(f"{Fore.MAGENTA}💾!{Style.RESET_ALL}")
        
        # Performance category
        time_val = metrics.execution_time
        if time_val < self.performance_targets["fast"]:
            info_parts.append(f"{Fore.GREEN}⚡{Style.RESET_ALL}")
        elif time_val < self.performance_targets["medium"]:
            info_parts.append(f"{Fore.YELLOW}🔥{Style.RESET_ALL}")
        elif time_val < self.performance_targets["slow"]:
            info_parts.append(f"{Fore.YELLOW}⏱️{Style.RESET_ALL}")
        else:
            info_parts.append(f"{Fore.RED}🐌{Style.RESET_ALL}")
        
        return f"({', '.join(info_parts)})"
    
    def _get_validation_symbol(self, status: str) -> str:
        """Get colored symbol for validation status."""
        if status == "PASS":
            return f"{Fore.GREEN}✓{Style.RESET_ALL}"
        elif status == "FAIL":
            return f"{Fore.RED}✗{Style.RESET_ALL}"
        elif status == "UNKNOWN":
            return f"{Fore.YELLOW}?{Style.RESET_ALL}"
        else:  # ERROR
            return f"{Fore.MAGENTA}!{Style.RESET_ALL}"
    
    def _print_enhanced_summary(self):
        """Print comprehensive summary with enhanced metrics."""
        if not self.results:
            return
        
        total = len(self.results)
        passed = sum(1 for r in self.results if r.success)
        failed = total - passed
        
        # Architecture analysis
        enhanced_count = sum(1 for r in self.results if r.solution_type.is_enhanced)
        legacy_count = sum(1 for r in self.results if r.solution_type.is_legacy)
        validation_count = sum(1 for r in self.results if r.solution_type.has_validation)
        
        # Performance analysis
        all_times = []
        for r in self.results:
            if r.part1_metrics.execution_time > 0:
                all_times.append(r.part1_metrics.execution_time)
            if r.part2_metrics.execution_time > 0:
                all_times.append(r.part2_metrics.execution_time)
        
        # Memory analysis
        memory_users = [r for r in self.results if r.part1_metrics.memory_peak or r.part2_metrics.memory_peak]
        
        print("\n" + "=" * 80)
        print("🎯 ENHANCED TEST RUNNER SUMMARY")
        print("=" * 80)
        
        # Execution Summary
        print(f"\n📊 EXECUTION SUMMARY")
        print(f"Total solutions: {total}")
        print(f"{Fore.GREEN}✓ Successful: {passed}{Style.RESET_ALL}")
        print(f"{Fore.RED}✗ Failed: {failed}{Style.RESET_ALL}")
        
        # Performance Summary
        if all_times:
            print(f"\n⚡ PERFORMANCE ANALYSIS")
            print(f"Total execution time: {sum(all_times):.3f}s")
            print(f"Average per part: {statistics.mean(all_times):.3f}s")
            print(f"Fastest solution: {min(all_times):.3f}s")
            print(f"Slowest solution: {max(all_times):.3f}s")
            
            # Find and display the slowest solution details
            slowest_time = max(all_times)
            slowest_solution = None
            slowest_part = None
            
            for result in self.results:
                if result.part1_metrics.execution_time == slowest_time:
                    slowest_solution = f"{result.year} Day {result.day}"
                    slowest_part = "Part 1"
                    break
                elif result.part2_metrics.execution_time == slowest_time:
                    slowest_solution = f"{result.year} Day {result.day}"
                    slowest_part = "Part 2"
                    break
            
            if slowest_solution:
                print(f"🐌 Slowest: {slowest_solution} {slowest_part} ({slowest_time:.3f}s)")
            
            # Performance categories
            fast_count = sum(1 for t in all_times if t < self.performance_targets["fast"])
            medium_count = sum(1 for t in all_times if self.performance_targets["fast"] <= t < self.performance_targets["medium"])
            slow_count = sum(1 for t in all_times if self.performance_targets["medium"] <= t < self.performance_targets["slow"])
            very_slow_count = sum(1 for t in all_times if t >= self.performance_targets["slow"])
            
            print(f"⚡ Fast (<100ms): {fast_count}")
            print(f"🔥 Medium (<1s): {medium_count}")
            print(f"⏱️ Slow (<5s): {slow_count}")
            print(f"🐌 Very slow (≥5s): {very_slow_count}")
        
        # Memory Summary
        if memory_users:
            memory_peaks = [r.part1_metrics.memory_peak for r in memory_users if r.part1_metrics.memory_peak]
            memory_peaks.extend([r.part2_metrics.memory_peak for r in memory_users if r.part2_metrics.memory_peak])
            
            if memory_peaks:
                print(f"\n💾 MEMORY ANALYSIS")
                print(f"Solutions monitored: {len(memory_users)}")
                print(f"Average peak memory: {statistics.mean(memory_peaks):.1f}MB")
                print(f"Highest memory usage: {max(memory_peaks):.1f}MB")
                
                # Find and display the highest memory usage details
                highest_memory = max(memory_peaks)
                highest_memory_solution = None
                highest_memory_part = None
                
                for result in memory_users:
                    if result.part1_metrics.memory_peak == highest_memory:
                        highest_memory_solution = f"{result.year} Day {result.day}"
                        highest_memory_part = "Part 1"
                        break
                    elif result.part2_metrics.memory_peak == highest_memory:
                        highest_memory_solution = f"{result.year} Day {result.day}"
                        highest_memory_part = "Part 2"
                        break
                
                if highest_memory_solution:
                    print(f"🏔️ Highest memory: {highest_memory_solution} {highest_memory_part} ({highest_memory:.1f}MB)")
        
        # Regression Summary
        regression_count = sum(1 for r in self.results if r.performance_regression)
        if regression_count > 0:
            print(f"\n⚠️  REGRESSION ANALYSIS")
            print(f"Solutions with performance regressions: {regression_count}")
            for r in self.results:
                if r.performance_regression:
                    print(f"   {r.year} Day {r.day}: {r.performance_regression:.1f}% slower")
        
        # Validation Health - show specific issues
        validation_analysis = self._get_validation_analysis()
        failing_count = len(validation_analysis['failing_validation'])
        missing_count = len(validation_analysis['missing_validation'])
        
        if missing_count > 0 or failing_count > 0:
            print(f"\n📊 VALIDATION HEALTH:")
            
            # Show solutions without validation methods
            if validation_analysis['missing_validation']:
                print(f"{Fore.YELLOW}Solutions without validation methods:{Style.RESET_ALL}")
                for year, day in validation_analysis['missing_validation']:
                    print(f"  {year} Day {day}")
            
            # Show solutions with failing validation
            if validation_analysis['failing_validation']:
                print(f"{Fore.RED}Solutions with failing validation:{Style.RESET_ALL}")
                for year, day in validation_analysis['failing_validation']:
                    print(f"  {year} Day {day}")
        else:
            print(f"\n📊 VALIDATION HEALTH:")
            print(f"{Fore.GREEN}✅ All solutions have working validation{Style.RESET_ALL}")
        
        # Validation Summary
        self._print_validation_summary()
        
        # Performance Distribution Table
        if TABULATE_AVAILABLE:
            self._print_performance_table()
        
        print(f"\n🎉 Enhanced test run complete!")
        print("=" * 80)
    
    def _print_validation_summary(self):
        """Print validation summary with details about failures."""
        total_validations = 0
        correct = 0
        incorrect = 0
        unknown = 0
        errors = 0
        
        # Track specific failures for detailed reporting
        incorrect_tests = []
        unknown_tests = []
        error_tests = []
        
        for result in self.results:
            if result.part1_result is not None:
                total_validations += 1
                status = result.part1_validation.status
                if status == "PASS":
                    correct += 1
                elif status == "FAIL":
                    incorrect += 1
                    incorrect_tests.append(f"{result.year} Day {result.day} Part 1")
                elif status == "UNKNOWN":
                    unknown += 1
                    unknown_tests.append(f"{result.year} Day {result.day} Part 1")
                else:
                    errors += 1
                    error_tests.append(f"{result.year} Day {result.day} Part 1")
            
            if result.part2_result is not None:
                total_validations += 1
                status = result.part2_validation.status
                if status == "PASS":
                    correct += 1
                elif status == "FAIL":
                    incorrect += 1
                    incorrect_tests.append(f"{result.year} Day {result.day} Part 2")
                elif status == "UNKNOWN":
                    unknown += 1
                    unknown_tests.append(f"{result.year} Day {result.day} Part 2")
                else:
                    errors += 1
                    error_tests.append(f"{result.year} Day {result.day} Part 2")
        
        if total_validations > 0:
            print(f"\n✅ SOLUTION SUMMARY")
            print(f"Total solutions: {total_validations}")
            print(f"{Fore.GREEN}✓ Correct: {correct}{Style.RESET_ALL}")
            print(f"{Fore.RED}✗ Incorrect: {incorrect}{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}? Unknown: {unknown}{Style.RESET_ALL}")
            print(f"{Fore.MAGENTA}! Errors: {errors}{Style.RESET_ALL}")
            
            if total_validations > 0:
                accuracy = (correct / total_validations) * 100
                print(f"Accuracy: {accuracy:.1f}%")
            
            # Show detailed failure information
            if incorrect_tests:
                print(f"\n{Fore.RED}✗ Incorrect solutions:{Style.RESET_ALL}")
                for test in sorted(incorrect_tests):
                    print(f"  {test}")
            
            if unknown_tests:
                print(f"\n{Fore.YELLOW}? Unknown solutions:{Style.RESET_ALL}")
                for test in sorted(unknown_tests):
                    print(f"  {test}")
            
            if error_tests:
                print(f"\n{Fore.MAGENTA}! Error solutions:{Style.RESET_ALL}")
                for test in sorted(error_tests):
                    print(f"  {test}")
    
    def _get_solutions_with_validation(self) -> List[Tuple[str, str]]:
        """Get list of problems (year, day) that have validation for at least one part."""
        solutions_with_validation = []
        seen_problems = set()
        
        for result in self.results:
            if result.success:
                problem_key = (result.year, result.day)
                if problem_key not in seen_problems:
                    # Check if this problem has any validation
                    has_part1_validation = (result.part1_result is not None and 
                                          result.part1_validation.status != "UNKNOWN")
                    has_part2_validation = (result.part2_result is not None and 
                                          result.part2_validation.status != "UNKNOWN")
                    
                    if has_part1_validation or has_part2_validation:
                        solutions_with_validation.append(problem_key)
                    
                    seen_problems.add(problem_key)
        
        return sorted(solutions_with_validation)

    def _get_solutions_without_validation(self) -> List[Tuple[str, str]]:
        """Get list of problems (year, day) that don't have validation methods in their AdventSolution class."""
        solutions_without_validation = []
        seen_problems = set()
        
        for result in self.results:
            if result.success:
                problem_key = (result.year, result.day)
                if problem_key not in seen_problems:
                    # Check if this solution has validation method implemented
                    if not result.solution_type.has_validation:
                        solutions_without_validation.append(problem_key)
                    
                    seen_problems.add(problem_key)
        
        return sorted(solutions_without_validation)
    
    def _get_validation_analysis(self) -> Dict[str, List[Tuple[str, str]]]:
        """
        Analyze validation status across all solutions.
        
        Returns:
            Dictionary with 'missing_validation' and 'failing_validation' lists
        """
        missing_validation = []
        failing_validation = []
        seen_problems = set()
        
        for result in self.results:
            if result.success:
                problem_key = (result.year, result.day)
                if problem_key not in seen_problems:
                    # Check if solution has validation method
                    if not result.solution_type.has_validation:
                        missing_validation.append(problem_key)
                    else:
                        # Check if validation actually passes
                        # A solution has failing validation if it has validation method but
                        # the validation results show failures
                        has_validation_failure = False
                        
                        # Check part 1 validation
                        if (result.part1_result is not None and 
                            result.part1_validation.status in ["FAIL", "ERROR"]):
                            has_validation_failure = True
                        
                        # Check part 2 validation  
                        if (result.part2_result is not None and 
                            result.part2_validation.status in ["FAIL", "ERROR"]):
                            has_validation_failure = True
                        
                        # Also check if validation method itself failed during execution
                        if "validation failed" in result.error.lower():
                            has_validation_failure = True
                        
                        if has_validation_failure:
                            failing_validation.append(problem_key)
                    
                    seen_problems.add(problem_key)
        
        return {
            'missing_validation': sorted(missing_validation),
            'failing_validation': sorted(failing_validation)
        }
    
    def _print_performance_table(self):
        """Print detailed performance table using tabulate."""
        headers = ["Year", "Day", "Arch", "P1 Time", "P1 Mem", "P2 Time", "P2 Mem", "Val", "Status"]
        table_data = []
        
        for result in self.results:
            # Architecture type
            arch = "Enhanced" if result.solution_type.is_enhanced else "Legacy"
            if result.solution_type.has_validation:
                arch += " ✓"
            
            # Performance data
            p1_time = f"{result.part1_metrics.execution_time:.3f}s" if result.part1_metrics.execution_time > 0 else "-"
            p2_time = f"{result.part2_metrics.execution_time:.3f}s" if result.part2_metrics.execution_time > 0 else "-"
            
            p1_mem = f"{result.part1_metrics.memory_peak:.1f}MB" if result.part1_metrics.memory_peak else "-"
            p2_mem = f"{result.part2_metrics.memory_peak:.1f}MB" if result.part2_metrics.memory_peak else "-"
            
            # Validation status
            p1_val = result.part1_validation.status[0] if result.part1_validation.status else "-"
            p2_val = result.part2_validation.status[0] if result.part2_validation.status else "-"
            validation = f"{p1_val}/{p2_val}"
            
            # Overall status
            status = "PASS" if result.success else "FAIL"
            if result.performance_regression:
                status += f" ⚠️{result.performance_regression:.0f}%"
            
            table_data.append([
                result.year,
                result.day,
                arch,
                p1_time,
                p1_mem,
                p2_time,
                p2_mem,
                validation,
                status
            ])
        
        print(f"\n📊 DETAILED PERFORMANCE TABLE")
        print(tabulate(table_data, headers=headers, tablefmt='grid'))
        print("Legend: P=Pass, F=Fail, U=Unknown, E=Error, ⚠️=Performance regression")


def main():
    """Main CLI interface for enhanced test runner."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Enhanced Advent of Code Test Runner")
    parser.add_argument("--year", "-y", help="Run only solutions from specific year")
    parser.add_argument("--day", "-d", help="Run only solutions for specific day")
    parser.add_argument("--parallel", "-p", type=int, default=4, help="Number of parallel workers (default: 4)")
    parser.add_argument("--no-parallel", action="store_true", help="Disable parallel execution")
    parser.add_argument("--regression-only", action="store_true", help="Only show solutions with performance regressions")
    parser.add_argument("--enhanced-only", action="store_true", help="Only run enhanced solutions")
    parser.add_argument("--legacy-only", action="store_true", help="Only run legacy solutions (DEPRECATED)")
    parser.add_argument("--strict", action="store_true", default=True, help="Enforce strict AdventSolution architecture (default: True)")
    parser.add_argument("--no-strict", action="store_true", help="Disable strict mode (allow legacy solutions)")
    
    args = parser.parse_args()
    
    # Determine strict mode
    strict_mode = args.strict and not args.no_strict
    
    # Show deprecation warning for legacy-only flag
    if args.legacy_only:
        print(f"{Fore.YELLOW}⚠️  WARNING: --legacy-only flag is deprecated. Legacy solutions are no longer supported.{Style.RESET_ALL}")
        if strict_mode:
            print(f"{Fore.RED}❌ STRICT MODE: Cannot run legacy solutions. Use --no-strict to disable strict mode.{Style.RESET_ALL}")
            return
    
    runner = EnhancedTestRunner(strict_mode=strict_mode)
    
    if args.no_parallel:
        print("Sequential execution mode not implemented in this version")
        print("Using parallel execution with 1 worker")
        args.parallel = 1
    
    if strict_mode:
        print(f"{Fore.CYAN}🔒 STRICT MODE: Only AdventSolution-based solutions will be executed{Style.RESET_ALL}")
    else:
        print(f"{Fore.YELLOW}⚠️  LEGACY MODE: Allowing deprecated solution formats{Style.RESET_ALL}")
    
    runner.run_parallel(
        max_workers=args.parallel,
        year_filter=args.year,
        day_filter=args.day
    )


if __name__ == "__main__":
    main()