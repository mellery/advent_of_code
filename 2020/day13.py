#!/usr/bin/env python3
"""
Advent of Code 2020 - Day 13: Shuttle Search

Bus scheduling system with two different optimization problems:
- Part 1: Find the earliest bus after a given departure time
- Part 2: Find timestamp where buses depart at consecutive time offsets (Chinese Remainder Theorem)

The challenge involves modular arithmetic and constraint satisfaction.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.advent_base import AdventSolution
from typing import List, Tuple, Dict, Any, Optional
import math


class Bus:
    """Represents a bus with a specific route ID and schedule."""
    
    def __init__(self, bus_id: int, offset: int = 0):
        """
        Initialize a bus.
        
        Args:
            bus_id: The bus route ID (also the period between departures)
            offset: Time offset for synchronized departures (Part 2)
        """
        self.id = bus_id
        self.offset = offset
    
    def next_departure_after(self, timestamp: int) -> int:
        """
        Calculate the next departure time at or after the given timestamp.
        
        Args:
            timestamp: Target timestamp
            
        Returns:
            Next departure timestamp
        """
        if timestamp % self.id == 0:
            return timestamp  # Bus departs exactly at this time
        
        # Find next multiple of bus_id after timestamp
        return ((timestamp // self.id) + 1) * self.id
    
    def wait_time_after(self, timestamp: int) -> int:
        """
        Calculate wait time for next departure after given timestamp.
        
        Args:
            timestamp: Target timestamp
            
        Returns:
            Wait time in minutes
        """
        return self.next_departure_after(timestamp) - timestamp
    
    def departs_at(self, timestamp: int) -> bool:
        """
        Check if bus departs at given timestamp.
        
        Args:
            timestamp: Timestamp to check
            
        Returns:
            True if bus departs at this timestamp
        """
        return timestamp % self.id == 0
    
    def satisfies_offset_constraint(self, base_timestamp: int) -> bool:
        """
        Check if bus satisfies its offset constraint relative to base timestamp.
        
        Args:
            base_timestamp: Base timestamp for constraint checking
            
        Returns:
            True if constraint is satisfied
        """
        target_time = base_timestamp + self.offset
        return self.departs_at(target_time)
    
    def __str__(self) -> str:
        return f"Bus {self.id} (offset: {self.offset})"
    
    def __repr__(self) -> str:
        return f"Bus(id={self.id}, offset={self.offset})"


class BusSchedule:
    """
    Manages bus schedules and solves scheduling optimization problems.
    
    Handles both earliest departure finding and synchronized departure constraints.
    """
    
    def __init__(self, schedule_data: str):
        """
        Initialize bus schedule from input data.
        
        Args:
            schedule_data: Raw schedule data
        """
        self.earliest_timestamp, self.bus_schedule_raw = self._parse_input(schedule_data)
        self.active_buses = self._parse_active_buses()
        self.constraint_buses = self._parse_constraint_buses()
    
    def _parse_input(self, data: str) -> Tuple[int, str]:
        """
        Parse the input data into timestamp and bus schedule string.
        
        Args:
            data: Raw input data
            
        Returns:
            Tuple of (earliest timestamp, bus schedule string)
        """
        lines = data.strip().split('\n')
        if len(lines) < 2:
            raise ValueError("Input must contain at least 2 lines")
        
        earliest_timestamp = int(lines[0])
        bus_schedule = lines[1]
        
        return earliest_timestamp, bus_schedule
    
    def _parse_active_buses(self) -> List[Bus]:
        """
        Parse active buses (non-'x' entries) for Part 1.
        
        Returns:
            List of active Bus objects
        """
        buses = []
        
        for bus_entry in self.bus_schedule_raw.split(','):
            bus_entry = bus_entry.strip()
            if bus_entry != 'x':
                bus_id = int(bus_entry)
                buses.append(Bus(bus_id))
        
        return buses
    
    def _parse_constraint_buses(self) -> List[Bus]:
        """
        Parse buses with offset constraints for Part 2.
        
        Returns:
            List of Bus objects with offset information
        """
        buses = []
        
        for offset, bus_entry in enumerate(self.bus_schedule_raw.split(',')):
            bus_entry = bus_entry.strip()
            if bus_entry != 'x':
                bus_id = int(bus_entry)
                buses.append(Bus(bus_id, offset))
        
        return buses
    
    def find_earliest_bus(self) -> Tuple[Bus, int, int]:
        """
        Find the earliest departing bus after the given timestamp.
        
        Returns:
            Tuple of (bus, departure_time, wait_time)
        """
        if not self.active_buses:
            raise ValueError("No active buses available")
        
        best_bus = None
        min_wait_time = float('inf')
        best_departure_time = 0
        
        for bus in self.active_buses:
            wait_time = bus.wait_time_after(self.earliest_timestamp)
            
            if wait_time < min_wait_time:
                min_wait_time = wait_time
                best_bus = bus
                best_departure_time = bus.next_departure_after(self.earliest_timestamp)
        
        return best_bus, best_departure_time, min_wait_time
    
    def solve_part1(self) -> int:
        """
        Solve Part 1: Find product of bus ID and wait time.
        
        Returns:
            Product of bus ID and wait time
        """
        bus, departure_time, wait_time = self.find_earliest_bus()
        return bus.id * wait_time
    
    def find_synchronized_timestamp_bruteforce(self, max_iterations: int = 100000) -> Optional[int]:
        """
        Find timestamp where all buses satisfy their offset constraints (brute force).
        
        Args:
            max_iterations: Maximum iterations to prevent infinite loops
            
        Returns:
            Timestamp if found, None if not found within iteration limit
        """
        if not self.constraint_buses:
            return None
        
        # Start checking from timestamp 0
        timestamp = 0
        iterations = 0
        
        while iterations < max_iterations:
            if self._all_constraints_satisfied(timestamp):
                return timestamp
            
            timestamp += 1
            iterations += 1
        
        return None  # Not found within iteration limit
    
    def find_synchronized_timestamp_crt(self) -> int:
        """
        Find timestamp using Chinese Remainder Theorem optimization.
        
        This is the efficient solution for Part 2 that can handle large inputs.
        
        Returns:
            Timestamp where all offset constraints are satisfied
        """
        if not self.constraint_buses:
            raise ValueError("No constraint buses available")
        
        # Start with the first bus constraint
        timestamp = 0
        step = 1
        
        for bus in self.constraint_buses:
            # Find timestamp that satisfies this bus's constraint
            while (timestamp + bus.offset) % bus.id != 0:
                timestamp += step
            
            # Once we find a solution for this bus, we can step by LCM
            # of all previous bus periods to maintain all previous constraints
            step = self._lcm(step, bus.id)
        
        return timestamp
    
    def _all_constraints_satisfied(self, timestamp: int) -> bool:
        """
        Check if all bus offset constraints are satisfied at given timestamp.
        
        Args:
            timestamp: Timestamp to check
            
        Returns:
            True if all constraints are satisfied
        """
        for bus in self.constraint_buses:
            if not bus.satisfies_offset_constraint(timestamp):
                return False
        return True
    
    def _gcd(self, a: int, b: int) -> int:
        """Calculate Greatest Common Divisor using Euclidean algorithm."""
        while b:
            a, b = b, a % b
        return a
    
    def _lcm(self, a: int, b: int) -> int:
        """Calculate Least Common Multiple."""
        return abs(a * b) // self._gcd(a, b)
    
    def validate_solution(self, timestamp: int) -> Dict[str, Any]:
        """
        Validate that a timestamp satisfies all constraints.
        
        Args:
            timestamp: Timestamp to validate
            
        Returns:
            Validation results
        """
        results = {
            'timestamp': timestamp,
            'valid': True,
            'constraint_results': [],
            'violations': []
        }
        
        for bus in self.constraint_buses:
            target_time = timestamp + bus.offset
            satisfies = bus.departs_at(target_time)
            
            constraint_result = {
                'bus_id': bus.id,
                'offset': bus.offset,
                'target_time': target_time,
                'satisfies': satisfies
            }
            
            results['constraint_results'].append(constraint_result)
            
            if not satisfies:
                results['valid'] = False
                results['violations'].append(constraint_result)
        
        return results
    
    def get_analysis(self) -> Dict[str, Any]:
        """
        Get comprehensive analysis of the bus schedule.
        
        Returns:
            Dictionary with schedule analysis
        """
        return {
            'earliest_timestamp': self.earliest_timestamp,
            'raw_schedule': self.bus_schedule_raw,
            'active_buses': len(self.active_buses),
            'constraint_buses': len(self.constraint_buses),
            'active_bus_ids': [bus.id for bus in self.active_buses],
            'constraint_specifications': [
                {'bus_id': bus.id, 'offset': bus.offset} 
                for bus in self.constraint_buses
            ],
            'lcm_of_all_buses': self._calculate_schedule_lcm(),
            'schedule_complexity': self._calculate_complexity_score()
        }
    
    def _calculate_schedule_lcm(self) -> int:
        """Calculate LCM of all constraint bus IDs."""
        if not self.constraint_buses:
            return 1
        
        result = self.constraint_buses[0].id
        for bus in self.constraint_buses[1:]:
            result = self._lcm(result, bus.id)
        
        return result
    
    def _calculate_complexity_score(self) -> float:
        """Calculate a complexity score for the scheduling problem."""
        if not self.constraint_buses:
            return 0.0
        
        # Complexity based on number of buses and their ID ranges
        num_buses = len(self.constraint_buses)
        max_id = max(bus.id for bus in self.constraint_buses)
        max_offset = max(bus.offset for bus in self.constraint_buses)
        
        return num_buses * math.log10(max_id) * math.log10(max_offset + 1)


class Day13Solution(AdventSolution):
    """Solution for Advent of Code 2020 Day 13: Shuttle Search."""
    
    def __init__(self):
        super().__init__(year=2020, day=13, title="Shuttle Search")
    
    def part1(self, input_data: str) -> Any:
        """
        Solve part 1: Find earliest bus and calculate wait time product.
        
        Args:
            input_data: Raw input data
            
        Returns:
            Product of bus ID and wait time
        """
        bus_schedule = BusSchedule(input_data)
        return bus_schedule.solve_part1()
    
    def part2(self, input_data: str) -> Any:
        """
        Solve part 2: Find synchronized departure timestamp using CRT.
        
        Args:
            input_data: Raw input data
            
        Returns:
            Timestamp where all buses satisfy offset constraints
        """
        bus_schedule = BusSchedule(input_data)
        return bus_schedule.find_synchronized_timestamp_crt()
    
    def analyze(self, input_data: str) -> Dict[str, Any]:
        """
        Provide comprehensive analysis of the bus scheduling problem.
        
        Args:
            input_data: Raw input data
            
        Returns:
            Analysis results for both parts
        """
        bus_schedule = BusSchedule(input_data)
        
        # Solve both parts
        part1_result = bus_schedule.solve_part1()
        part1_bus, part1_departure, part1_wait = bus_schedule.find_earliest_bus()
        
        part2_result = bus_schedule.find_synchronized_timestamp_crt()
        part2_validation = bus_schedule.validate_solution(part2_result)
        
        # Get schedule analysis
        schedule_analysis = bus_schedule.get_analysis()
        
        return {
            'schedule': schedule_analysis,
            'part1': {
                'result': part1_result,
                'earliest_bus_id': part1_bus.id,
                'departure_time': part1_departure,
                'wait_time': part1_wait,
                'method': 'earliest_departure'
            },
            'part2': {
                'result': part2_result,
                'validation': part2_validation,
                'method': 'chinese_remainder_theorem'
            },
            'performance': {
                'part1_complexity': 'O(n)',
                'part2_complexity': 'O(n * log(max_bus_id))',
                'crt_advantage': 'Scales efficiently with large bus IDs'
            }
        }
    
    def validate(self, expected_part1=None, expected_part2=None) -> bool:
        """Validate solution with test cases."""
        # Test case from problem description
        test_input = """939
7,13,x,x,59,x,31,19"""
        
        expected_part1 = 295
        expected_part2 = 1068781
        
        result1 = self.part1(test_input)
        if result1 != expected_part1:
            print(f"Part 1 test failed: expected {expected_part1}, got {result1}")
            return False
        
        result2 = self.part2(test_input)
        if result2 != expected_part2:
            print(f"Part 2 test failed: expected {expected_part2}, got {result2}")
            return False
        
        print("✅ All Day 13 validation tests passed!")
        return True




def main():
    """Main execution function."""
    solution = Day13Solution()
    solution.main()


if __name__ == "__main__":
    main()