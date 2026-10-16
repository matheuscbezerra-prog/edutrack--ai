# Proposal: feature-notas-atividades

## Why
Currently, EduTrack AI lacks a structured backend mechanism for instructors to record academic evaluations for students on specific tasks/activities. Providing this functionality is essential to enable grading workflows, ensuring that student submissions and academic evaluations can be tracked and persisted reliably with proper ownership.

## What Changes
- Create a new database table `activity_grades` to store student grades, referencing the professor (`user_id`), student (`student_id`), activity (`task_id`), and grade values.
- Create an API endpoint `POST /activity_grades` allowing authenticated instructors to submit grades and optional feedback for a specific student and activity.

## Impact
- Extends the data model to persist evaluations linked to authenticated users.
- Introduces the `POST /activity_grades` endpoint adhering to authentication and `user_id` ownership standards.
- No breaking changes to existing tables or user authentication flows.

