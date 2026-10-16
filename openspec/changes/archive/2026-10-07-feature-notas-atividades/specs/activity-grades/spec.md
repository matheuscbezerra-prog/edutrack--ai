# activity-grades Specification

## Purpose
Define the specifications for recording and persisting student grades for specific academic activities in EduTrack AI.

## ADDED Requirements

### Requirement: Create activity_grades table
The system SHALL store activity grade records in an `activity_grades` table, capturing the teacher (`user_id`), student (`student_id`), activity reference (`task_id`), grade numeric value (`grade`), and optional feedback (`feedback`).

#### Scenario: Grade record persistence
- **WHEN** a teacher submits an evaluation for an activity
- **THEN** the system SHALL persist the grade associated with `user_id`, `student_id`, and `task_id`

### Requirement: Post activity grade API
The system SHALL provide an authenticated API endpoint `POST /activity_grades` that receives the evaluation details, verifies user authentication, and creates the grade record associated with the authenticated teacher's `user_id`.

#### Scenario: Successful grade submission
- **WHEN** an authenticated user sends a valid payload with `student_id`, `task_id`, and `grade` to `POST /activity_grades`
- **THEN** the system SHALL create the grade entry linked to the authenticated `user_id` and return the created record

