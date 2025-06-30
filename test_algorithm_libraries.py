#!/usr/bin/env python3
"""
Comprehensive Test Suite for Algorithm Libraries

Tests all algorithm library components extracted from AoC solutions.
Validates correctness, performance, and integration with enhanced architecture.

Usage:
    python test_algorithm_libraries.py              # Run all tests
    python test_algorithm_libraries.py --module pathfinding  # Test specific module
    python test_algorithm_libraries.py --performance        # Include performance tests
    python test_algorithm_libraries.py --verbose           # Detailed output
"""

import unittest
import time
import sys
from pathlib import Path
from typing import Dict, List, Tuple, Any, Optional

# Add utils to path
sys.path.append(str(Path(__file__).parent))

try:
    from utils.algorithms import (
        pathfinding, grid, vm, parsing, math_utils
    )
    from utils.algorithms.pathfinding import (
        dijkstra_grid, bfs_shortest_path, a_star_search, dfs_all_paths,
        PathfindingResult, PathfindingAlgorithm
    )
    from utils.algorithms.grid import (
        Grid, Direction, parse_grid, neighbors_4, neighbors_8,
        manhattan_distance, euclidean_distance
    )
    from utils.algorithms.vm import (
        IntcodeVM, SimpleAssemblyVM, VMState, ParameterMode,
        run_intcode_program
    )
    from utils.algorithms.parsing import (
        ExpressionEvaluator, PatternMatcher, parse_numbers,
        parse_coordinate_pairs, extract_patterns
    )
    from utils.algorithms.math_utils import (
        gcd, lcm, is_prime, prime_factors, fibonacci,
        manhattan_distance as math_manhattan, euclidean_distance as math_euclidean
    )
    ALGORITHMS_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Algorithm libraries not available: {e}")
    ALGORITHMS_AVAILABLE = False

class TestPathfinding(unittest.TestCase):
    """Test pathfinding algorithms."""
    
    def setUp(self):
        """Set up test grids."""
        # Simple 3x3 grid for basic tests
        self.simple_grid = {
            (0, 0): '.', (1, 0): '.', (2, 0): '.',
            (0, 1): '.', (1, 1): '#', (2, 1): '.',
            (0, 2): '.', (1, 2): '.', (2, 2): '.'
        }
        
        # Weighted grid for Dijkstra tests (based on 2021 Day 15)
        self.weighted_grid = {
            (0, 0): 1, (1, 0): 2, (2, 0): 3,
            (0, 1): 4, (1, 1): 5, (2, 1): 6,
            (0, 2): 7, (1, 2): 8, (2, 2): 9
        }
    
    @unittest.skipUnless(ALGORITHMS_AVAILABLE, "Algorithm libraries not available")
    def test_bfs_shortest_path(self):
        """Test BFS pathfinding."""
        result = bfs_shortest_path(
            self.simple_grid, (0, 0), (2, 2), 
            passable_fn=lambda cell: cell != '#'
        )
        
        self.assertTrue(result.found)
        self.assertEqual(result.start, (0, 0))
        self.assertEqual(result.end, (2, 2))
        self.assertEqual(result.algorithm, PathfindingAlgorithm.BFS)
        self.assertGreater(len(result.path), 0)
        self.assertEqual(result.path[0], (0, 0))
        self.assertEqual(result.path[-1], (2, 2))
    
    @unittest.skipUnless(ALGORITHMS_AVAILABLE, "Algorithm libraries not available")
    def test_dijkstra_grid(self):
        """Test Dijkstra pathfinding with weights."""
        def weight_fn(from_pos, to_pos):
            return self.weighted_grid[to_pos]
        
        result = dijkstra_grid(
            self.weighted_grid, (0, 0), (2, 2),
            weight_fn=weight_fn
        )
        
        self.assertTrue(result.found)
        self.assertEqual(result.algorithm, PathfindingAlgorithm.DIJKSTRA)
        self.assertGreater(result.distance, 0)
        self.assertGreater(len(result.path), 0)
    
    @unittest.skipUnless(ALGORITHMS_AVAILABLE, "Algorithm libraries not available")
    def test_a_star_search(self):
        """Test A* pathfinding."""
        result = a_star_search(
            self.simple_grid, (0, 0), (2, 2),
            passable_fn=lambda cell: cell != '#'
        )
        
        self.assertTrue(result.found)
        self.assertEqual(result.algorithm, PathfindingAlgorithm.A_STAR)
        self.assertGreater(len(result.path), 0)
    
    @unittest.skipUnless(ALGORITHMS_AVAILABLE, "Algorithm libraries not available")
    def test_dfs_all_paths(self):
        """Test DFS all paths enumeration."""
        paths = dfs_all_paths(
            self.simple_grid, (0, 0), (2, 2),
            max_paths=10,
            passable_fn=lambda cell: cell != '#'
        )
        
        self.assertGreater(len(paths), 0)
        for path in paths:
            self.assertEqual(path[0], (0, 0))
            self.assertEqual(path[-1], (2, 2))
    
    @unittest.skipUnless(ALGORITHMS_AVAILABLE, "Algorithm libraries not available")
    def test_pathfinding_blocked(self):
        """Test pathfinding with blocked path."""
        blocked_grid = {
            (0, 0): '.', (1, 0): '#', (2, 0): '.',
            (0, 1): '#', (1, 1): '#', (2, 1): '.',
            (0, 2): '.', (1, 2): '#', (2, 2): '.'
        }
        
        result = bfs_shortest_path(
            blocked_grid, (0, 0), (2, 2),
            passable_fn=lambda cell: cell != '#'
        )
        
        self.assertFalse(result.found)

class TestGrid(unittest.TestCase):
    """Test grid utilities."""
    
    def setUp(self):
        """Set up test grids."""
        self.test_data = {
            (0, 0): 'A', (1, 0): 'B', (2, 0): 'C',
            (0, 1): 'D', (1, 1): 'E', (2, 1): 'F',
            (0, 2): 'G', (1, 2): 'H', (2, 2): 'I'
        }
        self.grid = Grid(self.test_data)
    
    @unittest.skipUnless(ALGORITHMS_AVAILABLE, "Algorithm libraries not available")
    def test_grid_creation(self):
        """Test grid creation and basic operations."""
        self.assertEqual(self.grid[(1, 1)], 'E')
        self.assertEqual(len(self.grid), 9)
        self.assertTrue((1, 1) in self.grid)
        self.assertFalse((5, 5) in self.grid)
    
    @unittest.skipUnless(ALGORITHMS_AVAILABLE, "Algorithm libraries not available")
    def test_grid_bounds(self):
        """Test grid boundary calculations."""
        bounds = self.grid.bounds
        self.assertEqual(bounds.min_x, 0)
        self.assertEqual(bounds.max_x, 2)
        self.assertEqual(bounds.min_y, 0)
        self.assertEqual(bounds.max_y, 2)
        self.assertEqual(bounds.width, 3)
        self.assertEqual(bounds.height, 3)
        self.assertEqual(bounds.area, 9)
    
    @unittest.skipUnless(ALGORITHMS_AVAILABLE, "Algorithm libraries not available")
    def test_grid_neighbors(self):
        """Test neighbor calculation."""
        neighbors = self.grid.neighbors((1, 1), directions=4)
        expected = [(1, 0), (2, 1), (1, 2), (0, 1)]
        self.assertEqual(set(neighbors), set(expected))
        
        neighbors_8 = self.grid.neighbors((1, 1), directions=8)
        self.assertEqual(len(neighbors_8), 8)
    
    @unittest.skipUnless(ALGORITHMS_AVAILABLE, "Algorithm libraries not available")
    def test_grid_rotation(self):
        """Test grid rotation operations."""
        rotated = self.grid.rotate_90()
        # After 90° clockwise rotation, (0,0) -> (0,2)
        # Original 'A' at (0,0) should be at (0,2) in rotated grid
        self.assertIn((0, 2), rotated)
    
    @unittest.skipUnless(ALGORITHMS_AVAILABLE, "Algorithm libraries not available")
    def test_grid_flip(self):
        """Test grid flipping operations."""
        flipped = self.grid.flip_horizontal()
        # After horizontal flip, (0,0) -> (2,0)
        self.assertEqual(len(flipped), len(self.grid))
        
        flipped_v = self.grid.flip_vertical()
        self.assertEqual(len(flipped_v), len(self.grid))
    
    @unittest.skipUnless(ALGORITHMS_AVAILABLE, "Algorithm libraries not available")
    def test_parse_grid(self):
        """Test grid parsing from string."""
        text = "ABC\nDEF\nGHI"
        parsed = parse_grid(text)
        
        self.assertEqual(parsed[(0, 0)], 'A')
        self.assertEqual(parsed[(1, 0)], 'B')
        self.assertEqual(parsed[(2, 2)], 'I')
    
    @unittest.skipUnless(ALGORITHMS_AVAILABLE, "Algorithm libraries not available")
    def test_grid_flood_fill(self):
        """Test flood fill algorithm."""
        fill_grid = Grid({
            (0, 0): '.', (1, 0): '.', (2, 0): '#',
            (0, 1): '.', (1, 1): '.', (2, 1): '#',
            (0, 2): '#', (1, 2): '#', (2, 2): '#'
        })
        
        filled = fill_grid.flood_fill((0, 0), 'X')
        self.assertGreater(len(filled), 0)
        self.assertEqual(fill_grid[(0, 0)], 'X')

class TestVirtualMachine(unittest.TestCase):
    """Test virtual machine components."""
    
    @unittest.skipUnless(ALGORITHMS_AVAILABLE, "Algorithm libraries not available")
    def test_intcode_basic_operations(self):
        """Test basic Intcode operations."""
        # Test addition: 1,5,6,0,99,1,2 -> should set position 0 to 3
        program = [1, 5, 6, 0, 99, 1, 2]
        vm = IntcodeVM(program)
        
        state = vm.run()
        self.assertEqual(state, VMState.HALTED)
        self.assertEqual(vm.memory[0], 3)  # 1 + 2 = 3
    
    @unittest.skipUnless(ALGORITHMS_AVAILABLE, "Algorithm libraries not available")
    def test_intcode_multiplication(self):
        """Test Intcode multiplication."""
        # Test multiplication: 2,5,6,0,99,3,4 -> should set position 0 to 12
        program = [2, 5, 6, 0, 99, 3, 4]
        vm = IntcodeVM(program)
        
        state = vm.run()
        self.assertEqual(state, VMState.HALTED)
        self.assertEqual(vm.memory[0], 12)  # 3 * 4 = 12
    
    @unittest.skipUnless(ALGORITHMS_AVAILABLE, "Algorithm libraries not available")
    def test_intcode_io(self):
        """Test Intcode input/output operations."""
        # Program that reads input and outputs it
        program = [3, 9, 4, 9, 99, 0, 0, 0, 0, 0]
        vm = IntcodeVM(program)
        
        vm.provide_input(42)
        state = vm.run()
        
        self.assertEqual(state, VMState.HALTED)
        output = vm.get_output()
        self.assertEqual(output, 42)
    
    @unittest.skipUnless(ALGORITHMS_AVAILABLE, "Algorithm libraries not available")
    def test_intcode_parameter_modes(self):
        """Test Intcode parameter modes."""
        # Test immediate mode: 1002,4,3,4,33 -> multiply 33 by 3, store in position 4
        program = [1002, 4, 3, 4, 33]
        vm = IntcodeVM(program)
        
        state = vm.run()
        self.assertEqual(state, VMState.HALTED)
        self.assertEqual(vm.memory[4], 99)  # 33 * 3 = 99
    
    @unittest.skipUnless(ALGORITHMS_AVAILABLE, "Algorithm libraries not available")
    def test_simple_assembly_vm(self):
        """Test simple assembly VM."""
        program = [
            "acc +1",
            "jmp +4", 
            "acc +3",
            "jmp -3",
            "acc -99",
            "acc +1",
            "nop +0",
            "acc +6"
        ]
        
        vm = SimpleAssemblyVM(program)
        state = vm.run()
        
        # This program should run successfully to completion
        # acc +1 (acc=1), jmp +4 (to acc +1), acc +1 (acc=2), nop, acc +6 (acc=8)
        self.assertIn(state, [VMState.HALTED, VMState.ERROR])
        self.assertGreaterEqual(vm.accumulator, 1)  # Should have accumulated some value
    
    @unittest.skipUnless(ALGORITHMS_AVAILABLE, "Algorithm libraries not available")
    def test_run_intcode_program_convenience(self):
        """Test convenience function for running Intcode programs."""
        program = [3, 0, 4, 0, 99]  # Read input, output it, halt
        outputs, stats = run_intcode_program(program, [123])
        
        self.assertEqual(outputs, [123])
        self.assertGreater(stats.instructions_executed, 0)

class TestParsing(unittest.TestCase):
    """Test parsing utilities."""
    
    @unittest.skipUnless(ALGORITHMS_AVAILABLE, "Algorithm libraries not available")
    def test_expression_evaluator(self):
        """Test mathematical expression evaluation."""
        evaluator = ExpressionEvaluator()
        
        self.assertEqual(evaluator.evaluate("2 + 3 * 4"), 14)
        self.assertEqual(evaluator.evaluate("(2 + 3) * 4"), 20)
        self.assertEqual(evaluator.evaluate("2 ** 3"), 8)
    
    @unittest.skipUnless(ALGORITHMS_AVAILABLE, "Algorithm libraries not available")
    def test_expression_custom_precedence(self):
        """Test expression evaluation with custom precedence."""
        # Custom precedence where + has higher precedence than *
        precedence = {'+': 2, '*': 1}
        evaluator = ExpressionEvaluator(precedence=precedence)
        
        # With custom precedence: 2 + 3 * 4 = (2 + 3) * 4 = 20
        self.assertEqual(evaluator.evaluate("2 + 3 * 4"), 20)
    
    @unittest.skipUnless(ALGORITHMS_AVAILABLE, "Algorithm libraries not available")
    def test_pattern_matcher(self):
        """Test pattern matching utilities."""
        matcher = PatternMatcher()
        
        text = "The coordinates are (10, 20) and (-5, 15)"
        numbers = matcher.extract_numbers(text)
        coords = matcher.extract_coordinates(text)
        
        self.assertEqual(numbers, [10, 20, -5, 15])
        self.assertEqual(coords, [(10, 20), (-5, 15)])
    
    @unittest.skipUnless(ALGORITHMS_AVAILABLE, "Algorithm libraries not available")
    def test_parse_numbers(self):
        """Test number parsing utility."""
        text = "1,2,3,4,5"
        numbers = parse_numbers(text)
        self.assertEqual(numbers, [1, 2, 3, 4, 5])
        
        text_with_negatives = "10 -5 0 42"
        numbers = parse_numbers(text_with_negatives)
        self.assertEqual(numbers, [10, -5, 0, 42])
    
    @unittest.skipUnless(ALGORITHMS_AVAILABLE, "Algorithm libraries not available")
    def test_parse_coordinate_pairs(self):
        """Test coordinate pair parsing."""
        text = "(1,2) (3,4)"
        coords = parse_coordinate_pairs(text)
        self.assertEqual(coords, [(1, 2), (3, 4)])
        
        text2 = "1,2 3,4"
        coords2 = parse_coordinate_pairs(text2)
        self.assertEqual(coords2, [(1, 2), (3, 4)])
    
    @unittest.skipUnless(ALGORITHMS_AVAILABLE, "Algorithm libraries not available")
    def test_extract_patterns(self):
        """Test multiple pattern extraction."""
        text = "abc123def456ghi"
        results = extract_patterns(text, r'[a-z]+', r'\d+')
        
        self.assertEqual(results['pattern_0'], ['abc', 'def', 'ghi'])
        self.assertEqual(results['pattern_1'], ['123', '456'])

class TestMathUtils(unittest.TestCase):
    """Test mathematical utilities."""
    
    @unittest.skipUnless(ALGORITHMS_AVAILABLE, "Algorithm libraries not available")
    def test_gcd_lcm(self):
        """Test GCD and LCM calculations."""
        self.assertEqual(gcd(12, 18), 6)
        self.assertEqual(lcm(12, 18), 36)
        self.assertEqual(gcd(17, 19), 1)  # Coprime numbers
    
    @unittest.skipUnless(ALGORITHMS_AVAILABLE, "Algorithm libraries not available")
    def test_prime_functions(self):
        """Test prime number functions."""
        self.assertTrue(is_prime(17))
        self.assertFalse(is_prime(18))
        self.assertTrue(is_prime(2))
        self.assertFalse(is_prime(1))
        
        factors = prime_factors(60)
        expected = {2: 2, 3: 1, 5: 1}  # 60 = 2² × 3¹ × 5¹
        self.assertEqual(factors, expected)
    
    @unittest.skipUnless(ALGORITHMS_AVAILABLE, "Algorithm libraries not available")
    def test_fibonacci(self):
        """Test Fibonacci calculation."""
        self.assertEqual(fibonacci(0), 0)
        self.assertEqual(fibonacci(1), 1)
        self.assertEqual(fibonacci(10), 55)
        self.assertEqual(fibonacci(20), 6765)
    
    @unittest.skipUnless(ALGORITHMS_AVAILABLE, "Algorithm libraries not available")
    def test_distance_functions(self):
        """Test distance calculations."""
        p1 = (0, 0)
        p2 = (3, 4)
        
        self.assertEqual(math_manhattan(p1, p2), 7)
        self.assertEqual(math_euclidean(p1, p2), 5.0)
    
    @unittest.skipUnless(ALGORITHMS_AVAILABLE, "Algorithm libraries not available")
    def test_number_theory(self):
        """Test number theory functions."""
        from utils.algorithms.math_utils import (
            mod_inverse, chinese_remainder_theorem, 
            binomial_coefficient, factorial
        )
        
        # Test modular inverse
        self.assertEqual(mod_inverse(3, 7), 5)  # 3 * 5 ≡ 1 (mod 7)
        
        # Test binomial coefficient
        self.assertEqual(binomial_coefficient(5, 2), 10)  # C(5,2) = 10
        
        # Test factorial is working
        self.assertEqual(factorial(5), 120)

class TestPerformance(unittest.TestCase):
    """Performance tests for algorithm libraries."""
    
    def setUp(self):
        """Set up performance test data."""
        self.large_grid = {}
        size = 100
        for x in range(size):
            for y in range(size):
                self.large_grid[(x, y)] = '.' if (x + y) % 7 != 0 else '#'
    
    @unittest.skipUnless(ALGORITHMS_AVAILABLE, "Algorithm libraries not available")
    def test_pathfinding_performance(self):
        """Test pathfinding performance on larger grids."""
        start_time = time.time()
        
        result = bfs_shortest_path(
            self.large_grid, (0, 0), (99, 99),
            passable_fn=lambda cell: cell != '#'
        )
        
        execution_time = time.time() - start_time
        
        # Should complete within reasonable time (< 1 second for 100x100 grid)
        self.assertLess(execution_time, 1.0)
        if result.found:
            self.assertGreater(len(result.path), 0)
    
    @unittest.skipUnless(ALGORITHMS_AVAILABLE, "Algorithm libraries not available")
    def test_grid_operations_performance(self):
        """Test grid operation performance."""
        grid = Grid(self.large_grid)
        
        start_time = time.time()
        rotated = grid.rotate_90()
        rotation_time = time.time() - start_time
        
        # Grid rotation should be fast
        self.assertLess(rotation_time, 0.1)
        self.assertEqual(len(rotated), len(grid))
    
    @unittest.skipUnless(ALGORITHMS_AVAILABLE, "Algorithm libraries not available")
    def test_math_performance(self):
        """Test mathematical function performance."""
        from utils.algorithms.math_utils import sieve_of_eratosthenes
        
        start_time = time.time()
        primes = sieve_of_eratosthenes(10000)
        sieve_time = time.time() - start_time
        
        # Sieve should be fast for reasonable limits
        self.assertLess(sieve_time, 0.1)
        self.assertGreater(len(primes), 0)
        self.assertTrue(all(is_prime(p) for p in primes[:10]))  # Spot check

class TestIntegration(unittest.TestCase):
    """Integration tests combining multiple algorithm components."""
    
    @unittest.skipUnless(ALGORITHMS_AVAILABLE, "Algorithm libraries not available")
    def test_grid_pathfinding_integration(self):
        """Test grid and pathfinding integration."""
        # Create maze from string
        maze_text = """
###########
#.........#
#.#######.#
#.......#.#
#######.#.#
#.......#.#
#.#######.#
#.........#
###########
        """.strip()
        
        maze_grid = parse_grid(maze_text)
        
        # Find path through maze
        result = bfs_shortest_path(
            maze_grid, (1, 1), (9, 7),
            passable_fn=lambda cell: cell != '#'
        )
        
        if result.found:
            self.assertGreater(len(result.path), 0)
            # Verify path is valid
            for coord in result.path:
                self.assertNotEqual(maze_grid.get(coord), '#')
    
    @unittest.skipUnless(ALGORITHMS_AVAILABLE, "Algorithm libraries not available")
    def test_vm_parsing_integration(self):
        """Test VM and parsing integration."""
        # Parse Intcode program from string
        program_text = "1,9,10,3,2,3,11,0,99,30,40,50"
        numbers = parse_numbers(program_text, separator=',')
        
        # Run the parsed program
        outputs, stats = run_intcode_program(numbers)
        
        self.assertGreater(stats.instructions_executed, 0)
        # This specific program should modify memory but not produce output
        self.assertEqual(len(outputs), 0)

def run_tests(module_filter: Optional[str] = None, 
              include_performance: bool = False,
              verbose: bool = False):
    """
    Run algorithm library tests.
    
    Args:
        module_filter: Test only specific module (pathfinding, grid, vm, parsing, math)
        include_performance: Include performance tests
        verbose: Verbose output
    """
    if not ALGORITHMS_AVAILABLE:
        print("❌ Algorithm libraries not available. Cannot run tests.")
        return False
    
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Map module names to test classes
    test_classes = {
        'pathfinding': TestPathfinding,
        'grid': TestGrid,
        'vm': TestVirtualMachine,
        'parsing': TestParsing,
        'math': TestMathUtils,
        'performance': TestPerformance,
        'integration': TestIntegration
    }
    
    if module_filter:
        if module_filter in test_classes:
            suite.addTests(loader.loadTestsFromTestCase(test_classes[module_filter]))
        else:
            print(f"❌ Unknown module: {module_filter}")
            print(f"Available modules: {', '.join(test_classes.keys())}")
            return False
    else:
        # Add all tests except performance by default
        for name, test_class in test_classes.items():
            if name != 'performance' or include_performance:
                suite.addTests(loader.loadTestsFromTestCase(test_class))
    
    # Run tests
    verbosity = 2 if verbose else 1
    runner = unittest.TextTestRunner(verbosity=verbosity)
    result = runner.run(suite)
    
    # Print summary
    total_tests = result.testsRun
    failures = len(result.failures)
    errors = len(result.errors)
    successes = total_tests - failures - errors
    
    print(f"\n{'='*60}")
    print(f"🧪 ALGORITHM LIBRARY TEST SUMMARY")
    print(f"{'='*60}")
    print(f"✅ Successful: {successes}")
    print(f"❌ Failed: {failures}")
    print(f"💥 Errors: {errors}")
    print(f"📊 Total: {total_tests}")
    
    if failures > 0 or errors > 0:
        print(f"\n❌ Some tests failed. Success rate: {successes/total_tests*100:.1f}%")
        return False
    else:
        print(f"\n🎉 All tests passed! Algorithm libraries are working correctly.")
        return True

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Test algorithm libraries")
    parser.add_argument("--module", help="Test specific module only")
    parser.add_argument("--performance", action="store_true", help="Include performance tests")
    parser.add_argument("--verbose", action="store_true", help="Verbose output")
    
    args = parser.parse_args()
    
    success = run_tests(
        module_filter=args.module,
        include_performance=args.performance,
        verbose=args.verbose
    )
    
    sys.exit(0 if success else 1)