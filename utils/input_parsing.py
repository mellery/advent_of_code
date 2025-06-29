"""
Enhanced input parsing utilities for Advent of Code solutions.

This module provides comprehensive input parsing functions with better
error handling, type conversion, and flexible parsing options.
"""

import re
from typing import List, Union, Optional, Any, Callable, Tuple, Dict, Set
from pathlib import Path
import json


class InputParser:
    """
    Comprehensive input parser with multiple parsing strategies and error handling.
    """
    
    def __init__(self, input_data: str):
        """
        Initialize parser with input data.
        
        Args:
            input_data: Raw input data as string
        """
        self.raw_data = input_data
        self.lines = input_data.strip().split('\n')
        self.non_empty_lines = [line for line in self.lines if line.strip()]
    
    @classmethod
    def from_file(cls, filename: str) -> 'InputParser':
        """
        Create parser from file.
        
        Args:
            filename: Path to input file
            
        Returns:
            InputParser instance
            
        Raises:
            FileNotFoundError: If file doesn't exist
        """
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                return cls(f.read())
        except FileNotFoundError:
            raise FileNotFoundError(f"Input file not found: {filename}")
        except Exception as e:
            raise RuntimeError(f"Error reading file {filename}: {e}")
    
    def as_lines(self, strip_whitespace: bool = True, 
                 skip_empty: bool = False) -> List[str]:
        """
        Get input as list of lines.
        
        Args:
            strip_whitespace: Strip whitespace from each line
            skip_empty: Skip empty lines
            
        Returns:
            List of lines
        """
        lines = self.non_empty_lines if skip_empty else self.lines
        
        if strip_whitespace:
            return [line.strip() for line in lines]
        return lines
    
    def as_integers(self, skip_invalid: bool = False) -> List[int]:
        """
        Parse input as list of integers, one per line.
        
        Args:
            skip_invalid: Skip lines that can't be converted to integers
            
        Returns:
            List of integers
            
        Raises:
            ValueError: If a line can't be converted and skip_invalid is False
        """
        integers = []
        
        for i, line in enumerate(self.non_empty_lines):
            line = line.strip()
            if not line:
                continue
                
            try:
                integers.append(int(line))
            except ValueError:
                if skip_invalid:
                    continue
                raise ValueError(f"Line {i+1} cannot be converted to integer: '{line}'")
        
        return integers
    
    def as_floats(self, skip_invalid: bool = False) -> List[float]:
        """
        Parse input as list of floats, one per line.
        
        Args:
            skip_invalid: Skip lines that can't be converted to floats
            
        Returns:
            List of floats
            
        Raises:
            ValueError: If a line can't be converted and skip_invalid is False
        """
        floats = []
        
        for i, line in enumerate(self.non_empty_lines):
            line = line.strip()
            if not line:
                continue
                
            try:
                floats.append(float(line))
            except ValueError:
                if skip_invalid:
                    continue
                raise ValueError(f"Line {i+1} cannot be converted to float: '{line}'")
        
        return floats
    
    def as_grid(self, convert_func: Optional[Callable[[str], Any]] = None) -> List[List[Any]]:
        """
        Parse input as 2D grid.
        
        Args:
            convert_func: Optional function to convert each character
            
        Returns:
            2D list representing the grid
        """
        grid = []
        
        for line in self.non_empty_lines:
            if convert_func:
                row = [convert_func(char) for char in line]
            else:
                row = list(line)
            grid.append(row)
        
        return grid
    
    def as_digit_grid(self) -> List[List[int]]:
        """
        Parse input as 2D grid of digits.
        
        Returns:
            2D list of integers
            
        Raises:
            ValueError: If any character is not a digit
        """
        return self.as_grid(lambda x: int(x) if x.isdigit() else 
                           (_ for _ in ()).throw(ValueError(f"'{x}' is not a digit")))
    
    def extract_integers(self, pattern: Optional[str] = None) -> List[int]:
        """
        Extract all integers from the input using regex.
        
        Args:
            pattern: Custom regex pattern (default finds all integers including negative)
            
        Returns:
            List of all integers found in the input
        """
        if pattern is None:
            pattern = r'-?\d+'
        
        matches = re.findall(pattern, self.raw_data)
        return [int(match) for match in matches]
    
    def extract_numbers(self, pattern: Optional[str] = None) -> List[float]:
        """
        Extract all numbers (including floats) from the input using regex.
        
        Args:
            pattern: Custom regex pattern (default finds all numbers including negative/decimal)
            
        Returns:
            List of all numbers found in the input
        """
        if pattern is None:
            pattern = r'-?\d+\.?\d*'
        
        matches = re.findall(pattern, self.raw_data)
        return [float(match) for match in matches if match]
    
    def split_by_blank_lines(self) -> List[List[str]]:
        """
        Split input into groups separated by blank lines.
        
        Returns:
            List of groups, where each group is a list of lines
        """
        groups = []
        current_group = []
        
        for line in self.lines:
            if line.strip():
                current_group.append(line.strip())
            else:
                if current_group:
                    groups.append(current_group)
                    current_group = []
        
        # Add the last group if it exists
        if current_group:
            groups.append(current_group)
        
        return groups
    
    def parse_key_value_pairs(self, separator: str = ':',
                             value_type: type = str) -> Dict[str, Any]:
        """
        Parse input as key-value pairs.
        
        Args:
            separator: Separator between key and value
            value_type: Type to convert values to
            
        Returns:
            Dictionary of key-value pairs
        """
        pairs = {}
        
        for line in self.non_empty_lines:
            if separator in line:
                key, value = line.split(separator, 1)
                key = key.strip()
                value = value.strip()
                
                if value_type != str:
                    try:
                        value = value_type(value)
                    except ValueError:
                        continue  # Skip invalid conversions
                
                pairs[key] = value
        
        return pairs
    
    def parse_structured_data(self, line_parser: Callable[[str], Any]) -> List[Any]:
        """
        Parse each line using a custom parser function.
        
        Args:
            line_parser: Function that takes a line and returns parsed data
            
        Returns:
            List of parsed data from each line
        """
        results = []
        
        for i, line in enumerate(self.non_empty_lines):
            try:
                result = line_parser(line.strip())
                results.append(result)
            except Exception as e:
                raise ValueError(f"Error parsing line {i+1} '{line}': {e}")
        
        return results
    
    def find_pattern_matches(self, pattern: str, 
                           group_names: Optional[List[str]] = None) -> List[Dict[str, str]]:
        """
        Find all matches of a regex pattern in the input.
        
        Args:
            pattern: Regex pattern to match
            group_names: Names for capturing groups
            
        Returns:
            List of dictionaries with matched groups
        """
        matches = []
        regex = re.compile(pattern)
        
        for line in self.non_empty_lines:
            match = regex.search(line)
            if match:
                if group_names:
                    match_dict = {}
                    for i, name in enumerate(group_names):
                        if i + 1 <= len(match.groups()):
                            match_dict[name] = match.group(i + 1)
                    matches.append(match_dict)
                else:
                    matches.append({'match': match.group(0), 'groups': match.groups()})
        
        return matches
    
    def as_coordinate_pairs(self, separator: str = ',') -> List[Tuple[int, int]]:
        """
        Parse input as coordinate pairs.
        
        Args:
            separator: Separator between coordinates
            
        Returns:
            List of (x, y) coordinate tuples
        """
        coordinates = []
        
        for line in self.non_empty_lines:
            if separator in line:
                parts = line.strip().split(separator)
                if len(parts) >= 2:
                    try:
                        x = int(parts[0].strip())
                        y = int(parts[1].strip())
                        coordinates.append((x, y))
                    except ValueError:
                        continue  # Skip invalid coordinates
        
        return coordinates
    
    def count_occurrences(self, target: str, per_line: bool = False) -> Union[int, List[int]]:
        """
        Count occurrences of a target string.
        
        Args:
            target: String to count
            per_line: If True, return counts per line; if False, return total count
            
        Returns:
            Total count or list of counts per line
        """
        if per_line:
            return [line.count(target) for line in self.lines]
        else:
            return self.raw_data.count(target)
    
    def as_json(self) -> Any:
        """
        Parse input as JSON.
        
        Returns:
            Parsed JSON data
            
        Raises:
            ValueError: If input is not valid JSON
        """
        try:
            return json.loads(self.raw_data)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON input: {e}")


# Convenience functions for backward compatibility and simple usage
def get_lines(filename: str, strip_whitespace: bool = True, 
              skip_empty: bool = False) -> List[str]:
    """Get input as list of lines."""
    return InputParser.from_file(filename).as_lines(strip_whitespace, skip_empty)


def get_integers(filename: str, skip_invalid: bool = False) -> List[int]:
    """Get input as list of integers."""
    return InputParser.from_file(filename).as_integers(skip_invalid)


def get_grid(filename: str, convert_func: Optional[Callable[[str], Any]] = None) -> List[List[Any]]:
    """Get input as 2D grid."""
    return InputParser.from_file(filename).as_grid(convert_func)


def get_digit_grid(filename: str) -> List[List[int]]:
    """Get input as 2D grid of digits."""
    return InputParser.from_file(filename).as_digit_grid()


def extract_all_integers(filename: str) -> List[int]:
    """Extract all integers from input file."""
    return InputParser.from_file(filename).extract_integers()


def split_by_blank_lines(filename: str) -> List[List[str]]:
    """Split input into groups separated by blank lines."""
    return InputParser.from_file(filename).split_by_blank_lines()


def parse_coordinate_pairs(filename: str, separator: str = ',') -> List[Tuple[int, int]]:
    """Parse input as coordinate pairs."""
    return InputParser.from_file(filename).as_coordinate_pairs(separator)


# Legacy compatibility - keep existing function names
def get_list_of_numbers(filename: str) -> List[int]:
    """Legacy function name for get_integers."""
    return get_integers(filename)