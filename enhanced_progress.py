#!/usr/bin/env python3
"""
Enhanced Progress Tracker for Advent of Code Solutions

Advanced progress tracking with algorithm library integration, performance analysis,
solution architecture detection, and comprehensive reporting capabilities.

Key Features:
- Integration with enhanced test runner and algorithm libraries
- Solution architecture analysis (legacy vs enhanced vs modern)
- Performance metrics and trend analysis
- Migration planning and tracking
- Advanced reporting with multiple output formats
- Solution difficulty and algorithm pattern analysis
"""

import os
import sys
import json
import time
from pathlib import Path
from typing import Dict, List, Set, Tuple, Optional, Any
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum

try:
    from colorama import init, Fore, Back, Style
    init()
    COLORS_AVAILABLE = True
except ImportError:
    COLORS_AVAILABLE = False
    class Fore:
        GREEN = RED = YELLOW = BLUE = CYAN = MAGENTA = WHITE = RESET = ""
    class Back:
        GREEN = RED = YELLOW = BLUE = CYAN = MAGENTA = WHITE = BLACK = RESET = ""
    class Style:
        BRIGHT = DIM = RESET_ALL = ""

try:
    from tabulate import tabulate
    TABULATE_AVAILABLE = True
except ImportError:
    TABULATE_AVAILABLE = False

# Add utils to path for algorithm library detection
sys.path.append(str(Path(__file__).parent))

# Try to import enhanced test runner for integration
try:
    from enhanced_test_runner import EnhancedTestRunner
    ENHANCED_RUNNER_AVAILABLE = True
except ImportError:
    ENHANCED_RUNNER_AVAILABLE = False

# Try to import algorithm libraries for analysis
try:
    from utils.algorithms import ALGORITHMS_AVAILABLE
    if ALGORITHMS_AVAILABLE:
        from utils import pathfinding, grid, vm, parsing, math_utils
except ImportError:
    ALGORITHMS_AVAILABLE = False

class SolutionType(Enum):
    """Types of solution architectures."""
    LEGACY = "legacy"
    ENHANCED = "enhanced"
    MODERN_LEGACY = "modern_legacy"
    UNKNOWN = "unknown"

class PerformanceCategory(Enum):
    """Performance categories from PERFORMANCE_BENCHMARKS.md."""
    FAST = "fast"      # < 100ms
    MEDIUM = "medium"  # 100ms - 1s
    SLOW = "slow"      # 1s - 5s
    VERY_SLOW = "very_slow"  # > 5s

@dataclass
class SolutionInfo:
    """Comprehensive information about a solution."""
    year: int
    day: int
    file_path: Path
    architecture_type: SolutionType = SolutionType.UNKNOWN
    has_validation: bool = False
    has_part1: bool = False
    has_part2: bool = False
    uses_algorithm_libs: bool = False
    algorithm_patterns: List[str] = field(default_factory=list)
    performance_category: Optional[PerformanceCategory] = None
    execution_time: Optional[float] = None
    memory_usage: Optional[float] = None
    last_modified: Optional[datetime] = None
    input_file_exists: bool = False
    test_status: Optional[str] = None
    validation_accuracy: Optional[float] = None

@dataclass
class YearSummary:
    """Summary statistics for a year."""
    year: int
    total_solutions: int = 0
    solutions_by_type: Dict[SolutionType, int] = field(default_factory=lambda: defaultdict(int))
    performance_distribution: Dict[PerformanceCategory, int] = field(default_factory=lambda: defaultdict(int))
    algorithm_usage: Dict[str, int] = field(default_factory=lambda: defaultdict(int))
    missing_days: List[int] = field(default_factory=list)
    average_performance: Optional[float] = None
    migration_candidates: List[int] = field(default_factory=list)

class EnhancedProgressTracker:
    """Enhanced progress tracker with algorithm library integration."""
    
    def __init__(self, root_dir: str = "."):
        self.root_dir = Path(root_dir)
        self.solutions: Dict[str, Dict[int, SolutionInfo]] = defaultdict(dict)
        self.year_summaries: Dict[int, YearSummary] = {}
        self.performance_history: Dict[str, List[Dict]] = {}
        
        # Load performance history if available
        self._load_performance_history()
        
        # Discover and analyze all solutions
        self.discover_solutions()
        self.analyze_solutions()
        self.generate_summaries()
    
    def _load_performance_history(self) -> None:
        """Load performance history from enhanced test runner."""
        history_file = self.root_dir / "test_performance_history.json"
        if history_file.exists():
            try:
                with open(history_file) as f:
                    self.performance_history = json.load(f)
            except (json.JSONDecodeError, IOError):
                self.performance_history = {}
    
    def discover_solutions(self) -> None:
        """Discover all existing solutions with enhanced detection."""
        for year_dir in self.root_dir.iterdir():
            if year_dir.is_dir() and year_dir.name.isdigit() and len(year_dir.name) == 4:
                year = int(year_dir.name)
                
                for file_path in year_dir.glob("*.py"):
                    filename = file_path.name
                    
                    # Skip template and test files
                    if any(skip in filename.lower() for skip in 
                          ["template", "test", "__pycache__", "intcode"]):
                        continue
                    
                    day = self._extract_day_number(filename)
                    if day and 1 <= day <= 25:
                        solution_info = SolutionInfo(
                            year=year,
                            day=day,
                            file_path=file_path,
                            last_modified=datetime.fromtimestamp(file_path.stat().st_mtime)
                        )
                        
                        # Check for input file
                        input_file = year_dir / f"day{day}_input.txt"
                        solution_info.input_file_exists = input_file.exists()
                        
                        self.solutions[str(year)][day] = solution_info
    
    def _extract_day_number(self, filename: str) -> Optional[int]:
        """Extract day number from filename with enhanced patterns."""
        import re
        
        patterns = [
            r"day(\d+)\.py",
            r"advent(\d+)\.py", 
            r"(\d+)\.py"
        ]
        
        for pattern in patterns:
            match = re.match(pattern, filename)
            if match:
                day = int(match.group(1))
                if 1 <= day <= 25:
                    return day
        
        return None
    
    def analyze_solutions(self) -> None:
        """Analyze solution architecture and patterns."""
        for year_str, year_solutions in self.solutions.items():
            for day, solution_info in year_solutions.items():
                self._analyze_single_solution(solution_info)
    
    def _analyze_single_solution(self, solution_info: SolutionInfo) -> None:
        """Analyze a single solution's architecture and patterns."""
        try:
            content = solution_info.file_path.read_text()
            
            # Detect architecture type
            solution_info.architecture_type = self._detect_architecture_type(content)
            
            # Check for part1/part2 functions
            solution_info.has_part1 = "def part1(" in content
            solution_info.has_part2 = "def part2(" in content
            
            # Check for validation
            solution_info.has_validation = any(pattern in content for pattern in [
                "def validate(", "def test(", "assert ", "TestCase"
            ])
            
            # Detect algorithm library usage
            if ALGORITHMS_AVAILABLE:
                solution_info.uses_algorithm_libs = self._detect_algorithm_usage(content)
                solution_info.algorithm_patterns = self._detect_algorithm_patterns(content)
            
            # Get performance data if available
            self._get_performance_data(solution_info)
            
        except (IOError, UnicodeDecodeError) as e:
            print(f"Warning: Could not analyze {solution_info.file_path}: {e}")
    
    def _detect_architecture_type(self, content: str) -> SolutionType:
        """Detect the architecture type of a solution."""
        # Enhanced architecture indicators
        if "class Day" in content and "AdventSolution" in content:
            return SolutionType.ENHANCED
        
        # Modern legacy (updated but not full enhanced)
        if any(pattern in content for pattern in [
            "from utils import", "InputParser", "timer", "benchmark"
        ]):
            return SolutionType.MODERN_LEGACY
        
        # Legacy architecture
        if any(pattern in content for pattern in [
            "def part1(filename", "def part2(filename", "get_list_of_numbers"
        ]):
            return SolutionType.LEGACY
        
        return SolutionType.UNKNOWN
    
    def _detect_algorithm_usage(self, content: str) -> bool:
        """Detect if solution uses algorithm libraries."""
        algorithm_imports = [
            "from utils.algorithms",
            "from utils import Grid",
            "from utils import dijkstra_grid",
            "from utils import IntcodeVM",
            "from utils import gcd",
            "from utils import fibonacci"
        ]
        
        return any(pattern in content for pattern in algorithm_imports)
    
    def _detect_algorithm_patterns(self, content: str) -> List[str]:
        """Detect which algorithm patterns are used."""
        patterns = []
        
        # Pathfinding algorithms
        if any(func in content for func in ["dijkstra", "bfs_shortest", "a_star", "find_path"]):
            patterns.append("pathfinding")
        
        # Grid operations
        if any(func in content for func in ["Grid(", "parse_grid", "neighbors_", "flood_fill"]):
            patterns.append("grid")
        
        # Virtual machines
        if any(func in content for func in ["IntcodeVM", "SimpleAssemblyVM", "run_intcode"]):
            patterns.append("vm")
        
        # Mathematical functions
        if any(func in content for func in ["gcd(", "lcm(", "fibonacci(", "is_prime"]):
            patterns.append("math")
        
        # Parsing utilities
        if any(func in content for func in ["ExpressionEvaluator", "PatternMatcher", "parse_numbers"]):
            patterns.append("parsing")
        
        return patterns
    
    def _get_performance_data(self, solution_info: SolutionInfo) -> None:
        """Get performance data from test runner history."""
        key = f"{solution_info.year}_day{solution_info.day}"
        
        if key in self.performance_history:
            history = self.performance_history[key]
            if history:
                # Get most recent performance data
                latest = history[-1]
                solution_info.execution_time = latest.get("execution_time")
                
                # Categorize performance
                if solution_info.execution_time:
                    if solution_info.execution_time < 0.1:
                        solution_info.performance_category = PerformanceCategory.FAST
                    elif solution_info.execution_time < 1.0:
                        solution_info.performance_category = PerformanceCategory.MEDIUM
                    elif solution_info.execution_time < 5.0:
                        solution_info.performance_category = PerformanceCategory.SLOW
                    else:
                        solution_info.performance_category = PerformanceCategory.VERY_SLOW
    
    def generate_summaries(self) -> None:
        """Generate summary statistics for each year."""
        for year_str, year_solutions in self.solutions.items():
            year = int(year_str)
            summary = YearSummary(year=year)
            
            # Basic counts
            summary.total_solutions = len(year_solutions)
            
            # Missing days
            all_days = set(range(1, 26))
            completed_days = set(year_solutions.keys())
            summary.missing_days = sorted(all_days - completed_days)
            
            # Analyze each solution
            execution_times = []
            for solution_info in year_solutions.values():
                # Architecture distribution
                summary.solutions_by_type[solution_info.architecture_type] += 1
                
                # Performance distribution
                if solution_info.performance_category:
                    summary.performance_distribution[solution_info.performance_category] += 1
                    
                if solution_info.execution_time:
                    execution_times.append(solution_info.execution_time)
                
                # Algorithm usage
                for pattern in solution_info.algorithm_patterns:
                    summary.algorithm_usage[pattern] += 1
                
                # Migration candidates (legacy solutions)
                if solution_info.architecture_type == SolutionType.LEGACY:
                    summary.migration_candidates.append(solution_info.day)
            
            # Average performance
            if execution_times:
                summary.average_performance = sum(execution_times) / len(execution_times)
            
            self.year_summaries[year] = summary
    
    def print_enhanced_summary(self) -> None:
        """Print comprehensive progress summary with enhanced metrics."""
        if not self.solutions:
            print("No solutions found!")
            return
        
        total_solutions = sum(len(year_sols) for year_sols in self.solutions.values())
        total_possible = len(self.solutions) * 25
        overall_percentage = (total_solutions / total_possible) * 100 if total_possible > 0 else 0
        
        print(f"{Style.BRIGHT}🎄 Enhanced Advent of Code Progress Dashboard 🎄{Style.RESET_ALL}")
        print("=" * 70)
        print(f"📊 Years with solutions: {len(self.solutions)}")
        print(f"🎯 Total solutions: {total_solutions}/{total_possible} ({overall_percentage:.1f}%)")
        
        # Architecture distribution
        arch_counts = defaultdict(int)
        for year_solutions in self.solutions.values():
            for solution in year_solutions.values():
                arch_counts[solution.architecture_type] += 1
        
        print(f"\n🏗️  Architecture Distribution:")
        for arch_type, count in arch_counts.items():
            percentage = (count / total_solutions) * 100 if total_solutions > 0 else 0
            icon = self._get_architecture_icon(arch_type)
            print(f"   {icon} {arch_type.value.title()}: {count} ({percentage:.1f}%)")
        
        # Algorithm library usage
        if ALGORITHMS_AVAILABLE:
            algo_users = sum(1 for year_sols in self.solutions.values() 
                           for sol in year_sols.values() if sol.uses_algorithm_libs)
            algo_percentage = (algo_users / total_solutions) * 100 if total_solutions > 0 else 0
            print(f"\n🧮 Algorithm Library Usage: {algo_users}/{total_solutions} ({algo_percentage:.1f}%)")
        
        print("\n" + "=" * 70)
    
    def _get_architecture_icon(self, arch_type: SolutionType) -> str:
        """Get icon for architecture type."""
        icons = {
            SolutionType.ENHANCED: "🚀",
            SolutionType.MODERN_LEGACY: "⚡",
            SolutionType.LEGACY: "📜",
            SolutionType.UNKNOWN: "❓"
        }
        return icons.get(arch_type, "❓")
    
    def print_detailed_year_analysis(self, year: Optional[int] = None) -> None:
        """Print detailed analysis for specific year or all years."""
        years_to_analyze = [year] if year else sorted(self.year_summaries.keys())
        
        for y in years_to_analyze:
            if y not in self.year_summaries:
                continue
                
            summary = self.year_summaries[y]
            print(f"\n{Style.BRIGHT}📅 {y} Detailed Analysis{Style.RESET_ALL}")
            print("-" * 50)
            
            # Basic stats
            completion_rate = (summary.total_solutions / 25) * 100
            print(f"📈 Completion: {summary.total_solutions}/25 ({completion_rate:.1f}%)")
            
            if summary.average_performance:
                print(f"⏱️  Average performance: {summary.average_performance:.3f}s")
            
            # Architecture breakdown
            if summary.solutions_by_type:
                print(f"\n🏗️  Architecture Breakdown:")
                for arch_type, count in summary.solutions_by_type.items():
                    if count > 0:
                        icon = self._get_architecture_icon(arch_type)
                        print(f"   {icon} {arch_type.value.title()}: {count}")
            
            # Performance distribution
            if any(summary.performance_distribution.values()):
                print(f"\n⚡ Performance Distribution:")
                perf_icons = {
                    PerformanceCategory.FAST: "⚡",
                    PerformanceCategory.MEDIUM: "🔥", 
                    PerformanceCategory.SLOW: "⏱️",
                    PerformanceCategory.VERY_SLOW: "🐌"
                }
                for perf_cat, count in summary.performance_distribution.items():
                    if count > 0:
                        icon = perf_icons.get(perf_cat, "❓")
                        print(f"   {icon} {perf_cat.value.replace('_', ' ').title()}: {count}")
            
            # Algorithm usage
            if summary.algorithm_usage:
                print(f"\n🧮 Algorithm Pattern Usage:")
                for pattern, count in summary.algorithm_usage.items():
                    print(f"   📐 {pattern.title()}: {count}")
            
            # Migration opportunities
            if summary.migration_candidates:
                print(f"\n🔄 Migration Candidates ({len(summary.migration_candidates)}):")
                candidates_str = ", ".join(map(str, sorted(summary.migration_candidates)))
                print(f"   Days: {candidates_str}")
            
            # Missing days
            if summary.missing_days:
                print(f"\n❌ Missing Days ({len(summary.missing_days)}):")
                missing_str = ", ".join(map(str, summary.missing_days))
                print(f"   Days: {missing_str}")
    
    def print_performance_analysis(self) -> None:
        """Print performance analysis across all solutions."""
        print(f"\n{Style.BRIGHT}⚡ Performance Analysis{Style.RESET_ALL}")
        print("-" * 50)
        
        all_solutions = []
        for year_solutions in self.solutions.values():
            all_solutions.extend(year_solutions.values())
        
        # Solutions with performance data
        perf_solutions = [s for s in all_solutions if s.execution_time is not None]
        
        if not perf_solutions:
            print("No performance data available. Run enhanced test runner to collect metrics.")
            return
        
        print(f"📊 Solutions with performance data: {len(perf_solutions)}/{len(all_solutions)}")
        
        # Performance statistics
        execution_times = [s.execution_time for s in perf_solutions]
        avg_time = sum(execution_times) / len(execution_times)
        max_time = max(execution_times)
        min_time = min(execution_times)
        
        print(f"⏱️  Average execution time: {avg_time:.3f}s")
        print(f"🏃 Fastest solution: {min_time:.3f}s")
        print(f"🐌 Slowest solution: {max_time:.3f}s")
        
        # Find slowest solutions
        slow_solutions = [(s.year, s.day, s.execution_time) for s in perf_solutions 
                         if s.execution_time > 5.0]
        
        if slow_solutions:
            print(f"\n🎯 Optimization Candidates (>5s):")
            for year, day, time_taken in sorted(slow_solutions, key=lambda x: x[2], reverse=True):
                print(f"   {year} Day {day}: {time_taken:.3f}s")
    
    def print_algorithm_analysis(self) -> None:
        """Print algorithm library usage analysis."""
        if not ALGORITHMS_AVAILABLE:
            print("Algorithm libraries not available for analysis.")
            return
        
        print(f"\n{Style.BRIGHT}🧮 Algorithm Library Analysis{Style.RESET_ALL}")
        print("-" * 50)
        
        all_solutions = []
        for year_solutions in self.solutions.values():
            all_solutions.extend(year_solutions.values())
        
        algo_solutions = [s for s in all_solutions if s.uses_algorithm_libs]
        print(f"📊 Solutions using algorithm libraries: {len(algo_solutions)}/{len(all_solutions)}")
        
        if not algo_solutions:
            print("No solutions currently use algorithm libraries.")
            print("Consider migrating legacy solutions to take advantage of:")
            print("  🗺️  High-performance pathfinding algorithms")
            print("  🔲 Advanced grid manipulation utilities")  
            print("  🤖 Complete virtual machine implementations")
            print("  🔢 Mathematical and parsing utilities")
            return
        
        # Pattern usage across all solutions
        all_patterns = defaultdict(int)
        for solution in all_solutions:
            for pattern in solution.algorithm_patterns:
                all_patterns[pattern] += 1
        
        if all_patterns:
            print(f"\n📐 Algorithm Pattern Usage:")
            pattern_icons = {
                "pathfinding": "🗺️",
                "grid": "🔲",
                "vm": "🤖", 
                "math": "🔢",
                "parsing": "📝"
            }
            
            for pattern, count in sorted(all_patterns.items(), key=lambda x: x[1], reverse=True):
                icon = pattern_icons.get(pattern, "📐")
                print(f"   {icon} {pattern.title()}: {count} solutions")
    
    def suggest_next_actions(self, limit: int = 5) -> None:
        """Suggest next actions for improvement."""
        print(f"\n{Style.BRIGHT}🎯 Suggested Next Actions{Style.RESET_ALL}")
        print("-" * 50)
        
        suggestions = []
        
        # Suggest missing solutions
        for year, summary in sorted(self.year_summaries.items(), reverse=True):
            for day in summary.missing_days[:3]:  # Top 3 missing per year
                suggestions.append(f"🎄 Solve {year} Day {day}")
                if len(suggestions) >= limit:
                    break
            if len(suggestions) >= limit:
                break
        
        # Suggest migrations
        migration_candidates = []
        for year, summary in self.year_summaries.items():
            for day in summary.migration_candidates[:2]:  # Top 2 per year
                migration_candidates.append((year, day))
        
        if migration_candidates:
            year, day = migration_candidates[0]
            suggestions.append(f"🔄 Migrate {year} Day {day} to enhanced architecture")
        
        # Suggest performance optimizations
        slow_solutions = []
        for year_solutions in self.solutions.values():
            for solution in year_solutions.values():
                if (solution.execution_time and solution.execution_time > 5.0 and 
                    solution.architecture_type == SolutionType.LEGACY):
                    slow_solutions.append((solution.year, solution.day, solution.execution_time))
        
        if slow_solutions:
            slow_solutions.sort(key=lambda x: x[2], reverse=True)
            year, day, time_taken = slow_solutions[0]
            suggestions.append(f"⚡ Optimize {year} Day {day} ({time_taken:.1f}s → target <1s)")
        
        # Print suggestions
        for i, suggestion in enumerate(suggestions[:limit], 1):
            print(f"{i}. {suggestion}")
        
        if not suggestions:
            print("🎉 All caught up! Great work!")
    
    def export_json_report(self, output_file: Optional[str] = None) -> None:
        """Export detailed progress report as JSON."""
        if not output_file:
            output_file = f"progress_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        report = {
            "generated_at": datetime.now().isoformat(),
            "summary": {
                "total_years": len(self.solutions),
                "total_solutions": sum(len(year_sols) for year_sols in self.solutions.values()),
                "total_possible": len(self.solutions) * 25
            },
            "years": {}
        }
        
        for year_str, year_solutions in self.solutions.items():
            year_data = {
                "solutions": {},
                "summary": {}
            }
            
            for day, solution_info in year_solutions.items():
                year_data["solutions"][str(day)] = {
                    "architecture_type": solution_info.architecture_type.value,
                    "has_validation": solution_info.has_validation,
                    "has_part1": solution_info.has_part1,
                    "has_part2": solution_info.has_part2,
                    "uses_algorithm_libs": solution_info.uses_algorithm_libs,
                    "algorithm_patterns": solution_info.algorithm_patterns,
                    "performance_category": solution_info.performance_category.value if solution_info.performance_category else None,
                    "execution_time": solution_info.execution_time,
                    "input_file_exists": solution_info.input_file_exists,
                    "last_modified": solution_info.last_modified.isoformat() if solution_info.last_modified else None
                }
            
            if year_str in [str(y) for y in self.year_summaries.keys()]:
                summary = self.year_summaries[int(year_str)]
                year_data["summary"] = {
                    "total_solutions": summary.total_solutions,
                    "missing_days": summary.missing_days,
                    "average_performance": summary.average_performance,
                    "migration_candidates": summary.migration_candidates,
                    "solutions_by_type": {k.value: v for k, v in summary.solutions_by_type.items()},
                    "algorithm_usage": dict(summary.algorithm_usage)
                }
            
            report["years"][year_str] = year_data
        
        with open(output_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"📄 Detailed report exported to {output_file}")

def main():
    """Main function for enhanced progress tracker."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Enhanced Advent of Code Progress Tracker")
    parser.add_argument("--year", "-y", type=int, help="Focus on specific year")
    parser.add_argument("--summary", "-s", action="store_true", 
                       help="Show enhanced summary (default)")
    parser.add_argument("--detailed", "-d", action="store_true",
                       help="Show detailed year analysis")
    parser.add_argument("--performance", "-p", action="store_true",
                       help="Show performance analysis")
    parser.add_argument("--algorithms", "-a", action="store_true",
                       help="Show algorithm library analysis")
    parser.add_argument("--suggest", "-g", action="store_true",
                       help="Suggest next actions")
    parser.add_argument("--export", "-e", action="store_true",
                       help="Export JSON report")
    parser.add_argument("--output", "-o", help="Output file for export")
    parser.add_argument("--limit", "-l", type=int, default=5,
                       help="Limit suggestions (default: 5)")
    
    args = parser.parse_args()
    
    tracker = EnhancedProgressTracker()
    
    # Default behavior: show summary
    if not any([args.detailed, args.performance, args.algorithms, args.suggest, args.export]):
        args.summary = True
    
    if args.summary:
        tracker.print_enhanced_summary()
    
    if args.detailed:
        tracker.print_detailed_year_analysis(args.year)
    
    if args.performance:
        tracker.print_performance_analysis()
    
    if args.algorithms:
        tracker.print_algorithm_analysis()
    
    if args.suggest:
        tracker.suggest_next_actions(args.limit)
    
    if args.export:
        tracker.export_json_report(args.output)

if __name__ == "__main__":
    main()