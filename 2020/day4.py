#!/usr/bin/env python3
"""
Advent of Code 2020 Day 4: Passport Processing
https://adventofcode.com/2020/day/4

Passport validation with required fields and value validation rules.
Enhanced solution using AdventSolution base class.
"""

import sys
from pathlib import Path
from typing import Any, Dict, List, Set, Optional
import re

# Add utils to path
sys.path.append(str(Path(__file__).parent.parent))
from utils import AdventSolution, InputParser


class PassportValidator:
    """Validates passport fields according to specific rules."""
    
    # Required fields (cid is optional)
    REQUIRED_FIELDS = {'byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid'}
    
    # Valid eye colors
    VALID_EYE_COLORS = {'amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'}
    
    @staticmethod
    def validate_birth_year(value: str) -> bool:
        """Validate birth year: four digits; at least 1920 and at most 2002."""
        try:
            year = int(value)
            return 1920 <= year <= 2002
        except ValueError:
            return False
    
    @staticmethod
    def validate_issue_year(value: str) -> bool:
        """Validate issue year: four digits; at least 2010 and at most 2020."""
        try:
            year = int(value)
            return 2010 <= year <= 2020
        except ValueError:
            return False
    
    @staticmethod
    def validate_expiration_year(value: str) -> bool:
        """Validate expiration year: four digits; at least 2020 and at most 2030."""
        try:
            year = int(value)
            return 2020 <= year <= 2030
        except ValueError:
            return False
    
    @staticmethod
    def validate_height(value: str) -> bool:
        """
        Validate height: a number followed by either cm or in.
        If cm, the number must be at least 150 and at most 193.
        If in, the number must be at least 59 and at most 76.
        """
        if value.endswith('cm'):
            try:
                height = int(value[:-2])
                return 150 <= height <= 193
            except ValueError:
                return False
        elif value.endswith('in'):
            try:
                height = int(value[:-2])
                return 59 <= height <= 76
            except ValueError:
                return False
        return False
    
    @staticmethod
    def validate_hair_color(value: str) -> bool:
        """Validate hair color: a # followed by exactly six characters 0-9 or a-f."""
        return bool(re.match(r'^#[0-9a-f]{6}$', value))
    
    @staticmethod
    def validate_eye_color(value: str) -> bool:
        """Validate eye color: exactly one of: amb blu brn gry grn hzl oth."""
        return value in PassportValidator.VALID_EYE_COLORS
    
    @staticmethod
    def validate_passport_id(value: str) -> bool:
        """Validate passport ID: a nine-digit number, including leading zeroes."""
        return bool(re.match(r'^\d{9}$', value))
    
    @classmethod
    def validate_field_value(cls, field: str, value: str) -> bool:
        """Validate a specific field value according to its rules."""
        validators = {
            'byr': cls.validate_birth_year,
            'iyr': cls.validate_issue_year,
            'eyr': cls.validate_expiration_year,
            'hgt': cls.validate_height,
            'hcl': cls.validate_hair_color,
            'ecl': cls.validate_eye_color,
            'pid': cls.validate_passport_id,
            'cid': lambda x: True  # Country ID is always valid (ignored)
        }
        
        validator = validators.get(field)
        if validator is None:
            return False  # Unknown field
        
        return validator(value)


class Passport:
    """Represents a passport with validation capabilities."""
    
    def __init__(self, fields: Dict[str, str]):
        """
        Initialize a passport with field data.
        
        Args:
            fields: Dictionary mapping field names to values
        """
        self.fields = fields
        self._has_required_fields = None
        self._is_valid = None
    
    @property
    def has_required_fields(self) -> bool:
        """Check if passport has all required fields (ignoring values)."""
        if self._has_required_fields is None:
            field_set = set(self.fields.keys())
            self._has_required_fields = PassportValidator.REQUIRED_FIELDS.issubset(field_set)
        return self._has_required_fields
    
    @property
    def is_valid(self) -> bool:
        """Check if passport has all required fields AND all values are valid."""
        if self._is_valid is None:
            if not self.has_required_fields:
                self._is_valid = False
            else:
                # Check that all field values are valid
                for field, value in self.fields.items():
                    if not PassportValidator.validate_field_value(field, value):
                        self._is_valid = False
                        break
                else:
                    self._is_valid = True
        return self._is_valid
    
    def get_missing_fields(self) -> Set[str]:
        """Get set of missing required fields."""
        field_set = set(self.fields.keys())
        return PassportValidator.REQUIRED_FIELDS - field_set
    
    def get_invalid_fields(self) -> Dict[str, str]:
        """Get dictionary of field names to values that fail validation."""
        invalid = {}
        for field, value in self.fields.items():
            if not PassportValidator.validate_field_value(field, value):
                invalid[field] = value
        return invalid
    
    def __repr__(self) -> str:
        field_count = len(self.fields)
        return f"Passport(fields={field_count}, required={self.has_required_fields}, valid={self.is_valid})"


class Day4Solution(AdventSolution):
    """Solution for 2020 Day 4: Passport Processing."""

    def __init__(self):
        super().__init__(2020, 4, "Passport Processing")

    def parse_passports(self, input_data: str) -> List[Passport]:
        """
        Parse passport data from input.
        
        Args:
            input_data: Raw input data with passports separated by blank lines
            
        Returns:
            List of Passport objects
        """
        passports = []
        current_passport_data = {}
        
        for line in input_data.strip().split('\n'):
            line = line.strip()
            
            if not line:  # Blank line indicates end of passport
                if current_passport_data:
                    passports.append(Passport(current_passport_data))
                    current_passport_data = {}
            else:
                # Parse key:value pairs from the line
                pairs = line.split()
                for pair in pairs:
                    if ':' in pair:
                        key, value = pair.split(':', 1)
                        current_passport_data[key] = value
        
        # Handle last passport if file doesn't end with blank line
        if current_passport_data:
            passports.append(Passport(current_passport_data))
        
        return passports

    def part1(self, input_data: str) -> int:
        """
        Solve part 1: Count passports with all required fields (ignoring values).
        
        Args:
            input_data: The input data as a string
            
        Returns:
            Number of passports with all required fields
        """
        passports = self.parse_passports(input_data)
        return sum(1 for passport in passports if passport.has_required_fields)

    def part2(self, input_data: str) -> int:
        """
        Solve part 2: Count passports with all required fields AND valid values.
        
        Args:
            input_data: The input data as a string
            
        Returns:
            Number of fully valid passports
        """
        passports = self.parse_passports(input_data)
        return sum(1 for passport in passports if passport.is_valid)

    def analyze_passports(self, input_data: str) -> str:
        """
        Analyze passport data for insights.
        
        Args:
            input_data: Raw input data
            
        Returns:
            Analysis summary as formatted string
        """
        passports = self.parse_passports(input_data)
        
        if not passports:
            return "No passports found."
        
        analysis = []
        analysis.append("=== Passport Analysis ===")
        analysis.append(f"Total passports: {len(passports)}")
        
        # Field presence analysis
        with_required_fields = sum(1 for p in passports if p.has_required_fields)
        fully_valid = sum(1 for p in passports if p.is_valid)
        
        analysis.append(f"With required fields: {with_required_fields}")
        analysis.append(f"Fully valid: {fully_valid}")
        analysis.append(f"Has fields but invalid values: {with_required_fields - fully_valid}")
        
        # Field coverage statistics
        all_fields = set()
        field_counts = {}
        for passport in passports:
            for field in passport.fields:
                all_fields.add(field)
                field_counts[field] = field_counts.get(field, 0) + 1
        
        analysis.append(f"Unique fields found: {sorted(all_fields)}")
        
        # Missing field analysis
        missing_field_stats = {}
        for passport in passports:
            missing = passport.get_missing_fields()
            for field in missing:
                missing_field_stats[field] = missing_field_stats.get(field, 0) + 1
        
        if missing_field_stats:
            analysis.append("Most commonly missing fields:")
            for field, count in sorted(missing_field_stats.items(), key=lambda x: x[1], reverse=True):
                analysis.append(f"  {field}: missing in {count} passports")
        
        # Validation failure analysis
        validation_failures = {}
        for passport in passports:
            if passport.has_required_fields and not passport.is_valid:
                invalid_fields = passport.get_invalid_fields()
                for field in invalid_fields:
                    validation_failures[field] = validation_failures.get(field, 0) + 1
        
        if validation_failures:
            analysis.append("Most common validation failures:")
            for field, count in sorted(validation_failures.items(), key=lambda x: x[1], reverse=True):
                analysis.append(f"  {field}: fails validation in {count} passports")
        
        return "\n".join(analysis)

    def validate(self, expected_part1=None, expected_part2=None) -> bool:
        """Validate solution with test cases."""
        # Test individual field validators
        validator_tests = [
            ('byr', '2002', True),
            ('byr', '2003', False),
            ('hgt', '60in', True),
            ('hgt', '190cm', True),
            ('hgt', '190in', False),
            ('hgt', '190', False),
            ('hcl', '#123abc', True),
            ('hcl', '#123abz', False),
            ('hcl', '123abc', False),
            ('ecl', 'brn', True),
            ('ecl', 'wat', False),
            ('pid', '000000001', True),
            ('pid', '0123456789', False),
        ]
        
        for field, value, expected in validator_tests:
            result = PassportValidator.validate_field_value(field, value)
            if result != expected:
                print(f"Validator test failed for {field}='{value}': expected {expected}, got {result}")
                return False
        
        # Test with example passport data
        test_input = """ecl:gry pid:860033327 eyr:2020 hcl:#fffffd
byr:1937 iyr:2017 cid:147 hgt:183cm

iyr:2013 ecl:amb cid:350 eyr:2023 pid:028048884
hcl:#cfa07d byr:1929

hcl:#ae17e1 iyr:2013
eyr:2024
ecl:brn pid:760753108 byr:1931
hgt:179cm

hcl:#cfa07d eyr:2025 pid:166559648
iyr:2011 ecl:brn hgt:59in"""
        
        passports = self.parse_passports(test_input)
        
        # Should have 4 passports
        if len(passports) != 4:
            print(f"Parsing test failed: expected 4 passports, got {len(passports)}")
            return False
        
        # Test part 1: should have 2 passports with required fields
        part1_result = sum(1 for p in passports if p.has_required_fields)
        if part1_result != 2:
            print(f"Part 1 test failed: expected 2, got {part1_result}")
            return False
        
        print("✅ All Day 4 validation tests passed!")
        return True


# Legacy compatibility functions for test runner
def part1(input_data: str = None) -> int:
    """Part 1 function compatible with test runner."""
    solution = Day4Solution()
    if input_data is None:
        # Use actual input file
        input_data = solution._load_input()
    return solution.part1(input_data)


def part2(input_data: str = None) -> int:
    """Part 2 function compatible with test runner."""
    solution = Day4Solution()
    if input_data is None:
        # Use actual input file
        input_data = solution._load_input()
    return solution.part2(input_data)


def main():
    """Main function to run the solution."""
    solution = Day4Solution()
    solution.main()


if __name__ == "__main__":
    main()