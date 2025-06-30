#!/usr/bin/env python3
"""
Advent of Code 2020 - Day 25: Combo Breaker

Cryptographic handshake protocol based on discrete logarithm problem:
- Two devices exchange public keys using modular exponentiation
- Need to determine the encryption key by finding loop sizes
- Only Part 1 exists (Part 2 is traditionally "collect all stars")

The challenge involves modular arithmetic and cryptographic key derivation.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.advent_base import AdventSolution
from typing import Dict, List, Tuple, Any, Optional
import time
from dataclasses import dataclass


@dataclass
class CryptoDevice:
    """Represents a cryptographic device with public/private keys."""
    name: str
    public_key: int
    secret_loop_size: Optional[int] = None
    subject_number: int = 7  # Default subject number
    
    def __str__(self) -> str:
        return f"{self.name}(public_key={self.public_key}, loop_size={self.secret_loop_size})"


class CryptoHandshake:
    """
    Implements the cryptographic handshake protocol from Day 25.
    
    The protocol is based on modular exponentiation:
    - Each device starts with subject number 7
    - Each device has a secret loop size
    - Public key = (subject_number ^ loop_size) mod 20201227
    - Encryption key is derived by transforming one public key with the other's loop size
    """
    
    MODULUS = 20201227
    DEFAULT_SUBJECT = 7
    
    def __init__(self, card_public_key: int, door_public_key: int):
        """
        Initialize the cryptographic handshake.
        
        Args:
            card_public_key: Card's public key
            door_public_key: Door's public key
        """
        self.card = CryptoDevice("card", card_public_key)
        self.door = CryptoDevice("door", door_public_key)
        self.encryption_key: Optional[int] = None
        self.operations_count = 0
    
    def transform_subject_number(self, subject_number: int, loop_size: int) -> int:
        """
        Transform a subject number using the given loop size.
        
        Args:
            subject_number: Subject number to transform
            loop_size: Number of transformation loops
            
        Returns:
            Transformed value
        """
        value = 1
        for _ in range(loop_size):
            value = (value * subject_number) % self.MODULUS
            self.operations_count += 1
        return value
    
    def find_loop_size(self, public_key: int, subject_number: int = DEFAULT_SUBJECT) -> Optional[int]:
        """
        Find the loop size that generates the given public key.
        
        Args:
            public_key: Target public key
            subject_number: Subject number used for transformation
            
        Returns:
            Loop size if found, None if not found within reasonable bounds
        """
        value = 1
        loop_size = 0
        max_iterations = 50000000  # Prevent infinite loops
        
        while loop_size < max_iterations:
            if value == public_key:
                return loop_size
            
            value = (value * subject_number) % self.MODULUS
            loop_size += 1
            self.operations_count += 1
        
        return None  # Not found within iteration limit
    
    def find_loop_size_optimized(self, public_key: int, subject_number: int = DEFAULT_SUBJECT) -> Optional[int]:
        """
        Find loop size using optimized algorithm with cycle detection.
        
        Args:
            public_key: Target public key
            subject_number: Subject number used for transformation
            
        Returns:
            Loop size if found, None if cycle detected without finding target
        """
        value = 1
        loop_size = 0
        seen = {}
        
        while value != public_key:
            if value in seen:
                # Cycle detected - public key is not reachable
                return None
            
            seen[value] = loop_size
            value = (value * subject_number) % self.MODULUS
            loop_size += 1
            self.operations_count += 1
            
            # Safety check
            if loop_size > 50000000:
                return None
        
        return loop_size
    
    def solve_handshake(self) -> int:
        """
        Solve the cryptographic handshake to find the encryption key.
        
        Returns:
            The encryption key
        """
        if self.encryption_key is not None:
            return self.encryption_key
        
        # Find the card's secret loop size
        self.card.secret_loop_size = self.find_loop_size_optimized(self.card.public_key)
        
        if self.card.secret_loop_size is None:
            raise ValueError(f"Could not find loop size for card public key {self.card.public_key}")
        
        # Calculate encryption key using card's loop size and door's public key
        self.encryption_key = self.transform_subject_number(
            self.door.public_key, 
            self.card.secret_loop_size
        )
        
        return self.encryption_key
    
    def verify_handshake(self) -> bool:
        """
        Verify the handshake by computing the encryption key both ways.
        
        Returns:
            True if both methods produce the same encryption key
        """
        if self.card.secret_loop_size is None:
            self.card.secret_loop_size = self.find_loop_size_optimized(self.card.public_key)
        
        # Also find door's secret loop size for verification
        self.door.secret_loop_size = self.find_loop_size_optimized(self.door.public_key)
        
        if self.door.secret_loop_size is None:
            return False
        
        # Calculate encryption key both ways
        key1 = self.transform_subject_number(self.door.public_key, self.card.secret_loop_size)
        key2 = self.transform_subject_number(self.card.public_key, self.door.secret_loop_size)
        
        return key1 == key2
    
    def get_analysis(self) -> Dict[str, Any]:
        """
        Get comprehensive analysis of the cryptographic handshake.
        
        Returns:
            Analysis results
        """
        # Make sure we have the solution
        encryption_key = self.solve_handshake()
        
        # Find door's loop size for complete analysis
        if self.door.secret_loop_size is None:
            self.door.secret_loop_size = self.find_loop_size_optimized(self.door.public_key)
        
        # Verify the handshake
        verification = self.verify_handshake()
        
        return {
            'devices': {
                'card': {
                    'public_key': self.card.public_key,
                    'secret_loop_size': self.card.secret_loop_size,
                    'subject_number': self.card.subject_number
                },
                'door': {
                    'public_key': self.door.public_key,
                    'secret_loop_size': self.door.secret_loop_size,
                    'subject_number': self.door.subject_number
                }
            },
            'encryption_key': encryption_key,
            'verification': {
                'handshake_valid': verification,
                'operations_performed': self.operations_count
            },
            'security_analysis': {
                'modulus': self.MODULUS,
                'difficulty': self._analyze_difficulty(),
                'key_space_size': self.MODULUS - 1,
                'theoretical_max_operations': self.MODULUS - 1
            },
            'algorithm': {
                'problem_type': 'Discrete Logarithm Problem',
                'security_basis': 'Difficulty of computing discrete logarithms in finite fields',
                'complexity': 'O(sqrt(n)) with best known algorithms',
                'brute_force_complexity': 'O(n) where n is the modulus'
            }
        }
    
    def _analyze_difficulty(self) -> Dict[str, Any]:
        """Analyze the cryptographic difficulty of the problem."""
        max_loop_size = max(
            self.card.secret_loop_size or 0,
            self.door.secret_loop_size or 0
        )
        
        return {
            'max_loop_size_found': max_loop_size,
            'operations_to_solve': self.operations_count,
            'efficiency_ratio': self.operations_count / max_loop_size if max_loop_size > 0 else 0,
            'security_level': self._classify_security_level(max_loop_size)
        }
    
    def _classify_security_level(self, loop_size: int) -> str:
        """Classify the security level based on loop size."""
        if loop_size < 1000:
            return "Very Low (toy example)"
        elif loop_size < 100000:
            return "Low (easily breakable)"
        elif loop_size < 10000000:
            return "Medium (computationally feasible)"
        else:
            return "High (computationally expensive)"
    
    def benchmark_performance(self, iterations: int = 3) -> Dict[str, float]:
        """
        Benchmark the performance of the handshake solution.
        
        Args:
            iterations: Number of iterations to average
            
        Returns:
            Performance statistics
        """
        times = []
        
        for _ in range(iterations):
            # Reset state
            self.card.secret_loop_size = None
            self.door.secret_loop_size = None
            self.encryption_key = None
            self.operations_count = 0
            
            start_time = time.time()
            self.solve_handshake()
            end_time = time.time()
            
            times.append(end_time - start_time)
        
        return {
            'avg_time': sum(times) / len(times),
            'min_time': min(times),
            'max_time': max(times),
            'total_operations': self.operations_count
        }


class Day25Solution(AdventSolution):
    """Solution for Advent of Code 2020 Day 25: Combo Breaker."""
    
    def __init__(self):
        super().__init__(year=2020, day=25, title="Combo Breaker")
    
    def _parse_public_keys(self, input_data: str) -> Tuple[int, int]:
        """
        Parse public keys from input data.
        
        Args:
            input_data: Raw input data
            
        Returns:
            Tuple of (card_public_key, door_public_key)
        """
        lines = input_data.strip().split('\n')
        
        if len(lines) != 2:
            raise ValueError("Input must contain exactly 2 lines with public keys")
        
        try:
            card_key = int(lines[0].strip())
            door_key = int(lines[1].strip())
            return card_key, door_key
        except ValueError as e:
            raise ValueError(f"Invalid public key format: {e}")
    
    def part1(self, input_data: str) -> Any:
        """
        Solve part 1: Find the encryption key.
        
        Args:
            input_data: Raw input data
            
        Returns:
            The encryption key
        """
        card_key, door_key = self._parse_public_keys(input_data)
        handshake = CryptoHandshake(card_key, door_key)
        return handshake.solve_handshake()
    
    def part2(self, input_data: str) -> Any:
        """
        Part 2 doesn't exist for Day 25 - it's the "collect all stars" day.
        
        Args:
            input_data: Raw input data
            
        Returns:
            Message indicating Part 2 is complete
        """
        return "Congratulations! All 49 stars collected. The sleigh is ready for Christmas!"
    
    def analyze(self, input_data: str) -> Dict[str, Any]:
        """
        Provide comprehensive analysis of the combo breaker problem.
        
        Args:
            input_data: Raw input data
            
        Returns:
            Analysis results
        """
        card_key, door_key = self._parse_public_keys(input_data)
        handshake = CryptoHandshake(card_key, door_key)
        
        # Solve and analyze
        encryption_key = handshake.solve_handshake()
        analysis = handshake.get_analysis()
        
        # Benchmark performance
        performance = handshake.benchmark_performance()
        
        return {
            'input': {
                'card_public_key': card_key,
                'door_public_key': door_key
            },
            'solution': {
                'encryption_key': encryption_key,
                'method': 'discrete_logarithm_brute_force'
            },
            'cryptographic_analysis': analysis,
            'performance': performance,
            'part2_note': "Day 25 traditionally has no Part 2 - it's the 'collect all stars' finale"
        }


# Legacy compatibility functions for test runner
def part1(filename: str) -> Any:
    """Legacy function for part 1."""
    with open(filename, 'r') as f:
        input_data = f.read()
    
    solution = Day25Solution()
    return solution.part1(input_data)


def part2(filename: str) -> Any:
    """Legacy function for part 2."""
    # Day 25 typically doesn't have part 2
    return "Merry Christmas! All stars collected!"


if __name__ == "__main__":
    solution = Day25Solution()
    solution.main()