"""
Enhanced timing and performance measurement utilities for Advent of Code solutions.

This module provides comprehensive timing, profiling, and performance analysis tools.
"""

import time
import functools
import statistics
from typing import Dict, List, Callable, Any, Optional, Tuple, Union
from contextlib import contextmanager
import sys
from dataclasses import dataclass, field
from collections import defaultdict


@dataclass
class TimingResult:
    """Container for timing measurement results."""
    function_name: str
    execution_time: float
    args_count: int = 0
    kwargs_count: int = 0
    result: Any = None
    error: Optional[str] = None
    
    def __str__(self) -> str:
        if self.error:
            return f"{self.function_name}: ERROR - {self.error}"
        return f"{self.function_name}: {self.execution_time:.4f}s"


@dataclass
class BenchmarkStats:
    """Container for benchmark statistics."""
    function_name: str
    iterations: int
    times: List[float] = field(default_factory=list)
    
    @property
    def mean(self) -> float:
        return statistics.mean(self.times) if self.times else 0.0
    
    @property
    def median(self) -> float:
        return statistics.median(self.times) if self.times else 0.0
    
    @property
    def min_time(self) -> float:
        return min(self.times) if self.times else 0.0
    
    @property
    def max_time(self) -> float:
        return max(self.times) if self.times else 0.0
    
    @property
    def std_dev(self) -> float:
        return statistics.stdev(self.times) if len(self.times) > 1 else 0.0
    
    def __str__(self) -> str:
        return (f"{self.function_name} ({self.iterations} runs): "
                f"avg={self.mean:.4f}s, "
                f"min={self.min_time:.4f}s, "
                f"max={self.max_time:.4f}s, "
                f"std={self.std_dev:.4f}s")


class PerformanceProfiler:
    """
    Advanced performance profiler for Advent of Code solutions.
    """
    
    def __init__(self):
        self.results: List[TimingResult] = []
        self.benchmarks: Dict[str, BenchmarkStats] = {}
        self._start_times: Dict[str, float] = {}
        
    def clear(self):
        """Clear all stored results."""
        self.results.clear()
        self.benchmarks.clear()
        self._start_times.clear()
    
    @contextmanager
    def timer(self, name: str):
        """
        Context manager for timing code blocks.
        
        Args:
            name: Name for the timing measurement
            
        Example:
            with profiler.timer("parsing"):
                data = parse_input(filename)
        """
        start_time = time.perf_counter()
        try:
            yield
        except Exception as e:
            end_time = time.perf_counter()
            result = TimingResult(
                function_name=name,
                execution_time=end_time - start_time,
                error=str(e)
            )
            self.results.append(result)
            raise
        else:
            end_time = time.perf_counter()
            result = TimingResult(
                function_name=name,
                execution_time=end_time - start_time
            )
            self.results.append(result)
    
    def time_function(self, func: Callable, *args, **kwargs) -> TimingResult:
        """
        Time a single function execution.
        
        Args:
            func: Function to time
            *args: Function arguments
            **kwargs: Function keyword arguments
            
        Returns:
            TimingResult with execution details
        """
        start_time = time.perf_counter()
        
        try:
            result = func(*args, **kwargs)
            end_time = time.perf_counter()
            
            timing_result = TimingResult(
                function_name=func.__name__,
                execution_time=end_time - start_time,
                args_count=len(args),
                kwargs_count=len(kwargs),
                result=result
            )
            
        except Exception as e:
            end_time = time.perf_counter()
            timing_result = TimingResult(
                function_name=func.__name__,
                execution_time=end_time - start_time,
                args_count=len(args),
                kwargs_count=len(kwargs),
                error=str(e)
            )
            raise
        
        self.results.append(timing_result)
        return timing_result
    
    def benchmark_function(self, func: Callable, iterations: int = 100,
                          *args, **kwargs) -> BenchmarkStats:
        """
        Benchmark a function over multiple iterations.
        
        Args:
            func: Function to benchmark
            iterations: Number of iterations to run
            *args: Function arguments
            **kwargs: Function keyword arguments
            
        Returns:
            BenchmarkStats with statistical analysis
        """
        times = []
        
        # Warm-up run
        try:
            func(*args, **kwargs)
        except:
            pass  # Ignore warm-up errors
        
        for _ in range(iterations):
            start_time = time.perf_counter()
            try:
                func(*args, **kwargs)
                end_time = time.perf_counter()
                times.append(end_time - start_time)
            except Exception:
                # Skip failed iterations
                continue
        
        stats = BenchmarkStats(
            function_name=func.__name__,
            iterations=len(times),
            times=times
        )
        
        self.benchmarks[func.__name__] = stats
        return stats
    
    def compare_functions(self, functions: List[Callable], iterations: int = 100,
                         *args, **kwargs) -> Dict[str, BenchmarkStats]:
        """
        Compare performance of multiple functions.
        
        Args:
            functions: List of functions to compare
            iterations: Number of iterations per function
            *args: Function arguments
            **kwargs: Function keyword arguments
            
        Returns:
            Dictionary of function names to benchmark stats
        """
        results = {}
        
        for func in functions:
            stats = self.benchmark_function(func, iterations, *args, **kwargs)
            results[func.__name__] = stats
        
        return results
    
    def print_summary(self, sort_by: str = 'time'):
        """
        Print a summary of all timing results.
        
        Args:
            sort_by: Sort results by 'time', 'name', or 'order'
        """
        if not self.results and not self.benchmarks:
            print("No timing results to display")
            return
        
        print("\n" + "="*60)
        print("PERFORMANCE SUMMARY")
        print("="*60)
        
        if self.results:
            print("\nFunction Timings:")
            print("-"*40)
            
            sorted_results = self.results
            if sort_by == 'time':
                sorted_results = sorted(self.results, key=lambda x: x.execution_time, reverse=True)
            elif sort_by == 'name':
                sorted_results = sorted(self.results, key=lambda x: x.function_name)
            
            for result in sorted_results:
                if result.error:
                    print(f"❌ {result}")
                else:
                    print(f"✅ {result}")
        
        if self.benchmarks:
            print("\nBenchmark Results:")
            print("-"*40)
            
            sorted_benchmarks = sorted(self.benchmarks.values(), 
                                     key=lambda x: x.mean, reverse=True)
            
            for stats in sorted_benchmarks:
                print(f"📊 {stats}")
        
        total_time = sum(r.execution_time for r in self.results if not r.error)
        if total_time > 0:
            print(f"\nTotal measured time: {total_time:.4f}s")


# Global profiler instance
_global_profiler = PerformanceProfiler()


def timer(func: Callable) -> Callable:
    """
    Decorator to time function execution.
    
    Args:
        func: Function to time
        
    Returns:
        Wrapped function that records timing
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return _global_profiler.time_function(func, *args, **kwargs).result
    
    return wrapper


def benchmark(iterations: int = 100):
    """
    Decorator to benchmark function execution.
    
    Args:
        iterations: Number of iterations to run
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Run benchmark
            stats = _global_profiler.benchmark_function(func, iterations, *args, **kwargs)
            print(f"Benchmark: {stats}")
            
            # Return single execution result
            return func(*args, **kwargs)
        
        return wrapper
    
    return decorator


@contextmanager
def time_block(name: str):
    """
    Context manager to time a block of code.
    
    Args:
        name: Name for the timing measurement
    """
    with _global_profiler.timer(name):
        yield


def measure_memory_usage(func: Callable, *args, **kwargs) -> Tuple[Any, float]:
    """
    Measure memory usage of a function (if psutil is available).
    
    Args:
        func: Function to measure
        *args: Function arguments
        **kwargs: Function keyword arguments
        
    Returns:
        Tuple of (result, memory_usage_mb)
    """
    try:
        import psutil
        import os
        
        process = psutil.Process(os.getpid())
        mem_before = process.memory_info().rss / 1024 / 1024  # MB
        
        result = func(*args, **kwargs)
        
        mem_after = process.memory_info().rss / 1024 / 1024  # MB
        memory_used = mem_after - mem_before
        
        return result, memory_used
        
    except ImportError:
        # psutil not available, just return result
        result = func(*args, **kwargs)
        return result, 0.0


def profile_solution(part1_func: Callable, part2_func: Callable, 
                    input_data: str, iterations: int = 5) -> Dict[str, Any]:
    """
    Comprehensive profiling of a complete solution.
    
    Args:
        part1_func: Part 1 function
        part2_func: Part 2 function
        input_data: Input data
        iterations: Number of iterations for benchmarking
        
    Returns:
        Dictionary with comprehensive profiling results
    """
    profiler = PerformanceProfiler()
    
    # Single execution timing
    result1_timing = profiler.time_function(part1_func, input_data)
    result2_timing = profiler.time_function(part2_func, input_data)
    
    # Benchmark if iterations > 1
    if iterations > 1:
        stats1 = profiler.benchmark_function(part1_func, iterations, input_data)
        stats2 = profiler.benchmark_function(part2_func, iterations, input_data)
    else:
        stats1 = stats2 = None
    
    # Memory usage (if available)
    result1, mem1 = measure_memory_usage(part1_func, input_data)
    result2, mem2 = measure_memory_usage(part2_func, input_data)
    
    return {
        'part1': {
            'result': result1,
            'single_time': result1_timing.execution_time,
            'memory_mb': mem1,
            'benchmark': stats1
        },
        'part2': {
            'result': result2,
            'single_time': result2_timing.execution_time,
            'memory_mb': mem2,
            'benchmark': stats2
        },
        'total_time': result1_timing.execution_time + result2_timing.execution_time,
        'total_memory_mb': mem1 + mem2
    }


def print_performance_report(profile_data: Dict[str, Any]):
    """
    Print a formatted performance report.
    
    Args:
        profile_data: Data from profile_solution()
    """
    print("\n" + "="*50)
    print("SOLUTION PERFORMANCE REPORT")
    print("="*50)
    
    for part_name in ['part1', 'part2']:
        if part_name in profile_data:
            part_data = profile_data[part_name]
            print(f"\n{part_name.upper()}:")
            print(f"  Result: {part_data['result']}")
            print(f"  Time: {part_data['single_time']:.4f}s")
            
            if part_data['memory_mb'] > 0:
                print(f"  Memory: {part_data['memory_mb']:.2f} MB")
            
            if part_data['benchmark']:
                stats = part_data['benchmark']
                print(f"  Benchmark ({stats.iterations} runs):")
                print(f"    Average: {stats.mean:.4f}s")
                print(f"    Range: {stats.min_time:.4f}s - {stats.max_time:.4f}s")
                print(f"    Std Dev: {stats.std_dev:.4f}s")
    
    print(f"\nTOTAL TIME: {profile_data['total_time']:.4f}s")
    if profile_data['total_memory_mb'] > 0:
        print(f"TOTAL MEMORY: {profile_data['total_memory_mb']:.2f} MB")


# Utility functions for quick access
def get_profiler() -> PerformanceProfiler:
    """Get the global profiler instance."""
    return _global_profiler


def clear_profiler():
    """Clear all profiler data."""
    _global_profiler.clear()


def print_profiler_summary():
    """Print summary of global profiler data."""
    _global_profiler.print_summary()