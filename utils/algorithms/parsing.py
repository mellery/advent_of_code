#!/usr/bin/env python3
"""
Parsing and Pattern Matching Library

Expression parsing, pattern matching, and text processing utilities
extracted from AoC solutions. Optimized for common AoC parsing patterns.

Key Features:
- Mathematical expression parsing with custom precedence
- Regex-based pattern extraction and matching
- Recursive descent parsing for complex grammars
- Number and coordinate extraction utilities
- String transformation and replacement helpers

Performance Targets:
- Simple parsing: < 1ms per operation
- Complex expressions: < 10ms for typical AoC expressions
- Large text processing: < 100ms for AoC-sized inputs
"""

import re
import ast
from typing import (
    Dict, List, Tuple, Optional, Callable, Any, Union,
    Pattern, Match, Iterator
)
from dataclasses import dataclass
from enum import Enum
from abc import ABC, abstractmethod
import operator

# Type definitions
Token = Tuple[str, str]  # (type, value)
ParseResult = Any

class TokenType(Enum):
    """Token types for parsing."""
    NUMBER = "NUMBER"
    OPERATOR = "OPERATOR"
    IDENTIFIER = "IDENTIFIER"
    LPAREN = "LPAREN"
    RPAREN = "RPAREN"
    COMMA = "COMMA"
    STRING = "STRING"
    EOF = "EOF"

@dataclass
class ParseError(Exception):
    """Custom exception for parsing errors."""
    message: str
    position: int = -1
    line: int = -1
    column: int = -1

class Tokenizer:
    """
    Generic tokenizer for parsing operations.
    
    Extracted patterns from expression parsing problems.
    """
    
    def __init__(self, text: str, token_patterns: Dict[str, str]):
        """
        Initialize tokenizer.
        
        Args:
            text: Text to tokenize
            token_patterns: Dictionary mapping token types to regex patterns
        """
        self.text = text
        self.position = 0
        self.tokens: List[Token] = []
        self.current_token = 0
        
        # Compile patterns
        self.patterns = {}
        for token_type, pattern in token_patterns.items():
            self.patterns[token_type] = re.compile(pattern)
        
        self._tokenize()
    
    def _tokenize(self):
        """Tokenize the input text."""
        while self.position < len(self.text):
            # Skip whitespace
            if self.text[self.position].isspace():
                self.position += 1
                continue
            
            matched = False
            for token_type, pattern in self.patterns.items():
                match = pattern.match(self.text, self.position)
                if match:
                    value = match.group(0)
                    self.tokens.append((token_type, value))
                    self.position = match.end()
                    matched = True
                    break
            
            if not matched:
                raise ParseError(f"Unexpected character: {self.text[self.position]}", self.position)
        
        self.tokens.append((TokenType.EOF.value, ""))
    
    def peek(self) -> Token:
        """Peek at current token without consuming it."""
        if self.current_token < len(self.tokens):
            return self.tokens[self.current_token]
        return (TokenType.EOF.value, "")
    
    def consume(self, expected_type: Optional[str] = None) -> Token:
        """
        Consume and return current token.
        
        Args:
            expected_type: Expected token type (raises error if mismatch)
            
        Returns:
            Consumed token
        """
        token = self.peek()
        
        if expected_type and token[0] != expected_type:
            raise ParseError(f"Expected {expected_type}, got {token[0]}")
        
        self.current_token += 1
        return token

class ExpressionEvaluator:
    """
    Mathematical expression evaluator with custom precedence.
    
    Extracted from 2020 Day 18 (Operation Order) and similar problems.
    """
    
    def __init__(self, 
                 precedence: Optional[Dict[str, int]] = None,
                 operators: Optional[Dict[str, Callable]] = None):
        """
        Initialize expression evaluator.
        
        Args:
            precedence: Operator precedence (higher = earlier evaluation)
            operators: Operator implementations
        """
        self.precedence = precedence or {
            '+': 1, '-': 1, '*': 2, '/': 2, '**': 3
        }
        
        self.operators = operators or {
            '+': operator.add,
            '-': operator.sub,
            '*': operator.mul,
            '/': operator.truediv,
            '//': operator.floordiv,
            '%': operator.mod,
            '**': operator.pow
        }
        
        # Token patterns for mathematical expressions (order matters!)
        self.token_patterns = {
            'NUMBER': r'\d+(?:\.\d+)?',
            'LPAREN': r'\(',
            'RPAREN': r'\)',
            'OPERATOR': r'\*\*|[+\-*/%]',  # ** must come before *
            'IDENTIFIER': r'[a-zA-Z_][a-zA-Z0-9_]*'
        }
    
    def evaluate(self, expression: str, variables: Optional[Dict[str, float]] = None) -> float:
        """
        Evaluate mathematical expression.
        
        Args:
            expression: Expression string to evaluate
            variables: Variable values for substitution
            
        Returns:
            Evaluated result
        """
        tokenizer = Tokenizer(expression, self.token_patterns)
        return self._parse_expression(tokenizer, variables or {})
    
    def _parse_expression(self, tokenizer: Tokenizer, variables: Dict[str, float]) -> float:
        """Parse expression using recursive descent."""
        return self._parse_binary_op(tokenizer, variables, 0)
    
    def _parse_binary_op(self, tokenizer: Tokenizer, variables: Dict[str, float], min_precedence: int) -> float:
        """Parse binary operations with precedence."""
        left = self._parse_primary(tokenizer, variables)
        
        while True:
            token = tokenizer.peek()
            if token[0] != 'OPERATOR' or token[1] not in self.precedence:
                break
            
            op = token[1]
            if self.precedence[op] < min_precedence:
                break
            
            tokenizer.consume('OPERATOR')
            right = self._parse_binary_op(tokenizer, variables, self.precedence[op] + 1)
            left = self.operators[op](left, right)
        
        return left
    
    def _parse_primary(self, tokenizer: Tokenizer, variables: Dict[str, float]) -> float:
        """Parse primary expressions (numbers, variables, parentheses)."""
        token = tokenizer.peek()
        
        if token[0] == 'NUMBER':
            tokenizer.consume('NUMBER')
            return float(token[1])
        
        elif token[0] == 'IDENTIFIER':
            tokenizer.consume('IDENTIFIER')
            if token[1] in variables:
                return variables[token[1]]
            else:
                raise ParseError(f"Unknown variable: {token[1]}")
        
        elif token[0] == 'LPAREN':
            tokenizer.consume('LPAREN')
            result = self._parse_expression(tokenizer, variables)
            tokenizer.consume('RPAREN')
            return result
        
        else:
            raise ParseError(f"Unexpected token: {token}")

class PatternMatcher:
    """
    Advanced pattern matching utilities.
    
    Extracted from problems involving string pattern recognition.
    """
    
    def __init__(self):
        # Common regex patterns
        self.patterns = {
            'integer': re.compile(r'-?\d+'),
            'float': re.compile(r'-?\d+(?:\.\d+)?'),
            'coordinate': re.compile(r'\((-?\d+),\s*(-?\d+)\)'),
            'word': re.compile(r'[a-zA-Z]+'),
            'identifier': re.compile(r'[a-zA-Z_][a-zA-Z0-9_]*'),
            'hex': re.compile(r'#?[0-9a-fA-F]+'),
            'binary': re.compile(r'[01]+'),
        }
    
    def extract_numbers(self, text: str, as_int: bool = True) -> List[Union[int, float]]:
        """
        Extract all numbers from text.
        
        Args:
            text: Input text
            as_int: Return integers if True, floats if False
            
        Returns:
            List of extracted numbers
        """
        pattern = self.patterns['integer'] if as_int else self.patterns['float']
        matches = pattern.findall(text)
        
        if as_int:
            return [int(match) for match in matches]
        else:
            return [float(match) for match in matches]
    
    def extract_coordinates(self, text: str) -> List[Tuple[int, int]]:
        """
        Extract coordinate pairs from text.
        
        Supports formats like (x, y), (x,y), etc.
        """
        matches = self.patterns['coordinate'].findall(text)
        return [(int(x), int(y)) for x, y in matches]
    
    def extract_words(self, text: str) -> List[str]:
        """Extract all words from text."""
        return self.patterns['word'].findall(text)
    
    def extract_pattern(self, text: str, pattern: Union[str, Pattern]) -> List[str]:
        """
        Extract matches for custom pattern.
        
        Args:
            text: Input text
            pattern: Regex pattern (string or compiled)
            
        Returns:
            List of matches
        """
        if isinstance(pattern, str):
            pattern = re.compile(pattern)
        
        return pattern.findall(text)
    
    def replace_pattern(self, text: str, pattern: Union[str, Pattern], 
                       replacement: Union[str, Callable]) -> str:
        """
        Replace pattern matches in text.
        
        Args:
            text: Input text
            pattern: Regex pattern
            replacement: Replacement string or function
            
        Returns:
            Text with replacements
        """
        if isinstance(pattern, str):
            pattern = re.compile(pattern)
        
        if callable(replacement):
            return pattern.sub(replacement, text)
        else:
            return pattern.sub(replacement, text)
    
    def split_on_pattern(self, text: str, pattern: Union[str, Pattern]) -> List[str]:
        """Split text on pattern matches."""
        if isinstance(pattern, str):
            pattern = re.compile(pattern)
        
        return pattern.split(text)
    
    def find_overlapping_matches(self, text: str, pattern: Union[str, Pattern]) -> List[Match]:
        """
        Find all overlapping matches of pattern.
        
        Useful for problems where overlapping matches matter.
        """
        if isinstance(pattern, str):
            pattern = re.compile(pattern)
        
        matches = []
        start = 0
        
        while start < len(text):
            match = pattern.search(text, start)
            if match:
                matches.append(match)
                start = match.start() + 1
            else:
                break
        
        return matches

def parse_numbers(text: str, separator: Optional[str] = None) -> List[int]:
    """
    Parse numbers from text with optional separator.
    
    Common utility extracted from multiple AoC solutions.
    
    Args:
        text: Input text containing numbers
        separator: Optional separator pattern
        
    Returns:
        List of parsed integers
    """
    if separator:
        parts = re.split(separator, text)
        numbers = []
        for part in parts:
            nums = re.findall(r'-?\d+', part.strip())
            numbers.extend(int(num) for num in nums)
        return numbers
    else:
        return [int(match) for match in re.findall(r'-?\d+', text)]

def parse_coordinate_pairs(text: str) -> List[Tuple[int, int]]:
    """
    Parse coordinate pairs from various formats.
    
    Supports: (x,y), x,y, x y, etc.
    """
    # Try parentheses format first
    paren_matches = re.findall(r'\((-?\d+),\s*(-?\d+)\)', text)
    if paren_matches:
        return [(int(x), int(y)) for x, y in paren_matches]
    
    # Try comma-separated
    comma_matches = re.findall(r'(-?\d+),\s*(-?\d+)', text)
    if comma_matches:
        return [(int(x), int(y)) for x, y in comma_matches]
    
    # Try space-separated
    numbers = parse_numbers(text)
    if len(numbers) % 2 == 0:
        return [(numbers[i], numbers[i+1]) for i in range(0, len(numbers), 2)]
    
    return []

def parse_grid_from_text(text: str, 
                        value_map: Optional[Dict[str, Any]] = None) -> Dict[Tuple[int, int], Any]:
    """
    Parse 2D grid from text representation.
    
    Args:
        text: Multi-line text representing grid
        value_map: Optional mapping from characters to values
        
    Returns:
        Dictionary mapping (row, col) to cell values
    """
    grid = {}
    lines = text.strip().split('\n')
    
    for row, line in enumerate(lines):
        for col, char in enumerate(line):
            value = value_map.get(char, char) if value_map else char
            grid[(row, col)] = value
    
    return grid

def extract_patterns(text: str, *patterns: str) -> Dict[str, List[str]]:
    """
    Extract multiple patterns from text.
    
    Args:
        text: Input text
        *patterns: Regex patterns to search for
        
    Returns:
        Dictionary mapping pattern index to matches
    """
    results = {}
    
    for i, pattern in enumerate(patterns):
        compiled_pattern = re.compile(pattern)
        matches = compiled_pattern.findall(text)
        results[f"pattern_{i}"] = matches
    
    return results

def parse_structured_data(text: str, 
                         field_patterns: Dict[str, str]) -> Dict[str, List[str]]:
    """
    Parse structured data using named field patterns.
    
    Args:
        text: Input text
        field_patterns: Dictionary mapping field names to regex patterns
        
    Returns:
        Dictionary mapping field names to extracted values
    """
    results = {}
    
    for field_name, pattern in field_patterns.items():
        compiled_pattern = re.compile(pattern)
        matches = compiled_pattern.findall(text)
        results[field_name] = matches
    
    return results

class RecursiveDescentParser(ABC):
    """
    Base class for recursive descent parsers.
    
    Useful for complex grammar parsing in AoC problems.
    """
    
    def __init__(self, text: str):
        self.text = text
        self.position = 0
        self.length = len(text)
    
    def peek(self, offset: int = 0) -> str:
        """Peek at character at current position + offset."""
        pos = self.position + offset
        if pos < self.length:
            return self.text[pos]
        return ''
    
    def consume(self, expected: Optional[str] = None) -> str:
        """Consume and return current character."""
        if self.position >= self.length:
            return ''
        
        char = self.text[self.position]
        if expected and char != expected:
            raise ParseError(f"Expected '{expected}', got '{char}'", self.position)
        
        self.position += 1
        return char
    
    def skip_whitespace(self):
        """Skip whitespace characters."""
        while self.position < self.length and self.text[self.position].isspace():
            self.position += 1
    
    def at_end(self) -> bool:
        """Check if at end of input."""
        return self.position >= self.length
    
    @abstractmethod
    def parse(self) -> Any:
        """Parse the input and return result."""
        pass

# Convenience functions for common parsing tasks

def safe_eval(expression: str, allowed_names: Optional[Dict[str, Any]] = None) -> Any:
    """
    Safely evaluate mathematical expressions.
    
    Uses AST parsing to avoid security issues with eval().
    """
    allowed_names = allowed_names or {}
    
    try:
        tree = ast.parse(expression, mode='eval')
        return _eval_node(tree.body, allowed_names)
    except Exception as e:
        raise ParseError(f"Invalid expression: {e}")

def _eval_node(node: ast.AST, names: Dict[str, Any]) -> Any:
    """Evaluate AST node safely."""
    if isinstance(node, ast.Constant):
        return node.value
    elif isinstance(node, ast.Name):
        if node.id in names:
            return names[node.id]
        else:
            raise ValueError(f"Unknown name: {node.id}")
    elif isinstance(node, ast.BinOp):
        left = _eval_node(node.left, names)
        right = _eval_node(node.right, names)
        
        ops = {
            ast.Add: operator.add,
            ast.Sub: operator.sub,
            ast.Mult: operator.mul,
            ast.Div: operator.truediv,
            ast.FloorDiv: operator.floordiv,
            ast.Mod: operator.mod,
            ast.Pow: operator.pow
        }
        
        if type(node.op) in ops:
            return ops[type(node.op)](left, right)
        else:
            raise ValueError(f"Unsupported operation: {type(node.op)}")
    else:
        raise ValueError(f"Unsupported node type: {type(node)}")

def extract_line_groups(text: str, empty_line_separator: bool = True) -> List[List[str]]:
    """
    Split text into groups of lines.
    
    Common pattern in AoC for parsing input with blank line separators.
    """
    lines = text.strip().split('\n')
    groups = []
    current_group = []
    
    for line in lines:
        if empty_line_separator and line.strip() == '':
            if current_group:
                groups.append(current_group)
                current_group = []
        else:
            current_group.append(line)
    
    if current_group:
        groups.append(current_group)
    
    return groups