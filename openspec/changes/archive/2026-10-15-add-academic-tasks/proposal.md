# Proposal

## Why

Students need a consistent way to record and manage lessons, exams, and assignments for each subject. A dedicated academic task capability will keep these obligations organized and associated with the relevant subject.

## What Changes

- Introduce the academic task capability and its `academic_tasks` table.
- Store each task's title, description, due date, status, and reference to its subject.

## Capabilities

### New Capabilities
- `academic-tasks`: Record and manage student academic obligations associated with subjects.

### Modified Capabilities
- None.

## Impact

- Xano table schema under `tables/`, with a relation to `subjects`.
- The repository currently has no tracked `subjects` table or OpenSpec capability. The referenced table must exist in the target Xano workspace before the relation is implemented; creating `subjects` is outside this change.
- No API or frontend changes are included in this table-focused change.
