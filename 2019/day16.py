#!/usr/bin/env python3
"""
Advent of Code 2019 Day 16: Flawed Frequency Transmission

Enhanced solution using the AdventSolution base class for Fast Fourier Transform
signal processing with mathematical optimizations for large datasets.
"""

import sys
from pathlib import Path
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
import time

# Add utils to path for enhanced base class
sys.path.append(str(Path(__file__).parent.parent))
from utils import AdventSolution

@dataclass
class FFTPattern:
    """Represents the base pattern for FFT calculations."""
    base_pattern: List[int]
    
    def get_pattern_value(self, position: int, index: int) -> int:
        """Get the pattern value for a specific position and index."""
        pattern_length = len(self.base_pattern) * (position + 1)
        pattern_index = ((index + 1) % pattern_length) // (position + 1)
        return self.base_pattern[pattern_index]

class FFTProcessor:
    """
    Domain class for Fast Fourier Transform signal processing.
    Implements optimized algorithms for both standard and large-scale FFT operations.
    """
    
    def __init__(self, base_pattern: List[int] = None):
        if base_pattern is None:
            base_pattern = [0, 1, 0, -1]
        self.pattern = FFTPattern(base_pattern)
        self.signal_cache: Dict[str, List[int]] = {}
    
    def apply_fft_phase_standard(self, signal: List[int]) -> List[int]:
        """
        Apply a single FFT phase using the standard algorithm.
        
        Args:
            signal: Input signal as list of digits
            
        Returns:
            Transformed signal after one phase
        """
        n = len(signal)
        result = [0] * n
        
        for i in range(n):
            total = 0
            
            # Use the pattern to calculate the sum efficiently
            # Pattern for position i: [0]*i + [1]*i + [0]*i + [-1]*i, repeated
            pos = i
            sign = 1
            
            while pos < n:
                # Add/subtract chunks of size (i+1)
                chunk_end = min(pos + i + 1, n)
                for j in range(pos, chunk_end):
                    total += signal[j] * sign
                
                # Skip the next chunk (zeros)
                pos = chunk_end + i + 1
                # Flip sign for next iteration
                sign *= -1
            
            result[i] = abs(total) % 10
        
        return result
    
    def apply_fft_optimized_large_offset(self, signal: List[int], offset: int, phases: int) -> List[int]:
        """
        Apply FFT for large signals with large offset optimization.
        
        When offset is large (> len(signal)/2), the pattern becomes very simple.
        Each position is just the cumulative sum from that position to the end.
        
        Args:
            signal: Input signal
            offset: Starting offset in the original signal
            phases: Number of phases to apply
            
        Returns:
            Transformed signal after all phases
        """
        # Work with the portion from offset onwards
        working_signal = signal[offset:]
        
        for phase in range(phases):
            # For large offsets, each position is the sum from that position to the end
            cumsum = 0
            new_signal = [0] * len(working_signal)
            
            # Calculate from right to left using cumulative sum
            for i in range(len(working_signal) - 1, -1, -1):
                cumsum += working_signal[i]
                new_signal[i] = cumsum % 10
            
            working_signal = new_signal
        
        return working_signal
    
    def process_signal_multiple_phases(self, signal: List[int], phases: int) -> List[int]:
        """
        Process signal through multiple FFT phases.
        
        Args:
            signal: Input signal
            phases: Number of phases to apply
            
        Returns:
            Final signal after all phases
        """
        current_signal = signal.copy()
        
        for phase in range(phases):
            current_signal = self.apply_fft_phase_standard(current_signal)
        
        return current_signal
    
    def extract_message(self, signal: List[int], start_pos: int = 0, length: int = 8) -> str:
        """
        Extract a message from the signal starting at the given position.
        
        Args:
            signal: Processed signal
            start_pos: Starting position to extract from
            length: Length of message to extract
            
        Returns:
            Message as string of digits
        """
        if start_pos + length > len(signal):
            raise ValueError(f"Cannot extract {length} digits starting at position {start_pos}")
        
        return ''.join(str(signal[i]) for i in range(start_pos, start_pos + length))
    
    def calculate_performance_metrics(self, signal_length: int, phases: int) -> Dict[str, Any]:
        """
        Calculate performance metrics for FFT processing.
        
        Args:
            signal_length: Length of the input signal
            phases: Number of phases
            
        Returns:
            Dictionary with performance metrics
        """
        # Theoretical complexity analysis
        standard_operations = signal_length ** 2 * phases
        
        return {
            'signal_length': signal_length,
            'phases': phases,
            'standard_complexity': standard_operations,
            'memory_usage_mb': (signal_length * 4) / (1024 * 1024),  # Rough estimate
            'recommended_algorithm': 'optimized' if signal_length > 10000 else 'standard'
        }

class Day16Solution(AdventSolution):
    """Enhanced solution for Advent of Code 2019 Day 16: Flawed Frequency Transmission."""
    
    def __init__(self):
        super().__init__(2019, 16, "Flawed Frequency Transmission")
        self.processor = FFTProcessor()
        self._input_signal: Optional[List[int]] = None
    
    def _parse_input(self, input_data: str) -> List[int]:
        """Parse input data into a list of digits."""
        signal_str = input_data.strip()
        if not signal_str:
            # Fallback to embedded signal for compatibility
            signal_str = "59796737047664322543488505082147966997246465580805791578417462788780740484409625674676660947541571448910007002821454068945653911486140823168233915285229075374000888029977800341663586046622003620770361738270014246730936046471831804308263177331723460787712423587453725840042234550299991238029307205348958992794024402253747340630378944672300874691478631846617861255015770298699407254311889484508545861264449878984624330324228278057377313029802505376260196904213746281830214352337622013473019245081834854781277565706545720492282616488950731291974328672252657631353765496979142830459889682475397686651923318015627694176893643969864689257620026916615305397"
        
        return [int(d) for d in signal_str]
    
    def part1(self, input_data: str) -> str:
        """
        Solve part 1: Apply FFT for 100 phases and return first 8 digits.
        
        Args:
            input_data: Raw input containing the signal
            
        Returns:
            First 8 digits of the signal after 100 phases
        """
        self._input_signal = self._parse_input(input_data)
        
        # Apply 100 phases of FFT
        processed_signal = self.processor.process_signal_multiple_phases(
            self._input_signal, 
            phases=100
        )
        
        # Return first 8 digits
        return self.processor.extract_message(processed_signal, 0, 8)
    
    def part2(self, input_data: str) -> str:
        """
        Solve part 2: Process signal repeated 10000 times with offset optimization.
        
        Args:
            input_data: Raw input containing the signal
            
        Returns:
            8 digits from the real message after offset processing
        """
        if self._input_signal is None:
            self._input_signal = self._parse_input(input_data)
        
        base_signal = self._input_signal
        
        # Get the offset from the first 7 digits
        offset = int(''.join(str(d) for d in base_signal[:7]))
        
        # Create the full signal (input repeated 10000 times)
        full_length = len(base_signal) * 10000
        
        # Key optimization: if offset > full_length/2, use the simplified pattern
        if offset > full_length // 2:
            # Generate only the part we need (from offset to end)
            repeats_before_offset = offset // len(base_signal)
            offset_in_repeat = offset % len(base_signal)
            
            # Build signal from offset onwards
            signal_from_offset = []
            
            # Add remaining part of the first repeat that contains the offset
            if offset_in_repeat > 0:
                signal_from_offset.extend(base_signal[offset_in_repeat:])
            
            # Add complete repeats after the offset
            remaining_repeats = 10000 - repeats_before_offset - (1 if offset_in_repeat > 0 else 0)
            for _ in range(remaining_repeats):
                signal_from_offset.extend(base_signal)
            
            # Apply optimized FFT for large offset
            result_signal = self.processor.apply_fft_optimized_large_offset(
                signal_from_offset, 0, 100
            )
            
            return self.processor.extract_message(result_signal, 0, 8)
        else:
            # For small offsets, we need the full algorithm (rare for AoC inputs)
            full_signal = base_signal * 10000
            
            processed_signal = self.processor.process_signal_multiple_phases(
                full_signal, 
                phases=100
            )
            
            return self.processor.extract_message(processed_signal, offset, 8)
    
    def analyze_signal(self) -> Dict[str, Any]:
        """
        Provide comprehensive analysis of the signal processing.
        
        Returns:
            Dictionary with detailed signal analysis
        """
        if self._input_signal is None:
            return {"error": "Signal not yet processed"}
        
        base_signal = self._input_signal
        offset = int(''.join(str(d) for d in base_signal[:7]))
        
        analysis = {
            'base_signal_length': len(base_signal),
            'offset': offset,
            'full_signal_length': len(base_signal) * 10000,
            'offset_ratio': offset / (len(base_signal) * 10000),
            'uses_optimization': offset > (len(base_signal) * 10000) // 2,
            'first_8_digits': ''.join(str(d) for d in base_signal[:8]),
            'last_8_digits': ''.join(str(d) for d in base_signal[-8:]),
        }
        
        # Add performance metrics
        performance = self.processor.calculate_performance_metrics(
            len(base_signal), 100
        )
        analysis['performance'] = performance
        
        # Add pattern analysis for first few positions
        pattern_analysis = {}
        for pos in range(min(5, len(base_signal))):
            pattern_analysis[f'position_{pos}'] = {
                'pattern_repeat_length': (pos + 1) * 4,
                'effective_elements': sum(1 for i in range(len(base_signal)) 
                                        if self.processor.pattern.get_pattern_value(pos, i) != 0)
            }
        
        analysis['pattern_analysis'] = pattern_analysis
        
        return analysis
    
    def validate(self, expected_part1: Any = None, expected_part2: Any = None) -> bool:
        """Validate the solution with known test cases."""
        print("Day 16 validation: Testing with known examples...")
        
        # Test case 1: Simple example
        test_input1 = "12345678"
        expected_after_1_phase = "48226158"
        expected_after_2_phases = "34040438"
        
        try:
            signal = [int(d) for d in test_input1]
            
            # Test one phase
            result_1_phase = self.processor.apply_fft_phase_standard(signal)
            result_1_str = ''.join(str(d) for d in result_1_phase)
            
            if result_1_str == expected_after_1_phase:
                print(f"✅ Phase 1 test: {result_1_str}")
            else:
                print(f"❌ Phase 1 test: expected {expected_after_1_phase}, got {result_1_str}")
                return False
            
            # Test two phases
            result_2_phases = self.processor.apply_fft_phase_standard(result_1_phase)
            result_2_str = ''.join(str(d) for d in result_2_phases)
            
            if result_2_str == expected_after_2_phases:
                print(f"✅ Phase 2 test: {result_2_str}")
            else:
                print(f"❌ Phase 2 test: expected {expected_after_2_phases}, got {result_2_str}")
                return False
            
            # Test larger example
            test_input2 = "80871224585914546619083218645595"
            signal2 = [int(d) for d in test_input2]
            result_100_phases = self.processor.process_signal_multiple_phases(signal2, 100)
            first_8 = self.processor.extract_message(result_100_phases, 0, 8)
            expected_first_8 = "24176176"
            
            if first_8 == expected_first_8:
                print(f"✅ 100 phases test: {first_8}")
            else:
                print(f"❌ 100 phases test: expected {expected_first_8}, got {first_8}")
                return False
            
            print("✅ All validation tests passed!")
            return True
            
        except Exception as e:
            print(f"❌ Validation failed with error: {e}")
            return False

def main():
    """Main execution function."""
    solution = Day16Solution()
    solution.main()

if __name__ == "__main__":
    main()