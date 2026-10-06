# Learning Outcomes: Unit 4.2 - SQLAlchemy Sessions

By the end of this unit, you will be able to:

1. **Understand the Unit of Work Pattern**: Explain how SQLAlchemy's `Session` acts as a staging area (Identity Map + Unit of Work) that batches database changes into atomic transactions.
2. **Deconstruct the Four Object States**: Track entity lifecycles across **Transient** (new Python object), **Pending** (added to session), **Persistent** (flushed/committed with primary key), and **Detached** (session closed).
3. **Control Session Transitions**: Master `session.add()`, `session.add_all()`, `session.flush()`, `session.commit()`, and `session.rollback()`.
4. **Execute Modern 2.0 Select Queries**: Use `select()` statements with `session.scalars().all()`, `session.scalars().first()`, and `session.scalar_one_or_none()`.
5. **Construct Relational Filters and Joins**: Combine predicates (`where()`, `and_()`, `or_()`, `like()`), sort results with `order_by(desc())`, and link related tables via `select(Model).join(RelatedModel)`.
