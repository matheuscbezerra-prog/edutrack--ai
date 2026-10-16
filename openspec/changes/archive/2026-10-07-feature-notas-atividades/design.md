# Design: feature-notas-atividades

## Architecture & Data Flow

This change introduces the backend structure required to allow instructors to assign grades to students for activities in EduTrack AI.

### Database Design (`activity_grades`)

Table: `activity_grades`
- `id`: integer, primary key, auto-increment
- `created_at`: timestamp, default `now`
- `user_id`: integer, reference to `user` (teacher/evaluator, authenticated user)
- `student_id`: integer, reference to `user` (student being evaluated)
- `task_id`: integer (reference to the academic task/activity)
- `grade`: decimal/numeric (grade assigned)
- `feedback`: text, optional (instructor comments)

Indexes:
- Primary key on `id`
- B-Tree index on `user_id`
- B-Tree index on `(task_id, student_id)`

### API Specification

#### `POST /activity_grades`
- **Authentication**: Required (`auth = true`)
- **Payload**:
  - `student_id`: integer (required)
  - `task_id`: integer (required)
  - `grade`: decimal (required)
  - `feedback`: text (optional)
- **Logic**:
  1. Authenticate teacher context (`user_id = auth.id`).
  2. Insert new record into `activity_grades` associating `user_id` with the authenticated teacher.
  3. Return the created grade record.

