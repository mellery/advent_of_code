#!/usr/bin/env python3
"""
Advent of Code 2020 Day 10: Adapter Array
https://adventofcode.com/2020/day/10

Joltage adapter chain analysis using dynamic programming for counting arrangements.
Enhanced solution using AdventSolution base class.
"""

import sys
from pathlib import Path
from typing import Any, List, Dict
from collections import Counter

# Add utils to path
sys.path.append(str(Path(__file__).parent.parent))
from utils import AdventSolution, InputParser


class AdapterChain:
    """Manages joltage adapter chains and arrangement counting."""
    
    def __init__(self, adapters: List[int]):
        """
        Initialize adapter chain.
        
        Args:
            adapters: List of adapter joltage ratings
        """
        self.adapters = sorted(adapters)
        self.device_joltage = max(self.adapters) + 3
        self.full_chain = [0] + self.adapters + [self.device_joltage]
        self._arrangements_cache = {}
    
    def get_joltage_differences(self) -> Dict[int, int]:
        """Get count of each joltage difference in the chain."""
        differences = Counter()
        
        for i in range(1, len(self.full_chain)):
            diff = self.full_chain[i] - self.full_chain[i-1]
            differences[diff] += 1
        
        return dict(differences)
    
    def count_arrangements(self) -> int:
        """
        Count total valid arrangements using dynamic programming.
        
        Returns:
            Number of valid adapter arrangements
        """
        # dp[i] = number of ways to reach adapter i
        dp = [0] * len(self.full_chain)
        dp[0] = 1  # One way to start (outlet)
        
        for i in range(1, len(self.full_chain)):
            current_joltage = self.full_chain[i]
            
            # Check all previous adapters within 3 joltage difference
            for j in range(i):
                prev_joltage = self.full_chain[j]
                if current_joltage - prev_joltage <= 3:
                    dp[i] += dp[j]
        
        return dp[-1]  # Ways to reach the device
    
    def find_removable_groups(self) -> List[List[int]]:
        """Find groups of consecutive optional adapters."""
        # Find adapters that MUST be included (3-jolt gaps)
        required = set()
        
        for i in range(1, len(self.full_chain)):
            if self.full_chain[i] - self.full_chain[i-1] == 3:
                required.add(self.full_chain[i-1])
                required.add(self.full_chain[i])
        
        # Add outlet and device as required
        required.add(0)
        required.add(self.device_joltage)
        
        # Find optional groups between required adapters
        optional_groups = []
        current_group = []
        
        for adapter in self.full_chain:
            if adapter in required:
                if current_group:
                    optional_groups.append(current_group)
                    current_group = []
            else:
                current_group.append(adapter)
        
        return optional_groups
    
    def get_chain_analysis(self) -> str:
        """Get detailed analysis of the adapter chain."""
        differences = self.get_joltage_differences()
        arrangements = self.count_arrangements()
        removable_groups = self.find_removable_groups()
        
        analysis = []
        analysis.append(f"Adapters: {len(self.adapters)}")
        analysis.append(f"Full chain length: {len(self.full_chain)}")
        analysis.append(f"Device joltage: {self.device_joltage}")
        analysis.append(f"Joltage differences: {differences}")
        analysis.append(f"Total arrangements: {arrangements}")
        
        if removable_groups:
            analysis.append(f"Optional adapter groups: {len(removable_groups)}")
            for i, group in enumerate(removable_groups):
                if len(group) <= 5:  # Only show small groups
                    analysis.append(f"  Group {i+1}: {group}")
        
        return "\n".join(analysis)


class Day10Solution(AdventSolution):
    """Solution for 2020 Day 10: Adapter Array."""

    def __init__(self):
        super().__init__(2020, 10, "Adapter Array")

    def parse_adapters(self, input_data: str) -> List[int]:
        """
        Parse adapter joltage ratings from input.
        
        Args:
            input_data: Raw input data containing adapter ratings
            
        Returns:
            List of adapter joltage ratings
        """
        adapters = []
        for line in input_data.strip().split('\n'):
            line = line.strip()
            if line and line.isdigit():
                adapters.append(int(line))
        return adapters

    def part1(self, input_data: str) -> int:
        """
        Solve part 1: Multiply 1-jolt and 3-jolt difference counts.
        
        Args:
            input_data: The input data as a string
            
        Returns:
            Product of 1-jolt and 3-jolt differences
        """
        adapters = self.parse_adapters(input_data)
        chain = AdapterChain(adapters)
        differences = chain.get_joltage_differences()
        
        ones = differences.get(1, 0)
        threes = differences.get(3, 0)
        
        return ones * threes

    def part2(self, input_data: str) -> int:
        """
        Solve part 2: Count distinct adapter arrangements.
        
        Args:
            input_data: The input data as a string
            
        Returns:
            Number of distinct valid arrangements
        """
        adapters = self.parse_adapters(input_data)
        chain = AdapterChain(adapters)
        return chain.count_arrangements()

    def analyze_adapters(self, input_data: str) -> str:
        """
        Analyze adapter chain properties and arrangements.
        
        Args:
            input_data: Raw input data
            
        Returns:
            Analysis summary as formatted string
        """
        adapters = self.parse_adapters(input_data)
        
        analysis = []
        analysis.append("=== Adapter Chain Analysis ===")
        
        if not adapters:
            analysis.append("No adapters found.")
            return "\n".join(analysis)
        
        chain = AdapterChain(adapters)
        analysis.append(chain.get_chain_analysis())
        
        return "\n".join(analysis)

    def validate(self, expected_part1=None, expected_part2=None) -> bool:
        """Validate solution with test cases."""
        # Test with simple example
        test_input1 = """16
10
15
5
1
11
7
19
6
12
4"""
        
        adapters = self.parse_adapters(test_input1)
        chain = AdapterChain(adapters)
        
        # Check parsing
        expected_adapters = [1, 4, 5, 6, 7, 10, 11, 12, 15, 16, 19]
        if chain.adapters != expected_adapters:
            print(f"Parsing test failed: expected {expected_adapters}, got {chain.adapters}")
            return False
        
        # Test differences
        differences = chain.get_joltage_differences()
        expected_diffs = {1: 7, 3: 5}
        if differences != expected_diffs:
            print(f"Differences test failed: expected {expected_diffs}, got {differences}")
            return False
        
        # Test part 1
        part1_result = differences[1] * differences[3]
        if part1_result != 35:
            print(f"Part 1 test failed: expected 35, got {part1_result}")
            return False
        
        # Test part 2
        part2_result = chain.count_arrangements()
        if part2_result != 8:
            print(f"Part 2 test failed: expected 8, got {part2_result}")
            return False
        
        # Test with larger example
        test_input2 = """28
33
18
42
31
14
46
20
48
47
24
23
49
45
19
38
39
11
1
32
25
35
8
17
7
9
4
2
34
10
3"""
        
        adapters2 = self.parse_adapters(test_input2)
        chain2 = AdapterChain(adapters2)
        
        part2_result2 = chain2.count_arrangements()
        if part2_result2 != 19208:
            print(f"Part 2 larger test failed: expected 19208, got {part2_result2}")
            return False
        
        print("✅ All Day 10 validation tests passed!")
        return True


# Legacy compatibility functions for test runner
def part1(input_data: str = None) -> int:
    """Part 1 function compatible with test runner."""
    solution = Day10Solution()
    if input_data is None:
        # Use actual input file
        input_data = solution._load_input()
    return solution.part1(input_data)


def part2(input_data: str = None) -> int:
    """Part 2 function compatible with test runner."""
    solution = Day10Solution()
    if input_data is None:
        # Use actual input file
        input_data = solution._load_input()
    return solution.part2(input_data)


def main():
    """Main function to run the solution."""
    solution = Day10Solution()
    solution.main()


if __name__ == "__main__":
    main()