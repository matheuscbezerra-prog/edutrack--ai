# academic-tasks Specification

## Purpose

Define the CRUD REST API endpoints for managing academic tasks with strict user data isolation verified through subject ownership.

## ADDED Requirements

### Requirement: Authenticated user creates academic task
The system SHALL provide a POST `/academic_tasks` endpoint allowing authenticated users to create a task for a subject they own.

#### Scenario: Successfully create task for owned subject
- **WHEN** an authenticated user sends a POST request to `/academic_tasks` with task details and a `subject_id` belonging to the user
- **THEN** the system stores the academic task linked to the subject and returns the created task

#### Scenario: Reject task creation for subject owned by another user
- **WHEN** an authenticated user sends a POST request to `/academic_tasks` with a `subject_id` that does not belong to the user
- **THEN** the system rejects the creation request with an authorization error

### Requirement: Authenticated user lists their academic tasks
The system SHALL provide a GET `/academic_tasks` endpoint returning only academic tasks linked to subjects owned by the authenticated user.

#### Scenario: Query own academic tasks
- **WHEN** an authenticated user sends a GET request to `/academic_tasks`
- **THEN** the system returns only tasks whose associated `subject_id` belongs to the authenticated user

### Requirement: Authenticated user updates their academic task
The system SHALL provide a PATCH `/academic_tasks/{id}` endpoint allowing authenticated users to update only tasks belonging to subjects they own.

#### Scenario: Successfully update owned task
- **WHEN** an authenticated user sends a PATCH request to `/academic_tasks/{id}` for a task linked to a subject they own
- **THEN** the system updates the task record and returns the updated task

#### Scenario: Attempt to update task belonging to another user
- **WHEN** an authenticated user sends a PATCH request to `/academic_tasks/{id}` for a task linked to another user's subject
- **THEN** the system denies the update operation

### Requirement: Authenticated user deletes their academic task
The system SHALL provide a DELETE `/academic_tasks/{id}` endpoint allowing authenticated users to delete only tasks belonging to subjects they own.

#### Scenario: Successfully delete owned task
- **WHEN** an authenticated user sends a DELETE request to `/academic_tasks/{id}` for a task linked to a subject they own
- **THEN** the system removes the task record and returns a success response

#### Scenario: Attempt to delete task belonging to another user
- **WHEN** an authenticated user sends a DELETE request to `/academic_tasks/{id}` for a task linked to another user's subject
- **THEN** the system denies the deletion operation

