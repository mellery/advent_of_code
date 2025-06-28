#!/usr/bin/env python3
"""
Input management script for Advent of Code.

This script helps download input files from the Advent of Code website
and organize them with consistent naming conventions.

IMPORTANT: This script respects AoC's automation guidelines:
- Requires manual session cookie setup
- Caches inputs locally to avoid repeated requests
- Does NOT automatically submit answers
"""

import os
import sys
import requests
import time
from pathlib import Path
from typing import Optional
import argparse

# Rate limiting: AoC requests no more than 1 request per second
REQUEST_DELAY = 1.0

class InputManager:
    """Manage Advent of Code input files."""
    
    def __init__(self, session_cookie: Optional[str] = None):
        """
        Initialize the input manager.
        
        Args:
            session_cookie: Your AoC session cookie (optional, can be set via env var)
        """
        self.session_cookie = session_cookie or os.getenv('AOC_SESSION')
        self.session = requests.Session()
        
        if self.session_cookie:
            self.session.cookies.set('session', self.session_cookie, domain='.adventofcode.com')
        
        self.base_url = "https://adventofcode.com"
        self.last_request_time = 0
    
    def _rate_limit(self) -> None:
        """Ensure we don't exceed rate limits."""
        elapsed = time.time() - self.last_request_time
        if elapsed < REQUEST_DELAY:
            time.sleep(REQUEST_DELAY - elapsed)
        self.last_request_time = time.time()
    
    def download_input(self, year: int, day: int, output_file: Optional[str] = None) -> bool:
        """
        Download input for a specific day.
        
        Args:
            year: Year (e.g., 2019, 2020)
            day: Day number (1-25)
            output_file: Output filename (optional, auto-generated if not provided)
            
        Returns:
            True if successful, False otherwise
        """
        if not self.session_cookie:
            print("Error: No session cookie provided. Set AOC_SESSION environment variable or pass as argument.")
            print("To get your session cookie:")
            print("1. Log into adventofcode.com")
            print("2. Open browser dev tools (F12)")
            print("3. Go to Application/Storage > Cookies > adventofcode.com")
            print("4. Copy the 'session' cookie value")
            return False
        
        if not (1 <= day <= 25):
            print(f"Error: Day must be between 1 and 25, got {day}")
            return False
        
        # Generate output filename if not provided
        if not output_file:
            year_dir = Path(str(year))
            year_dir.mkdir(exist_ok=True)
            output_file = year_dir / f"day{day}_input.txt"
        else:
            output_file = Path(output_file)
        
        # Check if file already exists
        if output_file.exists():
            print(f"Input file {output_file} already exists. Use --force to overwrite.")
            return True
        
        # Download the input
        url = f"{self.base_url}/{year}/day/{day}/input"
        
        print(f"Downloading input for {year} Day {day}...")
        
        self._rate_limit()
        
        try:
            response = self.session.get(url)
            response.raise_for_status()
            
            # Check if we got a valid response (not a login page)
            if "Puzzle inputs differ by user" in response.text or "Please log in" in response.text:
                print("Error: Invalid session cookie or not logged in")
                return False
            
            # Save the input
            output_file.parent.mkdir(parents=True, exist_ok=True)
            output_file.write_text(response.text.rstrip('\n'))
            
            print(f"Successfully downloaded to {output_file}")
            return True
            
        except requests.RequestException as e:
            print(f"Error downloading input: {e}")
            return False
    
    def normalize_input_filename(self, year_dir: Path, day: int) -> None:
        """
        Normalize input filename to standard convention.
        
        Args:
            year_dir: Directory containing the files
            day: Day number
        """
        standard_name = f"day{day}_input.txt"
        standard_path = year_dir / standard_name
        
        if standard_path.exists():
            return  # Already normalized
        
        # Look for existing files with various naming patterns
        patterns = [
            f"day{day}input.txt",
            f"input{day}.txt", 
            f"day{day}.txt",
            f"part1.txt",  # Some solutions use this
            f"input.txt"
        ]
        
        for pattern in patterns:
            candidate = year_dir / pattern
            if candidate.exists():
                print(f"Renaming {candidate} -> {standard_path}")
                candidate.rename(standard_path)
                return
    
    def normalize_all_inputs(self, root_dir: Path = Path(".")) -> None:
        """
        Normalize all input filenames in the repository.
        
        Args:
            root_dir: Root directory to search
        """
        for year_dir in root_dir.iterdir():
            if year_dir.is_dir() and year_dir.name.isdigit() and len(year_dir.name) == 4:
                print(f"Normalizing inputs in {year_dir.name}/")
                
                # Find all Python solution files to determine which days exist
                days = set()
                for py_file in year_dir.glob("*.py"):
                    if "template" in py_file.name or "test" in py_file.name:
                        continue
                    
                    day = self._extract_day_number(py_file.name)
                    if day and 1 <= day <= 25:
                        days.add(day)
                
                # Normalize inputs for discovered days
                for day in sorted(days):
                    self.normalize_input_filename(year_dir, day)
    
    def _extract_day_number(self, filename: str) -> Optional[int]:
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
        
        return None
    
    def check_missing_inputs(self, root_dir: Path = Path(".")) -> None:
        """
        Check for missing input files across all years.
        
        Args:
            root_dir: Root directory to search
        """
        missing = []
        
        for year_dir in root_dir.iterdir():
            if year_dir.is_dir() and year_dir.name.isdigit() and len(year_dir.name) == 4:
                year = int(year_dir.name)
                
                # Find all solution files
                days = set()
                for py_file in year_dir.glob("*.py"):
                    if "template" in py_file.name or "test" in py_file.name:
                        continue
                    
                    day = self._extract_day_number(py_file.name)
                    if day:
                        days.add(day)
                
                # Check for missing inputs
                for day in sorted(days):
                    input_file = year_dir / f"day{day}_input.txt"
                    if not input_file.exists():
                        missing.append((year, day))
        
        if missing:
            print("Missing input files:")
            for year, day in missing:
                print(f"  {year} Day {day}")
            print(f"\nTo download missing inputs:")
            print(f"export AOC_SESSION='your_session_cookie'")
            for year, day in missing:
                print(f"python input_manager.py --download --year {year} --day {day}")
        else:
            print("All input files are present!")


def main():
    """Main function for the input manager."""
    parser = argparse.ArgumentParser(description="Advent of Code Input Manager")
    parser.add_argument("--download", "-d", action="store_true", help="Download input")
    parser.add_argument("--year", "-y", type=int, help="Year (required for download)")
    parser.add_argument("--day", type=int, help="Day (required for download)")
    parser.add_argument("--output", "-o", help="Output filename")
    parser.add_argument("--session", "-s", help="Session cookie (or set AOC_SESSION env var)")
    parser.add_argument("--normalize", "-n", action="store_true", help="Normalize all input filenames")
    parser.add_argument("--check", "-c", action="store_true", help="Check for missing inputs")
    parser.add_argument("--force", "-f", action="store_true", help="Force overwrite existing files")
    
    args = parser.parse_args()
    
    manager = InputManager(args.session)
    
    if args.download:
        if not args.year or not args.day:
            print("Error: --year and --day are required for download")
            return 1
        
        success = manager.download_input(args.year, args.day, args.output)
        return 0 if success else 1
    
    elif args.normalize:
        manager.normalize_all_inputs()
    
    elif args.check:
        manager.check_missing_inputs()
    
    else:
        # Default: show help
        parser.print_help()
    
    return 0


if __name__ == "__main__":
    sys.exit(main())