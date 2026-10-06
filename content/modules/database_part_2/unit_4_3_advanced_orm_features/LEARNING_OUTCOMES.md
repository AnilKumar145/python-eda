# Learning Outcomes: Unit 4.3 - Advanced ORM Features

By the end of this unit, you will be able to:

1. **Model Many-to-Many Relationships**: Create secondary association tables (`Table("patient_allergies", Base.metadata, ...)`) and bind models via `relationship(secondary=...)`.
2. **Configure Fine-Grained Cascade Behaviors**: Select appropriate cascade options (`all`, `delete`, `delete-orphan`, `save-update`) to preserve relational integrity across complex entity graphs.
3. **Implement Hybrid Properties**: Author `@hybrid_property` getters and `@expression` decorators that calculate values in Python memory and compile down into database SQL queries seamlessly.
4. **Diagnose the N+1 Query Anti-Pattern**: Recognize how looping over lazy-loaded relationships triggers $1 + N$ individual SQL network round-trips.
5. **Optimize Queries with Eager Loading Strategies**: Choose correctly between `joinedload()` (SQL `LEFT OUTER JOIN` for 1-to-1 or many-to-1) and `selectinload()` (SQL `IN (...)` batch query for 1-to-many and many-to-many collections).
