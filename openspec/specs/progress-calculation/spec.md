# progress-calculation Specification

## Purpose

Define the logic for computing the progress percentage of an academic subject based on its tasks retrieved via CRUD endpoints, returning the results in a structured JSON format.

## Requirements

### Requirement: Fetch Tasks for a Subject via CRUD Endpoint
The system SHALL retrieve all academic tasks linked to a specified `subject_id` by making an authenticated request to the CRUD endpoint `GET /academic_tasks`.

#### Scenario: Successfully retrieve tasks for subject
- **WHEN** a valid `subject_id` and authentication token are provided
- **THEN** the system requests tasks from `GET /academic_tasks` filtering by `subject_id` and parses the returned task records

#### Scenario: Handle empty task list
- **WHEN** no tasks are found for the provided `subject_id`
- **THEN** the system handles the empty list gracefully without throwing an error

### Requirement: Calculate Progress Metrics
The system SHALL calculate the total number of tasks, the number of completed tasks, the number of pending tasks, and the completion percentage (`completed / total * 100.0`).

#### Scenario: Subject with completed and pending tasks
- **WHEN** a subject has 4 total tasks and 2 marked as completed
- **THEN** the system calculates `total_tasks` as 4, `completed_tasks` as 2, `pending_tasks` as 2, and `progress_percentage` as 50.0

#### Scenario: Subject with zero tasks
- **WHEN** a subject has 0 total tasks
- **THEN** the system calculates `total_tasks` as 0, `completed_tasks` as 0, `pending_tasks` as 0, and `progress_percentage` as 0.0 avoiding division by zero

### Requirement: Return Progress in JSON Format
The system SHALL return the calculated progress metrics as a valid JSON object containing `subject_id`, `total_tasks`, `completed_tasks`, `pending_tasks`, and `progress_percentage`.

#### Scenario: Format JSON output
- **WHEN** the progress metrics are computed
- **THEN** the system returns a JSON payload containing the fields `subject_id`, `total_tasks`, `completed_tasks`, `pending_tasks`, and `progress_percentage`
