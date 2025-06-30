#!/usr/bin/env python3
"""
Advent of Code 2020 Day 6: Custom Customs
https://adventofcode.com/2020/day/6

Customs declaration form processing using set operations for group answers.
Enhanced solution using AdventSolution base class.
"""

import sys
from pathlib import Path
from typing import Any, List, Set, Dict
from collections import Counter

# Add utils to path
sys.path.append(str(Path(__file__).parent.parent))
from utils import AdventSolution, InputParser


class CustomsGroup:
    """Represents a group of people and their customs declaration answers."""
    
    def __init__(self, answers: List[str]):
        """
        Initialize a customs group.
        
        Args:
            answers: List of answer strings, one per person in the group
        """
        self.answers = answers
        self.people_count = len(answers)
        self._anyone_yes = None
        self._everyone_yes = None
    
    @property
    def anyone_yes_count(self) -> int:
        """Count of questions where ANYONE in the group answered yes."""
        if self._anyone_yes is None:
            all_answers = set()
            for person_answers in self.answers:
                all_answers.update(person_answers)
            self._anyone_yes = len(all_answers)
        return self._anyone_yes
    
    @property
    def everyone_yes_count(self) -> int:
        """Count of questions where EVERYONE in the group answered yes."""
        if self._everyone_yes is None:
            if not self.answers:
                self._everyone_yes = 0
            else:
                # Start with first person's answers
                common_answers = set(self.answers[0])
                # Intersect with each other person's answers
                for person_answers in self.answers[1:]:
                    common_answers.intersection_update(person_answers)
                self._everyone_yes = len(common_answers)
        return self._everyone_yes
    
    def get_anyone_yes_questions(self) -> Set[str]:
        """Get the set of questions where anyone answered yes."""
        all_answers = set()
        for person_answers in self.answers:
            all_answers.update(person_answers)
        return all_answers
    
    def get_everyone_yes_questions(self) -> Set[str]:
        """Get the set of questions where everyone answered yes."""
        if not self.answers:
            return set()
        
        common_answers = set(self.answers[0])
        for person_answers in self.answers[1:]:
            common_answers.intersection_update(person_answers)
        return common_answers
    
    def get_answer_frequency(self) -> Dict[str, int]:
        """Get frequency count of each answer across all people in the group."""
        counter = Counter()
        for person_answers in self.answers:
            counter.update(person_answers)
        return dict(counter)
    
    def __repr__(self) -> str:
        return f"CustomsGroup(people={self.people_count}, anyone={self.anyone_yes_count}, everyone={self.everyone_yes_count})"


class Day6Solution(AdventSolution):
    """Solution for 2020 Day 6: Custom Customs."""

    def __init__(self):
        super().__init__(2020, 6, "Custom Customs")

    def parse_groups(self, input_data: str) -> List[CustomsGroup]:
        """
        Parse input data into customs groups.
        
        Args:
            input_data: Raw input data with groups separated by blank lines
            
        Returns:
            List of CustomsGroup objects
        """
        groups = []
        current_group_answers = []
        
        for line in input_data.strip().split('\n'):
            line = line.strip()
            
            if not line:  # Blank line indicates end of group
                if current_group_answers:
                    groups.append(CustomsGroup(current_group_answers))
                    current_group_answers = []
            else:
                current_group_answers.append(line)
        
        # Handle last group if file doesn't end with blank line
        if current_group_answers:
            groups.append(CustomsGroup(current_group_answers))
        
        return groups

    def part1(self, input_data: str) -> int:
        """
        Solve part 1: Sum of questions where ANYONE in each group answered yes.
        
        Args:
            input_data: The input data as a string
            
        Returns:
            Sum of counts where anyone in each group answered yes
        """
        groups = self.parse_groups(input_data)
        return sum(group.anyone_yes_count for group in groups)

    def part2(self, input_data: str) -> int:
        """
        Solve part 2: Sum of questions where EVERYONE in each group answered yes.
        
        Args:
            input_data: The input data as a string
            
        Returns:
            Sum of counts where everyone in each group answered yes
        """
        groups = self.parse_groups(input_data)
        return sum(group.everyone_yes_count for group in groups)

    def analyze_customs_data(self, input_data: str) -> str:
        """
        Analyze the customs declaration data for insights.
        
        Args:
            input_data: Raw input data
            
        Returns:
            Analysis summary as formatted string
        """
        groups = self.parse_groups(input_data)
        
        analysis = []
        analysis.append("=== Customs Declaration Analysis ===")
        analysis.append(f"Total groups: {len(groups)}")
        
        if not groups:
            return "\n".join(analysis)
        
        total_people = sum(group.people_count for group in groups)
        analysis.append(f"Total people: {total_people}")
        analysis.append(f"Average group size: {total_people / len(groups):.1f}")
        
        group_sizes = [group.people_count for group in groups]
        analysis.append(f"Group sizes: min={min(group_sizes)}, max={max(group_sizes)}")
        
        anyone_counts = [group.anyone_yes_count for group in groups]
        everyone_counts = [group.everyone_yes_count for group in groups]
        
        analysis.append(f"Anyone 'yes' answers: min={min(anyone_counts)}, max={max(anyone_counts)}, avg={sum(anyone_counts)/len(anyone_counts):.1f}")
        analysis.append(f"Everyone 'yes' answers: min={min(everyone_counts)}, max={max(everyone_counts)}, avg={sum(everyone_counts)/len(everyone_counts):.1f}")
        
        # Find most common answers across all groups
        all_answer_freq = Counter()
        for group in groups:
            for person_answers in group.answers:
                all_answer_freq.update(person_answers)
        
        if all_answer_freq:
            most_common = all_answer_freq.most_common(5)
            analysis.append(f"Most common answers: {', '.join([f'{q}({c})' for q, c in most_common])}")
        
        # Find groups with perfect consensus (everyone answered same questions)
        perfect_consensus = sum(1 for group in groups if group.anyone_yes_count == group.everyone_yes_count)
        analysis.append(f"Groups with perfect consensus: {perfect_consensus}")
        
        return "\n".join(analysis)

    def validate(self, expected_part1=None, expected_part2=None) -> bool:
        """Validate solution with test cases."""
        # Test with example from problem description
        test_input = """abc

a
b
c

ab
ac

a
a
a
a

b"""
        
        groups = self.parse_groups(test_input)
        
        # Validate parsing
        if len(groups) != 5:
            print(f"Parsing failed: expected 5 groups, got {len(groups)}")
            return False
        
        # Test individual group results
        expected_anyone = [3, 3, 3, 1, 1]  # abc, abc, abc, a, b
        expected_everyone = [3, 0, 1, 1, 1]  # abc, none, a, a, b
        
        for i, group in enumerate(groups):
            if group.anyone_yes_count != expected_anyone[i]:
                print(f"Group {i} anyone test failed: expected {expected_anyone[i]}, got {group.anyone_yes_count}")
                return False
            if group.everyone_yes_count != expected_everyone[i]:
                print(f"Group {i} everyone test failed: expected {expected_everyone[i]}, got {group.everyone_yes_count}")
                return False
        
        # Test part 1: sum should be 11
        part1_result = sum(group.anyone_yes_count for group in groups)
        if part1_result != 11:
            print(f"Part 1 validation failed: expected 11, got {part1_result}")
            return False
        
        # Test part 2: sum should be 6
        part2_result = sum(group.everyone_yes_count for group in groups)
        if part2_result != 6:
            print(f"Part 2 validation failed: expected 6, got {part2_result}")
            return False
        
        print("✅ All Day 6 validation tests passed!")
        return True


# Legacy compatibility functions for test runner
def part1(input_data: str = None) -> int:
    """Part 1 function compatible with test runner."""
    solution = Day6Solution()
    if input_data is None:
        # Use actual input file
        input_data = solution._load_input()
    return solution.part1(input_data)


def part2(input_data: str = None) -> int:
    """Part 2 function compatible with test runner."""
    solution = Day6Solution()
    if input_data is None:
        # Use actual input file
        input_data = solution._load_input()
    return solution.part2(input_data)


def main():
    """Main function to run the solution."""
    solution = Day6Solution()
    solution.main()


if __name__ == "__main__":
    main()