# Exercises Framework
## Structure & Approach for Concept-Focused Exercises

---

## Overview
Exercises are **concept-focused**, not domain-specific. Each unit has a single `.py` file containing drills for all topics in that unit. Exercises test implementation of concepts in isolation with starter code and test cases.

**File Structure**:
```
modules/<module_name>/
├── unit_1_<topic>/
│   └── exercises/
│       └── unit_1_<topic>_exercises.py
├── unit_2_<topic>/
│   └── exercises/
│       └── unit_2_<topic>_exercises.py
└── unit_N_<topic>/
    └── exercises/
        └── unit_N_<topic>_exercises.py
```

---

## Exercise File Structure

Each exercise file (`.py`) contains multiple exercises focused on ONE unit's topics. Structure:

```python
"""
Unit [N]: [Topic Name] - Exercises
Concept-focused drills testing implementation of [topic] fundamentals.
"""

# ============================================================================
# Exercise [Number]: [SubTopic Name]
# ============================================================================

# SubTopic: [e.g., Create, Slice, Filter, Transform, Sort]
# Objective: [What to implement]

# WRITE CODE HERE
# [Variable declarations and implementations]
# END OF YOUR CODE

# Test Cases
assert result == expected1, "Test 1 failed"
assert result == expected2, "Test 2 failed"
assert result == expected3, "Test 3 failed"

# ============================================================================
# Exercise [Number + 1]: [Next SubTopic Name]
# ============================================================================
# ... repeat pattern for each subtopic in the unit
```

---

## Exercise Design Template

### Module - Unit - Topic - SubTopic Header
```
Module: [e.g., Collections]
Unit: [e.g., unit_1_lists]
Topic: [e.g., Lists]
SubTopic: [e.g., Creation, Slicing, Filtering]
```

### Exercise Components

**1. Exercise Header with SubTopic**
```python
# ============================================================================
# Exercise [Number]: [SubTopic Name]
# ============================================================================

# SubTopic: [Specific skill being taught - e.g., Create, Slice, Filter]
# Objective: [What learner will achieve]

# Requirements:
# - Requirement 1
# - Requirement 2

# Reference Variables:
# variable_name = [value for learner reference]
```

**2. Code Section (Procedural)**
```python
# WRITE CODE HERE
# Implement logic using reference variables
# Don't modify input variables

# END OF YOUR CODE
```

**3. Test Cases**
```python
# Test Cases
assert result == expected1, "Test 1 failed: [Description]"
assert result == expected2, "Test 2 failed: [Description]"
assert result == expected3, "Test 3 failed: [Description]"
```
    
    Args:
        [param1]: [description]
        [param2]: [description]
    
    Returns:
        [Description of return value]
    """
    pass  # Your implementation here
```

**2. Test Cases Function**
```python
def test_exercise_[number]():
    """Test cases for Exercise [Number]"""
    
    # Test case 1: Basic functionality
    result = exercise_[number]_starter(input1)
    assert result == expected1, "Basic case failed"
    
    # Test case 2: Edge case
    result = exercise_[number]_starter(input2)
    assert result == expected2, "Edge case failed"
    
    # Test case 3: Variant
    result = exercise_[number]_starter(input3)
    assert result == expected3, "Variant case failed"
```

---

## Key Principles

### 1. Concept-Focused Only
- **NO real-world domain context** (no healthcare, eCommerce, banking)
- Test only the concept/technique in isolation
- Example: Test list slicing, NOT appointment scheduling

### 2. One Topic Per Exercise
- Each exercise focuses on ONE specific concept or technique
- Examples:
  - Exercise 1: List creation and indexing
  - Exercise 2: List slicing
  - Exercise 3: List methods (append, remove, sort)
  - Exercise 4: List comprehensions

### 3. No Incremental Building
- Each exercise is independent
- Later exercises do NOT reference earlier ones
- Each learner can tackle any exercise without prior completion

### 4. Starter Code
- Provide function signature and docstring
- Include Requirements section in docstring
- Learner fills in the implementation body
- Use `pass` as placeholder

### 5. Test Cases
- Always **3+ test cases per exercise**
- Test normal case, edge case, and variant
- Use clear assertion messages
- Use pure `assert` statements (no pytest decorators)
- Tests are the specification of expected output

---

## Example Exercise File (Lists Unit)

```python
"""
Unit 1: Lists - Exercises
Concept-focused drills testing list fundamentals.
"""

# ============================================================================
# Exercise 1: List Creation and Indexing
# ============================================================================

def exercise_1_starter(items):
    """
    Create a list from items and return the first and last elements.
    
    Objective: Master list creation and index access
    
    Requirements:
    - Accept any iterable
    - Return a tuple of (first_item, last_item)
    - Handle empty list by returning (None, None)
    
    Args:
        items: An iterable (list, tuple, string, etc.)
    
    Returns:
        Tuple of (first_element, last_element) or (None, None) if empty
    """
    # ========================================================================
    # WRITE CODE HERE
    # ========================================================================
    # Replace 'pass' with your implementation
    # You can use helper variables, conditions, indexing, etc.
    # Make sure your code satisfies all requirements above
    
    pass
    
    # ========================================================================
    # END OF YOUR CODE
    # ========================================================================


def test_exercise_1():
    """Test cases for Exercise 1"""
    
    # Test case 1: Basic list
    result = exercise_1_starter([1, 2, 3])
    assert result == (1, 3), "Failed for [1,2,3]"
    
    # Test case 2: Single item
    result = exercise_1_starter([42])
    assert result == (42, 42), "Failed for single item"
    
    # Test case 3: Empty list
    result = exercise_1_starter([])
    assert result == (None, None), "Failed for empty list"


# ============================================================================
# Exercise 2: List Slicing
# ============================================================================

def exercise_2_starter(items, start, end):
    """
    Return a slice of items from start index to end index (exclusive).
    
    Objective: Master list slicing syntax and behavior
    
    Requirements:
    - Use list slicing syntax [start:end]
    - Return a new list (don't modify original)
    - Handle out-of-bounds indices gracefully
    
    Args:
        items: A list to slice
        start: Starting index
        end: Ending index (exclusive)
    
    Returns:
        New list containing items from start to end-1
    """
    pass


def test_exercise_2():
    """Test cases for Exercise 2"""
    
    # Test case 1: Normal slice
    result = exercise_2_starter([1, 2, 3, 4, 5], 1, 4)
    assert result == [2, 3, 4], "Failed for slice [1:4]"
    
    # Test case 2: Slice from start
    result = exercise_2_starter([1, 2, 3], 0, 2)
    assert result == [1, 2], "Failed for slice [0:2]"
    
    # Test case 3: Out of bounds
    result = exercise_2_starter([1, 2, 3], 0, 100)
    assert result == [1, 2, 3], "Failed for out-of-bounds end"


# ============================================================================
# Exercise 3: List Methods (Append and Remove)
# ============================================================================

def exercise_3_starter(initial_list, to_add, to_remove):
    """
    Modify a list by adding and removing items.
    
    Objective: Master list mutating methods
    
    Requirements:
    - Append to_add to the end
    - Remove the first occurrence of to_remove (if it exists)
    - Return the modified list
    - If to_remove not found, return unchanged list (except with to_add appended)
    
    Args:
        initial_list: Starting list
        to_add: Item to append
        to_remove: Item to remove (first occurrence)
    
    Returns:
        Modified list
    """
    pass


def test_exercise_3():
    """Test cases for Exercise 3"""
    
    # Test case 1: Normal add and remove
    result = exercise_3_starter([1, 2, 3], 4, 2)
    assert result == [1, 3, 4], "Failed for add 4, remove 2"
    
    # Test case 2: Remove not found
    result = exercise_3_starter([1, 2, 3], 4, 99)
    assert result == [1, 2, 3, 4], "Failed when remove item not found"
    
    # Test case 3: Remove first occurrence only
    result = exercise_3_starter([1, 2, 2, 3], 4, 2)
    assert result == [1, 2, 3, 4], "Failed to remove only first occurrence"


# ============================================================================
# Exercise 4: List Comprehensions
# ============================================================================

def exercise_4_starter(numbers):
    """
    Filter and transform a list using list comprehension.
    
    Objective: Master list comprehension syntax and logic
    
    Requirements:
    - Use list comprehension (not loops)
    - Filter numbers greater than 5
    - Square each filtered number
    - Return new list
    
    Args:
        numbers: List of numbers
    
    Returns:
        List of squared values where original > 5
    """
    pass


def test_exercise_4():
    """Test cases for Exercise 4"""
    
    # Test case 1: Normal case
    result = exercise_4_starter([1, 6, 3, 8, 5, 10])
    assert result == [36, 64, 100], "Failed to filter and square"
    
    # Test case 2: All filtered out
    result = exercise_4_starter([1, 2, 3])
    assert result == [], "Failed when all filtered out"
    
    # Test case 3: All pass filter
    result = exercise_4_starter([6, 7, 8])
    assert result == [36, 49, 64], "Failed when all pass filter"


# ============================================================================
# If running as script, run tests
# ============================================================================

if __name__ == "__main__":
    test_exercise_1()
    test_exercise_2()
    test_exercise_3()
    test_exercise_4()
    print("All exercises passed!")
```

---

## Write Code Here Section

Each exercise file includes a clear **"Write Code Here"** section where learners implement their solution:

```python
# ============================================================================
# Exercise [Number]: [Topic Name]
# ============================================================================

def exercise_[number]_starter():
    """
    [Description of what to implement]
    
    Objective: [Learning goal]
    
    Requirements:
    - Requirement 1
    - Requirement 2
    """
    # ========================================================================
    # WRITE CODE HERE
    # ========================================================================
    # Replace 'pass' with your implementation
    # You can use helper variables, loops, conditions, etc.
    # Make sure your code satisfies all requirements
    
    pass
    
    # ========================================================================
    # END OF YOUR CODE
    # ========================================================================


def test_exercise_[number]():
    """Test cases for Exercise [Number]"""
    
    # Test case 1: Basic functionality
    result = exercise_[number]_starter(input1)
    assert result == expected1, "Basic case failed"
    
    # Test case 2: Edge case
    result = exercise_[number]_starter(input2)
    assert result == expected2, "Edge case failed"
    
    # Test case 3: Variant
    result = exercise_[number]_starter(input3)
    assert result == expected3, "Variant case failed"
```

### Learner Workflow
1. **Read** the exercise docstring (Objective & Requirements)
2. **Identify** what the function should do
3. **Review** test cases to understand expected behavior
4. **Write Code** between the "WRITE CODE HERE" markers
5. **Run** the script: `python unit_X_topic_exercises.py`
6. **Validate** output matches test assertions
7. **Iterate** if tests fail

---

## Guidelines

### Starter Code
- Provide function signature and docstring
- Include Objective and Requirements in docstring
- Leave implementation to learner (use `pass`)
- Mark the implementation area with clear "WRITE CODE HERE" comments

### Test Cases
- Always **3+ test cases** per exercise
- Label each: "Test case 1: [What it tests]"
- Include clear assertion messages
- Test normal, edge, and variant cases

### Naming Convention
- File: `unit_[N]_[topic]_exercises.py`
- Function: `exercise_[N]_starter()` for implementation
- Test function: `test_exercise_[N]()` for tests

### No Domain Context
- Use simple, neutral data (numbers, strings, generic items)
- Do NOT reference healthcare, eCommerce, banking
- Focus purely on the technical concept

### Expected Output
Not specified separately—test cases ARE the expected output specification.

---

## Learner Workflow

1. Open `unit_X_topic_exercises.py`
2. Read docstring for Exercise 1 to understand Objective and Requirements
3. Fill in the `exercise_1_starter()` function body
4. Run `test_exercise_1()` to validate
5. Review test output; iterate if needed
6. Move to next exercise
7. All tests pass = unit mastery
