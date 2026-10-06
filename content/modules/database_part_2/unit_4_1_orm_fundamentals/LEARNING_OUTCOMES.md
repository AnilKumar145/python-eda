# Learning Outcomes: Unit 4.1 - ORM Fundamentals

By the end of this unit, you will be able to:

1. **Articulate ORM Principles & Trade-offs**: Understand the Object-Relational Impedance Mismatch, when to use an ORM versus raw SQL, and the layered architecture of SQLAlchemy (Engine, Dialect, Core Schema/Expression Language, and ORM).
2. **Master SQLAlchemy 2.0 Declarative Modeling**: Subclass `DeclarativeBase` and define schema entities using modern PEP 484 type annotations with `Mapped[...]` and `mapped_column()`.
3. **Configure Columns and Table Constraints**: Set column nullability, unique keys, primary keys, check constraints, default values, and foreign keys.
4. **Model Relationships Across Entities**: Establish parent-child navigation using `relationship()`, bidirectional synchronization via `back_populates`, and configure cascade behaviors.
5. **Bridge Objects and Tables**: Generate SQLite/PostgreSQL DDL schema automatically using `Base.metadata.create_all(engine)` and inspect table reflection.
