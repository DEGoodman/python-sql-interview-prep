# 1-Hour Technical Interview Study Plan

## Interview Format
- **Duration**: 1 hour
- **Focus**: Basic data structures, programming, database concepts
- **Languages**: Python + SQL
- **Platform**: CoderPad (collaborative coding environment)

## Study Schedule (Recommended 2-3 weeks prep)

### Week 1: Foundations
**Day 1-2: Data Structures Review**
- Complete `exercises/data_structures/arrays_and_lists.py` (45 mins)
- Complete `exercises/data_structures/hash_maps_and_sets.py` (45 mins)
- Focus on: Time/space complexity, common patterns

**Day 3-4: SQL Basics**
- Set up database: `python scripts/setup_db.py` (or manually: `psql -d interview_practice -f database/schema.sql`)
- Load data: Database setup script handles this automatically
- Practice `exercises/sql/basic_queries.sql` (60 mins)

**Day 5-7: Combined Practice**
- Work through `exercises/combined/data_analysis.py` (choose 2-3 exercises)
- Time yourself: 15-20 minutes per exercise
- Focus on explaining your thought process

### Week 2: Interview Scenarios
**Day 1-3: API Design**
- Complete `exercises/combined/api_design.py` exercises
- Practice explaining database design decisions
- Focus on error handling and edge cases

**Day 4-5: Advanced SQL**
- Practice `exercises/sql/advanced_queries.sql`
- Focus on: JOINs, window functions, aggregations
- Time limit: 8-12 minutes per query

**Day 6-7: Mock Interviews**
- Pick random exercises from each category
- Use 1-hour time limit for mixed problems
- Practice coding while explaining your approach

### Week 3: Polish & Edge Cases
**Day 1-2: Optimization**
- Review time/space complexity of your solutions
- Practice optimizing slow solutions
- Focus on when to use different data structures

**Day 3-4: Error Handling**
- Add validation and error handling to previous solutions
- Practice discussing edge cases
- Review SQL injection prevention

**Day 5-7: Final Review**
- Mixed practice sessions
- Focus on communication and code clarity
- Review database design principles

## Daily Practice Routine (30-45 minutes)

### Warm-up (10 minutes)
1. One easy data structure problem
2. One simple SQL query
3. Review previous day's mistakes

### Core Practice (25-30 minutes)
1. Pick one exercise from current week's focus
2. Code solution while talking through approach
3. Test with provided test cases
4. Optimize if needed

### Review (5 minutes)
1. Note what went well/poorly
2. Identify patterns to remember
3. Plan tomorrow's focus

## Common Interview Question Types

### Data Structures (expect 1-2 problems)
- Array manipulation (searching, sorting, duplicates)
- Hash table usage (frequency counting, lookups)
- String processing (anagrams, pattern matching)
- **Time allocation**: 15-20 minutes each

### SQL Queries (expect 2-3 queries)
- JOINs between multiple tables
- Aggregation with GROUP BY
- Window functions for ranking/running totals  
- Date/time filtering
- **Time allocation**: 8-12 minutes each

### Combined Programming (expect 1 problem)
- Process database results in Python
- Data validation and transformation
- Basic business logic implementation
- **Time allocation**: 15-25 minutes

## CoderPad Tips
- **Test your code**: Always run test cases
- **Explain as you go**: Verbalize your thought process
- **Ask clarifying questions**: Confirm requirements upfront
- **Handle edge cases**: Consider nulls, empty inputs, invalid data
- **Clean code**: Use meaningful variable names, proper formatting

## Key Concepts to Review

### Python Fundamentals
- List comprehensions and dictionary operations
- Exception handling (`try/except`)
- Working with JSON data
- Basic OOP (classes, methods)

### SQL Essentials
- INNER/LEFT/RIGHT JOINs
- Aggregation functions (COUNT, SUM, AVG, MAX, MIN)
- Window functions (ROW_NUMBER, RANK, PARTITION BY)
- Subqueries and CTEs
- Date functions and formatting

### Database Design
- Primary/foreign key relationships
- Normalization principles
- Index usage for performance
- Data types selection

## Day-of-Interview Checklist
- [ ] Review common SQL syntax
- [ ] Practice one easy warm-up problem
- [ ] Test your setup (if remote)
- [ ] Prepare questions about the role/company
- [ ] Get a good night's sleep!

## Emergency Review (30 minutes before interview)
1. **Arrays**: Two pointers technique, hash table for O(1) lookup
2. **SQL**: JOIN syntax, basic aggregation patterns
3. **Python**: List/dict methods, string manipulation
4. **Debugging**: Print statements, step through logic

Remember: **Communication is key!** Explain your approach before coding, discuss trade-offs, and ask questions when unclear.