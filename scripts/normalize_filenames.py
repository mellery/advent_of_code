#!/usr/bin/env python3
"""
File Naming Standardization Script for Advent of Code Project

This script standardizes all file names to follow consistent patterns:
- Solution files: day{N}.py (e.g., day1.py, day12.py)
- Input files: day{N}_input.txt (e.g., day1_input.txt)
- Test files: day{N}_test.txt (e.g., day1_test.txt)

Handles edge cases and preserves git history where possible.
"""

import os
import re
import shutil
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import argparse

class FileNormalizer:
    """Handles standardization of Advent of Code file names."""
    
    def __init__(self, root_dir: str, dry_run: bool = True):
        self.root_dir = Path(root_dir)
        self.dry_run = dry_run
        self.renames: List[Tuple[Path, Path]] = []
        self.conflicts: List[Tuple[Path, Path]] = []
        
    def analyze_and_normalize(self) -> Dict[str, any]:
        """Analyze current files and prepare normalization plan."""
        print("🔍 Analyzing file naming patterns...")
        
        # Find all solution files that need renaming
        solution_renames = self._find_solution_renames()
        
        # Find all input files that need renaming  
        input_renames = self._find_input_renames()
        
        # Find all test files that need renaming
        test_renames = self._find_test_renames()
        
        all_renames = solution_renames + input_renames + test_renames
        
        # Check for conflicts
        conflicts = self._check_conflicts(all_renames)
        
        return {
            'solution_renames': solution_renames,
            'input_renames': input_renames, 
            'test_renames': test_renames,
            'total_renames': len(all_renames),
            'conflicts': conflicts
        }
    
    def _find_solution_renames(self) -> List[Tuple[Path, Path]]:
        """Find solution files that need to be renamed to day{N}.py format."""
        renames = []
        
        # Pattern to match advent files: advent{N}.py -> day{N}.py
        advent_pattern = re.compile(r'advent(\d+)\.py$')
        
        # Pattern to match special cases like advent1b.py
        special_pattern = re.compile(r'advent(\d+)([a-z])\.py$')
        
        for year_dir in self.root_dir.iterdir():
            if not year_dir.is_dir() or not year_dir.name.isdigit():
                continue
                
            for file_path in year_dir.glob("*.py"):
                filename = file_path.name
                
                # Handle advent{N}.py -> day{N}.py
                match = advent_pattern.match(filename)
                if match:
                    day_num = match.group(1)
                    new_name = f"day{day_num}.py"
                    new_path = file_path.parent / new_name
                    renames.append((file_path, new_path))
                    continue
                
                # Handle special cases like advent1b.py -> day1_part2.py
                match = special_pattern.match(filename)
                if match:
                    day_num = match.group(1)
                    variant = match.group(2)
                    if variant == 'b':
                        new_name = f"day{day_num}_part2.py"
                    else:
                        new_name = f"day{day_num}_{variant}.py"
                    new_path = file_path.parent / new_name
                    renames.append((file_path, new_path))
        
        return renames
    
    def _find_input_renames(self) -> List[Tuple[Path, Path]]:
        """Find input files that need to be renamed to day{N}_input.txt format."""
        renames = []
        
        # Pattern for non-standard input files
        patterns = [
            (re.compile(r'input(\d+)\.txt$'), r'day\1_input.txt'),
            (re.compile(r'day(\d+)input\.txt$'), r'day\1_input.txt'),
            (re.compile(r'day(\d+)_input_ex\.txt$'), r'day\1_test.txt'),
            (re.compile(r'day(\d+)_input2\.txt$'), r'day\1_part2_input.txt'),
        ]
        
        for year_dir in self.root_dir.iterdir():
            if not year_dir.is_dir() or not year_dir.name.isdigit():
                continue
                
            for file_path in year_dir.glob("*.txt"):
                filename = file_path.name
                
                for pattern, replacement in patterns:
                    match = pattern.match(filename)
                    if match:
                        new_name = pattern.sub(replacement, filename)
                        new_path = file_path.parent / new_name
                        renames.append((file_path, new_path))
                        break
        
        return renames
    
    def _find_test_renames(self) -> List[Tuple[Path, Path]]:
        """Find test files that need standardization."""
        renames = []
        
        # Pattern for test files
        test_patterns = [
            (re.compile(r'day(\d+)_ex(\d+)\.txt$'), r'day\1_test\2.txt'),
            (re.compile(r'day(\d+)_example\.txt$'), r'day\1_test.txt'),
        ]
        
        for year_dir in self.root_dir.iterdir():
            if not year_dir.is_dir() or not year_dir.name.isdigit():
                continue
                
            for file_path in year_dir.glob("*.txt"):
                filename = file_path.name
                
                for pattern, replacement in test_patterns:
                    match = pattern.match(filename)
                    if match:
                        new_name = pattern.sub(replacement, filename)
                        new_path = file_path.parent / new_name
                        renames.append((file_path, new_path))
                        break
        
        return renames
    
    def _check_conflicts(self, renames: List[Tuple[Path, Path]]) -> List[Tuple[Path, Path]]:
        """Check for naming conflicts where target files already exist."""
        conflicts = []
        
        for old_path, new_path in renames:
            if new_path.exists() and old_path != new_path:
                conflicts.append((old_path, new_path))
        
        return conflicts
    
    def execute_renames(self, renames: List[Tuple[Path, Path]]) -> None:
        """Execute the file renames."""
        if self.dry_run:
            print("🧪 DRY RUN - No files will actually be renamed")
            
        print(f"\n📝 Executing {len(renames)} file renames...")
        
        for i, (old_path, new_path) in enumerate(renames, 1):
            print(f"  {i:3d}. {old_path.name} → {new_path.name}")
            
            if not self.dry_run:
                try:
                    # Use git mv if in a git repo, otherwise regular move
                    if self._is_git_repo():
                        os.system(f'git mv "{old_path}" "{new_path}"')
                    else:
                        shutil.move(str(old_path), str(new_path))
                except Exception as e:
                    print(f"     ❌ Error: {e}")
                    continue
                    
                print(f"     ✅ Renamed successfully")
    
    def _is_git_repo(self) -> bool:
        """Check if we're in a git repository."""
        return (self.root_dir / '.git').exists()
    
    def print_summary(self, analysis: Dict[str, any]) -> None:
        """Print a summary of the normalization plan."""
        print("\n" + "="*60)
        print("🎯 FILE NAMING STANDARDIZATION SUMMARY")
        print("="*60)
        
        print(f"📁 Root directory: {self.root_dir}")
        print(f"🔄 Total renames needed: {analysis['total_renames']}")
        print(f"🐍 Solution files: {len(analysis['solution_renames'])}")
        print(f"📄 Input files: {len(analysis['input_renames'])}")
        print(f"🧪 Test files: {len(analysis['test_renames'])}")
        
        if analysis['conflicts']:
            print(f"\n⚠️  CONFLICTS DETECTED: {len(analysis['conflicts'])}")
            for old_path, new_path in analysis['conflicts']:
                print(f"   ❌ {old_path} → {new_path} (target exists)")
        
        print("\n📋 DETAILED RENAME PLAN:")
        
        if analysis['solution_renames']:
            print("\n🐍 Solution Files:")
            for old_path, new_path in analysis['solution_renames']:
                status = "⚠️" if (old_path, new_path) in analysis['conflicts'] else "✅"
                print(f"   {status} {old_path.name} → {new_path.name}")
        
        if analysis['input_renames']:
            print("\n📄 Input Files:")
            for old_path, new_path in analysis['input_renames']:
                status = "⚠️" if (old_path, new_path) in analysis['conflicts'] else "✅"
                print(f"   {status} {old_path.name} → {new_path.name}")
        
        if analysis['test_renames']:
            print("\n🧪 Test Files:")
            for old_path, new_path in analysis['test_renames']:
                status = "⚠️" if (old_path, new_path) in analysis['conflicts'] else "✅"
                print(f"   {status} {old_path.name} → {new_path.name}")

def main():
    """Main function to execute file normalization."""
    parser = argparse.ArgumentParser(description="Normalize Advent of Code file names")
    parser.add_argument("--root", default=".", help="Root directory of the project")
    parser.add_argument("--execute", action="store_true", help="Execute renames (default is dry-run)")
    parser.add_argument("--force", action="store_true", help="Force renames even with conflicts")
    
    args = parser.parse_args()
    
    normalizer = FileNormalizer(args.root, dry_run=not args.execute)
    
    # Analyze current state
    analysis = normalizer.analyze_and_normalize()
    
    # Print summary
    normalizer.print_summary(analysis)
    
    # Check for conflicts
    if analysis['conflicts'] and not args.force:
        print("\n❌ Cannot proceed due to conflicts. Use --force to override.")
        return 1
    
    # Execute renames if requested
    if args.execute:
        # Combine all renames
        all_renames = (analysis['solution_renames'] + 
                      analysis['input_renames'] + 
                      analysis['test_renames'])
        
        if not args.force:
            # Filter out conflicts
            all_renames = [r for r in all_renames if r not in analysis['conflicts']]
        
        normalizer.execute_renames(all_renames)
        print("\n✅ File normalization complete!")
    else:
        print("\n💡 This was a dry run. Use --execute to apply changes.")
    
    return 0

if __name__ == "__main__":
    exit(main())