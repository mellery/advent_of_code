#!/usr/bin/env python3
"""
Advent of Code 2020 Day 19: Monster Messages
https://adventofcode.com/2020/day/19

Grammar rule parsing and message validation using recursive descent parsing.
Enhanced solution using AdventSolution base class.
"""

import sys
import re
from pathlib import Path
from typing import Any, Dict, List, Set, Optional, Tuple
from collections import defaultdict

# Add utils to path
sys.path.append(str(Path(__file__).parent.parent))
from utils import AdventSolution, InputParser


class GrammarRule:
    """Represents a single grammar rule with parsing capabilities."""
    
    def __init__(self, rule_id: int, rule_text: str):
        """
        Initialize a grammar rule.
        
        Args:
            rule_id: The numeric ID of the rule
            rule_text: The rule definition text
        """
        self.rule_id = rule_id
        self.rule_text = rule_text.strip()
        self.is_terminal = False
        self.terminal_char = None
        self.alternatives = []  # List of lists of rule IDs
        
        self._parse_rule()
    
    def _parse_rule(self):
        """Parse the rule text into structured form."""
        if '"' in self.rule_text:
            # Terminal rule like 'a' or 'b'
            self.is_terminal = True
            self.terminal_char = self.rule_text.strip('"')
        else:
            # Non-terminal rule with alternatives
            alternatives = self.rule_text.split('|')
            for alt in alternatives:
                rule_sequence = [int(x.strip()) for x in alt.strip().split() if x.strip().isdigit()]
                if rule_sequence:
                    self.alternatives.append(rule_sequence)
    
    def __repr__(self) -> str:
        if self.is_terminal:
            return f"Rule({self.rule_id}: '{self.terminal_char}')"
        else:
            return f"Rule({self.rule_id}: {self.alternatives})"


class MessageValidator:
    """Validates messages against a set of grammar rules."""
    
    def __init__(self, rules: Dict[int, GrammarRule]):
        """
        Initialize the validator with grammar rules.
        
        Args:
            rules: Dictionary mapping rule IDs to GrammarRule objects
        """
        self.rules = rules
        self.memo = {}  # Memoization for performance
    
    def validate_message(self, message: str, start_rule: int = 0) -> bool:
        """
        Check if a message matches the grammar starting from a specific rule.
        
        Args:
            message: The message to validate
            start_rule: The rule ID to start validation from
            
        Returns:
            True if the message matches the grammar
        """
        # Use recursive descent parsing
        result = self._parse_recursive(message, 0, start_rule)
        # Check if we consumed the entire message
        return len(message) in result
    
    def _parse_recursive(self, message: str, pos: int, rule_id: int) -> Set[int]:
        """
        Recursively parse message starting at position using given rule.
        
        Args:
            message: The message being parsed
            pos: Current position in the message
            rule_id: The rule to apply
            
        Returns:
            Set of positions where parsing could end successfully
        """
        if pos >= len(message):
            return set()
        
        # Memoization key
        key = (pos, rule_id)
        if key in self.memo:
            return self.memo[key]
        
        rule = self.rules[rule_id]
        result = set()
        
        if rule.is_terminal:
            # Terminal rule: check if current character matches
            if pos < len(message) and message[pos] == rule.terminal_char:
                result.add(pos + 1)
        else:
            # Non-terminal rule: try each alternative
            for alternative in rule.alternatives:
                # For each alternative, try to parse the sequence of rules
                current_positions = {pos}
                
                for next_rule_id in alternative:
                    new_positions = set()
                    for current_pos in current_positions:
                        new_positions.update(self._parse_recursive(message, current_pos, next_rule_id))
                    current_positions = new_positions
                    
                    if not current_positions:
                        break  # This alternative failed
                
                result.update(current_positions)
        
        self.memo[key] = result
        return result
    
    def get_valid_messages(self, messages: List[str], start_rule: int = 0) -> List[str]:
        """Get all messages that are valid according to the grammar."""
        valid = []
        for message in messages:
            if self.validate_message(message, start_rule):
                valid.append(message)
        return valid
    
    def count_valid_messages(self, messages: List[str], start_rule: int = 0) -> int:
        """Count how many messages are valid according to the grammar."""
        count = 0
        for message in messages:
            if self.validate_message(message, start_rule):
                count += 1
        return count


class Day19Solution(AdventSolution):
    """Solution for 2020 Day 19: Monster Messages."""

    def __init__(self):
        super().__init__(2020, 19, "Monster Messages")

    def parse_input(self, input_data: str) -> Tuple[Dict[int, GrammarRule], List[str]]:
        """
        Parse input data into grammar rules and messages.
        
        Args:
            input_data: Raw input data containing rules and messages
            
        Returns:
            Tuple of (rules dictionary, messages list)
        """
        lines = input_data.strip().split('\n')
        
        rules = {}
        messages = []
        
        for line in lines:
            line = line.strip()
            if ':' in line:
                # Parse rule
                rule_id_str, rule_text = line.split(':', 1)
                rule_id = int(rule_id_str.strip())
                rules[rule_id] = GrammarRule(rule_id, rule_text.strip())
            elif line:
                # Parse message
                messages.append(line)
        
        return rules, messages

    def part1(self, input_data: str) -> int:
        """
        Solve part 1: Count messages that match rule 0.
        
        Args:
            input_data: The input data as a string
            
        Returns:
            Number of valid messages
        """
        rules, messages = self.parse_input(input_data)
        
        if not rules:
            return 0
        
        validator = MessageValidator(rules)
        return validator.count_valid_messages(messages, start_rule=0)

    def part2(self, input_data: str) -> int:
        """
        Solve part 2: Count messages with modified recursive rules.
        
        Args:
            input_data: The input data as a string
            
        Returns:
            Number of valid messages with modified rules
        """
        rules, messages = self.parse_input(input_data)
        
        if not rules:
            return 0
        
        # Apply the rule modifications for part 2
        # Rule 8: 42 | 42 8 (equivalent to 42+)
        # Rule 11: 42 31 | 42 11 31 (equivalent to 42^n 31^n)
        
        # Modify rule 8: 42 | 42 8
        rules[8] = GrammarRule(8, "42 | 42 8")
        
        # Modify rule 11: 42 31 | 42 11 31  
        rules[11] = GrammarRule(11, "42 31 | 42 11 31")
        
        validator = MessageValidator(rules)
        return validator.count_valid_messages(messages, start_rule=0)

    def analyze_grammar(self, input_data: str) -> str:
        """
        Analyze the grammar structure for insights.
        
        Args:
            input_data: Raw input data
            
        Returns:
            Analysis summary as formatted string
        """
        rules, messages = self.parse_input(input_data)
        
        analysis = []
        analysis.append("=== Grammar Analysis ===")
        analysis.append(f"Total rules: {len(rules)}")
        analysis.append(f"Total messages: {len(messages)}")
        
        if not rules:
            return "\n".join(analysis)
        
        # Categorize rules
        terminal_rules = [r for r in rules.values() if r.is_terminal]
        non_terminal_rules = [r for r in rules.values() if not r.is_terminal]
        
        analysis.append(f"Terminal rules: {len(terminal_rules)}")
        analysis.append(f"Non-terminal rules: {len(non_terminal_rules)}")
        
        # Show terminal rules
        if terminal_rules:
            analysis.append("\nTerminal rules:")
            for rule in sorted(terminal_rules, key=lambda x: x.rule_id):
                analysis.append(f"  {rule.rule_id}: '{rule.terminal_char}'")
        
        # Show some non-terminal rules
        if non_terminal_rules:
            analysis.append(f"\nSample non-terminal rules:")
            for rule in sorted(non_terminal_rules, key=lambda x: x.rule_id)[:10]:
                analysis.append(f"  {rule.rule_id}: {rule.rule_text}")
        
        # Message length statistics
        if messages:
            msg_lengths = [len(msg) for msg in messages]
            analysis.append(f"\nMessage lengths: min={min(msg_lengths)}, max={max(msg_lengths)}, avg={sum(msg_lengths)/len(msg_lengths):.1f}")
        
        # Validate messages
        validator = MessageValidator(rules)
        valid_count = validator.count_valid_messages(messages, start_rule=0)
        analysis.append(f"Valid messages (part 1): {valid_count}/{len(messages)}")
        
        return "\n".join(analysis)

    def debug_message_validation(self, input_data: str, message_index: int = 0) -> str:
        """
        Debug the validation process for a specific message.
        
        Args:
            input_data: Raw input data
            message_index: Index of the message to debug
            
        Returns:
            Debug information as formatted string
        """
        rules, messages = self.parse_input(input_data)
        
        if message_index >= len(messages):
            return f"Message index {message_index} not found (only {len(messages)} messages available)"
        
        message = messages[message_index]
        validator = MessageValidator(rules)
        
        debug_info = []
        debug_info.append(f"=== Debug Message {message_index + 1} ===")
        debug_info.append(f"Message: '{message}' (length: {len(message)})")
        
        # Check validation result
        is_valid = validator.validate_message(message, start_rule=0)
        debug_info.append(f"Valid: {is_valid}")
        
        # Show which positions rule 0 can reach
        if 0 in rules:
            end_positions = validator._parse_recursive(message, 0, 0)
            debug_info.append(f"Rule 0 can reach positions: {sorted(end_positions)}")
            debug_info.append(f"Full match needed at position: {len(message)}")
        
        return "\n".join(debug_info)

    def validate(self, expected_part1=None, expected_part2=None) -> bool:
        """Validate solution with test cases."""
        # Test with example from problem description
        test_input = """0: 4 1 5
1: 2 3 | 3 2
2: 4 4 | 5 5
3: 4 5 | 5 4
4: "a"
5: "b"

ababbb
bababa
abbbab
aaabbb
aaaabbb"""
        
        rules, messages = self.parse_input(test_input)
        
        # Validate parsing
        if len(rules) != 6:
            print(f"Rule parsing failed: expected 6 rules, got {len(rules)}")
            return False
        
        if len(messages) != 5:
            print(f"Message parsing failed: expected 5 messages, got {len(messages)}")
            return False
        
        # Check terminal rules
        if not rules[4].is_terminal or rules[4].terminal_char != 'a':
            print(f"Rule 4 parsing failed: expected terminal 'a', got {rules[4]}")
            return False
        
        if not rules[5].is_terminal or rules[5].terminal_char != 'b':
            print(f"Rule 5 parsing failed: expected terminal 'b', got {rules[5]}")
            return False
        
        # Test validation
        validator = MessageValidator(rules)
        
        # Test individual messages
        expected_results = [True, False, True, False, False]  # ababbb, bababa, abbbab, aaabbb, aaaabbb
        
        for i, (message, expected) in enumerate(zip(messages, expected_results)):
            result = validator.validate_message(message, start_rule=0)
            if result != expected:
                print(f"Message {i} validation failed: '{message}' expected {expected}, got {result}")
                return False
        
        # Test part 1: should be 2 valid messages
        part1_result = validator.count_valid_messages(messages, start_rule=0)
        if part1_result != 2:
            print(f"Part 1 test failed: expected 2, got {part1_result}")
            return False
        
        print("✅ All Day 19 validation tests passed!")
        return True


# Legacy compatibility functions for test runner
def part1(input_data: str = None) -> int:
    """Part 1 function compatible with test runner."""
    solution = Day19Solution()
    if input_data is None:
        # Use actual input file
        input_data = solution._load_input()
    return solution.part1(input_data)


def part2(input_data: str = None) -> int:
    """Part 2 function compatible with test runner."""
    solution = Day19Solution()
    if input_data is None:
        # Use actual input file
        input_data = solution._load_input()
    return solution.part2(input_data)


def main():
    """Main function to run the solution."""
    solution = Day19Solution()
    solution.main()


if __name__ == "__main__":
    main()