#!/usr/bin/env python3
"""
Advent of Code 2020 Day 21: Allergen Assessment
https://adventofcode.com/2020/day/21

Food allergen identification using constraint satisfaction and logical deduction.
Enhanced solution using AdventSolution base class.
"""

import sys
from pathlib import Path
from typing import Any, Dict, List, Set, Tuple
from collections import defaultdict

# Add utils to path
sys.path.append(str(Path(__file__).parent.parent))
from utils import AdventSolution, InputParser


class AllergenAnalyzer:
    """Analyzes food ingredients and allergens using constraint satisfaction."""
    
    def __init__(self):
        self.ingredient_possible_allergens = defaultdict(set)
        self.allergen_possible_ingredients = defaultdict(set)
        self.foods = []  # List of (ingredients, allergens) tuples
        self.all_ingredients = set()
        self.all_allergens = set()
    
    def add_food(self, ingredients: List[str], allergens: List[str]):
        """Add a food item with its ingredients and allergens."""
        ingredient_set = set(ingredients)
        allergen_set = set(allergens)
        
        self.foods.append((ingredient_set, allergen_set))
        self.all_ingredients.update(ingredient_set)
        self.all_allergens.update(allergen_set)
        
        # Initially, every ingredient could contain any allergen
        for ingredient in ingredients:
            self.ingredient_possible_allergens[ingredient].update(allergen_set)
        
        for allergen in allergens:
            self.allergen_possible_ingredients[allergen].update(ingredient_set)
    
    def apply_constraints(self):
        """Apply constraint satisfaction to narrow down allergen possibilities."""
        # For each allergen, it can only be in ingredients that appear in ALL foods containing that allergen
        for allergen in self.all_allergens:
            foods_with_allergen = [ingredients for ingredients, allergens in self.foods if allergen in allergens]
            
            if foods_with_allergen:
                # Intersection of all ingredient sets that contain this allergen
                possible_ingredients = foods_with_allergen[0]
                for ingredient_set in foods_with_allergen[1:]:
                    possible_ingredients = possible_ingredients.intersection(ingredient_set)
                
                self.allergen_possible_ingredients[allergen] = possible_ingredients
        
        # Update ingredient constraints based on allergen constraints
        for ingredient in self.all_ingredients:
            possible_allergens = set()
            for allergen in self.all_allergens:
                if ingredient in self.allergen_possible_ingredients[allergen]:
                    possible_allergens.add(allergen)
            self.ingredient_possible_allergens[ingredient] = possible_allergens
    
    def deduce_allergens(self) -> Dict[str, str]:
        """Use logical deduction to determine which ingredient contains which allergen."""
        allergen_mapping = {}
        ingredient_mapping = {}
        
        # Keep iterating until we can't deduce any more
        changed = True
        while changed:
            changed = False
            
            # Find allergens that can only be in one ingredient
            for allergen in self.all_allergens:
                if allergen not in allergen_mapping:
                    possible_ingredients = self.allergen_possible_ingredients[allergen]
                    # Remove already mapped ingredients
                    possible_ingredients = possible_ingredients - set(ingredient_mapping.keys())
                    
                    if len(possible_ingredients) == 1:
                        ingredient = list(possible_ingredients)[0]
                        allergen_mapping[allergen] = ingredient
                        ingredient_mapping[ingredient] = allergen
                        changed = True
            
            # Find ingredients that can only contain one allergen
            for ingredient in self.all_ingredients:
                if ingredient not in ingredient_mapping:
                    possible_allergens = self.ingredient_possible_allergens[ingredient]
                    # Remove already mapped allergens
                    possible_allergens = possible_allergens - set(allergen_mapping.keys())
                    
                    if len(possible_allergens) == 1:
                        allergen = list(possible_allergens)[0]
                        allergen_mapping[allergen] = ingredient
                        ingredient_mapping[ingredient] = allergen
                        changed = True
        
        return allergen_mapping
    
    def get_safe_ingredients(self) -> Set[str]:
        """Get ingredients that don't contain any allergens."""
        allergen_mapping = self.deduce_allergens()
        dangerous_ingredients = set(allergen_mapping.values())
        return self.all_ingredients - dangerous_ingredients
    
    def count_safe_ingredient_appearances(self) -> int:
        """Count how many times safe ingredients appear across all foods."""
        safe_ingredients = self.get_safe_ingredients()
        count = 0
        
        for ingredients, _ in self.foods:
            for ingredient in ingredients:
                if ingredient in safe_ingredients:
                    count += 1
        
        return count
    
    def get_canonical_dangerous_list(self) -> str:
        """Get the canonical dangerous ingredient list sorted by allergen name."""
        allergen_mapping = self.deduce_allergens()
        sorted_allergens = sorted(allergen_mapping.keys())
        dangerous_ingredients = [allergen_mapping[allergen] for allergen in sorted_allergens]
        return ','.join(dangerous_ingredients)


class Day21Solution(AdventSolution):
    """Solution for 2020 Day 21: Allergen Assessment."""

    def __init__(self):
        super().__init__(2020, 21, "Allergen Assessment")

    def parse_foods(self, input_data: str) -> AllergenAnalyzer:
        """
        Parse food data from input.
        
        Args:
            input_data: Raw input data containing food descriptions
            
        Returns:
            AllergenAnalyzer with parsed food data
        """
        analyzer = AllergenAnalyzer()
        
        for line in input_data.strip().split('\n'):
            line = line.strip()
            if not line:
                continue
            
            # Parse "sqjhc fvjkl (contains soy, fish)"
            if '(contains ' in line:
                ingredients_part, allergens_part = line.split(' (contains ')
                ingredients = ingredients_part.split()
                allergens = allergens_part.rstrip(')').split(', ')
                allergens = [allergen.strip() for allergen in allergens]
                
                analyzer.add_food(ingredients, allergens)
        
        # Apply constraint satisfaction
        analyzer.apply_constraints()
        
        return analyzer

    def part1(self, input_data: str) -> int:
        """
        Solve part 1: Count appearances of ingredients that don't contain allergens.
        
        Args:
            input_data: The input data as a string
            
        Returns:
            Number of times safe ingredients appear
        """
        analyzer = self.parse_foods(input_data)
        return analyzer.count_safe_ingredient_appearances()

    def part2(self, input_data: str) -> str:
        """
        Solve part 2: Get canonical dangerous ingredient list.
        
        Args:
            input_data: The input data as a string
            
        Returns:
            Comma-separated list of dangerous ingredients sorted by allergen
        """
        analyzer = self.parse_foods(input_data)
        return analyzer.get_canonical_dangerous_list()

    def analyze_allergens(self, input_data: str) -> str:
        """
        Analyze allergen constraints and deduction process.
        
        Args:
            input_data: Raw input data
            
        Returns:
            Analysis summary as formatted string
        """
        analyzer = self.parse_foods(input_data)
        
        analysis = []
        analysis.append("=== Allergen Analysis ===")
        analysis.append(f"Total foods: {len(analyzer.foods)}")
        analysis.append(f"Total ingredients: {len(analyzer.all_ingredients)}")
        analysis.append(f"Total allergens: {len(analyzer.all_allergens)}")
        
        # Show constraint satisfaction results
        analysis.append("\nAllergen constraints (ingredients that could contain each allergen):")
        for allergen in sorted(analyzer.all_allergens):
            possible = analyzer.allergen_possible_ingredients[allergen]
            analysis.append(f"  {allergen}: {sorted(possible)}")
        
        # Show deduction results
        allergen_mapping = analyzer.deduce_allergens()
        analysis.append(f"\nDeduced allergen mappings ({len(allergen_mapping)} solved):")
        for allergen in sorted(allergen_mapping.keys()):
            ingredient = allergen_mapping[allergen]
            analysis.append(f"  {allergen} -> {ingredient}")
        
        # Show safe ingredients
        safe_ingredients = analyzer.get_safe_ingredients()
        analysis.append(f"\nSafe ingredients ({len(safe_ingredients)}):")
        analysis.append(f"  {sorted(safe_ingredients)}")
        
        # Show unsolved constraints
        unsolved_allergens = analyzer.all_allergens - set(allergen_mapping.keys())
        if unsolved_allergens:
            analysis.append(f"\nUnsolved allergens: {sorted(unsolved_allergens)}")
        
        return "\n".join(analysis)

    def validate(self, expected_part1=None, expected_part2=None) -> bool:
        """Validate solution with test cases."""
        # Test with example from problem description
        test_input = """mxmxvkd kfcds sqjhc nhms (contains dairy, fish)
trh fvjkl sbzzf mxmxvkd (contains dairy)
sqjhc fvjkl (contains soy)
sqjhc mxmxvkd sbzzf (contains fish)"""
        
        analyzer = self.parse_foods(test_input)
        
        # Test constraint satisfaction
        # dairy should only be possible in mxmxvkd (appears in both dairy foods)
        if 'mxmxvkd' not in analyzer.allergen_possible_ingredients['dairy']:
            print("Constraint test failed: mxmxvkd should be possible for dairy")
            return False
        
        # Test deduction
        allergen_mapping = analyzer.deduce_allergens()
        expected_mapping = {'dairy': 'mxmxvkd', 'fish': 'sqjhc', 'soy': 'fvjkl'}
        
        for allergen, expected_ingredient in expected_mapping.items():
            if allergen_mapping.get(allergen) != expected_ingredient:
                print(f"Deduction test failed: {allergen} should map to {expected_ingredient}, got {allergen_mapping.get(allergen)}")
                return False
        
        # Test part 1: should be 5 (kfcds appears 1 time, nhms appears 1 time, sbzzf appears 2 times, trh appears 1 time)
        part1_result = analyzer.count_safe_ingredient_appearances()
        if part1_result != 5:
            print(f"Part 1 test failed: expected 5, got {part1_result}")
            return False
        
        # Test part 2: should be "mxmxvkd,sqjhc,fvjkl" (sorted by allergen: dairy,fish,soy)
        part2_result = analyzer.get_canonical_dangerous_list()
        if part2_result != "mxmxvkd,sqjhc,fvjkl":
            print(f"Part 2 test failed: expected 'mxmxvkd,sqjhc,fvjkl', got '{part2_result}'")
            return False
        
        print("✅ All Day 21 validation tests passed!")
        return True


# Legacy compatibility functions for test runner
def part1(input_data: str = None) -> int:
    """Part 1 function compatible with test runner."""
    solution = Day21Solution()
    if input_data is None:
        # Use actual input file
        input_data = solution._load_input()
    return solution.part1(input_data)


def part2(input_data: str = None) -> str:
    """Part 2 function compatible with test runner."""
    solution = Day21Solution()
    if input_data is None:
        # Use actual input file
        input_data = solution._load_input()
    return solution.part2(input_data)


def main():
    """Main function to run the solution."""
    solution = Day21Solution()
    solution.main()


if __name__ == "__main__":
    main()