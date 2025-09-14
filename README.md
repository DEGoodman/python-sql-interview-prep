# Python PostgreSQL Interview Practice

**🎯 Complete preparation toolkit for technical interviews combining Python programming, data structures, and PostgreSQL database skills.**

Perfect for 1-hour technical interviews on platforms like CoderPad that test basic data structures, programming concepts, and SQL proficiency.

## 🚀 Quick Start


### note: using pyenv-virtualenv (recommended with pyenv)
```bash
# 1) Select your local Python version (example)
pyenv local 3.11.9

# 2) Create and activate a virtualenv for this project
pyenv virtualenv 3.11.9 interview-practice-311

# Optional: auto-activate this env when you cd into the repo
pyenv local interview-practice-311

# Or activate manually for this shell
pyenv activate interview-practice-311

# 3) Install dependencies
python -m pip install -U pip setuptools wheel
pip install -r requirements.txt

# 4) Set up database
createdb interview_practice
cp .env.example .env  # Edit with your DB credentials

# 5) Initialize practice database
python scripts/setup_db.py

# 6) Start practicing!
# Begin with exercises/STUDY_PLAN.md

# 7) Running Tests
# Use pytest for better debugging and test organization:
pytest tests/                           # Run all tests
pytest tests/test_hash_maps_and_sets.py # Run specific test file
pytest tests/ --pdb                     # Drop into debugger on failures
pytest tests/ -v                        # Verbose output
```

To deactivate later: `pyenv deactivate`.


## 📚 What's Included

### 🧠 **Data Structures Practice** (`exercises/data_structures/`)
- **Arrays & Lists**: Two Sum, Missing Number, Anagram grouping
- **Hash Maps & Sets**: Frequency counting, intersections, subarray problems
- **Timing**: 5-15 minutes per problem (interview-paced)
- **Testing**: Use `pytest tests/test_*.py --pdb` for debugging

### 🗃️ **SQL Practice** (`exercises/sql/`)
- **Basic Queries**: JOINs, filtering, aggregations
- **Advanced Queries**: Window functions, CTEs, complex business logic
- **Real Database**: Complete e-commerce schema with sample data

### 🔄 **Combined Challenges** (`exercises/combined/`)
- **Data Analysis**: Customer analytics, sales reporting, inventory optimization
- **API Design**: REST endpoints with database integration
- **Real Scenarios**: Problems you'd face in actual interviews

### 📖 **Complete Study Plan** (`exercises/STUDY_PLAN.md`)
- **3-week structured program** with daily 30-45 minute sessions
- **Progressive difficulty** from foundations to interview-ready
- **CoderPad simulation** tips and strategies

## 🏗️ Project Structure

```
exercises/                  # 🎯 Your main practice area
├── STUDY_PLAN.md          # Complete 3-week prep guide
├── data_structures/       # Python coding challenges
├── sql/                   # SQL query practice
└── combined/              # Real-world scenarios

tests/                    # 🧪 Pytest test files
├── test_arrays_and_lists.py
├── test_hash_maps_and_sets.py
└── (test files for other exercises)

database/                  # 🗃️ Sample database setup
├── schema.sql            # E-commerce database structure
├── sample_data.sql       # Realistic test data
└── solutions/            # Example query solutions

src/                      # 🔧 Utilities and helpers
├── database.py          # Database connection class
├── test_runner.py       # Exercise validation
└── solutions/           # Reference implementations

scripts/                 # 🚀 Setup and utility scripts
└── setup_db.py         # One-command database setup
```

## 🎯 Interview Preparation Flow

1. **Week 1**: Master fundamentals with data structures and basic SQL
2. **Week 2**: Practice realistic scenarios combining Python + SQL  
3. **Week 3**: Polish with mock interviews and edge case handling
4. **Day-of**: Quick review and confidence building

## 💡 Key Features

- ✅ **Interview-timed exercises** (matching real interview pacing)
- ✅ **Progressive difficulty** (easy → interview-level complexity)
- ✅ **Complete test environment** (realistic database with sample data)
- ✅ **CoderPad simulation** (designed for collaborative coding platforms)
- ✅ **Business context** (e-commerce scenarios common in interviews)
- ✅ **Self-validation** (test cases and expected outputs included)

## 🛠️ Technical Stack

**Python Libraries:**
- `psycopg2-binary` - PostgreSQL database adapter
- `python-dotenv` - Environment configuration
- `pytest` - Testing framework

**Database:**
- PostgreSQL with realistic e-commerce schema
- Sample data covering customers, products, orders
- Optimized for common interview query patterns

## 📋 Common Interview Question Types

This toolkit prepares you for:

- **Data Structure Problems** (15-20 min): Array manipulation, hash table usage, string processing
- **SQL Queries** (8-12 min each): Multi-table JOINs, aggregations, window functions
- **Combined Programming** (15-25 min): Database integration, data transformation, business logic

## 🎓 Success Tips

1. **Practice explaining your approach** before coding
2. **Time yourself** - interview pressure is real
3. **Focus on clean, readable code** over clever optimizations
4. **Ask clarifying questions** - requirements matter
5. **Test edge cases** - null values, empty inputs, boundary conditions

---

**Ready to ace your technical interview?** Start with `exercises/STUDY_PLAN.md` and work through the structured program. Good luck! 🍀