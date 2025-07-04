#!/usr/bin/env python3
"""
Advent of Code 2019 - Day 4: Secure Container

You arrive at the Venus fuel depot only to discover it's protected by a password.
The password is a six-digit number within a certain range that meets specific criteria.

Key Concepts:
- Password validation rules
- Digit analysis and grouping
- Range-based search
- Adjacent digit constraints
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.advent_base import AdventSolution
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
from collections import Counter


@dataclass
class PasswordCriteria:
    """Defines password validation criteria."""
    min_value: int
    max_value: int
    length: int = 6
    require_adjacent_same: bool = True
    require_non_decreasing: bool = True
    require_exact_double: bool = False  # Part 2 requirement
    
    def __post_init__(self):
        """Validate criteria consistency."""
        if self.min_value > self.max_value:
            raise ValueError("min_value must be <= max_value")
        if self.length < 1:
            raise ValueError("length must be positive")


def validate_password_fast(password: int, part2: bool = False) -> bool:
    """
    Fast password validation without object overhead.
    
    Args:
        password: Integer password to validate
        part2: Whether to apply part 2 constraints (exact double requirement)
        
    Returns:
        True if password is valid
    """
    # Convert to string once
    s = str(password)
    
    # Check length (should be 6 digits for our range)
    if len(s) != 6:
        return False
    
    # Check non-decreasing and adjacent digits in one pass
    has_adjacent = False
    has_exact_double = False
    
    for i in range(5):
        # Non-decreasing check
        if s[i] > s[i + 1]:
            return False
        
        # Adjacent same digits check
        if s[i] == s[i + 1]:
            has_adjacent = True
            
            # For part 2, check if it's exactly a double (not triple+)
            if part2:
                # Check if this starts a run of exactly 2
                if i == 0 or s[i-1] != s[i]:  # Start of run
                    if i + 1 < 6 and s[i] == s[i+1]:  # Has a match
                        if i + 2 >= 6 or s[i+1] != s[i+2]:  # Ends after 2
                            has_exact_double = True
    
    return has_adjacent if not part2 else has_exact_double


class PasswordValidator:
    """Validates passwords against specified criteria."""
    
    def __init__(self, criteria: PasswordCriteria):
        """Initialize with password criteria."""
        self.criteria = criteria
    
    def is_valid_password(self, password: int, part2: bool = False) -> bool:
        """
        Check if password meets all required criteria.
        
        Args:
            password: Integer password to validate
            part2: Whether to apply part 2 constraints (exact double requirement)
            
        Returns:
            True if password is valid
        """
        results = self.validate_password(password)
        
        # Basic requirements
        if not (results['in_range'] and results['correct_length'] and 
                results['is_non_decreasing']):
            return False
        
        # Adjacent same digit requirement
        if self.criteria.require_adjacent_same:
            if part2 and self.criteria.require_exact_double:
                return results['has_exact_double']
            else:
                return results['has_adjacent_same']
        
        return True
    
    def _has_adjacent_same_digits(self, password_str: str) -> bool:
        """Check if password has at least two adjacent identical digits."""
        for i in range(len(password_str) - 1):
            if password_str[i] == password_str[i + 1]:
                return True
        return False
    
    def _is_non_decreasing(self, password_str: str) -> bool:
        """Check if digits are in non-decreasing order."""
        for i in range(len(password_str) - 1):
            if password_str[i] > password_str[i + 1]:
                return False
        return True
    
    def _has_exact_double(self, password_str: str) -> bool:
        """Check if password has at least one group of exactly two identical adjacent digits."""
        digit_groups = self._get_digit_groups(password_str)
        return 2 in digit_groups.values()
    
    def _get_digit_groups(self, password_str: str) -> Dict[str, int]:
        """
        Get groups of consecutive identical digits.
        
        Args:
            password_str: Password as string
            
        Returns:
            Dictionary mapping digit to its group size
        """
        if not password_str:
            return {}
        
        groups = {}
        current_digit = password_str[0]
        current_count = 1
        
        for i in range(1, len(password_str)):
            if password_str[i] == current_digit:
                current_count += 1
            else:
                groups[current_digit] = current_count
                current_digit = password_str[i]
                current_count = 1
        
        # Don't forget the last group
        groups[current_digit] = current_count
        
        return groups


class PasswordAnalyzer:
    """Analyzes password patterns and provides detailed statistics."""
    
    def __init__(self, validator: PasswordValidator):
        """Initialize with a password validator."""
        self.validator = validator
        self.criteria = validator.criteria
    
    def analyze_password(self, password: int) -> Dict:
        """
        Provide comprehensive analysis of a single password.
        
        Args:
            password: Password to analyze
            
        Returns:
            Dictionary with detailed analysis
        """
        password_str = str(password)
        validation = self.validator.validate_password(password)
        digit_groups = self.validator._get_digit_groups(password_str)
        
        analysis = {
            'password': password,
            'password_str': password_str,
            'validation': validation,
            'digit_groups': digit_groups,
            'digit_counts': Counter(password_str),
            'is_valid_part1': self.validator.is_valid_password(password, part2=False),
            'is_valid_part2': self.validator.is_valid_password(password, part2=True),
            'increasing_digits': self._count_increasing_sequences(password_str),
            'decreasing_digits': self._count_decreasing_sequences(password_str)
        }
        
        return analysis
    
    def find_valid_passwords(self, part2: bool = False) -> List[int]:
        """
        Find all valid passwords in the specified range.
        
        Args:
            part2: Whether to apply part 2 constraints
            
        Returns:
            List of valid passwords
        """
        valid_passwords = []
        
        for password in range(self.criteria.min_value, self.criteria.max_value + 1):
            if self.validator.is_valid_password(password, part2=part2):
                valid_passwords.append(password)
        
        return valid_passwords
    
    def generate_statistics(self, part2: bool = False) -> Dict:
        """
        Generate comprehensive statistics about password validation.
        
        Args:
            part2: Whether to apply part 2 constraints
            
        Returns:
            Dictionary with statistics
        """
        total_range = self.criteria.max_value - self.criteria.min_value + 1
        valid_passwords = self.find_valid_passwords(part2=part2)
        
        # Count passwords by criteria
        criteria_counts = {
            'in_range': 0,
            'correct_length': 0,
            'has_adjacent_same': 0,
            'is_non_decreasing': 0,
            'has_exact_double': 0
        }
        
        sample_size = min(10000, total_range)  # Limit sample for performance
        step = max(1, total_range // sample_size)
        
        for password in range(self.criteria.min_value, self.criteria.max_value + 1, step):
            validation = self.validator.validate_password(password)
            for criterion, result in validation.items():
                if result:
                    criteria_counts[criterion] += 1
        
        stats = {
            'total_range_size': total_range,
            'valid_passwords_count': len(valid_passwords),
            'valid_percentage': (len(valid_passwords) / total_range) * 100,
            'criteria_stats': criteria_counts,
            'sample_size': sample_size,
            'first_valid': valid_passwords[0] if valid_passwords else None,
            'last_valid': valid_passwords[-1] if valid_passwords else None
        }
        
        return stats
    
    def _count_increasing_sequences(self, password_str: str) -> int:
        """Count number of increasing digit sequences."""
        count = 0
        for i in range(len(password_str) - 1):
            if password_str[i] < password_str[i + 1]:
                count += 1
        return count
    
    def _count_decreasing_sequences(self, password_str: str) -> int:
        """Count number of decreasing digit sequences."""
        count = 0
        for i in range(len(password_str) - 1):
            if password_str[i] > password_str[i + 1]:
                count += 1
        return count


class Day4Solution(AdventSolution):
    """Enhanced solution for Day 4: Secure Container."""
    
    def __init__(self):
        super().__init__(year=2019, day=4, title="Secure Container")
    
    def _parse_range(self, input_data: str) -> Tuple[int, int]:
        """
        Parse the password range from input data.
        
        Args:
            input_data: Input containing the range (e.g., "125730-579381")
            
        Returns:
            Tuple of (min_value, max_value)
        """
        range_str = input_data.strip()
        if '-' in range_str:
            min_val, max_val = map(int, range_str.split('-'))
        else:
            # If no dash, try to parse as space-separated or assume single number
            parts = range_str.split()
            if len(parts) == 2:
                min_val, max_val = int(parts[0]), int(parts[1])
            else:
                # Default range from the problem if input is malformed
                min_val, max_val = 125730, 579381
        
        return min_val, max_val
    
    def part1(self, input_data: str) -> int:
        """
        Count passwords meeting Part 1 criteria (optimized).
        
        Args:
            input_data: Password range specification
            
        Returns:
            Count of valid passwords for Part 1
        """
        min_val, max_val = self._parse_range(input_data)
        
        # Fast counting without object overhead
        count = 0
        for password in range(min_val, max_val + 1):
            if validate_password_fast(password, part2=False):
                count += 1
        
        return count
    
    def part2(self, input_data: str) -> int:
        """
        Count passwords meeting Part 2 criteria (optimized with exact double requirement).
        
        Args:
            input_data: Password range specification
            
        Returns:
            Count of valid passwords for Part 2
        """
        min_val, max_val = self._parse_range(input_data)
        
        # Fast counting without object overhead
        count = 0
        for password in range(min_val, max_val + 1):
            if validate_password_fast(password, part2=True):
                count += 1
        
        return count
    
    def analyze_password_range(self, input_data: str) -> None:
        """
        Provide comprehensive analysis of the password range and criteria.
        
        Args:
            input_data: Password range specification
        """
        min_val, max_val = self._parse_range(input_data)
        
        print(f"Password Range Analysis: {min_val} - {max_val}")
        print(f"Total range size: {max_val - min_val + 1:,}")
        
        # Part 1 analysis
        criteria1 = PasswordCriteria(min_val, max_val, require_adjacent_same=True, 
                                   require_non_decreasing=True)
        validator1 = PasswordValidator(criteria1)
        analyzer1 = PasswordAnalyzer(validator1)
        stats1 = analyzer1.generate_statistics(part2=False)
        
        print(f"\nPart 1 Results:")
        print(f"Valid passwords: {stats1['valid_passwords_count']:,}")
        print(f"Percentage of range: {stats1['valid_percentage']:.2f}%")
        if stats1['first_valid'] and stats1['last_valid']:
            print(f"First valid: {stats1['first_valid']}")
            print(f"Last valid: {stats1['last_valid']}")
        
        # Part 2 analysis
        criteria2 = PasswordCriteria(min_val, max_val, require_adjacent_same=True,
                                   require_non_decreasing=True, require_exact_double=True)
        validator2 = PasswordValidator(criteria2)
        analyzer2 = PasswordAnalyzer(validator2)
        stats2 = analyzer2.generate_statistics(part2=True)
        
        print(f"\nPart 2 Results:")
        print(f"Valid passwords: {stats2['valid_passwords_count']:,}")
        print(f"Percentage of range: {stats2['valid_percentage']:.2f}%")
        if stats2['first_valid'] and stats2['last_valid']:
            print(f"First valid: {stats2['first_valid']}")
            print(f"Last valid: {stats2['last_valid']}")
        
        # Show examples
        part1_valid = analyzer1.find_valid_passwords(part2=False)[:5]
        part2_valid = analyzer2.find_valid_passwords(part2=True)[:5]
        
        print(f"\nFirst 5 Part 1 valid passwords: {part1_valid}")
        print(f"First 5 Part 2 valid passwords: {part2_valid}")
        
        # Analyze a few example passwords
        examples = [111111, 223450, 123789] + part1_valid[:2]
        print(f"\nExample Password Analysis:")
        for password in examples:
            if min_val <= password <= max_val:
                analysis = analyzer1.analyze_password(password)
                print(f"{password}: Part1={analysis['is_valid_part1']}, "
                      f"Part2={analysis['is_valid_part2']}, "
                      f"Groups={analysis['digit_groups']}")

    def validate(self, expected_part1=None, expected_part2=None) -> bool:
        """Validate solution with test cases."""

        # Test cases for part 1
        example_input = """111111-111111"""
        expected_part1 = 1
        
        result = self.part1(example_input)
        if result != expected_part1:
            print(f"Part 1 test failed for example input: expected {expected_part1}, got {result}")
            return False
        
        # Test cases for part 2
        example_input = """112233-112233"""
        expected_part2 = 1
        
        result = self.part2(example_input)
        if result != expected_part2:
            print(f"Part 2 test failed for example input: expected {expected_part2}, got {result}")
            return False

        print("✅ All Day 4 validation tests passed!")
        return True

def main():
    """Main execution function."""
    solution = Day4Solution()
    
    # If run with analyze flag, show comprehensive analysis
    if len(sys.argv) > 1 and sys.argv[1] == 'analyze':
        # Use default range or try to load from input
        try:
            input_data = solution._load_input()
        except:
            input_data = "125730-579381"
        solution.analyze_password_range(input_data)
    else:
        solution.main()


if __name__ == "__main__":
    main()