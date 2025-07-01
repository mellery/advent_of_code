#!/usr/bin/env python3
"""
Advent of Code 2020 Day 5: Binary Boarding
https://adventofcode.com/2020/day/5

Binary space partitioning for airplane seat identification.
Enhanced solution using AdventSolution base class.
"""

import sys
from pathlib import Path
from typing import Any, List, Set, Tuple, Optional

# Add utils to path
sys.path.append(str(Path(__file__).parent.parent))
from utils import AdventSolution, InputParser


class BoardingPass:
    """Represents a boarding pass with binary space partitioning encoding."""
    
    def __init__(self, code: str):
        """
        Initialize a boarding pass.
        
        Args:
            code: 10-character boarding pass code (e.g., "FBFBBFFRLR")
        """
        self.code = code.strip()
        if len(self.code) != 10:
            raise ValueError(f"Invalid boarding pass code: {self.code} (must be 10 characters)")
        
        self.row_code = self.code[:7]  # First 7 characters for row (F/B)
        self.col_code = self.code[7:]  # Last 3 characters for column (L/R)
        
        self._row = None
        self._col = None
        self._seat_id = None
    
    @property
    def row(self) -> int:
        """Get the row number (0-127) using binary space partitioning."""
        if self._row is None:
            self._row = self._binary_search(self.row_code, 0, 127, 'F', 'B')
        return self._row
    
    @property
    def col(self) -> int:
        """Get the column number (0-7) using binary space partitioning."""
        if self._col is None:
            self._col = self._binary_search(self.col_code, 0, 7, 'L', 'R')
        return self._col
    
    @property
    def seat_id(self) -> int:
        """Get the unique seat ID (row * 8 + col)."""
        if self._seat_id is None:
            self._seat_id = self.row * 8 + self.col
        return self._seat_id
    
    def _binary_search(self, code: str, min_val: int, max_val: int, 
                      lower_char: str, upper_char: str) -> int:
        """
        Perform binary space partitioning.
        
        Args:
            code: The code string to process
            min_val: Minimum value in range
            max_val: Maximum value in range
            lower_char: Character indicating lower half
            upper_char: Character indicating upper half
            
        Returns:
            Final value after partitioning
        """
        for char in code:
            mid = (min_val + max_val) // 2
            if char == lower_char:
                max_val = mid
            elif char == upper_char:
                min_val = mid + 1
            else:
                raise ValueError(f"Invalid character '{char}' in code '{code}'")
        
        if min_val != max_val:
            raise ValueError(f"Binary search didn't converge: min={min_val}, max={max_val}")
        
        return min_val
    
    def __repr__(self) -> str:
        return f"BoardingPass('{self.code}', row={self.row}, col={self.col}, id={self.seat_id})"
    
    def __eq__(self, other) -> bool:
        if isinstance(other, BoardingPass):
            return self.code == other.code
        return False
    
    def __hash__(self) -> int:
        return hash(self.code)


class Day5Solution(AdventSolution):
    """Solution for 2020 Day 5: Binary Boarding."""

    def __init__(self):
        super().__init__(2020, 5, "Binary Boarding")

    def parse_boarding_passes(self, input_data: str) -> List[BoardingPass]:
        """
        Parse boarding pass codes from input data.
        
        Args:
            input_data: Raw input data containing boarding pass codes
            
        Returns:
            List of BoardingPass objects
        """
        boarding_passes = []
        
        for line in input_data.strip().split('\n'):
            line = line.strip()
            if line:
                boarding_passes.append(BoardingPass(line))
        
        return boarding_passes

    def get_all_possible_seat_ids(self) -> Set[int]:
        """Get all theoretically possible seat IDs (0-1023)."""
        return set(row * 8 + col for row in range(128) for col in range(8))

    def find_missing_seat(self, occupied_seats: Set[int]) -> Optional[int]:
        """
        Find the missing seat ID where both adjacent seats exist.
        
        Args:
            occupied_seats: Set of occupied seat IDs
            
        Returns:
            The missing seat ID, or None if not found
        """
        all_seats = self.get_all_possible_seat_ids()
        missing_seats = all_seats - occupied_seats
        
        # Find the missing seat where both adjacent seats are occupied
        for seat_id in missing_seats:
            if (seat_id - 1 in occupied_seats and 
                seat_id + 1 in occupied_seats):
                return seat_id
        
        return None

    def part1(self, input_data: str) -> int:
        """
        Solve part 1: Find the highest seat ID on a boarding pass.
        
        Args:
            input_data: The input data as a string
            
        Returns:
            The highest seat ID
        """
        boarding_passes = self.parse_boarding_passes(input_data)
        
        if not boarding_passes:
            raise ValueError("No boarding passes found in input")
        
        return max(bp.seat_id for bp in boarding_passes)

    def part2(self, input_data: str) -> int:
        """
        Solve part 2: Find your seat ID (missing seat with adjacent occupied seats).
        
        Args:
            input_data: The input data as a string
            
        Returns:
            Your seat ID
        """
        boarding_passes = self.parse_boarding_passes(input_data)
        
        if not boarding_passes:
            raise ValueError("No boarding passes found in input")
        
        occupied_seats = set(bp.seat_id for bp in boarding_passes)
        missing_seat = self.find_missing_seat(occupied_seats)
        
        if missing_seat is None:
            raise ValueError("Could not find missing seat with adjacent occupied seats")
        
        return missing_seat

    def analyze_seating(self, input_data: str) -> str:
        """
        Analyze the seating arrangement for insights.
        
        Args:
            input_data: Raw input data
            
        Returns:
            Analysis summary as formatted string
        """
        boarding_passes = self.parse_boarding_passes(input_data)
        
        if not boarding_passes:
            return "No boarding passes found."
        
        analysis = []
        analysis.append("=== Seating Analysis ===")
        analysis.append(f"Total boarding passes: {len(boarding_passes)}")
        
        # Seat ID statistics
        seat_ids = [bp.seat_id for bp in boarding_passes]
        analysis.append(f"Seat ID range: {min(seat_ids)} - {max(seat_ids)}")
        
        # Row and column distributions
        rows = [bp.row for bp in boarding_passes]
        cols = [bp.col for bp in boarding_passes]
        
        analysis.append(f"Row range: {min(rows)} - {max(rows)}")
        analysis.append(f"Column range: {min(cols)} - {max(cols)}")
        
        # Find completely empty rows
        occupied_rows = set(rows)
        all_rows = set(range(128))
        empty_rows = sorted(all_rows - occupied_rows)
        if empty_rows:
            if len(empty_rows) <= 10:
                analysis.append(f"Empty rows: {empty_rows}")
            else:
                analysis.append(f"Empty rows: {len(empty_rows)} rows ({empty_rows[:5]}...{empty_rows[-5:]})")
        
        # Row occupancy statistics
        from collections import Counter
        row_counts = Counter(rows)
        most_occupied_row = row_counts.most_common(1)[0]
        analysis.append(f"Most occupied row: {most_occupied_row[0]} ({most_occupied_row[1]} seats)")
        
        # Missing seats analysis
        occupied_seats = set(seat_ids)
        all_possible = self.get_all_possible_seat_ids()
        missing_seats = all_possible - occupied_seats
        
        analysis.append(f"Missing seats: {len(missing_seats)} out of {len(all_possible)} possible")
        
        # Find the specific missing seat for part 2
        my_seat = self.find_missing_seat(occupied_seats)
        if my_seat is not None:
            my_row, my_col = divmod(my_seat, 8)
            analysis.append(f"Your seat: ID {my_seat} (row {my_row}, col {my_col})")
        
        return "\n".join(analysis)

    def validate(self, expected_part1=None, expected_part2=None) -> bool:
        """Validate solution with test cases."""
        # Test with examples from the problem description
        test_cases = [
            ("FBFBBFFRLR", 44, 5, 357),  # (code, row, col, seat_id)
            ("BFFFBBFRRR", 70, 7, 567),
            ("FFFBBBFRRR", 14, 7, 119),
            ("BBFFBBFRLL", 102, 4, 820)
        ]
        
        for code, expected_row, expected_col, expected_seat_id in test_cases:
            bp = BoardingPass(code)
            
            if bp.row != expected_row:
                print(f"Row validation failed for {code}: expected {expected_row}, got {bp.row}")
                return False
            
            if bp.col != expected_col:
                print(f"Column validation failed for {code}: expected {expected_col}, got {bp.col}")
                return False
            
            if bp.seat_id != expected_seat_id:
                print(f"Seat ID validation failed for {code}: expected {expected_seat_id}, got {bp.seat_id}")
                return False
        
        # Test the highest seat ID from the examples
        test_input = "\n".join([case[0] for case in test_cases])
        highest_id = self.part1(test_input)
        if highest_id != 820:
            print(f"Part 1 validation failed: expected 820, got {highest_id}")
            return False
        
        print("✅ All Day 5 validation tests passed!")
        return True


def main():
    """Main execution function."""
    solution = Day5Solution()
    solution.main()


if __name__ == "__main__":
    main()