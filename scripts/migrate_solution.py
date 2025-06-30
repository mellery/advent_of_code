#!/usr/bin/env python3
"""
Solution Migration Script

This script migrates existing Advent of Code solutions to use the enhanced
AdventSolution base class and modern Python patterns.
"""

import re
import ast
import argparse
import shutil
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import sys

# Add utils to path for imports
script_dir = Path(__file__).parent
project_root = script_dir.parent
sys.path.append(str(project_root))


class SolutionMigrator:
    """Migrates legacy solutions to enhanced AdventSolution architecture."""
    
    def __init__(self, source_file: Path, backup: bool = True):
        """
        Initialize migrator.
        
        Args:
            source_file: Path to the solution file to migrate
            backup: Whether to create backup of original file
        """
        self.source_file = source_file
        self.backup = backup
        self.source_code = ""
        self.analysis = {}
        
    def analyze_solution(self) -> Dict:
        """
        Analyze the existing solution to understand its structure.
        
        Returns:
            Dictionary containing analysis results
        """
        with open(self.source_file, 'r') as f:
            self.source_code = f.read()
        
        # Parse file with AST for more reliable analysis
        try:
            tree = ast.parse(self.source_code)
        except SyntaxError as e:
            raise ValueError(f"Failed to parse {self.source_file}: {e}")
        
        analysis = {
            'year': self._extract_year(),
            'day': self._extract_day(),
            'title': self._extract_title(),
            'imports': self._extract_imports(tree),
            'classes': self._extract_classes(tree),
            'functions': self._extract_functions(tree),
            'part1_function': self._find_part_function(tree, 1),
            'part2_function': self._find_part_function(tree, 2),
            'main_function': self._find_main_function(tree),
            'has_input_handling': self._has_input_handling(),
            'test_cases': self._extract_test_cases(),
            'complexity_level': self._assess_complexity(tree)
        }
        
        self.analysis = analysis
        return analysis
    
    def _extract_year(self) -> int:
        """Extract year from file path or code."""
        # Try to get from path first
        path_parts = self.source_file.parts
        for part in path_parts:
            if part.isdigit() and len(part) == 4 and part.startswith('20'):
                return int(part)
        
        # Try to extract from docstring or comments
        year_pattern = r'Advent of Code (\d{4})'
        match = re.search(year_pattern, self.source_code)
        if match:
            return int(match.group(1))
        
        # Default fallback
        return 2023
    
    def _extract_day(self) -> int:
        """Extract day number from filename or code."""
        # Try filename first
        filename = self.source_file.stem
        day_match = re.search(r'day(\d+)', filename, re.IGNORECASE)
        if day_match:
            return int(day_match.group(1))
        
        advent_match = re.search(r'advent(\d+)', filename, re.IGNORECASE)
        if advent_match:
            return int(advent_match.group(1))
        
        # Try to extract from docstring
        day_pattern = r'Day (\d+)'
        match = re.search(day_pattern, self.source_code)
        if match:
            return int(match.group(1))
        
        return 1  # Default fallback
    
    def _extract_title(self) -> str:
        """Extract problem title from docstring."""
        # Look for pattern like "Day X: Title"
        title_pattern = r'Day \d+:\s*([^\n\r]+)'
        match = re.search(title_pattern, self.source_code)
        if match:
            return match.group(1).strip()
        
        # Look for title in first docstring
        docstring_pattern = r'"""([^"]+)"""'
        match = re.search(docstring_pattern, self.source_code)
        if match:
            lines = match.group(1).split('\n')
            for line in lines:
                line = line.strip()
                if line and not line.startswith('Advent of Code'):
                    return line
        
        return "Migrated Solution"
    
    def _extract_imports(self, tree: ast.AST) -> List[str]:
        """Extract import statements."""
        imports = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append(f"import {alias.name}")
            elif isinstance(node, ast.ImportFrom):
                module = node.module or ""
                names = [alias.name for alias in node.names]
                imports.append(f"from {module} import {', '.join(names)}")
        return imports
    
    def _extract_classes(self, tree: ast.AST) -> List[str]:
        """Extract class definitions."""
        classes = []
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                classes.append(node.name)
        return classes
    
    def _extract_functions(self, tree: ast.AST) -> List[str]:
        """Extract function definitions."""
        functions = []
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                functions.append(node.name)
        return functions
    
    def _find_part_function(self, tree: ast.AST, part_num: int) -> Optional[str]:
        """Find part1 or part2 function."""
        target_names = [
            f"part{part_num}",
            f"part_{part_num}",
            f"solve_part{part_num}",
            f"solve_part_{part_num}",
            f"day{self._extract_day()}p{part_num}",
        ]
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                if node.name in target_names:
                    return node.name
        
        return None
    
    def _find_main_function(self, tree: ast.AST) -> Optional[str]:
        """Find main execution function."""
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                if node.name == "main":
                    return node.name
        return None
    
    def _has_input_handling(self) -> bool:
        """Check if solution has input file handling."""
        input_patterns = [
            r'open\s*\(',
            r'read\s*\(',
            r'filename',
            r'input_file',
            r'input_data'
        ]
        
        for pattern in input_patterns:
            if re.search(pattern, self.source_code):
                return True
        return False
    
    def _extract_test_cases(self) -> List[Dict]:
        """Extract test cases from the code."""
        test_cases = []
        
        # Look for embedded test data
        test_patterns = [
            r'test_input\s*=\s*["\']([^"\']+)["\']',
            r'example\s*=\s*["\']([^"\']+)["\']',
            r'assert.*==\s*(\d+)',
        ]
        
        for pattern in test_patterns:
            matches = re.findall(pattern, self.source_code, re.MULTILINE | re.DOTALL)
            for match in matches:
                test_cases.append({'data': match})
        
        return test_cases
    
    def _assess_complexity(self, tree: ast.AST) -> str:
        """Assess complexity level of the solution."""
        complexity_score = 0
        
        # Count various complexity indicators
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                complexity_score += 2
            elif isinstance(node, ast.FunctionDef):
                complexity_score += 1
            elif isinstance(node, ast.For):
                complexity_score += 1
            elif isinstance(node, ast.While):
                complexity_score += 1
            elif isinstance(node, ast.If):
                complexity_score += 0.5
        
        if complexity_score > 20:
            return "very_high"
        elif complexity_score > 10:
            return "high"
        elif complexity_score > 5:
            return "medium"
        else:
            return "low"
    
    def generate_migrated_code(self) -> str:
        """
        Generate the migrated code using AdventSolution base class.
        
        Returns:
            Migrated code as string
        """
        if not self.analysis:
            self.analyze_solution()
        
        # Build the new solution
        migrated_code = self._build_migrated_solution()
        return migrated_code
    
    def _build_migrated_solution(self) -> str:
        """Build the complete migrated solution."""
        lines = []
        
        # Header and imports
        lines.extend(self._build_header())
        lines.append("")
        lines.extend(self._build_imports())
        lines.append("")
        
        # Preserve any utility classes (like IntcodeSimple)
        lines.extend(self._preserve_utility_classes())
        if lines and lines[-1] != "":
            lines.append("")
        
        # Main solution class
        lines.extend(self._build_solution_class())
        lines.append("")
        
        # Main execution
        lines.extend(self._build_main_execution())
        
        return "\n".join(lines)
    
    def _build_header(self) -> List[str]:
        """Build file header with docstring."""
        year = self.analysis['year']
        day = self.analysis['day']
        title = self.analysis['title']
        
        return [
            '#!/usr/bin/env python3',
            '"""',
            f'Advent of Code {year} Day {day}: {title}',
            f'https://adventofcode.com/{year}/day/{day}',
            '',
            'Enhanced solution using AdventSolution base class.',
            'Migrated from legacy implementation.',
            '"""'
        ]
    
    def _build_imports(self) -> List[str]:
        """Build import statements."""
        imports = [
            'import sys',
            'from pathlib import Path',
            'from typing import Any, List, Dict, Optional, Tuple',
            '',
            '# Add utils to path',
            'sys.path.append(str(Path(__file__).parent.parent))',
            'from utils import AdventSolution, InputParser'
        ]
        
        # Add specific imports based on analysis
        if 'itertools' in str(self.analysis['imports']):
            imports.append('import itertools')
        if 'collections' in str(self.analysis['imports']):
            imports.append('from collections import defaultdict, deque, Counter')
        if 'functools' in str(self.analysis['imports']):
            imports.append('from functools import lru_cache')
        if 're' in str(self.analysis['imports']):
            imports.append('import re')
        
        return imports
    
    def _preserve_utility_classes(self) -> List[str]:
        """Preserve utility classes like IntcodeSimple."""
        lines = []
        
        # Extract class definitions from original code
        for class_name in self.analysis['classes']:
            if class_name != 'AdventSolution':  # Don't preserve if already exists
                class_code = self._extract_class_code(class_name)
                if class_code:
                    lines.extend(class_code)
                    lines.append("")
        
        return lines
    
    def _extract_class_code(self, class_name: str) -> List[str]:
        """Extract the complete code for a specific class."""
        lines = self.source_code.split('\n')
        class_lines = []
        in_class = False
        indent_level = 0
        
        for line in lines:
            stripped = line.strip()
            
            if stripped.startswith(f'class {class_name}'):
                in_class = True
                indent_level = len(line) - len(line.lstrip())
                class_lines.append(line)
            elif in_class:
                if line.strip() == "":
                    class_lines.append(line)
                elif len(line) - len(line.lstrip()) > indent_level:
                    class_lines.append(line)
                else:
                    # End of class
                    break
        
        return class_lines
    
    def _build_solution_class(self) -> List[str]:
        """Build the main solution class."""
        year = self.analysis['year']
        day = self.analysis['day']
        title = self.analysis['title']
        
        lines = [
            f'class Day{day}Solution(AdventSolution):',
            f'    """Solution for {year} Day {day}: {title}."""',
            '',
            '    def __init__(self):',
            f'        super().__init__({year}, {day}, "{title}")',
            '',
        ]
        
        # Add part1 method
        lines.extend(self._build_part_method(1))
        lines.append('')
        
        # Add part2 method
        lines.extend(self._build_part_method(2))
        
        # Add any utility methods that were functions
        utility_methods = self._convert_functions_to_methods()
        if utility_methods:
            lines.append('')
            lines.extend(utility_methods)
        
        return lines
    
    def _build_part_method(self, part_num: int) -> List[str]:
        """Build part1 or part2 method."""
        lines = [
            f'    def part{part_num}(self, input_data: str) -> Any:',
            f'        """',
            f'        Solve part {part_num} of the problem.',
            f'        ',
            f'        Args:',
            f'            input_data: Raw input data as string',
            f'            ',
            f'        Returns:',
            f'            Solution for part {part_num}',
            f'        """',
        ]
        
        # Try to extract existing part function logic
        part_func_name = self.analysis[f'part{part_num}_function']
        if part_func_name:
            # Extract the function body and adapt it
            func_body = self._extract_function_body(part_func_name)
            adapted_body = self._adapt_function_body(func_body, part_num)
            lines.extend(adapted_body)
        else:
            # Placeholder implementation
            lines.extend([
                '        parser = InputParser(input_data)',
                '        # TODO: Implement solution logic',
                '        return 0'
            ])
        
        return lines
    
    def _extract_function_body(self, func_name: str) -> List[str]:
        """Extract the body of a specific function."""
        lines = self.source_code.split('\n')
        func_lines = []
        in_function = False
        indent_level = 0
        
        for line in lines:
            stripped = line.strip()
            
            if stripped.startswith(f'def {func_name}'):
                in_function = True
                indent_level = len(line) - len(line.lstrip())
                continue  # Skip the def line
            elif in_function:
                if line.strip() == "":
                    func_lines.append(line)
                elif len(line) - len(line.lstrip()) > indent_level:
                    func_lines.append(line)
                else:
                    # End of function
                    break
        
        return func_lines
    
    def _adapt_function_body(self, func_body: List[str], part_num: int) -> List[str]:
        """Adapt function body for class method context."""
        adapted = []
        
        for line in func_body:
            # Remove docstring lines
            if '"""' in line or "'''" in line:
                continue
            
            # Adjust indentation (add 4 more spaces for class method)
            if line.strip():
                adapted_line = "        " + line
            else:
                adapted_line = line
            
            # Replace file reading with InputParser usage
            adapted_line = self._replace_input_handling(adapted_line)
            
            adapted.append(adapted_line)
        
        # If body is empty, add placeholder
        if not any(line.strip() for line in adapted):
            adapted = [
                '        parser = InputParser(input_data)',
                '        # TODO: Implement solution logic',
                '        return 0'
            ]
        
        return adapted
    
    def _replace_input_handling(self, line: str) -> str:
        """Replace file input handling with InputParser."""
        # Replace common file reading patterns
        replacements = [
            (r'with open\([^)]+\) as f:', 'parser = InputParser(input_data)'),
            (r'\.read\(\)\.strip\(\)', ''),
            (r'\.readlines\(\)', 'parser.as_lines()'),
            (r'\.split\(\'\\n\'\)', 'parser.as_lines()'),
            (r'f\.read\(\)', 'input_data'),
        ]
        
        for pattern, replacement in replacements:
            line = re.sub(pattern, replacement, line)
        
        return line
    
    def _convert_functions_to_methods(self) -> List[str]:
        """Convert utility functions to class methods."""
        lines = []
        
        # Skip main execution functions
        skip_functions = {
            'main', 'part1', 'part2', 'solve_part1', 'solve_part2',
            self.analysis.get('part1_function', ''),
            self.analysis.get('part2_function', ''),
            self.analysis.get('main_function', '')
        }
        
        utility_functions = [f for f in self.analysis['functions'] 
                           if f not in skip_functions and not f.startswith('day')]
        
        for func_name in utility_functions:
            func_code = self._extract_function_code(func_name)
            if func_code:
                # Convert to method by adding self parameter and proper indentation
                method_code = self._convert_function_to_method(func_code)
                lines.extend(method_code)
                lines.append('')
        
        return lines
    
    def _extract_function_code(self, func_name: str) -> List[str]:
        """Extract the complete code for a specific function."""
        lines = self.source_code.split('\n')
        func_lines = []
        in_function = False
        indent_level = 0
        
        for line in lines:
            stripped = line.strip()
            
            if stripped.startswith(f'def {func_name}'):
                in_function = True
                indent_level = len(line) - len(line.lstrip())
                func_lines.append(line)
            elif in_function:
                if line.strip() == "":
                    func_lines.append(line)
                elif len(line) - len(line.lstrip()) > indent_level:
                    func_lines.append(line)
                else:
                    # End of function
                    break
        
        return func_lines
    
    def _convert_function_to_method(self, func_code: List[str]) -> List[str]:
        """Convert function to class method."""
        if not func_code:
            return []
        
        method_lines = []
        
        for i, line in enumerate(func_code):
            if i == 0:  # Function definition line
                # Add self parameter
                method_line = line.replace('def ', '    def ')
                if '(self' not in method_line:
                    method_line = method_line.replace('(', '(self, ', 1)
                    if method_line.endswith('(self, ):'):
                        method_line = method_line.replace('(self, ):', '(self):')
                method_lines.append(method_line)
            else:
                # Add proper indentation for method
                if line.strip():
                    method_lines.append('    ' + line)
                else:
                    method_lines.append(line)
        
        return method_lines
    
    def _build_main_execution(self) -> List[str]:
        """Build main execution section."""
        day = self.analysis['day']
        
        return [
            'def main():',
            '    """Main execution function."""',
            f'    solution = Day{day}Solution()',
            '    solution.main()',
            '',
            '',
            'if __name__ == "__main__":',
            '    main()'
        ]
    
    def migrate(self, output_file: Optional[Path] = None) -> Path:
        """
        Perform the complete migration.
        
        Args:
            output_file: Optional custom output file path
            
        Returns:
            Path to the migrated file
        """
        if not output_file:
            # Create output filename with _enhanced suffix
            output_file = self.source_file.with_name(
                self.source_file.stem + "_enhanced" + self.source_file.suffix
            )
        
        # Create backup if requested
        if self.backup:
            backup_file = self.source_file.with_name(
                self.source_file.stem + "_backup" + self.source_file.suffix
            )
            shutil.copy2(self.source_file, backup_file)
            print(f"Created backup: {backup_file}")
        
        # Generate migrated code
        migrated_code = self.generate_migrated_code()
        
        # Write migrated file
        with open(output_file, 'w') as f:
            f.write(migrated_code)
        
        print(f"Migration complete: {self.source_file} -> {output_file}")
        return output_file


def main():
    """Main CLI interface."""
    parser = argparse.ArgumentParser(description="Migrate Advent of Code solutions to enhanced architecture")
    parser.add_argument("source_file", type=Path, help="Source solution file to migrate")
    parser.add_argument("-o", "--output", type=Path, help="Output file path")
    parser.add_argument("--no-backup", action="store_true", help="Don't create backup of original")
    parser.add_argument("--analyze-only", action="store_true", help="Only analyze, don't migrate")
    parser.add_argument("--in-place", action="store_true", help="Replace original file")
    
    args = parser.parse_args()
    
    if not args.source_file.exists():
        print(f"Error: Source file {args.source_file} does not exist")
        return 1
    
    migrator = SolutionMigrator(args.source_file, backup=not args.no_backup)
    
    if args.analyze_only:
        analysis = migrator.analyze_solution()
        print("Analysis Results:")
        print("=" * 50)
        for key, value in analysis.items():
            print(f"{key}: {value}")
        return 0
    
    try:
        if args.in_place:
            output_file = args.source_file
        else:
            output_file = args.output
        
        migrated_file = migrator.migrate(output_file)
        
        print(f"\nMigration Summary:")
        print(f"Source: {args.source_file}")
        print(f"Output: {migrated_file}")
        print(f"Year: {migrator.analysis['year']}")
        print(f"Day: {migrator.analysis['day']}")
        print(f"Title: {migrator.analysis['title']}")
        print(f"Complexity: {migrator.analysis['complexity_level']}")
        
        return 0
        
    except Exception as e:
        print(f"Migration failed: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())