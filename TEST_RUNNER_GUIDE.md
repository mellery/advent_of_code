# Enhanced Test Runner Guide

The enhanced `test_runner.py` now provides comprehensive validation of Advent of Code solutions against expected answers stored in `expected_answers.json`.

## Key Features

### 🎯 **Answer Validation**
- ✅ **PASS** - Answer matches expected result
- ❌ **FAIL** - Answer doesn't match expected result  
- ❓ **UNKNOWN** - No expected answer stored
- ❗ **ERROR** - Validation error occurred

### 📊 **Comprehensive Reporting**
- **Execution Summary** - Success/failure rates and timing
- **Validation Summary** - Answer accuracy statistics
- **Detailed Table** - Grid view with validation status
- **Missing Answers** - List of solutions needing expected answers
- **Incorrect Answers** - List of validation failures

### 🔧 **Advanced Features**
- **Auto-update answers** - Capture results from successful runs
- **Filtering options** - Run only unknown/failing solutions
- **Timeout control** - Prevent hanging solutions
- **JSON storage** - Version-controllable expected answers

## Usage Examples

### Basic Usage
```bash
# Run all solutions with validation
python test_runner.py

# Run specific year/day
python test_runner.py --year 2019 --day 19
```

### Answer Management
```bash
# Update expected answers for solutions without them
python test_runner.py --update-answers --only-unknown

# Update all answers (including existing ones)
python test_runner.py --update-answers

# Run only solutions that don't have expected answers
python test_runner.py --only-unknown
```

### Filtering and Control
```bash
# Set timeout per solution (default: 30s)
python test_runner.py --timeout 60

# Run only solutions with expected answers (to check for regressions)
python test_runner.py --only-failing
```

### Helper Script
```bash
# Populate answers for all solutions
python populate_answers.py

# Populate answers for specific year
python populate_answers.py --year 2019

# See what would be updated without changes
python populate_answers.py --dry-run
```

## Expected Answers Format

The `expected_answers.json` file uses this structure:

```json
{
  "2019": {
    "19": {
      "part1": 231,
      "part2": 8771184
    }
  }
}
```

- Use `null` for unknown answers
- Numbers, strings, and other JSON types are supported
- File is automatically sorted and formatted

## Validation Logic

1. **Exact Match** - `actual_result == expected_result`
2. **String Match** - `str(actual_result) == str(expected_result)`
3. **Type Conversion** - Handles different numeric types gracefully

## Output Example

```
Running 2019 Day 19...
2019 Day 19: PASS
  Part 1: 231 ✓
  Part 2: 8771184 ✓  
  Time: 2.888s

============================================================
VALIDATION SUMMARY
============================================================
Total parts validated: 2
✓ Correct answers: 2
✗ Incorrect answers: 0
? Unknown answers: 0
! Validation errors: 0
Validation accuracy: 100.0%
```

## Integration with Development Workflow

### 1. **Initial Setup**
```bash
# Populate baseline answers
python populate_answers.py --year 2019
```

### 2. **Development**
```bash
# Test specific solution you're working on
python test_runner.py --year 2019 --day 19

# Update answer after fixing
python test_runner.py --year 2019 --day 19 --update-answers
```

### 3. **Regression Testing**
```bash
# Run all solutions to check for regressions
python test_runner.py

# Focus on solutions with known answers
python test_runner.py --only-failing
```

### 4. **Performance Monitoring**
```bash
# Check if any solutions are taking too long
python test_runner.py --timeout 10
```

## Benefits

### ✅ **Quality Assurance**
- Prevents regression when refactoring
- Validates optimization efforts don't change results
- Catches errors early in development

### 📈 **Progress Tracking**
- Visual indication of solution completeness
- Easy identification of missing answers
- Performance benchmarking over time

### 🚀 **Productivity**
- Automated validation saves manual checking
- Batch operations for efficiency
- Clear reporting for debugging

### 🔄 **Maintainability**
- Version-controlled expected answers
- Reproducible test results
- Easy integration with CI/CD

## Command Reference

| Command | Description |
|---------|-------------|
| `--year YEAR` | Filter by year |
| `--day DAY` | Filter by day |
| `--update-answers` | Update expected answers from results |
| `--only-unknown` | Only run solutions without expected answers |
| `--only-failing` | Only run solutions with expected answers |
| `--timeout SECONDS` | Set timeout per solution (default: 30) |
| `--verbose` | Enable verbose output |

The enhanced test runner transforms the development experience from manual verification to automated validation, ensuring solution quality and enabling confident refactoring.