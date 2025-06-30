#!/usr/bin/env python3
"""
Advent of Code 2019 - Day 8: Space Image Format

The Elves contact you over a radio modem and give you an encrypted password
in a special image format. The image consists of layers, and you need to
decode them to find the password.

Key Concepts:
- Layer-based image processing
- Pixel transparency and composition
- Data validation through layer analysis
- Image rendering and visualization
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.advent_base import AdventSolution
from typing import List, Dict, Tuple, Optional, Union
from dataclasses import dataclass
from collections import Counter


@dataclass
class ImageDimensions:
    """Represents image dimensions."""
    width: int
    height: int
    
    @property
    def size(self) -> int:
        """Total number of pixels in the image."""
        return self.width * self.height
    
    def get_position(self, index: int) -> Tuple[int, int]:
        """Convert linear index to (row, col) position."""
        return divmod(index, self.width)
    
    def get_index(self, row: int, col: int) -> int:
        """Convert (row, col) position to linear index."""
        return row * self.width + col
    
    def is_valid_position(self, row: int, col: int) -> bool:
        """Check if position is within image bounds."""
        return 0 <= row < self.height and 0 <= col < self.width


class SpaceImageLayer:
    """Represents a single layer of the space image."""
    
    def __init__(self, data: str, dimensions: ImageDimensions):
        """
        Initialize layer with raw data and dimensions.
        
        Args:
            data: String of pixel data
            dimensions: Image dimensions
        """
        if len(data) != dimensions.size:
            raise ValueError(f"Data length {len(data)} doesn't match dimensions {dimensions.size}")
        
        self.data = data
        self.dimensions = dimensions
        self._pixel_counts: Optional[Dict[str, int]] = None
    
    def get_pixel(self, row: int, col: int) -> str:
        """
        Get pixel value at specific position.
        
        Args:
            row: Row index
            col: Column index
            
        Returns:
            Pixel value as string
        """
        if not self.dimensions.is_valid_position(row, col):
            raise IndexError(f"Position ({row}, {col}) out of bounds")
        
        index = self.dimensions.get_index(row, col)
        return self.data[index]
    
    def get_pixel_counts(self) -> Dict[str, int]:
        """Get count of each pixel value in the layer."""
        if self._pixel_counts is None:
            self._pixel_counts = Counter(self.data)
        return self._pixel_counts.copy()
    
    def count_pixel(self, pixel_value: str) -> int:
        """Count occurrences of a specific pixel value."""
        return self.get_pixel_counts().get(pixel_value, 0)
    
    def get_checksum(self) -> int:
        """Calculate layer checksum (1s * 2s)."""
        counts = self.get_pixel_counts()
        return counts.get('1', 0) * counts.get('2', 0)
    
    def to_grid(self) -> List[List[str]]:
        """Convert layer to 2D grid representation."""
        grid = []
        for row in range(self.dimensions.height):
            grid_row = []
            for col in range(self.dimensions.width):
                grid_row.append(self.get_pixel(row, col))
            grid.append(grid_row)
        return grid
    
    def render(self, pixel_map: Dict[str, str] = None) -> str:
        """
        Render layer as a visual string.
        
        Args:
            pixel_map: Optional mapping of pixel values to display characters
            
        Returns:
            Multi-line string representation of the layer
        """
        if pixel_map is None:
            pixel_map = {'0': ' ', '1': '█', '2': '░'}
        
        lines = []
        for row in range(self.dimensions.height):
            line = ""
            for col in range(self.dimensions.width):
                pixel = self.get_pixel(row, col)
                line += pixel_map.get(pixel, pixel)
            lines.append(line)
        
        return '\n'.join(lines)
    
    def parse_letters_from_art(self) -> str:
        """
        Parse ASCII art into letters using shared utility.
        
        Returns:
            String of recognized letters
        """
        from utils import parse_ascii_letters
        art = self.render()
        return parse_ascii_letters(art, 'thick')


class SpaceImage:
    """Represents a complete space image with multiple layers."""
    
    def __init__(self, image_data: str, dimensions: ImageDimensions):
        """
        Initialize image from raw data.
        
        Args:
            image_data: Complete image data string
            dimensions: Image dimensions
        """
        self.dimensions = dimensions
        self.raw_data = image_data
        self.layers: List[SpaceImageLayer] = []
        self._parse_layers()
    
    def _parse_layers(self) -> None:
        """Parse raw data into individual layers."""
        layer_size = self.dimensions.size
        
        if len(self.raw_data) % layer_size != 0:
            raise ValueError(f"Image data length {len(self.raw_data)} is not divisible by layer size {layer_size}")
        
        num_layers = len(self.raw_data) // layer_size
        
        for i in range(num_layers):
            start_idx = i * layer_size
            end_idx = start_idx + layer_size
            layer_data = self.raw_data[start_idx:end_idx]
            self.layers.append(SpaceImageLayer(layer_data, self.dimensions))
    
    def get_layer(self, index: int) -> SpaceImageLayer:
        """Get specific layer by index."""
        if not 0 <= index < len(self.layers):
            raise IndexError(f"Layer index {index} out of range")
        return self.layers[index]
    
    def find_layer_with_fewest_zeros(self) -> Tuple[int, SpaceImageLayer]:
        """
        Find the layer with the fewest '0' pixels.
        
        Returns:
            Tuple of (layer_index, layer)
        """
        min_zeros = float('inf')
        best_layer_idx = 0
        
        for idx, layer in enumerate(self.layers):
            zero_count = layer.count_pixel('0')
            if zero_count < min_zeros:
                min_zeros = zero_count
                best_layer_idx = idx
        
        return best_layer_idx, self.layers[best_layer_idx]
    
    def compose_final_image(self) -> SpaceImageLayer:
        """
        Compose final image by applying transparency rules.
        
        Pixel values:
        - 0: black
        - 1: white  
        - 2: transparent
        
        Returns:
            Final composed layer
        """
        final_pixels = ['2'] * self.dimensions.size  # Start with all transparent
        
        # Process layers from front to back
        for layer in self.layers:
            for i, pixel in enumerate(layer.data):
                if final_pixels[i] == '2':  # If current pixel is transparent
                    final_pixels[i] = pixel
        
        final_data = ''.join(final_pixels)
        return SpaceImageLayer(final_data, self.dimensions)
    
    def analyze_layers(self) -> Dict:
        """
        Analyze all layers and provide statistics.
        
        Returns:
            Dictionary with layer analysis
        """
        layer_stats = []
        total_pixels = self.dimensions.size * len(self.layers)
        
        for idx, layer in enumerate(self.layers):
            counts = layer.get_pixel_counts()
            stats = {
                'layer_index': idx,
                'pixel_counts': counts,
                'checksum': layer.get_checksum(),
                'zero_percentage': (counts.get('0', 0) / self.dimensions.size) * 100
            }
            layer_stats.append(stats)
        
        # Find extremes
        min_zeros_idx, min_zeros_layer = self.find_layer_with_fewest_zeros()
        max_checksum = max(stats['checksum'] for stats in layer_stats)
        
        analysis = {
            'total_layers': len(self.layers),
            'dimensions': self.dimensions,
            'total_pixels': total_pixels,
            'layer_stats': layer_stats,
            'min_zeros_layer': min_zeros_idx,
            'min_zeros_checksum': min_zeros_layer.get_checksum(),
            'max_checksum': max_checksum
        }
        
        return analysis


class SpaceImageDecoder:
    """Decodes and analyzes space image format data."""
    
    def __init__(self, width: int = 25, height: int = 6):
        """
        Initialize decoder with default dimensions.
        
        Args:
            width: Image width in pixels
            height: Image height in pixels
        """
        self.dimensions = ImageDimensions(width, height)
    
    def decode_image(self, image_data: str) -> SpaceImage:
        """
        Decode raw image data into SpaceImage object.
        
        Args:
            image_data: Raw image data string
            
        Returns:
            Decoded SpaceImage object
        """
        return SpaceImage(image_data.strip(), self.dimensions)
    
    def find_corruption_checksum(self, image_data: str) -> int:
        """
        Find corruption checksum from the layer with fewest zeros.
        
        Args:
            image_data: Raw image data string
            
        Returns:
            Corruption checksum value
        """
        image = self.decode_image(image_data)
        _, layer = image.find_layer_with_fewest_zeros()
        return layer.get_checksum()
    
    def decode_password(self, image_data: str) -> str:
        """
        Decode the password from the image.
        
        Args:
            image_data: Raw image data string
            
        Returns:
            Rendered final image as string
        """
        image = self.decode_image(image_data)
        final_layer = image.compose_final_image()
        return final_layer.render()
    
    def decode_password_letters(self, image_data: str) -> str:
        """
        Decode the password letters from the image.
        
        Args:
            image_data: Raw image data string
            
        Returns:
            Password as recognized letters
        """
        image = self.decode_image(image_data)
        final_layer = image.compose_final_image()
        return final_layer.parse_letters_from_art()
    
    def analyze_image_quality(self, image_data: str) -> Dict:
        """
        Perform comprehensive image quality analysis.
        
        Args:
            image_data: Raw image data string
            
        Returns:
            Dictionary with quality analysis
        """
        image = self.decode_image(image_data)
        analysis = image.analyze_layers()
        
        # Additional quality metrics
        final_image = image.compose_final_image()
        final_counts = final_image.get_pixel_counts()
        
        quality_analysis = {
            'basic_analysis': analysis,
            'final_image_stats': {
                'pixel_counts': final_counts,
                'transparency_resolved': final_counts.get('2', 0) == 0,
                'black_white_ratio': final_counts.get('0', 0) / max(final_counts.get('1', 1), 1)
            }
        }
        
        return quality_analysis


class Day8Solution(AdventSolution):
    """Enhanced solution for Day 8: Space Image Format."""
    
    def __init__(self):
        super().__init__(year=2019, day=8, title="Space Image Format")
        self.decoder = SpaceImageDecoder()
    
    def part1(self, input_data: str) -> int:
        """
        Find the corruption checksum.
        
        Args:
            input_data: Raw image data
            
        Returns:
            Corruption checksum (1s * 2s from layer with fewest 0s)
        """
        return self.decoder.find_corruption_checksum(input_data)
    
    def part2(self, input_data: str) -> str:
        """
        Decode the password message.
        
        Args:
            input_data: Raw image data
            
        Returns:
            Password letters as string
        """
        return self.decoder.decode_password_letters(input_data)
    
    def analyze_space_image(self, input_data: str) -> None:
        """
        Provide comprehensive analysis of the space image.
        
        Args:
            input_data: Raw image data
        """
        image = self.decoder.decode_image(input_data)
        quality_analysis = self.decoder.analyze_image_quality(input_data)
        
        print("=== Space Image Format Analysis ===")
        print(f"Image dimensions: {image.dimensions.width}x{image.dimensions.height}")
        print(f"Total layers: {len(image.layers)}")
        print(f"Pixels per layer: {image.dimensions.size}")
        print(f"Total pixels: {len(input_data.strip())}")
        
        # Layer analysis
        analysis = quality_analysis['basic_analysis']
        print(f"\nCorruption Check:")
        print(f"Layer with fewest zeros: {analysis['min_zeros_layer']}")
        print(f"Corruption checksum: {analysis['min_zeros_checksum']}")
        
        # Show first few layers
        print(f"\nFirst 3 layers analysis:")
        for i, stats in enumerate(analysis['layer_stats'][:3]):
            counts = stats['pixel_counts']
            print(f"  Layer {i}: 0s={counts.get('0', 0)}, 1s={counts.get('1', 0)}, "
                  f"2s={counts.get('2', 0)}, checksum={stats['checksum']}")
        
        # Final image analysis
        final_stats = quality_analysis['final_image_stats']
        print(f"\nFinal Image Analysis:")
        final_counts = final_stats['pixel_counts']
        print(f"Final pixel counts: 0s={final_counts.get('0', 0)}, 1s={final_counts.get('1', 0)}, "
              f"2s={final_counts.get('2', 0)}")
        print(f"All transparency resolved: {final_stats['transparency_resolved']}")
        print(f"Black/White ratio: {final_stats['black_white_ratio']:.2f}")
        
        # Render the final image
        final_image = image.compose_final_image()
        print(f"\nDecoded Password:")
        print(final_image.render())
        
        # Alternative rendering for better visibility
        print(f"\nAlternative rendering (0=' ', 1='#'):")
        alt_render = final_image.render({'0': ' ', '1': '#', '2': '?'})
        print(alt_render)
        
        # Part results
        print(f"\n=== Final Results ===")
        print(f"Part 1 - Corruption checksum: {self.part1(input_data)}")
        print(f"Part 2 - Password decoded (see above)")


# Legacy functions for test runner compatibility
def part1(input_data: str = None) -> int:
    """Legacy function for test runner compatibility."""
    if input_data is None:
        # Auto-discover input file
        import os
        day = 8
        possible_files = [
            f"day{day}_input.txt",
            f"day{day}input.txt", 
            f"input{day}.txt",
            "input.txt"
        ]
        
        input_file = None
        for filename in possible_files:
            if os.path.exists(filename):
                input_file = filename
                break
        
        if input_file is None:
            raise FileNotFoundError(f"No input file found for day {day}")
        
        with open(input_file, 'r') as f:
            input_data = f.read()
    
    solution = Day8Solution()
    return solution.part1(input_data)


def part2(input_data: str = None) -> str:
    """Legacy function for test runner compatibility."""
    if input_data is None:
        # Auto-discover input file
        import os
        day = 8
        possible_files = [
            f"day{day}_input.txt",
            f"day{day}input.txt", 
            f"input{day}.txt",
            "input.txt"
        ]
        
        input_file = None
        for filename in possible_files:
            if os.path.exists(filename):
                input_file = filename
                break
        
        if input_file is None:
            raise FileNotFoundError(f"No input file found for day {day}")
        
        with open(input_file, 'r') as f:
            input_data = f.read()
    
    solution = Day8Solution()
    return solution.part2(input_data)


def main():
    """Main function to run the enhanced solution."""
    solution = Day8Solution()
    
    # If run with analyze flag, show comprehensive analysis
    if len(sys.argv) > 1 and sys.argv[1] == 'analyze':
        input_data = solution._load_input()
        solution.analyze_space_image(input_data)
    else:
        solution.main()


if __name__ == "__main__":
    main()