# academic-tasks Specification

## Purpose

Provides a persistent representation of lessons, exams, and assignments so that academic obligations can be associated with the subject they belong to.

## Requirements

### Requirement: Academic obligations store their identifying and tracking details
The system SHALL store each academic obligation with a title, description, due date, and status.

#### Scenario: Store an academic obligation
- **WHEN** an academic obligation is recorded with its details
- **THEN** the system stores and returns its title, description, due date, and status without changing their values

### Requirement: Academic obligations are associated with a subject
The system SHALL associate every academic obligation with an existing subject.

#### Scenario: Store an obligation for an existing subject
- **WHEN** an academic obligation is recorded with a valid subject reference
- **THEN** the system stores the reference to that subject with the obligation

#### Scenario: Reject a missing subject reference
- **WHEN** an academic obligation is recorded without a subject reference or with a reference to a subject that does not exist
- **THEN** the system does not store the obligation
