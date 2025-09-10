"""
Test Runner for Interview Practice Exercises
Validates your solutions and provides feedback
"""

import os
import sys
import importlib.util
import traceback
from typing import Dict, List, Any, Callable
from database import Database

class TestRunner:
    def __init__(self):
        self.db = Database()
        self.results = []
    
    def run_data_structure_tests(self, exercise_file: str) -> Dict[str, Any]:
        """Run tests for data structure exercises"""
        try:
            # Load the exercise module
            spec = importlib.util.spec_from_file_location("exercise", exercise_file)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            # Run the test cases in the module
            print(f"\n🧪 Testing {os.path.basename(exercise_file)}...")
            
            # Capture test output
            import io
            import contextlib
            
            f = io.StringIO()
            with contextlib.redirect_stdout(f):
                # Execute the test section
                if hasattr(module, '__name__'):
                    # Run the if __name__ == "__main__" block
                    exec(compile(open(exercise_file).read(), exercise_file, 'exec'))
            
            output = f.getvalue()
            
            if "All tests passed!" in output:
                return {"status": "PASS", "message": "All tests passed!", "output": output}
            else:
                return {"status": "FAIL", "message": "Some tests failed", "output": output}
                
        except Exception as e:
            return {"status": "ERROR", "message": f"Error running tests: {str(e)}", "traceback": traceback.format_exc()}
    
    def run_sql_tests(self, sql_file: str, solution_file: str = None) -> Dict[str, Any]:
        """Run tests for SQL exercises by comparing with solutions"""
        try:
            print(f"\n🗃️  Testing SQL queries in {os.path.basename(sql_file)}...")
            
            if not self.db.connect():
                return {"status": "ERROR", "message": "Could not connect to database"}
            
            # Read the exercise file
            with open(sql_file, 'r') as f:
                content = f.read()
            
            # Check if there are any TODO comments (indicating incomplete exercises)
            if "TODO:" in content:
                todo_count = content.count("TODO:")
                return {
                    "status": "INCOMPLETE", 
                    "message": f"Found {todo_count} TODO items. Complete the exercises first!",
                    "todos": todo_count
                }
            
            # If solution file exists, we could compare results (advanced feature)
            if solution_file and os.path.exists(solution_file):
                return {"status": "INFO", "message": "Exercise appears complete. Compare with solutions manually."}
            
            return {"status": "INFO", "message": "SQL exercises ready for manual review."}
            
        except Exception as e:
            return {"status": "ERROR", "message": f"Error checking SQL: {str(e)}"}
    
    def validate_database_setup(self) -> Dict[str, Any]:
        """Validate that the practice database is set up correctly"""
        try:
            if not self.db.connect():
                return {"status": "ERROR", "message": "Cannot connect to database. Run setup_db.py first."}
            
            # Check if required tables exist
            required_tables = ['customers', 'products', 'categories', 'orders', 'order_items']
            missing_tables = []
            
            for table in required_tables:
                result = self.db.execute_query(
                    "SELECT COUNT(*) FROM information_schema.tables WHERE table_name = %s", 
                    (table,)
                )
                if not result or result[0][0] == 0:
                    missing_tables.append(table)
            
            if missing_tables:
                return {
                    "status": "ERROR", 
                    "message": f"Missing tables: {', '.join(missing_tables)}. Run setup_db.py"
                }
            
            # Check if tables have data
            data_counts = {}
            for table in required_tables:
                result = self.db.execute_query(f"SELECT COUNT(*) FROM {table}")
                data_counts[table] = result[0][0] if result else 0
            
            if all(count > 0 for count in data_counts.values()):
                return {
                    "status": "PASS", 
                    "message": "Database setup is complete and ready!",
                    "data_counts": data_counts
                }
            else:
                return {
                    "status": "WARNING", 
                    "message": "Database exists but some tables are empty",
                    "data_counts": data_counts
                }
                
        except Exception as e:
            return {"status": "ERROR", "message": f"Database validation error: {str(e)}"}
        finally:
            self.db.close()
    
    def run_exercise_suite(self, exercise_path: str) -> None:
        """Run a complete test suite for a specific exercise directory"""
        print(f"\n🚀 Running test suite for: {exercise_path}")
        print("=" * 60)
        
        # First validate database
        db_result = self.validate_database_setup()
        print(f"📊 Database Status: {db_result['status']} - {db_result['message']}")
        
        if db_result['status'] == 'ERROR':
            print("❌ Cannot proceed without database setup")
            return
        
        # Test data structure exercises
        ds_path = os.path.join(exercise_path, 'data_structures')
        if os.path.exists(ds_path):
            for file in os.listdir(ds_path):
                if file.endswith('.py') and not file.startswith('__'):
                    result = self.run_data_structure_tests(os.path.join(ds_path, file))
                    status_emoji = "✅" if result['status'] == 'PASS' else "❌" if result['status'] == 'FAIL' else "⚠️"
                    print(f"{status_emoji} {file}: {result['message']}")
        
        # Test SQL exercises
        sql_path = os.path.join(exercise_path, 'sql')
        if os.path.exists(sql_path):
            solution_path = os.path.join('database', 'solutions')
            for file in os.listdir(sql_path):
                if file.endswith('.sql'):
                    solution_file = os.path.join(solution_path, file.replace('.sql', '_solutions.sql'))
                    result = self.run_sql_tests(os.path.join(sql_path, file), solution_file)
                    status_emoji = "✅" if result['status'] == 'PASS' else "❌" if result['status'] == 'FAIL' else "ℹ️"
                    print(f"{status_emoji} {file}: {result['message']}")

def main():
    """Command line interface for test runner"""
    runner = TestRunner()
    
    if len(sys.argv) > 1:
        # Run specific file
        file_path = sys.argv[1]
        if file_path.endswith('.py'):
            result = runner.run_data_structure_tests(file_path)
            print(f"Result: {result}")
        elif file_path.endswith('.sql'):
            result = runner.run_sql_tests(file_path)
            print(f"Result: {result}")
        else:
            print("Unsupported file type. Use .py or .sql files.")
    else:
        # Run complete exercise suite
        exercises_path = 'exercises'
        if os.path.exists(exercises_path):
            runner.run_exercise_suite(exercises_path)
        else:
            print("❌ Exercises directory not found")

if __name__ == "__main__":
    main()