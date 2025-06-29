"""
Expected answers for Advent of Code solutions.

This module stores the correct answers for each day and part,
allowing test_runner.py to validate solutions automatically.

Format: EXPECTED_ANSWERS[year][day][part] = expected_result
Use None for unknown answers.
"""

from typing import Dict, Any, Optional, Union

# Type alias for clarity
Answer = Optional[Union[int, str]]
PartAnswers = Dict[str, Answer]
DayAnswers = Dict[int, PartAnswers] 
YearAnswers = Dict[str, DayAnswers]

EXPECTED_ANSWERS: YearAnswers = {
    "2015": {
        1: {"part1": None, "part2": None},
        2: {"part1": None, "part2": None},
    },
    
    "2017": {
        1: {"part1": None, "part2": None},
    },
    
    "2019": {
        1: {"part1": None, "part2": None},
        2: {"part1": None, "part2": None},
        5: {"part1": None, "part2": None},
        7: {"part1": None, "part2": None},
        9: {"part1": None, "part2": None},
        11: {"part1": None, "part2": None},
        13: {"part1": None, "part2": None},
        15: {"part1": None, "part2": None},
        17: {"part1": None, "part2": None},
        18: {"part1": None, "part2": None},
        19: {"part1": 231, "part2": None},  # Part 2 needs debugging
        20: {"part1": None, "part2": None},
        21: {"part1": None, "part2": None},
        23: {"part1": None, "part2": None},
        25: {"part1": None, "part2": None},
    },
    
    "2020": {
        1: {"part1": None, "part2": None},
        15: {"part1": None, "part2": None},
        19: {"part1": None, "part2": None},
    },
    
    "2021": {
        1: {"part1": None, "part2": None},
        2: {"part1": None, "part2": None},
        3: {"part1": None, "part2": None},
        4: {"part1": None, "part2": None},
        5: {"part1": None, "part2": None},
        6: {"part1": None, "part2": None},
        7: {"part1": None, "part2": None},
        8: {"part1": None, "part2": None},
        9: {"part1": None, "part2": None},
        10: {"part1": None, "part2": None},
        11: {"part1": None, "part2": None},
        12: {"part1": None, "part2": None},
        13: {"part1": None, "part2": None},
        14: {"part1": None, "part2": None},
        15: {"part1": None, "part2": None},
        16: {"part1": None, "part2": None},
        17: {"part1": None, "part2": None},
        18: {"part1": None, "part2": None},
        19: {"part1": None, "part2": None},
        20: {"part1": None, "part2": None},
        21: {"part1": None, "part2": None},
        22: {"part1": None, "part2": None},
        23: {"part1": None, "part2": None},
        24: {"part1": None, "part2": None},
        25: {"part1": None, "part2": None},
    },
    
    "2022": {
        1: {"part1": None, "part2": None},
        2: {"part1": None, "part2": None},
        3: {"part1": None, "part2": None},
        4: {"part1": None, "part2": None},
        5: {"part1": None, "part2": None},
        6: {"part1": None, "part2": None},
        7: {"part1": None, "part2": None},
        8: {"part1": None, "part2": None},
        9: {"part1": None, "part2": None},
        10: {"part1": None, "part2": None},
        11: {"part1": None, "part2": None},
        12: {"part1": None, "part2": None},
        13: {"part1": None, "part2": None},
        14: {"part1": None, "part2": None},
        15: {"part1": None, "part2": None},
        16: {"part1": None, "part2": None},
        17: {"part1": None, "part2": None},
        18: {"part1": None, "part2": None},
        19: {"part1": None, "part2": None},
        20: {"part1": None, "part2": None},
        21: {"part1": None, "part2": None},
        22: {"part1": None, "part2": None},
        23: {"part1": None, "part2": None},
        24: {"part1": None, "part2": None},
        25: {"part1": None, "part2": None},
    },
    
    "2023": {
        1: {"part1": None, "part2": None},
    }
}


def get_expected_answer(year: str, day: int, part: str) -> Answer:
    """
    Get the expected answer for a specific year/day/part.
    
    Args:
        year: Year as string (e.g., "2019")
        day: Day number as integer (e.g., 19)
        part: Part as string ("part1" or "part2")
        
    Returns:
        Expected answer or None if unknown
    """
    return EXPECTED_ANSWERS.get(year, {}).get(day, {}).get(part)


def set_expected_answer(year: str, day: int, part: str, answer: Answer) -> None:
    """
    Set the expected answer for a specific year/day/part.
    
    Args:
        year: Year as string (e.g., "2019")
        day: Day number as integer (e.g., 19)
        part: Part as string ("part1" or "part2")
        answer: Expected answer to set
    """
    if year not in EXPECTED_ANSWERS:
        EXPECTED_ANSWERS[year] = {}
    if day not in EXPECTED_ANSWERS[year]:
        EXPECTED_ANSWERS[year][day] = {}
    EXPECTED_ANSWERS[year][day][part] = answer


def has_expected_answer(year: str, day: int, part: str) -> bool:
    """
    Check if we have an expected answer for a specific year/day/part.
    
    Args:
        year: Year as string
        day: Day number as integer
        part: Part as string
        
    Returns:
        True if expected answer exists and is not None
    """
    answer = get_expected_answer(year, day, part)
    return answer is not None


def get_completion_stats() -> Dict[str, Any]:
    """
    Get statistics about how many expected answers we have.
    
    Returns:
        Dictionary with completion statistics
    """
    total_parts = 0
    known_parts = 0
    
    for year_data in EXPECTED_ANSWERS.values():
        for day_data in year_data.values():
            for part_answer in day_data.values():
                total_parts += 1
                if part_answer is not None:
                    known_parts += 1
    
    return {
        "total_parts": total_parts,
        "known_parts": known_parts,
        "unknown_parts": total_parts - known_parts,
        "completion_percentage": (known_parts / total_parts * 100) if total_parts > 0 else 0
    }


if __name__ == "__main__":
    # Print completion statistics
    stats = get_completion_stats()
    print("Expected Answers Completion Statistics:")
    print(f"  Total parts: {stats['total_parts']}")
    print(f"  Known answers: {stats['known_parts']}")
    print(f"  Unknown answers: {stats['unknown_parts']}")
    print(f"  Completion: {stats['completion_percentage']:.1f}%")
    
    # Show some examples
    print("\nExample known answers:")
    for year, year_data in EXPECTED_ANSWERS.items():
        for day, day_data in year_data.items():
            for part, answer in day_data.items():
                if answer is not None:
                    print(f"  {year} Day {day} {part}: {answer}")
                    break
        else:
            continue
        break