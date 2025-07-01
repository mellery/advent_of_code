#!/usr/bin/env python3
"""
ASCII Art Character Recognition Utility

This module provides functionality to parse ASCII art representations
of letters commonly used in Advent of Code challenges.

The parser supports different font styles and character widths,
automatically detecting the format and parsing letters accordingly.
"""

from typing import Dict, List, Optional


class AsciiArtParser:
    """Parser for ASCII art letters in Advent of Code format."""
    
    # Character patterns for different font styles
    FONT_PATTERNS = {
        # Day 8 style - 6x4 characters with thick font
        'thick': {
            'char_width': 5,  # 4 pixels + 1 space
            'char_height': 6,
            'patterns': {
                'A': [
                    " ██ ",
                    "█  █",
                    "█  █",
                    "████",
                    "█  █",
                    "█  █"
                ],
                'B': [
                    "███ ",
                    "█  █",
                    "███ ",
                    "█  █",
                    "█  █",
                    "███ "
                ],
                'C': [
                    " ███",
                    "█   ",
                    "█   ",
                    "█   ",
                    "█   ",
                    " ███"
                ],
                'E': [
                    "████",
                    "█   ",
                    "███ ",
                    "█   ",
                    "█   ",
                    "████"
                ],
                'F': [
                    "████",
                    "█   ",
                    "███ ",
                    "█   ",
                    "█   ",
                    "█   "
                ],
                'G': [
                    " ███",
                    "█   ",
                    "█   ",
                    "█ ██",
                    "█  █",
                    " ███"
                ],
                'H': [
                    "█  █",
                    "█  █",
                    "████",
                    "█  █",
                    "█  █",
                    "█  █"
                ],
                'J': [
                    "  ██",
                    "   █",
                    "   █",
                    "   █",
                    "█  █",
                    " ██ "
                ],
                'L': [
                    "█   ",
                    "█   ",
                    "█   ",
                    "█   ",
                    "█   ",
                    "████"
                ],
                'P': [
                    "███ ",
                    "█  █",
                    "█  █",
                    "███ ",
                    "█   ",
                    "█   "
                ],
                'R': [
                    "███ ",
                    "█  █",
                    "███ ",
                    "█ █ ",
                    "█  █",
                    "█  █"
                ],
                'U': [
                    "█  █",
                    "█  █",
                    "█  █",
                    "█  █",
                    "█  █",
                    " ██ "
                ],
                'Z': [
                    "████",
                    "   █",
                    "  █ ",
                    " █  ",
                    "█   ",
                    "████"
                ]
            }
        },
        
        # Day 11 style - 6x4 characters with thin font (leading space)
        'thin': {
            'char_width': 5,  # 4 pixels + 1 space
            'char_height': 6,
            'patterns': {
                'C': [
                    "  ██",
                    " █  ",
                    " █  ",
                    " █  ",
                    " █  ",
                    "  ██"
                ],
                'E': [
                    " ███",
                    " █  ",
                    " ███",
                    " █  ",
                    " █  ",
                    " ███"
                ],
                'G': [
                    "  ██",
                    " █  ",
                    " █  ",
                    " █ █",
                    " █  ",
                    "  ██"
                ],
                'H': [
                    " █  ",
                    " █  ",
                    " ███",
                    " █  ",
                    " █  ",
                    " █  "
                ],
                'J': [
                    "   █",
                    "    ",
                    "    ",
                    "    ",
                    " █  ",
                    "  ██"
                ],
                'P': [
                    " ███",
                    " █  ",
                    " █  ",
                    " ███",
                    " █  ",
                    " █  "
                ],
                'U': [
                    " █  ",
                    " █  ",
                    " █  ",
                    " █  ",
                    " █  ",
                    "  ██"
                ]
            }
        },
        
        # Day 13 style - 6x4 characters with dots/hashes
        'day13': {
            'char_width': 5,  # 4 pixels + 1 space
            'char_height': 6,
            'patterns': {
                'C': [
                    ".##.",
                    "#..#",
                    "#...",
                    "#...",
                    "#..#",
                    ".##."
                ],
                'E': [
                    "####",
                    "#...",
                    "###.",
                    "#...",
                    "#...",
                    "####"
                ],
                'H': [
                    "#..#",
                    "#..#",
                    "####",
                    "#..#",
                    "#..#",
                    "#..#"
                ],
                'J': [
                    "..##",
                    "...#",
                    "...#",
                    "...#",
                    "#..#",
                    ".##."
                ],
                'R': [
                    "###.",
                    "#..#",
                    "#..#",
                    "###.",
                    "#.#.",
                    "#..#"
                ]
            }
        }
    }
    
    def __init__(self):
        """Initialize the ASCII art parser."""
        pass
    
    def detect_font_style(self, ascii_art: str) -> str:
        """
        Detect which font style is used in the ASCII art.
        
        Args:
            ascii_art: ASCII art string to analyze
            
        Returns:
            Font style name ('thick' or 'thin')
        """
        if not ascii_art:
            return 'thick'  # Default
        
        lines = ascii_art.split('\n')
        if not lines:
            return 'thick'
        
        # Check first line for leading spaces pattern
        first_line = lines[0] if lines else ''
        
        # If most characters start with spaces, it's likely thin font
        if first_line.startswith(' ') and '  ' in first_line:
            return 'thin'
        else:
            return 'thick'
    
    def parse_letters(self, ascii_art: str, font_style: Optional[str] = None) -> str:
        """
        Parse ASCII art into letters.
        
        Args:
            ascii_art: ASCII art string to parse
            font_style: Optional font style override ('thick' or 'thin')
            
        Returns:
            String of recognized letters
        """
        if not ascii_art:
            return ""
        
        # Auto-detect font style if not provided
        if font_style is None:
            font_style = self.detect_font_style(ascii_art)
        
        if font_style not in self.FONT_PATTERNS:
            font_style = 'thick'  # Fallback
        
        font_config = self.FONT_PATTERNS[font_style]
        patterns = font_config['patterns']
        char_width = font_config['char_width']
        char_height = font_config['char_height']
        
        lines = ascii_art.split('\n')
        if len(lines) < char_height:
            return ""
        
        # Calculate number of characters
        line_length = len(lines[0]) if lines else 0
        num_chars = (line_length + char_width - 1) // char_width
        
        result = ""
        
        for char_idx in range(num_chars):
            start_col = char_idx * char_width
            end_col = min(start_col + 4, line_length)  # 4 pixels wide
            
            # Extract character pattern
            char_pattern = []
            for line in lines[:char_height]:
                if start_col < len(line):
                    char_slice = line[start_col:end_col]
                    # Pad to 4 characters if needed
                    char_slice = char_slice.ljust(4)
                    char_pattern.append(char_slice)
                else:
                    char_pattern.append("    ")
            
            # Match against known patterns
            best_match = '?'
            best_score = 0
            
            for letter, pattern in patterns.items():
                if len(pattern) == len(char_pattern):
                    matches = sum(1 for i in range(len(pattern)) 
                                if pattern[i] == char_pattern[i])
                    if matches > best_score:
                        best_score = matches
                        best_match = letter
            
            # Only accept matches with at least 5 out of 6 lines matching
            if best_score >= 5:
                result += best_match
            else:
                result += '?'
        
        return result
    
    def add_pattern(self, letter: str, pattern: List[str], font_style: str = 'thick') -> None:
        """
        Add a new character pattern to the parser.
        
        Args:
            letter: Letter to add (single character)
            pattern: List of strings representing the character pattern
            font_style: Font style to add the pattern to
        """
        if font_style in self.FONT_PATTERNS:
            self.FONT_PATTERNS[font_style]['patterns'][letter] = pattern
    
    def get_available_letters(self, font_style: str = 'thick') -> List[str]:
        """
        Get list of available letters for a font style.
        
        Args:
            font_style: Font style to query
            
        Returns:
            List of available letter patterns
        """
        if font_style in self.FONT_PATTERNS:
            return sorted(self.FONT_PATTERNS[font_style]['patterns'].keys())
        return []


# Convenience function for direct use
def parse_ascii_letters(ascii_art: str, font_style: Optional[str] = None) -> str:
    """
    Parse ASCII art into letters using the default parser.
    
    Args:
        ascii_art: ASCII art string to parse
        font_style: Optional font style ('thick' or 'thin')
        
    Returns:
        String of recognized letters
    """
    parser = AsciiArtParser()
    return parser.parse_letters(ascii_art, font_style)


if __name__ == "__main__":
    # Test the parser with sample data
    parser = AsciiArtParser()
    
    # Test thick font (Day 8 style)
    thick_art = """█  █ ███  █  █ ████ ███  
█  █ █  █ █  █ █    █  █ 
█  █ ███  █  █ ███  █  █ 
█  █ █  █ █  █ █    ███  
█  █ █  █ █  █ █    █    
 ██  ███   ██  █    █    """
    
    print("Testing thick font:")
    print(f"Result: {parser.parse_letters(thick_art, 'thick')}")
    
    # Test thin font (Day 11 style)
    thin_art = """ ███   ██  █  █ ████ █  █  ██    ██ █  █
 █  █ █  █ █  █ █    █  █ █  █    █ █  █
 █  █ █    █  █ ███  ████ █       █ ████
 ███  █ ██ █  █ █    █  █ █       █ █  █
 █    █  █ █  █ █    █  █ █  █ █  █ █  █
 █     ███  ██  ████ █  █  ██   ██  █  █"""
    
    print("\nTesting thin font:")
    print(f"Result: {parser.parse_letters(thin_art, 'thin')}")
    
    # Test auto-detection
    print("\nTesting auto-detection:")
    print(f"Thick auto: {parser.parse_letters(thick_art)}")
    print(f"Thin auto: {parser.parse_letters(thin_art)}")