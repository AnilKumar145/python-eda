---
title: "Radiology DICOM Study Metadata Store"
type: app_lab
module: database_part_1
unit: unit_3_3_working_with_postgresql
lab_number: 1
difficulty: easy
use_case: radiology_dicom_study_metadata_store
domain: healthcare
order: 1
duration_hours: 2
tags:
  topics:
    - database
    - postgresql
  subtopics:
    - json-metadata
    - decimal-costs
    - null-handling
    - dicom-store
---

# Lab Level 1: Radiology DICOM Study Metadata Store
**Module**: Database Programming — Part 1
**Objective**: Build a semi-structured radiology study repository handling flexible JSON DICOM headers, fixed-precision Decimal examination fees, and NULL-safe radiology report reading.
**Difficulty**: Easy
**Context**: Hospital Radiology PACS (Picture Archiving and Communication System)

## Generic Information
**Problem Statement**: Medical imaging studies (MRI, CT, Ultrasound) produce variable DICOM metadata tags (e.g. slice thickness, contrast volume, radiation dose). Storing these in rigid columns leads to schema maintenance friction. You will implement a `RadiologyStudyStore` supporting semi-structured study records, exact financial cost tracking with `Decimal`, and null-safe interpretation reporting using `COALESCE`.

**Goals**:
- Implement `RadiologyStudyStore` with SQLite backing.
- Support storing and parsing JSON study attributes.
- Use Python `Decimal` for procedure fee tracking.
- Query studies by modality and date with `COALESCE` status fallbacks.

## Use Case
**Title**: PACS Study Metadata Repository
**Description**: Ingest radiology studies with JSON metadata, query by modality, and report diagnosis summaries safely handling pending radiologist interpretations.

### Rules
- Metadata must be serialized to JSON on insert and deserialized to `dict` on query.
- Cost fees must use Python `Decimal`.
- Unreported studies (NULL `findings`) must return fallback `"[PENDING RADIOLOGIST REVIEW]"`.

### Test Cases
- Case 1: Ingest MRI and CT studies with JSON metadata. Verify exact dictionary retrieval.
- Case 2: Ingest study without findings. Verify `COALESCE` fallback returns `"[PENDING RADIOLOGIST REVIEW]"`.
- Case 3: Verify decimal financial fee preservation.
