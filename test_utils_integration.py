#!/usr/bin/env python3
"""Test utils integration."""

import sys
from pathlib import Path

# Test both old and new utils
sys.path.insert(0, str(Path(__file__).parent))

print("Testing utils integration...")

# Test legacy utils.py
import utils as legacy_utils
print(f"Legacy utils loaded: {hasattr(legacy_utils, 'get_list_of_numbers')}")
print(f"Enhanced utils available: {getattr(legacy_utils, 'ENHANCED_UTILS_AVAILABLE', False)}")

# Test enhanced utils package
try:
    from utils import AdventSolution, InputParser, timer
    print("✅ Enhanced utils package loaded successfully")
    print("Available components:")
    print("  - AdventSolution")
    print("  - InputParser") 
    print("  - timer")
    
    # Test basic functionality
    parser = InputParser("1\n2\n3")
    numbers = parser.as_integers()
    print(f"  - InputParser test: {numbers}")
    
except ImportError as e:
    print(f"❌ Enhanced utils package import failed: {e}")

print("\nIntegration test complete.")