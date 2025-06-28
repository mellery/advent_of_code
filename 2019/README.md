# Advent of Code 2019

This directory contains solutions for Advent of Code 2019, a year notable for its **Intcode computer** theme that ran throughout multiple challenges.

## Year Overview

2019 introduced the Intcode computer, a virtual machine that processes comma-separated integer programs. The Intcode challenges progressively added complexity:

- **Day 2**: Basic ADD and MULTIPLY operations
- **Day 5**: INPUT/OUTPUT and conditional jumps  
- **Day 7**: Amplifier chains requiring concurrent execution
- **Day 9**: Relative addressing mode and extended memory
- **And more**: The Intcode computer appeared in many subsequent days

## Key Components

### Intcode Computer (`intcode.py`)
A complete threaded implementation of the Intcode virtual machine supporting:
- All opcodes (ADD, MULTIPLY, INPUT, OUTPUT, JUMP, COMPARE, RELATIVE BASE, HALT)
- All parameter modes (position, immediate, relative)
- Extended memory allocation
- Concurrent execution via threading
- Input/output queues for inter-program communication

### Test Suite (`intcode_test.py`)
Assertion-based tests validating multiple solutions against expected outputs.

## Solutions

| Day | Status | Description |
|-----|--------|-------------|
| 1   | ✅ | Fuel calculations |
| 2   | ✅ | Intcode computer introduction |
| 3   | ✅ | Wire intersection |
| 4   | ✅ | Password validation |
| 5   | ✅ | Intcode improvements |
| 6   | ✅ | Orbital mechanics |
| 7   | ✅ | Amplifier circuits |
| 8   | ✅ | Image processing |
| 9   | ✅ | Intcode relative mode |
| 10  | ✅ | Asteroid monitoring |
| 11  | ✅ | Intcode robot painting |
| 12  | ✅ | N-body simulation |
| 13  | ✅ | Intcode arcade game |
| 14  | ✅ | Chemical reactions |
| 15  | ✅ | Intcode maze exploration |
| 16  | ✅ | FFT signal processing |
| 17  | ✅ | Intcode ASCII computer |
| 18  | ✅ | Maze key collection |
| 19  | ✅ | Intcode tractor beam |
| 20  | ✅ | Recursive maze |
| 21+ | ❌ | Not yet implemented |

## Running Solutions

```bash
# Individual solutions
python advent1.py
python advent2.py

# Run Intcode tests
python intcode_test.py

# Using the enhanced template (for new solutions)
python -m day_template --day 1 --input day1_input.txt
```

## Notes

- Most solutions follow the `adventN.py` naming convention
- Input files use various patterns (`dayN_input.txt`, `inputN.txt`)
- The Intcode computer is heavily reused across multiple days
- Some solutions include example/test input files for validation