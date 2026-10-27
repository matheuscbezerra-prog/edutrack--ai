# subjects Specification

## Purpose

Define the CRUD REST API endpoints for managing academic subjects with strict user data isolation.

## ADDED Requirements

### Requirement: Authenticated user creates subject
The system SHALL provide a POST `/subjects` endpoint allowing authenticated users to create a subject associated with their authenticated `user_id`.

#### Scenario: Successfully create a subject
- **WHEN** an authenticated user sends a POST request to `/subjects` with valid subject fields (`name`, `teacher`, `hours`)
- **THEN** the system stores the record with `user_id` set to the authenticated user's ID and returns the created subject

#### Scenario: Unauthenticated request is rejected
- **WHEN** an unauthenticated client sends a POST request to `/subjects`
- **THEN** the system rejects the request with an authentication error

### Requirement: Authenticated user lists their subjects
The system SHALL provide a GET `/subjects` endpoint returning only the subjects belonging to the authenticated user.

#### Scenario: Query own subjects
- **WHEN** an authenticated user sends a GET request to `/subjects`
- **THEN** the system returns only the subjects where `user_id` matches the authenticated user's ID

### Requirement: Authenticated user updates their subject
The system SHALL provide a PATCH `/subjects/{id}` endpoint allowing authenticated users to update only subjects they own.

#### Scenario: Successfully update owned subject
- **WHEN** an authenticated user sends a PATCH request to `/subjects/{id}` with valid update data for a subject they own
- **THEN** the system updates the subject record and returns the updated subject

#### Scenario: Attempt to update another user's subject
- **WHEN** an authenticated user sends a PATCH request to `/subjects/{id}` for a subject owned by another user
- **THEN** the system denies the operation and preserves existing data

### Requirement: Authenticated user deletes their subject
The system SHALL provide a DELETE `/subjects/{id}` endpoint allowing authenticated users to delete only subjects they own.

#### Scenario: Successfully delete owned subject
- **WHEN** an authenticated user sends a DELETE request to `/subjects/{id}` for a subject they own
- **THEN** the system removes the subject record and returns a success response

#### Scenario: Attempt to delete another user's subject
- **WHEN** an authenticated user sends a DELETE request to `/subjects/{id}` for a subject owned by another user
- **THEN** the system denies the operation and does not delete the record

