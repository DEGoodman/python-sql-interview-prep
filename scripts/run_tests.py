#!/usr/bin/env python3
"""
Quick test runner script for interview practice exercises
"""

import os
import sys

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from test_runner import TestRunner

def main():
    runner = TestRunner()
    
    print("🎯 Python PostgreSQL Interview Practice - Test Runner")
    print("=" * 60)
    
    if len(sys.argv) > 1:
        # Run specific exercise
        exercise_path = sys.argv[1]
        if os.path.exists(exercise_path):
            if exercise_path.endswith('.py'):
                result = runner.run_data_structure_tests(exercise_path)
                status_emoji = "✅" if result['status'] == 'PASS' else "❌" if result['status'] == 'FAIL' else "⚠️"
                print(f"{status_emoji} {os.path.basename(exercise_path)}: {result['message']}")
                if result.get('output'):
                    print("\nOutput:")
                    print(result['output'])
            elif exercise_path.endswith('.sql'):
                result = runner.run_sql_tests(exercise_path)
                status_emoji = "✅" if result['status'] == 'PASS' else "❌" if result['status'] == 'FAIL' else "ℹ️"
                print(f"{status_emoji} {os.path.basename(exercise_path)}: {result['message']}")
            else:
                print("❌ Unsupported file type. Use .py or .sql files.")
        else:
            print(f"❌ File not found: {exercise_path}")
    else:
        # Run full test suite
        runner.run_exercise_suite('exercises')
    
    print("\n📖 For detailed study plan, see: exercises/STUDY_PLAN.md")

if __name__ == "__main__":
    main()