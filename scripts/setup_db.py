#!/usr/bin/env python3
"""
Database Setup Script for Interview Practice
One-command database initialization with schema and sample data
"""

import os
import sys
import subprocess
from pathlib import Path

# Add src to path to import database module
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from database import Database

def run_sql_file_psql(sql_file: str, description: str = "") -> bool:
    """
    Execute a SQL file using psql so that PL/pgSQL dollar-quoted blocks
    and multi-statement scripts execute correctly.
    """
    try:
        print(f"📄 {description or f'Running {os.path.basename(sql_file)}'}...", end=" ")

        env = os.environ.copy()
        db_password = env.get('DB_PASSWORD')
        if db_password:
            # Allow non-interactive auth if password is provided
            env['PGPASSWORD'] = db_password

        host = env.get('DB_HOST', 'localhost')
        port = env.get('DB_PORT', '5432')
        dbname = env.get('DB_NAME', 'interview_practice')
        user = env.get('DB_USER')

        cmd = [
            'psql',
            '-v', 'ON_ERROR_STOP=1',
            '-h', host,
            '-p', str(port),
            '-d', dbname,
        ]

        if user:
            cmd.extend(['-U', user])

        cmd.extend(['-f', sql_file])

        result = subprocess.run(cmd, capture_output=True, text=True, env=env)
        if result.returncode == 0:
            print("✅ Success")
            return True
        else:
            # Surface a concise error; keep stderr for details
            print("❌ Failed")
            if result.stderr:
                print(result.stderr.strip())
            return False
    except Exception as e:
        print(f"❌ Failed: {str(e)}")
        return False

def check_postgresql():
    """Check if PostgreSQL is installed and accessible"""
    try:
        result = subprocess.run(['psql', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ PostgreSQL found: {result.stdout.strip()}")
            return True
    except FileNotFoundError:
        pass
    
    print("❌ PostgreSQL not found in PATH")
    print("📋 Install PostgreSQL:")
    print("   - macOS: brew install postgresql")
    print("   - Ubuntu: sudo apt-get install postgresql postgresql-contrib")
    print("   - Windows: Download from https://www.postgresql.org/download/")
    return False

def check_database_exists(db_name: str = "interview_practice"):
    """Check if the target database exists"""
    try:
        # Try to connect to the database
        result = subprocess.run(
            ['psql', '-d', db_name, '-c', 'SELECT 1;'], 
            capture_output=True, 
            text=True
        )
        return result.returncode == 0
    except:
        return False

def create_database(db_name: str = "interview_practice"):
    """Create the database if it doesn't exist"""
    if check_database_exists(db_name):
        print(f"✅ Database '{db_name}' already exists")
        return True
    
    try:
        print(f"🏗️  Creating database '{db_name}'...", end=" ")
        result = subprocess.run(['createdb', db_name], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Success")
            return True
        else:
            print(f"❌ Failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Failed: {str(e)}")
        return False

def setup_environment():
    """Set up environment file if it doesn't exist"""
    env_file = '.env'
    env_example = '.env.example'
    
    if os.path.exists(env_file):
        print("✅ Environment file (.env) already exists")
        return True
    
    if os.path.exists(env_example):
        print("📝 Creating .env from .env.example...", end=" ")
        try:
            with open(env_example, 'r') as src, open(env_file, 'w') as dst:
                content = src.read()
                # Set default values that work with local PostgreSQL
                content = content.replace('your_username', os.getenv('USER', 'postgres'))
                content = content.replace('your_password', '')
                dst.write(content)
            print("✅ Success")
            print("⚠️  Edit .env file with your actual database credentials if needed")
            return True
        except Exception as e:
            print(f"❌ Failed: {str(e)}")
            return False
    else:
        print("❌ .env.example not found")
        return False

def main():
    print("🎯 Python PostgreSQL Interview Practice - Database Setup")
    print("=" * 60)
    
    # Get project root directory
    project_root = Path(__file__).parent.parent
    os.chdir(project_root)
    
    # Check prerequisites
    print("\n📋 Checking prerequisites...")
    if not check_postgresql():
        return 1
    
    # Set up environment
    print("\n🔧 Setting up environment...")
    if not setup_environment():
        return 1
    
    # Create database
    print("\n🗃️  Setting up database...")
    if not create_database():
        return 1
    
    # Connect to database and run setup scripts
    print("\n📊 Initializing database schema and data...")
    # Use psql to run SQL scripts to properly handle PL/pgSQL blocks
    schema_file = os.path.join('database', 'schema.sql')
    if not run_sql_file_psql(schema_file, "Setting up database schema"):
        return 1

    data_file = os.path.join('database', 'sample_data.sql')
    if not run_sql_file_psql(data_file, "Loading sample data"):
        return 1

    # Verify setup using application connection
    db = Database()
    if not db.connect():
        print("❌ Could not connect to database")
        print("🔍 Check your .env file and ensure PostgreSQL is running")
        return 1

    try:
        print("\n✅ Verifying database setup...")
        tables = ['customers', 'products', 'categories', 'orders', 'order_items']
        all_good = True
        
        for table in tables:
            result = db.execute_query(f"SELECT COUNT(*) FROM {table}")
            if result:
                count = result[0][0]
                print(f"   📊 {table}: {count} records")
            else:
                print(f"   ❌ {table}: Error checking")
                all_good = False
        
        if all_good:
            print("\n🎉 Database setup completed successfully!")
            print("\n🚀 You're ready to start practicing!")
            print("   📖 Begin with: exercises/STUDY_PLAN.md")
            print("   🧪 Test your setup: python src/test_runner.py")
            print("   🔍 Connect to DB: psql -d interview_practice")
            return 0
        else:
            print("\n⚠️  Setup completed with some issues")
            return 1
    finally:
        db.close()

if __name__ == "__main__":
    sys.exit(main())