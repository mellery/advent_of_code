#!/usr/bin/env python3
"""
Advent of Code 2019 Day 14: Space Stoichiometry
Enhanced solution with object-oriented design and comprehensive analysis.
"""

import sys
import os
import re
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from collections import defaultdict
from math import ceil

# Add project root to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.advent_base import AdventSolution


@dataclass
class Chemical:
    """Represents a chemical with a name and quantity."""
    name: str
    quantity: int
    
    def __str__(self) -> str:
        return f"{self.quantity} {self.name}"
    
    def __hash__(self) -> int:
        return hash(self.name)
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, Chemical):
            return False
        return self.name == other.name


@dataclass
class Reaction:
    """
    Represents a chemical reaction with inputs and a single output.
    
    Each reaction converts a specific set of input chemicals into
    a fixed quantity of a single output chemical.
    """
    inputs: List[Chemical]
    output: Chemical
    
    def __str__(self) -> str:
        inputs_str = ", ".join(str(chem) for chem in self.inputs)
        return f"{inputs_str} => {self.output}"
    
    def get_input_by_name(self, name: str) -> Optional[Chemical]:
        """Get an input chemical by name."""
        for chemical in self.inputs:
            if chemical.name == name:
                return chemical
        return None
    
    def requires_chemical(self, name: str) -> bool:
        """Check if this reaction requires a specific chemical as input."""
        return any(chem.name == name for chem in self.inputs)


class NanoFactory:
    """
    Advanced chemical processing facility for converting ORE into FUEL.
    
    The NanoFactory manages chemical reactions, inventory tracking,
    and optimization algorithms for efficient resource utilization.
    """
    
    def __init__(self, reactions: List[Reaction]):
        """
        Initialize the NanoFactory with available reactions.
        
        Args:
            reactions: List of chemical reactions available
        """
        self.reactions = reactions
        self.reaction_map: Dict[str, Reaction] = {}
        self.inventory: Dict[str, int] = defaultdict(int)
        self.production_history: List[Tuple[str, int]] = []
        
        # Build reaction lookup map
        for reaction in reactions:
            self.reaction_map[reaction.output.name] = reaction
        
        # Verify we can produce FUEL
        if 'FUEL' not in self.reaction_map:
            raise ValueError("No reaction found to produce FUEL")
    
    def reset_inventory(self) -> None:
        """Reset the factory inventory to empty state."""
        self.inventory.clear()
        self.production_history.clear()
    
    def calculate_ore_needed(self, fuel_quantity: int = 1) -> int:
        """
        Calculate the minimum ORE needed to produce the specified FUEL quantity.
        
        Args:
            fuel_quantity: Amount of FUEL to produce
            
        Returns:
            Minimum ORE required
        """
        self.reset_inventory()
        
        # Start with the requirement for FUEL
        requirements = defaultdict(int)
        requirements['FUEL'] = fuel_quantity
        
        while requirements:
            # Find a chemical we need that isn't ORE
            chemical_name = None
            for name in requirements:
                if name != 'ORE' and requirements[name] > 0:
                    chemical_name = name
                    break
            
            if chemical_name is None:
                break
            
            needed = requirements[chemical_name]
            requirements[chemical_name] = 0
            
            # Check if we have enough in inventory
            available = self.inventory[chemical_name]
            if available >= needed:
                self.inventory[chemical_name] -= needed
                continue
            
            # Need to produce more
            still_needed = needed - available
            self.inventory[chemical_name] = 0
            
            # Find the reaction to produce this chemical
            if chemical_name not in self.reaction_map:
                raise ValueError(f"No reaction found to produce {chemical_name}")
            
            reaction = self.reaction_map[chemical_name]
            
            # Calculate how many times we need to run this reaction
            reactions_needed = ceil(still_needed / reaction.output.quantity)
            
            # Track production
            total_produced = reactions_needed * reaction.output.quantity
            self.production_history.append((chemical_name, total_produced))
            
            # Add excess to inventory
            excess = total_produced - still_needed
            if excess > 0:
                self.inventory[chemical_name] += excess
            
            # Add input requirements
            for input_chem in reaction.inputs:
                requirements[input_chem.name] += input_chem.quantity * reactions_needed
        
        return requirements.get('ORE', 0)
    
    def find_max_fuel_from_ore(self, available_ore: int) -> int:
        """
        Find the maximum FUEL that can be produced from available ORE.
        
        Uses binary search to efficiently find the optimal amount.
        
        Args:
            available_ore: Total ORE available
            
        Returns:
            Maximum FUEL that can be produced
        """
        # Start with bounds based on naive calculation
        ore_per_fuel = self.calculate_ore_needed(1)
        lower_bound = available_ore // ore_per_fuel
        upper_bound = lower_bound * 2
        
        # Expand upper bound until we find an amount that requires too much ore
        while self.calculate_ore_needed(upper_bound) <= available_ore:
            lower_bound = upper_bound
            upper_bound *= 2
        
        # Binary search for the exact maximum
        while lower_bound < upper_bound - 1:
            mid = (lower_bound + upper_bound) // 2
            ore_needed = self.calculate_ore_needed(mid)
            
            if ore_needed <= available_ore:
                lower_bound = mid
            else:
                upper_bound = mid
        
        # Verify the result
        final_ore_needed = self.calculate_ore_needed(lower_bound)
        if final_ore_needed > available_ore:
            lower_bound -= 1
        
        return lower_bound
    
    def analyze_reaction_tree(self, target_chemical: str = 'FUEL') -> Dict[str, any]:
        """
        Analyze the reaction dependency tree for a target chemical.
        
        Args:
            target_chemical: Chemical to analyze (default: FUEL)
            
        Returns:
            Analysis data including dependencies and complexity metrics
        """
        def get_dependencies(chemical: str, visited: set = None) -> set:
            if visited is None:
                visited = set()
            
            if chemical in visited or chemical == 'ORE':
                return set()
            
            visited.add(chemical)
            dependencies = set()
            
            if chemical in self.reaction_map:
                reaction = self.reaction_map[chemical]
                for input_chem in reaction.inputs:
                    dependencies.add(input_chem.name)
                    dependencies.update(get_dependencies(input_chem.name, visited.copy()))
            
            return dependencies
        
        dependencies = get_dependencies(target_chemical)
        
        # Calculate tree depth
        def get_depth(chemical: str, visited: set = None) -> int:
            if visited is None:
                visited = set()
            
            if chemical in visited or chemical == 'ORE':
                return 0
            
            visited.add(chemical)
            
            if chemical not in self.reaction_map:
                return 0
            
            reaction = self.reaction_map[chemical]
            max_depth = 0
            for input_chem in reaction.inputs:
                depth = get_depth(input_chem.name, visited.copy())
                max_depth = max(max_depth, depth)
            
            return max_depth + 1
        
        tree_depth = get_depth(target_chemical)
        
        # Find chemicals that only produce one output
        single_use_chemicals = set()
        for name in dependencies:
            used_count = sum(1 for reaction in self.reactions 
                           if reaction.requires_chemical(name))
            if used_count == 1:
                single_use_chemicals.add(name)
        
        return {
            'target_chemical': target_chemical,
            'total_dependencies': len(dependencies),
            'dependency_tree_depth': tree_depth,
            'single_use_chemicals': len(single_use_chemicals),
            'total_reactions': len(self.reactions),
            'ore_dependencies': len([name for name in dependencies 
                                   if self.reaction_map.get(name, Reaction([], Chemical('ORE', 0))).requires_chemical('ORE')]),
            'all_dependencies': sorted(list(dependencies))
        }
    
    def get_production_efficiency(self, fuel_quantity: int = 1000) -> Dict[str, any]:
        """
        Analyze production efficiency for a given FUEL quantity.
        
        Args:
            fuel_quantity: Amount of FUEL to analyze
            
        Returns:
            Efficiency metrics and waste analysis
        """
        ore_needed = self.calculate_ore_needed(fuel_quantity)
        
        # Calculate waste (chemicals produced but not used)
        waste_analysis = {}
        total_waste_value = 0
        
        for chemical, amount in self.inventory.items():
            if amount > 0:
                waste_analysis[chemical] = amount
                # Estimate waste value based on complexity
                if chemical in self.reaction_map:
                    total_waste_value += amount
        
        # Calculate production steps
        production_steps = len(self.production_history)
        chemicals_produced = len(set(chem for chem, _ in self.production_history))
        
        return {
            'fuel_quantity': fuel_quantity,
            'ore_required': ore_needed,
            'ore_efficiency': fuel_quantity / ore_needed if ore_needed > 0 else 0,
            'production_steps': production_steps,
            'chemicals_produced': chemicals_produced,
            'waste_chemicals': len(waste_analysis),
            'total_waste_amount': sum(waste_analysis.values()),
            'waste_breakdown': waste_analysis,
            'production_history': self.production_history.copy()
        }


class ReactionParser:
    """Utility class for parsing chemical reaction specifications."""
    
    @staticmethod
    def parse_chemical(chemical_str: str) -> Chemical:
        """
        Parse a chemical string like "7 A" into a Chemical object.
        
        Args:
            chemical_str: String representation of chemical and quantity
            
        Returns:
            Chemical object
        """
        parts = chemical_str.strip().split()
        if len(parts) != 2:
            raise ValueError(f"Invalid chemical format: {chemical_str}")
        
        try:
            quantity = int(parts[0])
            name = parts[1]
            return Chemical(name, quantity)
        except ValueError:
            raise ValueError(f"Invalid chemical format: {chemical_str}")
    
    @staticmethod
    def parse_reaction_line(line: str) -> Reaction:
        """
        Parse a reaction line like "7 A, 1 E => 1 FUEL".
        
        Args:
            line: Reaction specification string
            
        Returns:
            Reaction object
        """
        if '=>' not in line:
            raise ValueError(f"Invalid reaction format: {line}")
        
        input_part, output_part = line.split('=>')
        
        # Parse inputs
        input_chemicals = []
        for input_str in input_part.split(','):
            if input_str.strip():
                input_chemicals.append(ReactionParser.parse_chemical(input_str))
        
        # Parse output
        output_chemical = ReactionParser.parse_chemical(output_part)
        
        return Reaction(input_chemicals, output_chemical)
    
    @staticmethod
    def parse_reactions(input_data: str) -> List[Reaction]:
        """
        Parse multiple reaction lines from input data.
        
        Args:
            input_data: Multi-line string with reaction specifications
            
        Returns:
            List of Reaction objects
        """
        reactions = []
        for line in input_data.strip().split('\n'):
            line = line.strip()
            if line:
                reactions.append(ReactionParser.parse_reaction_line(line))
        
        return reactions


class Day14Solution(AdventSolution):
    """Enhanced solution for Advent of Code 2019 Day 14: Space Stoichiometry."""
    
    def __init__(self):
        super().__init__(year=2019, day=14, title="Space Stoichiometry")
    
    def part1(self, input_data: str) -> int:
        """
        Calculate ORE needed to produce 1 FUEL.
        
        Args:
            input_data: Reaction specifications
            
        Returns:
            Minimum ORE required for 1 FUEL
        """
        reactions = ReactionParser.parse_reactions(input_data)
        factory = NanoFactory(reactions)
        return factory.calculate_ore_needed(1)
    
    def part2(self, input_data: str) -> int:
        """
        Find maximum FUEL producible from 1 trillion ORE.
        
        Args:
            input_data: Reaction specifications
            
        Returns:
            Maximum FUEL from 1,000,000,000,000 ORE
        """
        reactions = ReactionParser.parse_reactions(input_data)
        factory = NanoFactory(reactions)
        return factory.find_max_fuel_from_ore(1_000_000_000_000)
    
    def analyze(self, input_data: str) -> None:
        """
        Provide comprehensive analysis of the chemical reaction system.
        
        Args:
            input_data: Reaction specifications
        """
        reactions = ReactionParser.parse_reactions(input_data)
        factory = NanoFactory(reactions)
        
        print("=== Space Stoichiometry Analysis ===\n")
        
        # Basic reaction analysis
        print(f"Total Reactions: {len(reactions)}")
        print(f"Unique Chemicals: {len(set([r.output.name for r in reactions] + ['ORE']))}")
        
        print("\nReaction Overview:")
        for i, reaction in enumerate(reactions, 1):
            print(f"  {i:2}: {reaction}")
        
        # Dependency analysis
        print(f"\nDependency Analysis:")
        tree_analysis = factory.analyze_reaction_tree('FUEL')
        for key, value in tree_analysis.items():
            if key != 'all_dependencies':
                print(f"  {key.replace('_', ' ').title()}: {value}")
        
        # Part 1 analysis
        ore_for_one_fuel = factory.calculate_ore_needed(1)
        efficiency_1 = factory.get_production_efficiency(1)
        
        print(f"\nPart 1 Analysis (1 FUEL):")
        print(f"  ORE Required: {ore_for_one_fuel}")
        print(f"  Production Steps: {efficiency_1['production_steps']}")
        print(f"  Chemicals Produced: {efficiency_1['chemicals_produced']}")
        print(f"  Waste Chemicals: {efficiency_1['waste_chemicals']}")
        
        # Efficiency analysis at different scales
        print(f"\nEfficiency Analysis:")
        for fuel_amount in [1, 10, 100, 1000]:
            efficiency = factory.get_production_efficiency(fuel_amount)
            ore_per_fuel = efficiency['ore_required'] / fuel_amount
            print(f"  {fuel_amount:4} FUEL: {efficiency['ore_required']:8} ORE "
                  f"({ore_per_fuel:.2f} ORE/FUEL, {efficiency['waste_chemicals']} waste types)")
        
        # Part 2 analysis
        max_fuel = factory.find_max_fuel_from_ore(1_000_000_000_000)
        ore_used = factory.calculate_ore_needed(max_fuel)
        ore_leftover = 1_000_000_000_000 - ore_used
        
        print(f"\nPart 2 Analysis (1 Trillion ORE):")
        print(f"  Maximum FUEL: {max_fuel:,}")
        print(f"  ORE Used: {ore_used:,}")
        print(f"  ORE Leftover: {ore_leftover:,}")
        print(f"  Efficiency: {max_fuel / 1_000_000_000_000 * 1_000_000:.2f} FUEL per million ORE")
        
        print(f"\nResults:")
        print(f"  Part 1: {ore_for_one_fuel} ORE")
        print(f"  Part 2: {max_fuel:,} FUEL")


# Legacy functions for test runner compatibility
def part1(input_data: str = None) -> int:
    """Legacy part1 function for test runner compatibility."""
    if input_data is None:
        # Auto-load input file
        try:
            with open('/home/mike/src/advent_of_code/2019/day14_input.txt', 'r') as f:
                input_data = f.read()
        except FileNotFoundError:
            # Fallback to a simple test case
            input_data = """10 ORE => 10 A
1 ORE => 1 B
7 A, 1 B => 1 C
7 A, 1 C => 1 D
7 A, 1 D => 1 E
7 A, 1 E => 1 FUEL"""
    
    solution = Day14Solution()
    return solution.part1(input_data)


def part2(input_data: str = None) -> int:
    """Legacy part2 function for test runner compatibility."""
    if input_data is None:
        # Auto-load input file
        try:
            with open('/home/mike/src/advent_of_code/2019/day14_input.txt', 'r') as f:
                input_data = f.read()
        except FileNotFoundError:
            # Fallback to a simple test case
            input_data = """10 ORE => 10 A
1 ORE => 1 B
7 A, 1 B => 1 C
7 A, 1 C => 1 D
7 A, 1 D => 1 E
7 A, 1 E => 1 FUEL"""
    
    solution = Day14Solution()
    return solution.part2(input_data)


if __name__ == "__main__":
    solution = Day14Solution()
    solution.main()