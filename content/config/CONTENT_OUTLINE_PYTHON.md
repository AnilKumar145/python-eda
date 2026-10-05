# Python — Real-Time Product Engineering

## Unit 1: Threads

### Unit 1.1: Threading Fundamentals
- What is a thread?
- Process vs thread
- Why use threads?
- CPU-bound vs I/O-bound tasks
- Python threading model
- Creating threads with `threading.Thread`
- Starting and joining threads
- Thread lifecycle
- Main thread vs worker threads

### Unit 1.2: Thread Management
- Passing arguments to threads
- Thread naming
- Checking thread status
- `is_alive()`
- Daemon vs non-daemon threads
- Running multiple threads
- Thread termination considerations

### Unit 1.3: Thread Synchronization
- Shared data and shared state
- Race conditions
- Critical sections
- `Lock`
- `RLock`
- `Semaphore`
- `Event`
- `Condition`
- Synchronization strategies

### Unit 1.4: Thread Communication
- Inter-thread communication
- `queue.Queue`
- Producer–Consumer pattern
- Thread-safe data exchange
- Signaling between threads
- Avoiding shared mutable state

### Unit 1.5: Thread Pools
- Why thread pools?
- `concurrent.futures`
- `ThreadPoolExecutor`
- `submit()`
- `map()`
- `Future`
- Retrieving results
- Exception handling
- Shutting down executors


## Unit 2: Concurrency

### Unit 2.1: Concurrency Fundamentals
- What is concurrency?
- Concurrency vs parallelism
- Synchronous vs asynchronous execution
- I/O-bound vs CPU-bound workloads
- Threads vs processes vs async
- Choosing the right concurrency model

### Unit 2.2: Multiprocessing
- Why multiprocessing?
- Process vs thread
- Python GIL and its impact
- `multiprocessing`
- Creating processes
- Process lifecycle
- Process communication
- `Queue`
- `Pipe`
- Shared memory basics

### Unit 2.3: Process Pools
- `ProcessPoolExecutor`
- Submitting CPU-intensive tasks
- `Future`
- Result handling
- Exception handling
- Worker processes
- Thread pool vs process pool

### Unit 2.4: Asynchronous Programming
- Event loop
- `async` and `await`
- Coroutines
- `asyncio`
- Creating and running tasks
- `asyncio.create_task()`
- `gather()`
- Async I/O
- Cancellation and timeouts

### Unit 2.5: Concurrent Programming Patterns
- Producer–Consumer
- Worker Pool
- Task Queue
- Fan-out / Fan-in
- Parallel execution
- Synchronization strategies
- Deadlocks
- Starvation
- Race conditions
- Avoiding shared state

### Unit 2.6: Choosing the Right Concurrency Model
- Threads for I/O-bound workloads
- Multiprocessing for CPU-bound workloads
- Asyncio for high-volume I/O
- Thread pool vs process pool
- Async vs threads
- Combining concurrency models
- Real-world use cases


## Unit 3: Database Programming — Part 1

### Unit 3.1: Database Fundamentals
- Relational database concepts
- SQL basics (`SELECT`, `INSERT`, `UPDATE`, `DELETE`)
- Primary keys and foreign keys
- Indexes and performance
- PostgreSQL vs SQLite vs MySQL
- Python database connectivity overview

### Unit 3.2: Python Database API (DB-API)
- DB-API 2.0 specification
- Database drivers
- Connection objects
- Cursor objects
- Parameterized queries
- Commit and rollback
- Connection pooling basics

### Unit 3.3: Working with PostgreSQL
- Installing `psycopg2`
- Connecting to PostgreSQL
- Executing queries
- Fetching results (`fetchone()`, `fetchall()`, `fetchmany()`)
- Handling `NULL` values
- Data type mapping between Python and PostgreSQL
- Context managers for database connections

### Unit 3.4: Security and Best Practices
- SQL injection prevention
- Parameterized queries vs string formatting
- Transaction management
- Error handling with database operations
- Connection cleanup and resource management
- Context managers and `with` statements
- Database connection best practices


## Unit 4: Database Programming — Part 2

### Unit 4.1: ORM Fundamentals
- What is an ORM and why use it?
- SQLAlchemy overview
- SQLAlchemy Core vs ORM
- Declarative approach
- Defining models with SQLAlchemy
- Column types and constraints
- One-to-many relationships
- Many-to-many relationships

### Unit 4.2: SQLAlchemy Sessions
- Creating sessions
- Session lifecycle
- Adding and committing objects
- Updating and deleting objects
- Querying with ORM
- Filtering and ordering
- Joining tables
- Lazy vs eager loading

### Unit 4.3: Advanced ORM Features
- Relationship configurations
- Cascade operations
- `backref` and `back_populates`
- Association tables
- Many-to-many relationships
- Hybrid properties
- N+1 query problem
- Query optimization techniques

### Unit 4.4: Database Migrations
- Why migrations matter
- Alembic setup and configuration
- Creating migrations
- Applying migrations
- Reverting migrations
- Managing schema changes
- Versioning database changes
- Team collaboration with migrations

### Unit 4.5: Database Logging
- SQLAlchemy query logging
- Query logging configuration
- Analyzing slow queries
- Connection pool monitoring
- Debugging database issues
- Database performance monitoring
- Identifying inefficient queries


## Unit 5: Unit Testing

### Unit 5.1: Testing Fundamentals
- What is software testing?
- Why unit testing matters
- Unit testing vs integration testing
- Test cases and test scenarios
- Test-driven development (TDD) basics
- Arrange, Act, Assert (AAA) pattern
- Test isolation
- Test naming and organization

### Unit 5.2: pytest Fundamentals
- Installing and configuring `pytest`
- Test file conventions
- Test function conventions
- Writing test cases
- Assertions
- Running tests
- Test discovery
- Targeted test execution

### Unit 5.3: Fixtures and Test Data
- What are fixtures?
- `@pytest.fixture`
- Fixture scope
- Setup and teardown
- Reusable test data
- Parameterized testing
- `@pytest.mark.parametrize`
- Temporary files and directories

### Unit 5.4: Mocking and Isolation
- Why mocking is required
- `unittest.mock`
- `Mock`
- `MagicMock`
- `patch`
- Mocking functions and methods
- Mocking external APIs
- Mocking database operations
- Testing external dependencies

### Unit 5.5: Exceptions and Edge Cases
- Testing expected exceptions
- `pytest.raises`
- Testing invalid inputs
- Boundary-value testing
- Edge cases
- Negative test cases
- Error handling validation

### Unit 5.6: Database Testing
- Testing database operations
- Test database setup
- CRUD testing
- Transaction testing
- Rollback during tests
- Testing SQLAlchemy models
- Testing repository/data-access logic
- Integration testing basics

### Unit 5.7: Test Coverage and Best Practices
- Code coverage
- `pytest-cov`
- Measuring coverage
- Identifying untested code
- Unit testing best practices
- Avoiding brittle tests
- Test independence
- Maintainable test suites
- CI/CD testing basics