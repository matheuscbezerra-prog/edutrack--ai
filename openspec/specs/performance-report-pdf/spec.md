# performance-report-pdf Specification

## Purpose

Define the generation of an academic performance report in PDF format via Python and the creation of an authenticated Xano endpoint allowing students to download their report file.

## Requirements

### Requirement: Generate Performance Report PDF via Python Script
The system SHALL provide a Python script that compiles student academic performance data (student details, subjects, tasks, and completion metrics) and generates a formatted PDF document.

#### Scenario: Successfully generate performance report PDF
- **WHEN** the Python script is executed with student data, subjects, and task progress
- **THEN** the system creates a valid PDF file at the target output path containing the formatted performance report

#### Scenario: Generate report for student without recorded tasks
- **WHEN** a student has registered subjects but no completed or pending tasks
- **THEN** the system generates a valid PDF indicating zero tasks and 0.0% completion without errors

### Requirement: Authenticated Xano Endpoint for Report Download
The system SHALL provide an authenticated GET endpoint in Xano allowing users to download their performance report PDF with appropriate response headers (`Content-Type: application/pdf` and `Content-Disposition: attachment`).

#### Scenario: Authenticated student downloads report
- **WHEN** an authenticated student requests the report download endpoint with a valid auth token
- **THEN** the system generates/retrieves the student's performance report PDF, sets HTTP headers for attachment download, and delivers the file content

#### Scenario: Unauthenticated request is rejected
- **WHEN** a request is made to the report download endpoint without valid authentication
- **THEN** the system rejects the request with an authentication error
