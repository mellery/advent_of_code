#!/usr/bin/env python3
"""
Progress tracking dashboard for Advent of Code solutions.

This script provides a visual overview of completion status across all years,
helping identify missing solutions and track overall progress.
"""

import os
import sys
from pathlib import Path
from typing import Dict, List, Set, Tuple
from collections import defaultdict
import calendar

try:
    from colorama import init, Fore, Back, Style
    init()
    COLORS_AVAILABLE = True
except ImportError:
    COLORS_AVAILABLE = False
    # Fallback color constants
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


class ProgressTracker:
    """Track and display Advent of Code progress across all years."""
    
    def __init__(self, root_dir: str = "."):
        self.root_dir = Path(root_dir)
        self.solutions: Dict[str, Set[int]] = defaultdict(set)
        self.discover_solutions()
    
    def discover_solutions(self) -> None:
        """Discover all existing solutions."""
        for year_dir in self.root_dir.iterdir():
            if year_dir.is_dir() and year_dir.name.isdigit() and len(year_dir.name) == 4:
                year = year_dir.name
                
                for file_path in year_dir.glob("*.py"):
                    filename = file_path.name
                    
                    # Skip template and test files
                    if "template" in filename or "test" in filename:
                        continue
                    
                    day = self._extract_day_number(filename)
                    if day and 1 <= day <= 25:
                        self.solutions[year].add(day)
    
    def _extract_day_number(self, filename: str) -> int:
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
                day = int(match.group(1))
                if 1 <= day <= 25:
                    return day
        
        return 0
    
    def get_completion_stats(self) -> Dict[str, Dict[str, int]]:
        """Get completion statistics for each year."""
        stats = {}
        
        for year in sorted(self.solutions.keys()):
            completed = len(self.solutions[year])
            remaining = 25 - completed
            percentage = (completed / 25) * 100
            
            stats[year] = {
                'completed': completed,
                'remaining': remaining, 
                'percentage': percentage
            }
        
        return stats
    
    def print_summary(self) -> None:
        """Print overall progress summary."""
        if not self.solutions:
            print("No solutions found!")
            return
        
        stats = self.get_completion_stats()
        total_completed = sum(s['completed'] for s in stats.values())
        total_possible = len(stats) * 25
        overall_percentage = (total_completed / total_possible) * 100 if total_possible > 0 else 0
        
        print(f"{Style.BRIGHT}=== Advent of Code Progress Summary ==={Style.RESET_ALL}")
        print(f"Years with solutions: {len(stats)}")
        print(f"Total solutions: {total_completed}/{total_possible} ({overall_percentage:.1f}%)")
        print()
        
        # Year-by-year breakdown
        if TABULATE_AVAILABLE:
            headers = ["Year", "Completed", "Remaining", "Progress", "Percentage"]
            table_data = []
            
            for year in sorted(stats.keys()):
                s = stats[year]
                progress_bar = self._create_progress_bar(s['percentage'])
                table_data.append([
                    year,
                    s['completed'],
                    s['remaining'],
                    progress_bar,
                    f"{s['percentage']:.1f}%"
                ])
            
            print(tabulate(table_data, headers=headers, tablefmt='grid'))
        else:
            for year in sorted(stats.keys()):
                s = stats[year]
                progress_bar = self._create_progress_bar(s['percentage'])
                print(f"{year}: {s['completed']:2d}/25 {progress_bar} {s['percentage']:5.1f}%")
    
    def _create_progress_bar(self, percentage: float, width: int = 20) -> str:
        """Create a visual progress bar."""
        if not COLORS_AVAILABLE:
            filled = int((percentage / 100) * width)
            return "[" + "█" * filled + "░" * (width - filled) + "]"
        
        filled = int((percentage / 100) * width)
        bar = ""
        bar += Back.GREEN + " " * filled + Back.RESET
        bar += Back.RED + " " * (width - filled) + Back.RESET
        return "[" + bar + "]"
    
    def print_calendar_view(self, year: str = None) -> None:
        """Print calendar view for a specific year or all years."""
        if year and year in self.solutions:
            self._print_year_calendar(year)
        else:
            for year in sorted(self.solutions.keys()):
                self._print_year_calendar(year)
                print()
    
    def _print_year_calendar(self, year: str) -> None:
        """Print calendar view for a single year."""
        print(f"{Style.BRIGHT}=== {year} Calendar ==={Style.RESET_ALL}")
        
        # Create a 5x5 grid for days 1-25
        grid = []
        for week in range(5):
            row = []
            for day_offset in range(5):
                day = week * 5 + day_offset + 1
                if day <= 25:
                    if day in self.solutions[year]:
                        if COLORS_AVAILABLE:
                            cell = f"{Back.GREEN}{Fore.BLACK} {day:2d} {Style.RESET_ALL}"
                        else:
                            cell = f"[{day:2d}]"
                    else:
                        if COLORS_AVAILABLE:
                            cell = f"{Back.RED}{Fore.WHITE} {day:2d} {Style.RESET_ALL}"
                        else:
                            cell = f" {day:2d} "
                else:
                    cell = "    "
                row.append(cell)
            grid.append(row)
        
        # Print the grid
        for row in grid:
            print(" ".join(row))
        
        completed = len(self.solutions[year])
        print(f"\nCompleted: {completed}/25 ({(completed/25)*100:.1f}%)")
    
    def find_missing_days(self, year: str = None) -> Dict[str, List[int]]:
        """Find missing days for each year."""
        missing = {}
        
        years_to_check = [year] if year else sorted(self.solutions.keys())
        
        for y in years_to_check:
            if y in self.solutions:
                all_days = set(range(1, 26))
                completed_days = self.solutions[y]
                missing_days = sorted(all_days - completed_days)
                missing[y] = missing_days
        
        return missing
    
    def print_missing_days(self, year: str = None) -> None:
        """Print missing days for each year."""
        missing = self.find_missing_days(year)
        
        if not missing:
            print("No missing days found!")
            return
        
        print(f"{Style.BRIGHT}=== Missing Days ==={Style.RESET_ALL}")
        
        for y in sorted(missing.keys()):
            missing_days = missing[y]
            if missing_days:
                days_str = ", ".join(map(str, missing_days))
                print(f"{y}: Days {days_str} ({len(missing_days)} remaining)")
            else:
                print(f"{y}: Complete! 🎉")
    
    def suggest_next_challenges(self, limit: int = 5) -> List[Tuple[str, int]]:
        """Suggest next challenges to work on."""
        suggestions = []
        
        for year in sorted(self.solutions.keys(), reverse=True):  # Start with recent years
            missing_days = self.find_missing_days(year)[year]
            for day in sorted(missing_days)[:limit]:
                suggestions.append((year, day))
                if len(suggestions) >= limit:
                    break
            if len(suggestions) >= limit:
                break
        
        return suggestions
    
    def print_suggestions(self, limit: int = 5) -> None:
        """Print suggested next challenges."""
        suggestions = self.suggest_next_challenges(limit)
        
        if not suggestions:
            print("All caught up! Great job! 🎉")
            return
        
        print(f"{Style.BRIGHT}=== Suggested Next Challenges ==={Style.RESET_ALL}")
        for i, (year, day) in enumerate(suggestions, 1):
            print(f"{i}. {year} Day {day}")
            # Print AoC URL
            print(f"   https://adventofcode.com/{year}/day/{day}")


def main():
    """Main function for the progress tracker."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Advent of Code Progress Tracker")
    parser.add_argument("--year", "-y", help="Focus on specific year")
    parser.add_argument("--calendar", "-c", action="store_true", 
                       help="Show calendar view")
    parser.add_argument("--missing", "-m", action="store_true",
                       help="Show missing days")
    parser.add_argument("--suggest", "-s", action="store_true",
                       help="Suggest next challenges")
    parser.add_argument("--limit", "-l", type=int, default=5,
                       help="Limit suggestions (default: 5)")
    
    args = parser.parse_args()
    
    tracker = ProgressTracker()
    
    if args.calendar:
        tracker.print_calendar_view(args.year)
    elif args.missing:
        tracker.print_missing_days(args.year)
    elif args.suggest:
        tracker.print_suggestions(args.limit)
    else:
        # Default: show summary
        tracker.print_summary()
        print()
        tracker.print_suggestions(3)


if __name__ == "__main__":
    main()