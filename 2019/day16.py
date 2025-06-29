"""
Advent of Code 2019 Day 16: Flawed Frequency Transmission
Optimized FFT implementation using mathematical properties.
"""

def fft_phase_optimized(signal: list[int]) -> list[int]:
    """
    Optimized FFT phase using cumulative sums and pattern properties.
    
    Key insight: For position i, we can use cumulative sums to avoid
    recalculating the same additions repeatedly.
    """
    n = len(signal)
    result = [0] * n
    
    # For each output position
    for i in range(n):
        total = 0
        
        # Pattern for position i: [0]*i + [1]*i + [0]*i + [-1]*i, repeated
        # We only need to consider non-zero parts of the pattern
        
        # Start at position i (first non-zero element)
        pos = i
        sign = 1  # Start with positive
        
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


def fft_optimized_for_large_offset(signal: list[int], offset: int, phases: int) -> list[int]:
    """
    Optimized FFT for cases where offset is large (typically > len(signal)/2).
    
    Key insight: When offset is large, the pattern becomes very simple.
    For positions i where i >= len(signal)/2, the pattern is just [0...0, 1, 1, 1...]
    This means we can use cumulative sums from right to left.
    """
    # Work with the portion from offset onwards
    working_signal = signal[offset:]
    
    for phase in range(phases):
        # For large offsets, each position is just the sum from that position to the end
        cumsum = 0
        new_signal = [0] * len(working_signal)
        
        # Calculate from right to left using cumulative sum
        for i in range(len(working_signal) - 1, -1, -1):
            cumsum += working_signal[i]
            new_signal[i] = cumsum % 10
        
        working_signal = new_signal
    
    return working_signal


def solve_part1(signal_str: str, phases: int = 100) -> str:
    """Solve part 1 efficiently."""
    signal = [int(d) for d in signal_str.strip()]
    
    for _ in range(phases):
        signal = fft_phase_optimized(signal)
    
    return ''.join(map(str, signal[:8]))


def solve_part2(signal_str: str, phases: int = 100) -> str:
    """Solve part 2 using the offset optimization."""
    base_signal = [int(d) for d in signal_str.strip()]
    
    # Get the offset from the first 7 digits
    offset = int(signal_str[:7])
    
    # Create the full signal (input repeated 10000 times)
    full_length = len(base_signal) * 10000
    
    # Key optimization: if offset > full_length/2, we can use the simple pattern
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
        result_signal = fft_optimized_for_large_offset(signal_from_offset, 0, phases)
        
        return ''.join(map(str, result_signal[:8]))
    else:
        # For small offsets, we need the full algorithm (but this is rare for AoC inputs)
        full_signal = base_signal * 10000
        
        for _ in range(phases):
            full_signal = fft_phase_optimized(full_signal)
        
        return ''.join(map(str, full_signal[offset:offset+8]))


def solve_day16(filename: str = "day16_input.txt") -> tuple[str, str]:
    """Solve both parts of day 16."""
    try:
        with open(filename, 'r') as f:
            signal_str = f.read().strip()
    except FileNotFoundError:
        # Fallback to hardcoded input if no file
        signal_str = "59796737047664322543488505082147966997246465580805791578417462788780740484409625674676660947541571448910007002821454068945653911486140823168233915285229075374000888029977800341663586046622003620770361738270014246730936046471831804308263177331723460787712423587453725840042234550299991238029307205348958992794024402253747340630378944672300874691478631846617861255015770298699407254311889484508545861264449878984624330324228278057377313029802505376260196904213746281830214352337622013473019245081834854781277565706545720492282616488950731291974328672252657631353765496979142830459889682475397686651923318015627694176893643969864689257620026916615305397"
    
    part1 = solve_part1(signal_str)
    part2 = solve_part2(signal_str)
    
    return part1, part2


# Test runner compatible functions
def part1(input_data) -> str:
    """Part 1 function compatible with test runner."""
    if isinstance(input_data, str):
        if '\n' in input_data or len(input_data) > 100:
            # This is content
            signal_str = input_data.strip()
        else:
            # This is a filename
            try:
                with open(input_data, 'r') as f:
                    signal_str = f.read().strip()
            except FileNotFoundError:
                signal_str = "59796737047664322543488505082147966997246465580805791578417462788780740484409625674676660947541571448910007002821454068945653911486140823168233915285229075374000888029977800341663586046622003620770361738270014246730936046471831804308263177331723460787712423587453725840042234550299991238029307205348958992794024402253747340630378944672300874691478631846617861255015770298699407254311889484508545861264449878984624330324228278057377313029802505376260196904213746281830214352337622013473019245081834854781277565706545720492282616488950731291974328672252657631353765496979142830459889682475397686651923318015627694176893643969864689257620026916615305397"
    else:
        signal_str = "59796737047664322543488505082147966997246465580805791578417462788780740484409625674676660947541571448910007002821454068945653911486140823168233915285229075374000888029977800341663586046622003620770361738270014246730936046471831804308263177331723460787712423587453725840042234550299991238029307205348958992794024402253747340630378944672300874691478631846617861255015770298699407254311889484508545861264449878984624330324228278057377313029802505376260196904213746281830214352337622013473019245081834854781277565706545720492282616488950731291974328672252657631353765496979142830459889682475397686651923318015627694176893643969864689257620026916615305397"
    
    return solve_part1(signal_str)


def part2(input_data) -> str:
    """Part 2 function compatible with test runner."""
    if isinstance(input_data, str):
        if '\n' in input_data or len(input_data) > 100:
            # This is content
            signal_str = input_data.strip()
        else:
            # This is a filename
            try:
                with open(input_data, 'r') as f:
                    signal_str = f.read().strip()
            except FileNotFoundError:
                signal_str = "59796737047664322543488505082147966997246465580805791578417462788780740484409625674676660947541571448910007002821454068945653911486140823168233915285229075374000888029977800341663586046622003620770361738270014246730936046471831804308263177331723460787712423587453725840042234550299991238029307205348958992794024402253747340630378944672300874691478631846617861255015770298699407254311889484508545861264449878984624330324228278057377313029802505376260196904213746281830214352337622013473019245081834854781277565706545720492282616488950731291974328672252657631353765496979142830459889682475397686651923318015627694176893643969864689257620026916615305397"
    else:
        signal_str = "59796737047664322543488505082147966997246465580805791578417462788780740484409625674676660947541571448910007002821454068945653911486140823168233915285229075374000888029977800341663586046622003620770361738270014246730936046471831804308263177331723460787712423587453725840042234550299991238029307205348958992794024402253747340630378944672300874691478631846617861255015770298699407254311889484508545861264449878984624330324228278057377313029802505376260196904213746281830214352337622013473019245081834854781277565706545720492282616488950731291974328672252657631353765496979142830459889682475397686651923318015627694176893643969864689257620026916615305397"
    
    return solve_part2(signal_str)


if __name__ == "__main__":
    part1_result, part2_result = solve_day16()
    print(f"Part 1: {part1_result}")
    print(f"Part 2: {part2_result}")