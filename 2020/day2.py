#!/usr/bin/env python3
"""
Advent of Code 2020 Day 2: Password Philosophy
https://adventofcode.com/2020/day/2

Password validation with different policy rules for corporate password policies.
Enhanced solution using AdventSolution base class.
"""

import sys
from pathlib import Path
from typing import Any, List, Dict, Tuple
import re

# Add utils to path
sys.path.append(str(Path(__file__).parent.parent))
from utils import AdventSolution, InputParser


class PasswordPolicy:
    """Represents a password policy with validation rules."""
    
    def __init__(self, min_count: int, max_count: int, character: str):
        """
        Initialize a password policy.
        
        Args:
            min_count: Minimum count for sled rental policy, or first position for toboggan policy
            max_count: Maximum count for sled rental policy, or second position for toboggan policy
            character: The character the policy applies to
        """
        self.min_count = min_count
        self.max_count = max_count
        self.character = character
    
    def is_valid_sled_rental(self, password: str) -> bool:
        """
        Validate password using sled rental policy (character count range).
        
        Args:
            password: The password to validate
            
        Returns:
            True if password meets sled rental policy requirements
        """
        char_count = password.count(self.character)
        return self.min_count <= char_count <= self.max_count
    
    def is_valid_toboggan_corporate(self, password: str) -> bool:
        """
        Validate password using toboggan corporate policy (positional XOR).
        
        Args:
            password: The password to validate
            
        Returns:
            True if password meets toboggan corporate policy requirements
        """
        # Convert to 0-indexed positions
        pos1 = self.min_count - 1
        pos2 = self.max_count - 1
        
        # Check if positions are valid
        if pos1 < 0 or pos2 < 0 or pos1 >= len(password) or pos2 >= len(password):
            return False
        
        # XOR: exactly one position should contain the character
        char_at_pos1 = password[pos1] == self.character
        char_at_pos2 = password[pos2] == self.character
        
        return char_at_pos1 != char_at_pos2  # XOR logic
    
    def __repr__(self) -> str:
        return f"PasswordPolicy({self.min_count}-{self.max_count} {self.character})"


class PasswordEntry:
    """Represents a password entry with its associated policy."""
    
    def __init__(self, policy: PasswordPolicy, password: str):
        """
        Initialize a password entry.
        
        Args:
            policy: The password policy to apply
            password: The password to validate
        """
        self.policy = policy
        self.password = password
        self._sled_valid = None
        self._toboggan_valid = None
    
    @property
    def is_valid_sled_rental(self) -> bool:
        """Check if password is valid under sled rental policy (cached)."""
        if self._sled_valid is None:
            self._sled_valid = self.policy.is_valid_sled_rental(self.password)
        return self._sled_valid
    
    @property
    def is_valid_toboggan_corporate(self) -> bool:
        """Check if password is valid under toboggan corporate policy (cached)."""
        if self._toboggan_valid is None:
            self._toboggan_valid = self.policy.is_valid_toboggan_corporate(self.password)
        return self._toboggan_valid
    
    def get_character_analysis(self) -> Dict[str, Any]:
        """Get detailed analysis of the password character distribution."""
        char_count = self.password.count(self.policy.character)
        total_chars = len(self.password)
        
        # Check positions for toboggan policy
        pos1 = self.policy.min_count - 1
        pos2 = self.policy.max_count - 1
        
        pos1_char = self.password[pos1] if 0 <= pos1 < len(self.password) else None
        pos2_char = self.password[pos2] if 0 <= pos2 < len(self.password) else None
        
        return {
            'target_character': self.policy.character,
            'character_count': char_count,
            'total_length': total_chars,
            'character_frequency': char_count / total_chars if total_chars > 0 else 0,
            'sled_range': f"{self.policy.min_count}-{self.policy.max_count}",
            'toboggan_pos1': pos1 + 1,
            'toboggan_pos2': pos2 + 1,
            'char_at_pos1': pos1_char,
            'char_at_pos2': pos2_char,
            'positions_match_target': (pos1_char == self.policy.character, pos2_char == self.policy.character)
        }
    
    def __repr__(self) -> str:
        return f"PasswordEntry({self.policy}, '{self.password}', sled={self.is_valid_sled_rental}, toboggan={self.is_valid_toboggan_corporate})"


class Day2Solution(AdventSolution):
    """Solution for 2020 Day 2: Password Philosophy."""

    def __init__(self):
        super().__init__(2020, 2, "Password Philosophy")

    def parse_password_entries(self, input_data: str) -> List[PasswordEntry]:
        """
        Parse password entries from input data.
        
        Args:
            input_data: Raw input data containing password entries
            
        Returns:
            List of PasswordEntry objects
        """
        entries = []
        
        # Pattern: "1-3 a: abcde"
        pattern = r'(\d+)-(\d+)\s+(\w):\s+(.+)'
        
        for line in input_data.strip().split('\n'):
            line = line.strip()
            if not line:
                continue
                
            match = re.match(pattern, line)
            if not match:
                continue
            
            min_count = int(match.group(1))
            max_count = int(match.group(2))
            character = match.group(3)
            password = match.group(4)
            
            policy = PasswordPolicy(min_count, max_count, character)
            entries.append(PasswordEntry(policy, password))
        
        return entries

    def part1(self, input_data: str) -> int:
        """
        Solve part 1: Count passwords valid under sled rental policy.
        
        Args:
            input_data: The input data as a string
            
        Returns:
            Number of passwords valid under sled rental policy
        """
        entries = self.parse_password_entries(input_data)
        return sum(1 for entry in entries if entry.is_valid_sled_rental)

    def part2(self, input_data: str) -> int:
        """
        Solve part 2: Count passwords valid under toboggan corporate policy.
        
        Args:
            input_data: The input data as a string
            
        Returns:
            Number of passwords valid under toboggan corporate policy
        """
        entries = self.parse_password_entries(input_data)
        return sum(1 for entry in entries if entry.is_valid_toboggan_corporate)

    def analyze_passwords(self, input_data: str) -> str:
        """
        Analyze password patterns and policy compliance.
        
        Args:
            input_data: Raw input data
            
        Returns:
            Analysis summary as formatted string
        """
        entries = self.parse_password_entries(input_data)
        
        if not entries:
            return "No password entries found."
        
        analysis = []
        analysis.append("=== Password Policy Analysis ===")
        analysis.append(f"Total password entries: {len(entries)}")
        
        # Policy validation results
        sled_valid = sum(1 for entry in entries if entry.is_valid_sled_rental)
        toboggan_valid = sum(1 for entry in entries if entry.is_valid_toboggan_corporate)
        both_valid = sum(1 for entry in entries if entry.is_valid_sled_rental and entry.is_valid_toboggan_corporate)
        neither_valid = sum(1 for entry in entries if not entry.is_valid_sled_rental and not entry.is_valid_toboggan_corporate)
        
        analysis.append(f"Sled rental policy valid: {sled_valid} ({sled_valid/len(entries)*100:.1f}%)")
        analysis.append(f"Toboggan corporate policy valid: {toboggan_valid} ({toboggan_valid/len(entries)*100:.1f}%)")
        analysis.append(f"Valid under both policies: {both_valid}")
        analysis.append(f"Valid under neither policy: {neither_valid}")
        
        # Character frequency analysis
        from collections import Counter
        policy_chars = Counter(entry.policy.character for entry in entries)
        most_common_char = policy_chars.most_common(1)[0]
        analysis.append(f"Most common policy character: '{most_common_char[0]}' ({most_common_char[1]} entries)")
        
        # Password length statistics
        password_lengths = [len(entry.password) for entry in entries]
        analysis.append(f"Password lengths: min={min(password_lengths)}, max={max(password_lengths)}, avg={sum(password_lengths)/len(password_lengths):.1f}")
        
        # Policy range analysis
        policy_ranges = [entry.policy.max_count - entry.policy.min_count for entry in entries]
        analysis.append(f"Policy ranges: min={min(policy_ranges)}, max={max(policy_ranges)}, avg={sum(policy_ranges)/len(policy_ranges):.1f}")
        
        return "\n".join(analysis)

    def debug_entry(self, input_data: str, entry_index: int = 0) -> str:
        """
        Provide detailed debugging information for a specific password entry.
        
        Args:
            input_data: Raw input data
            entry_index: Index of the entry to debug
            
        Returns:
            Detailed debug information as formatted string
        """
        entries = self.parse_password_entries(input_data)
        
        if entry_index >= len(entries):
            return f"Entry index {entry_index} not found (only {len(entries)} entries available)"
        
        entry = entries[entry_index]
        analysis = entry.get_character_analysis()
        
        debug_info = []
        debug_info.append(f"=== Debug Entry {entry_index + 1} ===")
        debug_info.append(f"Password: '{entry.password}'")
        debug_info.append(f"Policy: {entry.policy.min_count}-{entry.policy.max_count} {entry.policy.character}")
        debug_info.append("")
        debug_info.append("Sled Rental Policy (character count):")
        debug_info.append(f"  Target character '{analysis['target_character']}' appears {analysis['character_count']} times")
        debug_info.append(f"  Required range: {analysis['sled_range']}")
        debug_info.append(f"  Valid: {entry.is_valid_sled_rental}")
        debug_info.append("")
        debug_info.append("Toboggan Corporate Policy (positional XOR):")
        debug_info.append(f"  Position {analysis['toboggan_pos1']}: '{analysis['char_at_pos1']}' (matches: {analysis['positions_match_target'][0]})")
        debug_info.append(f"  Position {analysis['toboggan_pos2']}: '{analysis['char_at_pos2']}' (matches: {analysis['positions_match_target'][1]})")
        debug_info.append(f"  XOR result: {analysis['positions_match_target'][0]} != {analysis['positions_match_target'][1]} = {entry.is_valid_toboggan_corporate}")
        debug_info.append(f"  Valid: {entry.is_valid_toboggan_corporate}")
        
        return "\n".join(debug_info)

    def validate(self, expected_part1=None, expected_part2=None) -> bool:
        """Validate solution with test cases."""
        # Test with examples from problem description
        test_input = """1-3 a: abcde
1-3 b: cdefg
2-9 c: ccccccccc"""
        
        entries = self.parse_password_entries(test_input)
        
        # Should parse 3 entries
        if len(entries) != 3:
            print(f"Parsing test failed: expected 3 entries, got {len(entries)}")
            return False
        
        # Test individual entries
        expected_sled = [True, False, True]  # abcde (1 'a'), cdefg (0 'b'), ccccccccc (9 'c')
        expected_toboggan = [True, False, False]  # pos1='a'&pos3='d' (XOR), pos1='c'&pos3='e' (neither 'b'), pos2='c'&pos9='c' (both 'c')
        
        for i, entry in enumerate(entries):
            if entry.is_valid_sled_rental != expected_sled[i]:
                print(f"Entry {i} sled test failed: expected {expected_sled[i]}, got {entry.is_valid_sled_rental}")
                return False
            if entry.is_valid_toboggan_corporate != expected_toboggan[i]:
                print(f"Entry {i} toboggan test failed: expected {expected_toboggan[i]}, got {entry.is_valid_toboggan_corporate}")
                return False
        
        # Test part 1: should be 2
        part1_result = sum(1 for entry in entries if entry.is_valid_sled_rental)
        if part1_result != 2:
            print(f"Part 1 test failed: expected 2, got {part1_result}")
            return False
        
        # Test part 2: should be 1
        part2_result = sum(1 for entry in entries if entry.is_valid_toboggan_corporate)
        if part2_result != 1:
            print(f"Part 2 test failed: expected 1, got {part2_result}")
            return False
        
        print("✅ All Day 2 validation tests passed!")
        return True


# Legacy compatibility functions for test runner
def part1(input_data: str = None) -> int:
    """Part 1 function compatible with test runner."""
    solution = Day2Solution()
    if input_data is None:
        # Use actual input file
        input_data = solution._load_input()
    return solution.part1(input_data)


def part2(input_data: str = None) -> int:
    """Part 2 function compatible with test runner."""
    solution = Day2Solution()
    if input_data is None:
        # Use actual input file
        input_data = solution._load_input()
    return solution.part2(input_data)


def main():
    """Main function to run the solution."""
    solution = Day2Solution()
    solution.main()


if __name__ == "__main__":
    main()