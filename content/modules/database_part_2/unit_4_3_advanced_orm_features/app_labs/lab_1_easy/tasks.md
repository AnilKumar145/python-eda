# Tasks: Patient Allergy Cross-Reference & Eager Loading Hub

## Task 1: Define Many-to-Many Declarative Schema
In `AllergyRegistryBase`:
1. Junction table `patient_allergy_links`:
   - `patient_id`: Integer, ForeignKey `patients.id`, ondelete `CASCADE`, primary key.
   - `allergy_id`: Integer, ForeignKey `allergies.id`, ondelete `CASCADE`, primary key.
2. `Allergen`:
   - Table `allergies`: `id` (int PK), `name` (str unique), `category` (str, e.g. "DRUG", "FOOD").
   - Relationship `patients` linked via `patient_allergy_links`.
3. `Patient`:
   - Table `patients`: `id` (int PK), `mrn` (str unique), `name` (str).
   - Relationship `allergies` linked via `patient_allergy_links`.

## Task 2: Implement Patient Allergy Service
In `PatientAllergyService`:
- `initialize_schema(engine)`: Create tables.
- `record_allergen(session, name, category)`: Insert allergen entity.
- `register_patient(session, mrn, name)`: Insert patient entity.
- `link_allergy(session, mrn, allergen_name)`: Look up patient and allergen; link them and commit.
- `get_patient_allergies_eager(session, mrn)`: Look up patient by MRN with allergies eagerly loaded via `selectinload()`. Return list of allergen names.
- `find_patients_allergic_to(session, allergen_name)`: Return all patients allergic to the given allergen using `join()`.
