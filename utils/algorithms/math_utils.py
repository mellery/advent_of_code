#!/usr/bin/env python3
"""
Mathematical Utilities Library

Mathematical functions and number theory utilities extracted from AoC solutions.
Optimized for common AoC mathematical patterns and constraints.

Key Features:
- Number theory functions (GCD, LCM, primes, factorization)
- Combinatorics and permutation utilities
- Distance calculations and geometry
- Modular arithmetic and Chinese Remainder Theorem
- Sequence analysis and pattern detection

Performance Targets:
- Basic operations: < 1ms for typical inputs
- Prime operations: < 100ms for numbers up to 10^6
- Complex calculations: < 1s for AoC-sized problems
"""

import math
from typing import List, Tuple, Dict, Set, Iterator, Optional, Union
from functools import lru_cache
from collections import defaultdict
import itertools

# Type definitions
Number = Union[int, float]

def gcd(a: int, b: int) -> int:
    """
    Greatest Common Divisor using Euclidean algorithm.
    
    More efficient than math.gcd for large numbers in some cases.
    """
    while b:
        a, b = b, a % b
    return abs(a)

def lcm(a: int, b: int) -> int:
    """Least Common Multiple."""
    return abs(a * b) // gcd(a, b)

def gcd_multiple(*numbers: int) -> int:
    """GCD of multiple numbers."""
    result = numbers[0]
    for num in numbers[1:]:
        result = gcd(result, num)
    return result

def lcm_multiple(*numbers: int) -> int:
    """LCM of multiple numbers."""
    result = numbers[0]
    for num in numbers[1:]:
        result = lcm(result, num)
    return result

def extended_gcd(a: int, b: int) -> Tuple[int, int, int]:
    """
    Extended Euclidean Algorithm.
    
    Returns (gcd, x, y) such that a*x + b*y = gcd(a, b)
    Useful for modular arithmetic and Diophantine equations.
    """
    if b == 0:
        return a, 1, 0
    
    gcd_val, x1, y1 = extended_gcd(b, a % b)
    x = y1
    y = x1 - (a // b) * y1
    
    return gcd_val, x, y

def mod_inverse(a: int, m: int) -> Optional[int]:
    """
    Modular multiplicative inverse.
    
    Returns x such that (a * x) % m = 1, or None if it doesn't exist.
    """
    gcd_val, x, y = extended_gcd(a, m)
    if gcd_val != 1:
        return None  # Inverse doesn't exist
    return (x % m + m) % m

def chinese_remainder_theorem(remainders: List[int], moduli: List[int]) -> Optional[int]:
    """
    Chinese Remainder Theorem solver.
    
    Finds x such that x ≡ remainders[i] (mod moduli[i]) for all i.
    Common in AoC problems involving cycles and periodicity.
    """
    if len(remainders) != len(moduli):
        return None
    
    # Check if moduli are pairwise coprime
    for i in range(len(moduli)):
        for j in range(i + 1, len(moduli)):
            if gcd(moduli[i], moduli[j]) != 1:
                return None
    
    total = 0
    product = 1
    for m in moduli:
        product *= m
    
    for i in range(len(remainders)):
        partial_product = product // moduli[i]
        inverse = mod_inverse(partial_product, moduli[i])
        if inverse is None:
            return None
        total += remainders[i] * partial_product * inverse
    
    return total % product

@lru_cache(maxsize=10000)
def is_prime(n: int) -> bool:
    """
    Efficient primality test with caching.
    
    Uses trial division optimized for AoC constraints.
    """
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    
    # Check odd divisors up to sqrt(n)
    for i in range(3, int(n**0.5) + 1, 2):
        if n % i == 0:
            return False
    
    return True

def sieve_of_eratosthenes(limit: int) -> List[int]:
    """
    Generate all primes up to limit using Sieve of Eratosthenes.
    
    Efficient for finding many primes at once.
    """
    if limit < 2:
        return []
    
    sieve = [True] * (limit + 1)
    sieve[0] = sieve[1] = False
    
    for i in range(2, int(limit**0.5) + 1):
        if sieve[i]:
            for j in range(i*i, limit + 1, i):
                sieve[j] = False
    
    return [i for i, is_prime in enumerate(sieve) if is_prime]

def prime_factors(n: int) -> Dict[int, int]:
    """
    Prime factorization with exponents.
    
    Returns dictionary mapping prime factors to their exponents.
    Example: prime_factors(12) = {2: 2, 3: 1} for 12 = 2² × 3¹
    """
    factors = defaultdict(int)
    d = 2
    
    while d * d <= n:
        while n % d == 0:
            factors[d] += 1
            n //= d
        d += 1
    
    if n > 1:
        factors[n] += 1
    
    return dict(factors)

def divisors(n: int) -> List[int]:
    """
    Find all divisors of n.
    
    Returns sorted list of all positive divisors.
    """
    divs = []
    for i in range(1, int(n**0.5) + 1):
        if n % i == 0:
            divs.append(i)
            if i != n // i:
                divs.append(n // i)
    
    return sorted(divs)

def fibonacci(n: int) -> int:
    """
    Efficient Fibonacci calculation using matrix exponentiation.
    
    Handles large n values efficiently.
    """
    if n <= 1:
        return n
    
    def matrix_multiply(A, B):
        return [[A[0][0]*B[0][0] + A[0][1]*B[1][0],
                 A[0][0]*B[0][1] + A[0][1]*B[1][1]],
                [A[1][0]*B[0][0] + A[1][1]*B[1][0],
                 A[1][0]*B[0][1] + A[1][1]*B[1][1]]]
    
    def matrix_power(matrix, power):
        if power == 1:
            return matrix
        if power % 2 == 0:
            half = matrix_power(matrix, power // 2)
            return matrix_multiply(half, half)
        else:
            return matrix_multiply(matrix, matrix_power(matrix, power - 1))
    
    base_matrix = [[1, 1], [1, 0]]
    result_matrix = matrix_power(base_matrix, n)
    return result_matrix[0][1]

def factorial(n: int) -> int:
    """Factorial with caching for repeated calculations."""
    return math.factorial(n)

@lru_cache(maxsize=1000)
def binomial_coefficient(n: int, k: int) -> int:
    """
    Binomial coefficient C(n, k) = n! / (k! * (n-k)!)
    
    Optimized to avoid large factorial calculations.
    """
    if k > n or k < 0:
        return 0
    if k == 0 or k == n:
        return 1
    
    # Use symmetry: C(n, k) = C(n, n-k)
    k = min(k, n - k)
    
    result = 1
    for i in range(k):
        result = result * (n - i) // (i + 1)
    
    return result

def permutations_count(n: int, r: int) -> int:
    """Number of permutations P(n, r) = n! / (n-r)!"""
    if r > n or r < 0:
        return 0
    
    result = 1
    for i in range(n, n - r, -1):
        result *= i
    
    return result

def manhattan_distance(point1: Tuple[Number, ...], point2: Tuple[Number, ...]) -> Number:
    """
    Manhattan distance between n-dimensional points.
    
    Common in AoC grid problems.
    """
    return sum(abs(a - b) for a, b in zip(point1, point2))

def euclidean_distance(point1: Tuple[Number, ...], point2: Tuple[Number, ...]) -> float:
    """Euclidean distance between n-dimensional points."""
    return sum((a - b) ** 2 for a, b in zip(point1, point2)) ** 0.5

def chebyshev_distance(point1: Tuple[Number, ...], point2: Tuple[Number, ...]) -> Number:
    """Chebyshev distance (maximum coordinate difference)."""
    return max(abs(a - b) for a, b in zip(point1, point2))

def sign(x: Number) -> int:
    """Sign function: returns -1, 0, or 1."""
    if x > 0:
        return 1
    elif x < 0:
        return -1
    else:
        return 0

def clamp(value: Number, min_val: Number, max_val: Number) -> Number:
    """Clamp value between min and max."""
    return max(min_val, min(value, max_val))

def mod_pow(base: int, exponent: int, modulus: int) -> int:
    """
    Modular exponentiation: (base^exponent) % modulus
    
    Efficient for large exponents.
    """
    return pow(base, exponent, modulus)

def digit_sum(n: int) -> int:
    """Sum of digits in a number."""
    return sum(int(digit) for digit in str(abs(n)))

def digit_product(n: int) -> int:
    """Product of digits in a number."""
    result = 1
    for digit in str(abs(n)):
        result *= int(digit)
    return result

def reverse_number(n: int) -> int:
    """Reverse the digits of a number."""
    sign = -1 if n < 0 else 1
    return sign * int(str(abs(n))[::-1])

def is_palindrome(n: int) -> bool:
    """Check if a number is a palindrome."""
    s = str(abs(n))
    return s == s[::-1]

def next_permutation(arr: List[int]) -> bool:
    """
    Generate next lexicographic permutation in-place.
    
    Returns True if next permutation exists, False if this was the last one.
    """
    # Find the largest index i such that arr[i] < arr[i + 1]
    i = len(arr) - 2
    while i >= 0 and arr[i] >= arr[i + 1]:
        i -= 1
    
    if i == -1:
        return False  # This was the last permutation
    
    # Find the largest index j such that arr[i] < arr[j]
    j = len(arr) - 1
    while arr[j] <= arr[i]:
        j -= 1
    
    # Swap arr[i] and arr[j]
    arr[i], arr[j] = arr[j], arr[i]
    
    # Reverse the suffix starting at arr[i + 1]
    arr[i + 1:] = arr[i + 1:][::-1]
    
    return True

def quadratic_formula(a: float, b: float, c: float) -> Tuple[Optional[float], Optional[float]]:
    """
    Solve quadratic equation ax² + bx + c = 0.
    
    Returns tuple of solutions (may contain None for complex solutions).
    """
    discriminant = b * b - 4 * a * c
    
    if discriminant < 0:
        return None, None  # Complex solutions
    elif discriminant == 0:
        solution = -b / (2 * a)
        return solution, solution
    else:
        sqrt_discriminant = discriminant ** 0.5
        solution1 = (-b + sqrt_discriminant) / (2 * a)
        solution2 = (-b - sqrt_discriminant) / (2 * a)
        return solution1, solution2

def triangle_number(n: int) -> int:
    """nth triangular number: 1 + 2 + ... + n = n(n+1)/2"""
    return n * (n + 1) // 2

def is_triangle_number(x: int) -> bool:
    """Check if x is a triangular number."""
    if x < 0:
        return False
    
    # Solve n(n+1)/2 = x for n
    # This gives n = (-1 + sqrt(1 + 8x)) / 2
    discriminant = 1 + 8 * x
    sqrt_discriminant = int(discriminant ** 0.5)
    
    return sqrt_discriminant * sqrt_discriminant == discriminant and (sqrt_discriminant - 1) % 2 == 0

def pentagonal_number(n: int) -> int:
    """nth pentagonal number: n(3n-1)/2"""
    return n * (3 * n - 1) // 2

def hexagonal_number(n: int) -> int:
    """nth hexagonal number: n(2n-1)"""
    return n * (2 * n - 1)

def collatz_sequence_length(n: int) -> int:
    """
    Length of Collatz sequence starting from n.
    
    With memoization for efficiency.
    """
    @lru_cache(maxsize=10000)
    def collatz_length_cached(x):
        if x == 1:
            return 1
        elif x % 2 == 0:
            return 1 + collatz_length_cached(x // 2)
        else:
            return 1 + collatz_length_cached(3 * x + 1)
    
    return collatz_length_cached(n)

def find_cycle(sequence: List[int]) -> Tuple[int, int]:
    """
    Find cycle in sequence using Floyd's cycle detection.
    
    Returns (start_index, cycle_length) or (-1, -1) if no cycle.
    """
    if len(sequence) < 2:
        return -1, -1
    
    # Floyd's cycle detection algorithm
    slow = fast = 0
    
    # Phase 1: Find if cycle exists
    while True:
        slow = slow + 1
        fast = fast + 2
        
        if fast >= len(sequence) or slow >= len(sequence):
            return -1, -1  # No cycle
        
        if sequence[slow] == sequence[fast]:
            break
    
    # Phase 2: Find start of cycle
    start = 0
    while sequence[start] != sequence[slow]:
        start += 1
        slow += 1
        
        if start >= len(sequence) or slow >= len(sequence):
            return -1, -1
    
    # Phase 3: Find cycle length
    cycle_length = 1
    current = slow + 1
    while current < len(sequence) and sequence[current] != sequence[slow]:
        cycle_length += 1
        current += 1
    
    if current >= len(sequence):
        return -1, -1
    
    return start, cycle_length

def base_conversion(number: int, from_base: int, to_base: int) -> str:
    """
    Convert number from one base to another.
    
    Args:
        number: Number as integer (assumed to be in from_base)
        from_base: Source base (2-36)
        to_base: Target base (2-36)
        
    Returns:
        String representation in target base
    """
    # First convert to decimal if needed
    if from_base != 10:
        decimal = int(str(number), from_base)
    else:
        decimal = number
    
    # Then convert from decimal to target base
    if to_base == 10:
        return str(decimal)
    
    if decimal == 0:
        return "0"
    
    digits = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    result = ""
    
    while decimal > 0:
        result = digits[decimal % to_base] + result
        decimal //= to_base
    
    return result

# Geometry utilities
def point_in_polygon(point: Tuple[float, float], polygon: List[Tuple[float, float]]) -> bool:
    """
    Check if point is inside polygon using ray casting algorithm.
    
    Args:
        point: (x, y) coordinates of test point
        polygon: List of (x, y) coordinates defining polygon vertices
        
    Returns:
        True if point is inside polygon
    """
    x, y = point
    n = len(polygon)
    inside = False
    
    p1x, p1y = polygon[0]
    for i in range(1, n + 1):
        p2x, p2y = polygon[i % n]
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or x <= xinters:
                        inside = not inside
        p1x, p1y = p2x, p2y
    
    return inside

def polygon_area(polygon: List[Tuple[float, float]]) -> float:
    """
    Calculate area of polygon using shoelace formula.
    
    Args:
        polygon: List of (x, y) coordinates defining polygon vertices
        
    Returns:
        Area of polygon (positive for counter-clockwise, negative for clockwise)
    """
    n = len(polygon)
    area = 0.0
    
    for i in range(n):
        j = (i + 1) % n
        area += polygon[i][0] * polygon[j][1]
        area -= polygon[j][0] * polygon[i][1]
    
    return abs(area) / 2.0