# App Labs Framework
## Structure & Approach for Progressive Labs

---

## Overview
App Labs are hands-on implementation projects within real-world domains. Default domain: Healthcare (can adapt to eCommerce, Banking, etc.).

**Structure:**
- **Labs are unit-focused** - Each unit has 1 real-world use case with **multiple labs** (numbered sequentially)
- **Each lab has a complexity level** (Easy, Intermediate, Advanced, Expert) - not limited to 3 labs
- **Comprehensive coverage** - Add as many labs as needed to thoroughly cover all topics/concepts from that unit in realistic context
- **Progression**: Exercises (isolation) → App Labs (unit use cases with progressive complexity) → Capstone (integrated system)
- Add unit micro-labs only for exceptionally complex topics

Every lab MUST begin with clear context and a use case.

Generic Information Template:
```
## Generic Information
**Problem Statement**: [What problem is being solved]
**Goals**:
- Goal 1
- Goal 2
- Goal 3
**Data Elements**: [Key entities/fields involved]
```

Use Case Template:
```
## Use Case
**Title**: Schedule an appointment
**Description**: Allow patients to book an appointment with a chosen doctor at an available time slot, with validation and conflict checks.

### Rules
- Only available slots can be booked
- No overlapping bookings per doctor
- Basic validation for patient/doctor IDs

### Test Cases
- Case 1: Valid booking
- Case 2: Overlapping booking (reject)
- Case 3: Invalid doctor/patient (error)

### Success Criteria
- Booking succeeds for valid inputs
- Conflicts prevented per rules
- Clear errors for invalid inputs
```

**File Structure**:
```
app_labs/
├── unit_1_[topic_name]/
│   ├── lab_1_[easy]/
│   │   ├── README.md
│   │   ├── tasks.md
│   │   ├── starter_code.py
│   │   ├── solution/
│   │   │   └── solution.py
│   │   └── tests.py
│   ├── lab_2_[easy]/
│   │   ├── README.md
│   │   ├── tasks.md
│   │   └── ...
│   ├── lab_3_[intermediate]/
│   │   ├── README.md
│   │   ├── tasks.md
│   │   └── ...
│   ├── lab_4_[intermediate]/
│   ├── lab_5_[advanced]/
│   ├── lab_6_[advanced]/
│   └── lab_7_[expert]/
├── unit_2_[topic_name]/
│   ├── lab_1_[easy]/
│   ├── lab_2_[easy]/
│   ├── lab_3_[intermediate]/
│   └── ... (as many as needed)
└── unit_3_[topic_name]/
    ├── lab_1_[easy]/
    ├── lab_2_[intermediate]/
    ├── lab_3_[advanced]/
    └── ...
```

---

## Learning Progression

### How App Labs Fit Into Your Learning Journey

```
Iteration 1: EXERCISES (Topics in Isolation)
├── Unit 1: Lists - Individual drills on list methods
├── Unit 2: Dicts - Individual drills on dict operations
├── Unit 3: Sets - Individual drills on set operations
└── Unit 4: Tuples - Individual drills on tuple operations

     ↓

Iteration 2: APP LABS (Unit-Focused Real-World Use Cases - Comprehensive)
├── Unit 1 Lab (Lists): "Appointment Scheduling"
│   ├── Lab 1 (Easy): Basic list operations
│   ├── Lab 2 (Easy): List methods and indexing
│   ├── Lab 3 (Intermediate): List comprehensions
│   ├── Lab 4 (Intermediate): Sorting and searching
│   ├── Lab 5 (Advanced): Complex filtering
│   ├── Lab 6 (Advanced): Performance optimization
│   └── Lab 7 (Expert): Production-grade implementation
│
├── Unit 2 Lab (Dicts): "Patient Records Management"
│   ├── Lab 1 (Easy): Dict basics
│   ├── Lab 2 (Easy): Dict operations
│   ├── Lab 3 (Intermediate): Nested dicts
│   ├── Lab 4 (Intermediate): Dict comprehensions
│   ├── Lab 5 (Advanced): Complex queries
│   └── Lab 6 (Expert): Performance tuning
│
├── Unit 3 Lab (Sets): "Hospital Departments & Staff"
│   ├── Lab 1 (Easy): Set basics
│   ├── Lab 2 (Easy): Set operations
│   ├── Lab 3 (Intermediate): Set mathematics
│   ├── Lab 4 (Advanced): Complex operations
│   └── Lab 5 (Expert): Optimization
│
└── Unit 4 Lab (Tuples): "Immutable Medical Data"
    ├── Lab 1 (Easy): Tuple basics
    ├── Lab 2 (Easy): Tuple unpacking
    ├── Lab 3 (Intermediate): Named tuples
    └── Lab 4 (Advanced): Complex scenarios

     ↓

Iteration 3: CAPSTONE PROJECT (Integrated System)
└── Complete Healthcare Management System
    └── Integrates all concepts from all units into larger problem statement
```

---

## Lab Complexity Levels

Labs are numbered sequentially for each use case and tagged with a complexity level. Create as many labs as needed to comprehensively cover all unit topics.

### Easy (Labs 1-2 typically)
**Purpose**: Understand core concepts in isolation
**Characteristics**:
- Single responsibility per task
- Basic operations and fundamentals
- 3-5 implementation tasks
- Simple, clear requirements
- Can be completed in 1-2 hours

### Intermediate (Labs 3-4 typically)
**Purpose**: Combine concepts and solve realistic problems
**Characteristics**:
- Combine multiple concepts from unit
- Real-world scenarios
- 5-8 implementation tasks
- Some complexity in logic/algorithms
- Partial error handling required
- Can be completed in 2-4 hours

### Advanced (Labs 5-6 typically)
**Purpose**: Complex problem-solving with best practices
**Characteristics**:
- Complex business logic
- 8-12 implementation tasks
- Comprehensive error handling
- Security/validation considerations
- Performance considerations
- Can be completed in 3-5 hours

### Expert (Lab 7+ as needed)
**Purpose**: Production-grade implementation
**Characteristics**:
- Complete, integrated feature
- Production-ready code quality
- 12+ implementation tasks
- All edge cases handled
- Full test coverage (>80%)
- Security/performance optimized
- Can be completed in 4-6+ hours

---

## Lab Level Definitions

### Lab Level 1: Foundation
**Purpose**: Understand core concepts in isolation
**Complexity**: Beginner-friendly, focused learning

**Characteristics**:
- Single responsibility per task
- Basic data structures and operations
- 3-5 implementation tasks
- Emphasis on understanding fundamentals
- Simple, clear requirements
- Can be completed in 1-2 hours

**Example Scope**:
```
Collections Module - Unit 1 (Lists) Lab 1 [EASY]
Use Case: Appointment Scheduling (Part 1)
- Create list of appointments
- Add appointments using list methods
- Access appointments by index
- Retrieve all appointments
- Calculate total appointments
- All list fundamentals covered in context
```

**Success Criteria**:
- All tasks functional
- Code runs without errors
- Test cases pass
- Outputs match expected results

---

## Lab Frontmatter & Metadata

Every lab README.md must include frontmatter with these fields:

```yaml
---
title: "Appointment Scheduling - Part 1"
type: app_lab
module: collections
unit: unit_1_lists
lab_number: 1
difficulty: easy                    # easy, intermediate, advanced, expert
use_case: appointment_scheduling
domain: healthcare                  # default: healthcare; also: ecommerce, banking
order: 1
duration_hours: 2
tags:
  topics: ["lists", "collections"]  # Broader categories
  subtopics:                        # Specific skills covered
    - indexing
    - methods-append
    - methods-remove
    - iteration
---
```

**Tags Explanation**:
- **topics**: Broad collection categories (lists, dicts, sets, tuples, functions, async, etc.)
- **subtopics**: Specific skills and concepts covered in the lab
  - Subtopic examples for Lists: indexing, slicing, methods-append, methods-remove, iteration, comprehension-filtering, comprehension-transformation, sorting, membership, searching, performance
  - Subtopic examples for Dicts: key-access, dict-methods, nested-dicts, dict-comprehension, merging, querying
  - Subtopic examples for Sets: set-operations, set-mathematics, uniqueness, unions, intersections

**Purpose of Tags**:
- **Analytics**: Track which topics/subtopics are most practiced
- **Search**: Find labs by specific skill (e.g., "membership operations")
- **Coverage**: Ensure all unit concepts are covered across labs
- **Recommendations**: Suggest relevant labs based on learner's focus areas

---

### Lab Level 2: Intermediate
**Purpose**: Combine concepts and solve realistic problems
**Complexity**: Intermediate, multi-step thinking

**Characteristics**:
- Combine multiple concepts from unit
- Real-world healthcare scenarios
- 5-8 implementation tasks
- Some complexity in logic/algorithms
- Partial error handling required
- Can be completed in 2-4 hours

**Example Scope**:
```
Collections Module - Unit 1 (Lists) Lab 3 [INTERMEDIATE]
Use Case: Appointment Scheduling (Part 2)
- Use list comprehensions for filtering
- Sort appointments by date/time
- Search appointments
- Handle duplicates and conflicts
- Implement list operations for real problems
- More complex list manipulations
```

**Success Criteria**:
- All tasks functional and correct
- Handles common edge cases
- Test cases pass
- Code is reasonably optimized
- Some error handling implemented

---

### Lab Level 3: Advanced
**Purpose**: Production-grade implementation with full features
**Complexity**: Advanced, comprehensive system thinking

**Characteristics**:
- Complete, integrated feature
- Production-ready code quality
- 8-12 implementation tasks
- Complex business logic
- Comprehensive error handling
- Security/validation considerations
- Full test coverage expected
- Can be completed in 4-6 hours

**Example Scope**:
```
Collections Module - Unit 1 (Lists) Lab 5 [ADVANCED]
Use Case: Appointment Scheduling (Part 3)
- Production-grade appointment system using lists
- Advanced list operations and algorithms
- Performance optimization for large datasets
- Comprehensive validation and error handling
- Full test suite for list-based operations
- Ready to integrate with other data structures
```

**Success Criteria**:
- Production-grade code quality
- Handles all edge cases
- Comprehensive test coverage (>80%)
- Error handling for invalid inputs
- Well-structured and documented
- Performance optimized
- Ready for real use

---

## Lab Level 1: README.md Template

```markdown
# Lab Level 1: [Title]
**Module**: [Module Name]
**Objective**: [What learner will achieve]
**Difficulty**: Beginner
**Context**: Domain (Default: Healthcare; also eCommerce/Banking)

## Generic Information
**Problem Statement**: [What problem is being solved]
**Goals**:
- Goal 1
- Goal 2
- Goal 3
**Data Elements**: [Key entities/fields]

## Use Case
**Title**: [e.g., Schedule an appointment]
**Description**: [Plain-language description of the feature]
**Rules**:
- Rule 1
- Rule 2
- Rule 3

### Test Cases
- Case 1: [Description]
- Case 2: [Description]
- Case 3: [Description]

### Success Criteria
- Criterion 1
- Criterion 2
- Criterion 3

## Overview
[2-3 sentence description of what this lab covers]

This is a foundational exercise focused on understanding core concepts
in isolation.

## Learning Goals
- Understand [concept 1]
- Practice [concept 2]
- Implement [concept 3]
- Apply [skill] to healthcare scenarios

## The Scenario
[Describe the real-world situation for this use case]

Example:
```
The healthcare clinic needs a simple way to track appointments.
For now, we just need to store appointments and perform basic operations.
```

## What You'll Build
[Describe what the learner will create]

## How to Use This Lab

1. **Read** `README.md` (this file) for overview
2. **Review** `tasks.md` for specific requirements
3. **Start** with `starter_code.py`
4. **Implement** each task one by one
5. **Run** `tests.py` to verify each task
6. **Compare** your solution with `solution/solution.py`

## Task Summary
- Task 1: [Brief description]
- Task 2: [Brief description]
- Task 3: [Brief description]
- Task 4: [Brief description]
- Task 5: [Brief description]

## Time Estimate
- Reading: 10 minutes
- Implementation: 60-90 minutes
- Testing & review: 15 minutes
- **Total**: 1.5-2 hours

## Success Criteria
- [ ] All tasks implemented
- [ ] Code runs without errors
- [ ] All test cases pass
- [ ] Outputs match expected results
- [ ] Code is readable with comments

## Key Concepts Practiced
- Concept 1 and how it's used
- Concept 2 and when to apply it
- Concept 3 in practical context

## Common Pitfalls
- Mistake 1: [Description and how to avoid]
- Mistake 2: [Description and how to avoid]

## Next Steps
After completing Lab Level 1:
1. Review your solution against provided solution
2. Move on to Lab Level 2 for more complexity
3. Compare implementations and understand differences

---
```

---

## Lab Level 2: README.md Template

```markdown
# Lab Level 2: [Title]
**Module**: [Module Name]
**Objective**: [What learner will achieve]
**Difficulty**: Intermediate
**Context**: Domain (Default: Healthcare; also eCommerce/Banking)

## Generic Information
**Problem Statement**: [What problem is being solved]
**Goals**:
- Goal 1
- Goal 2
- Goal 3
**Data Elements**: [Key entities/fields]

## Use Case
**Title**: [e.g., Manage doctor schedules]
**Description**: [Feature description with user actions]
**Rules**:
- Rule 1
- Rule 2
- Rule 3

### Test Cases
- Case 1: [Description]
- Case 2: [Description]
- Case 3: [Description]

### Success Criteria
- Criterion 1
- Criterion 2
- Criterion 3

## Overview
[2-3 sentence description]

This intermediate lab combines concepts from this module to solve
realistic healthcare problems.

## Learning Goals
- Combine [concept 1] with [concept 2]
- Implement [feature] with multiple data structures
- Practice [real-world scenario]
- Handle [edge cases]

## The Scenario
[More complex real-world situation]

Example:
```
The clinic has grown. We need a more sophisticated appointment system
that can handle multiple doctors, search appointments, and generate reports.
```

## What You'll Build
[More complex system description]

## Prerequisites
- Completed Lab Level 1 (or equivalent understanding)
- Understanding of [related concepts]

## How to Use This Lab

1. **Read** `README.md` for context
2. **Study** `tasks.md` for detailed requirements
3. **Start** with `starter_code.py`
4. **Implement** tasks, considering edge cases
5. **Run** `tests.py` frequently during implementation
6. **Check** `solution/solution.py` for reference if stuck

## Task Summary
- Task 1: [Description]
- Task 2: [Description]
- Task 3: [Description]
- Task 4: [Description]
- Task 5: [Description]
- Task 6: [Description]

## Time Estimate
- Reading & planning: 15 minutes
- Implementation: 120-180 minutes
- Testing & refinement: 30 minutes
- **Total**: 2.5-4 hours

## Success Criteria
- [ ] All tasks implemented correctly
- [ ] Handles common edge cases
- [ ] All test cases pass
- [ ] Code is well-structured
- [ ] Error handling for invalid inputs
- [ ] Comments explain complex logic

## Key Concepts Practiced
- How [concept 1] and [concept 2] work together
- Real-world problem solving
- Edge case handling
- Basic optimization

## Common Pitfalls
- Mistake 1: [How to avoid]
- Mistake 2: [How to avoid]
- Mistake 3: [How to avoid]

## Hints for Implementation
- Hint 1: [If stuck on task X]
- Hint 2: [If stuck on task Y]

## Progression
After Lab Level 2:
1. Your code should handle realistic scenarios
2. Ready for Lab Level 3's added complexity
3. You're building real skills toward capstone project

---
```

---

## Lab Level 3: README.md Template

```markdown
# Lab Level 3: [Title]
**Module**: [Module Name]
**Objective**: [What learner will achieve]
**Difficulty**: Advanced
**Context**: Domain (Default: Healthcare; also eCommerce/Banking)

## Generic Information
**Problem Statement**: [What problem is being solved]
**Goals**:
- Goal 1
- Goal 2
- Goal 3
**Data Elements**: [Key entities/fields]

## Use Case
**Title**: [e.g., End-to-end appointment management]
**Description**: [Production-grade feature description]
**Rules**:
- Rule 1
- Rule 2
- Rule 3

### Test Cases
- Case 1: [Description]
- Case 2: [Description]
- Case 3: [Description]

### Success Criteria
- Criterion 1
- Criterion 2
- Criterion 3

## Overview
[Comprehensive system description]

This advanced lab brings together all concepts from this module into
a production-grade implementation.

## Learning Goals
- Implement complete [feature] system
- Apply [best practices] in production code
- Handle [complex scenarios]
- Optimize for [performance/reliability]
- Ensure [security/validation]

## The Scenario
[Complex, realistic healthcare situation]

Example:
```
The clinic system needs a comprehensive appointment management system
with multiple user roles, validation, audit trails, and reporting.
This should be production-ready and handle edge cases gracefully.
```

## What You'll Build
[Complete system description with all features]

## Prerequisites
- Completed Lab Levels 1 & 2 (or equivalent understanding)
- Familiarity with [related modules/concepts]
- Understanding of [best practices]

## Architecture Overview
[Describe system structure if applicable]

```
Patient Appointments
├── Storage: Dictionary of lists by doctor
├── Validation: Input validation and sanitization
├── Operations: CRUD operations with error handling
├── Queries: Search, filter, sort functionality
└── Reporting: Generate various reports
```

## How to Use This Lab

1. **Study** the full system architecture
2. **Review** `tasks.md` for all requirements
3. **Plan** before coding (sketch structure)
4. **Implement** incrementally, testing frequently
5. **Refactor** for clarity and performance
6. **Document** with comments and docstrings
7. **Reference** `solution/solution.py` only if completely stuck

## Task Summary
- Task 1: [Description]
- Task 2: [Description]
- Task 3: [Description]
- Task 4: [Description]
- Task 5: [Description]
- Task 6: [Description]
- Task 7: [Description]
- Task 8: [Description]

## Time Estimate
- Understanding requirements: 20 minutes
- Planning & design: 30 minutes
- Implementation: 180-240 minutes
- Testing & refinement: 60 minutes
- Documentation: 30 minutes
- **Total**: 4-6 hours

## Success Criteria
- [ ] All tasks fully implemented
- [ ] Handles all edge cases gracefully
- [ ] All test cases pass with >80% coverage
- [ ] Code is production-quality
- [ ] Proper error handling and validation
- [ ] Well-documented with comments/docstrings
- [ ] Performance optimized
- [ ] Follows Python best practices (PEP 8)

## Key Concepts Practiced
- Complete [feature] implementation
- [Concept 1] in production context
- [Concept 2] with [Concept 3]
- Error handling and validation
- Performance optimization
- Code documentation

## Production Checklist
- [ ] All functions have docstrings
- [ ] Error handling for all inputs
- [ ] Input validation before processing
- [ ] Meaningful error messages
- [ ] Audit logging where applicable
- [ ] Performance optimization
- [ ] Test coverage >80%
- [ ] Code passes style checks

## Common Pitfalls
- Mistake 1: [Description and mitigation]
- Mistake 2: [Description and mitigation]
- Mistake 3: [Description and mitigation]

## Optimization Opportunities
[Discuss performance improvements, scalability considerations]

## Next Steps
After Lab Level 3:
1. Code is production-ready
2. Ready for capstone project integration
3. Solid foundation for advanced topics
4. Consider how this system could scale

---
```

---

## tasks.md Template Structure

### Lab Level 1: tasks.md

```markdown
# Lab Level 1 Tasks

## Task 1: [Task Title]
**Difficulty**: Easy
**Points**: 10

### Objective
[What learner should accomplish]

### Description
[Detailed task description with context]

### Requirements
- Requirement 1
- Requirement 2
- Requirement 3

### Example
\`\`\`
Input: [Example input]
Expected Output: [Example output]
\`\`\`

### Hints
- Hint 1: [If learner gets stuck]
- Hint 2: [Alternative approach]

---

## Task 2: [Task Title]
[Same structure as Task 1]

---
```

### Lab Level 2: tasks.md

```markdown
# Lab Level 2 Tasks

## Task 1: [More Complex Task]
**Difficulty**: Medium
**Points**: 15

### Objective
[What learner should accomplish]

### Description
[Detailed task description with real-world context]

### Requirements
- Requirement 1 (with specifics)
- Requirement 2 (with specifics)
- Requirement 3 (consider edge cases)

### Edge Cases to Handle
- Edge case 1
- Edge case 2

### Example
\`\`\`
Input: [Example]
Processing: [Steps involved]
Output: [Expected result]
\`\`\`

### Hints
- Hint 1: [Approach to take]
- Hint 2: [If stuck on specific part]

---
```

### Lab Level 3: tasks.md

```markdown
# Lab Level 3 Tasks

## Task 1: [Complex, Multi-Step Task]
**Difficulty**: Hard
**Points**: 20

### Objective
[What learner should accomplish]

### Description
[Detailed, realistic scenario]

### Requirements
- Requirement 1 (specific and detailed)
- Requirement 2 (consider performance)
- Requirement 3 (include error handling)
- Requirement 4 (add validation)

### Considerations
- Performance requirements
- Error handling expectations
- Edge cases and boundaries
- Security/validation aspects

### Test Cases
- Case 1: [Describe input and expected output]
- Case 2: [Edge case]
- Case 3: [Error condition]
- Case 4: [Performance-related test]

### Success Criteria
- Criterion 1: [Measurable]
- Criterion 2: [Testable]
- Criterion 3: [Observable]

### Hints
- Hint 1: [High-level approach]
- Hint 2: [If stuck on specific challenge]

---

## Lab Focus Strategy (Unit vs Module)

### Recommendation: Module-Focused Labs with Optional Unit Micro-Labs
- **Primary**: Keep labs module-focused to encourage synthesis across units and avoid fragmentation.
- **Optional**: Add short unit-focused “micro-labs” for complex topics that benefit from isolated practice (e.g., `modules/oop/app_labs/micro/encapsulation/`).

### When to Use Unit Micro-Labs
- The unit introduces a foundational pattern (e.g., decorators, async tasks)
- Learners struggle to bridge theory to implementation
- The module has heavy integration and needs stepwise ramp-up

### Directory Guidance
```
modules/<module_name>/app_labs/
├── lab_1/
├── lab_2/
├── lab_3/
└── micro/              # optional
    ├── use_case_1/
    └── use_case_2/
```

### Rationale
- Module labs provide end-to-end, realistic scenarios
- Micro-labs provide focused practice on a single concept/use case
- Together they support both mastery and integration
```

---

## Starter Code Guidelines

### Lab Level 1: Starter Code
Provide significant scaffolding:

```python
def add_appointment(appointments_list, appointment_data):
    """
    Add an appointment to the list.
    
    Args:
        appointments_list: List to add to
        appointment_data: Appointment dictionary
    
    Returns:
        Updated list
    """
    # Your implementation here
    pass

def get_appointment_count(appointments_list):
    """
    Get total number of appointments.
    """
    pass

def print_appointments(appointments_list):
    """
    Print all appointments in formatted way.
    """
    pass

# Main execution
if __name__ == "__main__":
    # Initialize empty appointments list
    appointments = []
    
    # Your code here to test functions
```

### Lab Level 2: Moderate Scaffolding
Provide class structure but less detail:

```python
class AppointmentManager:
    def __init__(self):
        """Initialize the appointment manager."""
        self.appointments = {}  # Structure as needed
    
    def add_appointment(self, doctor_id, appointment):
        """Add appointment for doctor."""
        pass
    
    def search_by_patient(self, patient_id):
        """Search appointments by patient."""
        pass
    
    def generate_report(self):
        """Generate appointment report."""
        pass
```

### Lab Level 3: Minimal Scaffolding
Provide only imports and hints:

```python
"""
Complete Appointment Management System

Implement a production-grade appointment system with:
- Multiple data structures
- Comprehensive validation
- Error handling
- Reporting capabilities
- Audit trails
"""

# Your implementation here
```

---

## Test File Structure

### tests.py Organization

```python
"""
Test suite for [Lab Level X]

Tests validate:
- Basic functionality
- Edge cases
- Error handling (Lab 2+)
- Performance (Lab 3)
"""

import pytest
from starter_code import *

class TestLabLevel1:
    """Test basic functionality."""
    
    def test_task_1_basic(self):
        """Test basic task 1 functionality."""
        result = function_1()
        assert result == expected
    
    def test_task_1_edge_case(self):
        """Test edge case for task 1."""
        result = function_1(edge_input)
        assert result == expected

# More comprehensive tests for Lab 2 & 3
```

---

## Healthcare Context Integration

### Patient Appointment Domain
- Patient ID, name, contact info
- Doctor ID, specialty
- Appointment date/time
- Status (scheduled, completed, cancelled)
- Notes/descriptions

### Common Operations
- Schedule appointment
- Cancel appointment
- Reschedule appointment
- View doctor schedule
- Find available slots
- Generate reports
- Handle conflicts/errors

### Data Structures Used
```python
# Simple representation
appointment = {
    "patient_id": 101,
    "doctor_id": 201,
    "date": "2024-01-15",
    "time": "10:00",
    "status": "scheduled"
}

# More complex
schedule = {
    (doctor_id, date): [appointments],
    # ...
}
```

---

## Quality Standards

### Content Requirements
- ✅ Clear progression from Lab 1 → 2 → 3
- ✅ Each level standalone but related
- ✅ Healthcare context consistent
- ✅ Tasks are well-defined and achievable
- ✅ Test cases comprehensive
- ✅ Solutions complete and correct

### Code Quality
- ✅ All code syntactically correct
- ✅ Follows Python conventions
- ✅ Proper error handling
- ✅ Well-commented
- ✅ Demonstrates best practices

### Documentation
- ✅ Clear README for each level
- ✅ Detailed tasks with examples
- ✅ Helpful hints without giving away solutions
- ✅ Comprehensive test cases
- ✅ Working solutions for reference

