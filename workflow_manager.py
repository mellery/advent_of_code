#!/usr/bin/env python3
"""
Unified Workflow Manager for Advent of Code

Central command interface that integrates all enhanced tools:
- Enhanced progress tracking
- Input management
- Solution generation
- Migration tracking
- Algorithm library integration
- Enhanced test runner integration

Key Features:
- Unified command interface for all tools
- Automated workflow recommendations
- Cross-tool integration and data sharing
- Progress tracking across all aspects
- Smart suggestions based on current state
- Batch operations and automation
"""

import os
import sys
import argparse
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime

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

# Add current directory to path
sys.path.append(str(Path(__file__).parent))

# Import enhanced tools
try:
    from enhanced_progress import EnhancedProgressTracker
    PROGRESS_AVAILABLE = True
except ImportError:
    PROGRESS_AVAILABLE = False

try:
    from enhanced_input_manager import EnhancedInputManager
    INPUT_MANAGER_AVAILABLE = True
except ImportError:
    INPUT_MANAGER_AVAILABLE = False

try:
    from solution_generator import SolutionTemplateGenerator
    GENERATOR_AVAILABLE = True
except ImportError:
    GENERATOR_AVAILABLE = False

try:
    from migration_tracker import MigrationTracker
    MIGRATION_AVAILABLE = True
except ImportError:
    MIGRATION_AVAILABLE = False

try:
    from enhanced_test_runner import EnhancedTestRunner
    TEST_RUNNER_AVAILABLE = True
except ImportError:
    TEST_RUNNER_AVAILABLE = False

# Try to import algorithm libraries for status
try:
    from utils.algorithms import ALGORITHMS_AVAILABLE
except ImportError:
    ALGORITHMS_AVAILABLE = False

class WorkflowManager:
    """Unified workflow manager for AoC development."""
    
    def __init__(self, root_dir: str = "."):
        self.root_dir = Path(root_dir)
        
        # Initialize all available tools
        self.progress_tracker = None
        self.input_manager = None
        self.solution_generator = None
        self.migration_tracker = None
        
        if PROGRESS_AVAILABLE:
            self.progress_tracker = EnhancedProgressTracker(str(self.root_dir))
        
        if INPUT_MANAGER_AVAILABLE:
            self.input_manager = EnhancedInputManager(root_dir=str(self.root_dir))
        
        if GENERATOR_AVAILABLE:
            self.solution_generator = SolutionTemplateGenerator(str(self.root_dir))
        
        if MIGRATION_AVAILABLE:
            self.migration_tracker = MigrationTracker(str(self.root_dir))
    
    def print_status_dashboard(self) -> None:
        """Print comprehensive status dashboard."""
        print(f"{Style.BRIGHT}🎄 Advent of Code Workflow Dashboard 🎄{Style.RESET_ALL}")
        print("=" * 80)
        
        # Tool availability status
        print(f"\n🔧 Tool Status:")
        tools = [
            ("Enhanced Progress Tracker", PROGRESS_AVAILABLE),
            ("Enhanced Input Manager", INPUT_MANAGER_AVAILABLE),
            ("Solution Generator", GENERATOR_AVAILABLE),
            ("Migration Tracker", MIGRATION_AVAILABLE),
            ("Enhanced Test Runner", TEST_RUNNER_AVAILABLE),
            ("Algorithm Libraries", ALGORITHMS_AVAILABLE)
        ]
        
        for tool, available in tools:
            status = "✅" if available else "❌"
            print(f"  {status} {tool}")
        
        print("\n" + "=" * 80)
        
        # Progress summary
        if self.progress_tracker:
            print(f"\n📊 Progress Summary:")
            stats = self.progress_tracker.get_completion_stats() if hasattr(self.progress_tracker, 'get_completion_stats') else {}
            if stats:
                total_solutions = sum(s['completed'] for s in stats.values())
                total_possible = len(stats) * 25
                overall_percentage = (total_solutions / total_possible) * 100 if total_possible > 0 else 0
                print(f"  Solutions: {total_solutions}/{total_possible} ({overall_percentage:.1f}%)")
                print(f"  Years: {len(stats)}")
            else:
                total_solutions = sum(len(year_sols) for year_sols in self.progress_tracker.solutions.values())
                total_possible = len(self.progress_tracker.solutions) * 25
                overall_percentage = (total_solutions / total_possible) * 100 if total_possible > 0 else 0
                print(f"  Solutions: {total_solutions}/{total_possible} ({overall_percentage:.1f}%)")
                print(f"  Years: {len(self.progress_tracker.solutions)}")
        
        # Input file status
        if self.input_manager:
            print(f"\n📁 Input File Status:")
            input_files = self.input_manager.discover_input_files()
            total_files = sum(len(year_files) for year_files in input_files.values())
            valid_files = sum(sum(1 for info in year_files.values() if info.is_valid) 
                            for year_files in input_files.values())
            missing_files = sum(sum(1 for info in year_files.values() if not info.exists)
                              for year_files in input_files.values())
            
            print(f"  Total files: {total_files}")
            print(f"  Valid files: {valid_files}")
            print(f"  Missing files: {missing_files}")
        
        # Migration status
        if self.migration_tracker:
            print(f"\n🔄 Migration Status:")
            total_candidates = len(self.migration_tracker.candidates)
            migrated = sum(1 for c in self.migration_tracker.candidates.values() if c.migration_successful)
            print(f"  Migration candidates: {total_candidates}")
            print(f"  Successfully migrated: {migrated}")
        
        print("\n" + "=" * 80)
    
    def suggest_next_actions(self) -> List[str]:
        """Suggest next actions based on current state."""
        suggestions = []
        
        if not self.progress_tracker:
            suggestions.append("🔧 Install enhanced progress tracker for better insights")
            return suggestions
        
        # Analyze current state
        solutions = self.progress_tracker.solutions
        
        # Find missing solutions
        missing_solutions = []
        for year_str, year_solutions in solutions.items():
            year = int(year_str)
            existing_days = set(year_solutions.keys())
            missing_days = set(range(1, 26)) - existing_days
            for day in sorted(missing_days)[:3]:  # Top 3 per year
                missing_solutions.append((year, day))
        
        if missing_solutions:
            year, day = missing_solutions[0]
            suggestions.append(f"🎄 Create solution for {year} Day {day}")
        
        # Check for missing input files
        if self.input_manager:
            input_files = self.input_manager.discover_input_files()
            missing_inputs = []
            for year, year_files in input_files.items():
                for day, info in year_files.items():
                    if not info.exists:
                        missing_inputs.append((year, day))
            
            if missing_inputs:
                year, day = missing_inputs[0]
                suggestions.append(f"📥 Download input for {year} Day {day}")
        
        # Migration opportunities
        if self.migration_tracker and self.migration_tracker.candidates:
            high_priority = [c for c in self.migration_tracker.candidates.values() 
                           if c.priority.value in ['critical', 'high'] and not c.migration_successful]
            if high_priority:
                candidate = high_priority[0]
                suggestions.append(f"🔄 Migrate {candidate.year} Day {candidate.day} to enhanced architecture")
        
        # Performance optimization
        if self.progress_tracker:
            slow_solutions = []
            for year_solutions in self.progress_tracker.solutions.values():
                for solution in year_solutions.values():
                    if solution.execution_time and solution.execution_time > 5.0:
                        slow_solutions.append((solution.year, solution.day, solution.execution_time))
            
            if slow_solutions:
                slow_solutions.sort(key=lambda x: x[2], reverse=True)
                year, day, time_taken = slow_solutions[0]
                suggestions.append(f"⚡ Optimize {year} Day {day} (currently {time_taken:.1f}s)")
        
        # Algorithm library adoption
        if ALGORITHMS_AVAILABLE and self.progress_tracker:
            non_enhanced = []
            for year_solutions in self.progress_tracker.solutions.values():
                for solution in year_solutions.values():
                    if not solution.uses_algorithm_libs and solution.architecture_type.value == 'legacy':
                        non_enhanced.append((solution.year, solution.day))
            
            if non_enhanced:
                year, day = non_enhanced[0]
                suggestions.append(f"🧮 Add algorithm libraries to {year} Day {day}")
        
        if not suggestions:
            suggestions.append("🎉 All caught up! Great work!")
        
        return suggestions[:5]  # Top 5 suggestions
    
    def run_full_analysis(self) -> None:
        """Run full analysis across all tools."""
        print(f"{Style.BRIGHT}🔍 Running Full Analysis{Style.RESET_ALL}")
        print("=" * 60)
        
        # Progress analysis
        if self.progress_tracker:
            print("\n📊 Analyzing progress...")
            self.progress_tracker.print_enhanced_summary()
        
        # Input file analysis
        if self.input_manager:
            print(f"\n📁 Analyzing input files...")
            issues = self.input_manager.validate_all_inputs()
            if not issues:
                print("✅ All input files are valid")
        
        # Migration analysis
        if self.migration_tracker:
            print(f"\n🔄 Analyzing migration opportunities...")
            self.migration_tracker.analyze_migration_candidates()
        
        print(f"\n{Style.BRIGHT}📝 Analysis Complete{Style.RESET_ALL}")
    
    def setup_new_year(self, year: int, download_inputs: bool = True) -> bool:
        """Set up a complete new year with templates and inputs."""
        print(f"{Style.BRIGHT}🎄 Setting up {year}{Style.RESET_ALL}")
        print("=" * 50)
        
        success = True
        
        # Create year directory
        year_dir = self.root_dir / str(year)
        year_dir.mkdir(exist_ok=True)
        print(f"✅ Created year directory: {year_dir}")
        
        # Generate solution templates for available days
        if self.solution_generator:
            print(f"\n📝 Generating solution templates...")
            # Start with just day 1 to test
            template_success = self.solution_generator.create_solution(
                year, 1, 
                fetch_info=True, 
                download_input=download_inputs
            )
            if template_success:
                print(f"✅ Created template for Day 1")
            else:
                print(f"❌ Failed to create template for Day 1")
                success = False
        
        # Download available inputs if requested
        if download_inputs and self.input_manager:
            print(f"\n📥 Downloading available inputs...")
            # Try to download day 1 input
            result = self.input_manager.download_input(year, 1)
            if result.success:
                print(f"✅ Downloaded input for Day 1")
            else:
                print(f"⚠️  Input download failed: {result.error_message}")
        
        print(f"\n{'✅ Setup complete!' if success else '⚠️  Setup completed with issues'}")
        return success
    
    def create_solution_workflow(self, year: int, day: int) -> bool:
        """Complete workflow for creating a new solution."""
        print(f"{Style.BRIGHT}🎄 Creating solution {year} Day {day}{Style.RESET_ALL}")
        print("=" * 60)
        
        success = True
        
        # Step 1: Generate solution template
        if self.solution_generator:
            print("📝 Generating solution template...")
            template_success = self.solution_generator.create_solution(
                year, day,
                fetch_info=True,
                download_input=False  # Download separately for better control
            )
            if template_success:
                print("✅ Solution template created")
            else:
                print("❌ Failed to create solution template")
                success = False
        else:
            print("❌ Solution generator not available")
            success = False
        
        # Step 2: Download input file
        if self.input_manager:
            print("\n📥 Downloading input file...")
            result = self.input_manager.download_input(year, day)
            if result.success:
                print("✅ Input file downloaded")
            else:
                print(f"⚠️  Input download failed: {result.error_message}")
                print("   You can download it manually later")
        else:
            print("❌ Input manager not available")
        
        # Step 3: Show next steps
        print(f"\n📋 Next steps:")
        print(f"  1. Open {year}/day{day}.py")
        print(f"  2. Implement your solution")
        print(f"  3. Test with: python {year}/day{day}.py")
        print(f"  4. Run enhanced test: python enhanced_test_runner.py --year {year} --day {day}")
        
        return success
    
    def migration_workflow(self, year: int, day: int) -> bool:
        """Complete workflow for migrating a solution."""
        print(f"{Style.BRIGHT}🔄 Migrating solution {year} Day {day}{Style.RESET_ALL}")
        print("=" * 60)
        
        if not self.migration_tracker:
            print("❌ Migration tracker not available")
            return False
        
        # Check if candidate exists
        key = f"{year}_day{day}"
        if key not in self.migration_tracker.candidates:
            print("📊 Analyzing migration candidate...")
            self.migration_tracker.analyze_migration_candidates()
        
        if key not in self.migration_tracker.candidates:
            print(f"❌ No migration candidate found for {year} Day {day}")
            return False
        
        candidate = self.migration_tracker.candidates[key]
        
        # Show migration info
        print(f"📋 Migration candidate information:")
        print(f"  Current architecture: {candidate.current_architecture.value}")
        print(f"  Priority: {candidate.priority.value}")
        print(f"  Complexity: {candidate.complexity.value}")
        print(f"  Algorithm opportunities: {', '.join(candidate.algorithm_opportunities)}")
        print(f"  Estimated benefit: {candidate.estimated_benefit}")
        
        # Start migration (create backup)
        success = self.migration_tracker.start_migration("default", key)
        if success:
            print("\n✅ Migration started - backup created")
            print("📋 Next steps:")
            print("  1. Manually migrate the solution")
            print(f"  2. Mark complete: python migration_tracker.py --complete {key}:true:'notes'")
            print(f"  3. Or rollback: python migration_tracker.py --rollback {key}")
        
        return success

def main():
    """Main function for workflow manager."""
    parser = argparse.ArgumentParser(description="Advent of Code Workflow Manager")
    
    # Dashboard commands
    parser.add_argument("--dashboard", "-d", action="store_true", help="Show status dashboard")
    parser.add_argument("--analyze", "-a", action="store_true", help="Run full analysis")
    parser.add_argument("--suggest", "-s", action="store_true", help="Suggest next actions")
    
    # Workflow commands
    parser.add_argument("--setup-year", type=int, help="Setup new year")
    parser.add_argument("--create", help="Create solution (format: year:day)")
    parser.add_argument("--migrate", help="Migrate solution (format: year:day)")
    
    # Options
    parser.add_argument("--no-input", action="store_true", help="Don't download input files")
    
    args = parser.parse_args()
    
    manager = WorkflowManager()
    
    # Default behavior: show dashboard
    if not any([args.analyze, args.suggest, args.setup_year, args.create, args.migrate]):
        args.dashboard = True
    
    if args.dashboard:
        manager.print_status_dashboard()
        
        # Also show suggestions
        suggestions = manager.suggest_next_actions()
        print(f"\n💡 Suggested Next Actions:")
        for i, suggestion in enumerate(suggestions, 1):
            print(f"  {i}. {suggestion}")
    
    if args.analyze:
        manager.run_full_analysis()
    
    if args.suggest:
        suggestions = manager.suggest_next_actions()
        print(f"💡 Suggested Next Actions:")
        for i, suggestion in enumerate(suggestions, 1):
            print(f"  {i}. {suggestion}")
    
    if args.setup_year:
        success = manager.setup_new_year(args.setup_year, not args.no_input)
        return 0 if success else 1
    
    if args.create:
        try:
            year, day = map(int, args.create.split(":"))
            success = manager.create_solution_workflow(year, day)
            return 0 if success else 1
        except ValueError:
            print("Error: --create format should be year:day")
            return 1
    
    if args.migrate:
        try:
            year, day = map(int, args.migrate.split(":"))
            success = manager.migration_workflow(year, day)
            return 0 if success else 1
        except ValueError:
            print("Error: --migrate format should be year:day")
            return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())