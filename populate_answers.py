#!/usr/bin/env python3
"""
Helper script to populate expected answers for Advent of Code solutions.

This script runs all solutions and captures their outputs as expected answers,
making it easy to establish a baseline for validation.
"""

import argparse
import subprocess
import sys
from pathlib import Path


def main():
    """Main function to populate expected answers."""
    parser = argparse.ArgumentParser(
        description="Populate expected answers for Advent of Code solutions"
    )
    parser.add_argument("--year", "-y", help="Populate answers only for specific year")
    parser.add_argument("--dry-run", action="store_true", 
                       help="Show what would be updated without making changes")
    parser.add_argument("--force", action="store_true",
                       help="Update answers even if they already exist")
    
    args = parser.parse_args()
    
    # Build command
    cmd = [sys.executable, "test_runner.py", "--update-answers"]
    
    if args.year:
        cmd.extend(["--year", args.year])
    
    if not args.force:
        cmd.append("--only-unknown")
    
    print("🚀 Populating expected answers...")
    print(f"Command: {' '.join(cmd)}")
    
    if args.dry_run:
        print("\n🔍 DRY RUN MODE - No changes will be made")
        print("Add --force to update existing answers")
        print("Remove --dry-run to actually update answers")
        return
    
    try:
        subprocess.run(cmd, check=True)
        print("\n✅ Expected answers have been updated!")
        print("\nNext steps:")
        print("1. Review the updated expected_answers.json file")
        print("2. Run 'python test_runner.py' to validate all solutions")
        print("3. Commit the changes to version control")
        
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Error populating answers: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n⏹️ Operation cancelled by user")
        sys.exit(1)


if __name__ == "__main__":
    main()