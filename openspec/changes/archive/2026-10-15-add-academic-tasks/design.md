# Design

## Context

See proposal.md for motivation. The repository uses XanoScript table definitions; `AGENTS.md` assigns table schema implementation to the Xano Table Designer and requires an `id` primary key. Existing local table definitions use integer IDs and represent references with a table mapping. The user authorized creating the local definition assuming the Xano workspace has a `subjects` table with an integer `id`; no such table definition is tracked in this repository, so the assumption cannot be independently verified here.

## Goals / Non-Goals

**Goals:**
- Define a table schema that stores the requested task details and links each record to one subject.
- Keep task status as text, as requested, without introducing an unapproved fixed status vocabulary.

**Non-Goals:**
- Create or modify the `subjects` table.
- Add APIs, frontend flows, or student ownership fields beyond the subject relationship.

## Decisions

- Add `id` as the integer primary key, following the repository's Xano table guidance and existing local table definitions.
- Model `title` as text, `description` as text, `due_date` as date, and `status` as text. Use a date rather than a timestamp because the requested value is a due date without a time.
- Model `subject_id` as a required integer reference mapped to `subjects`, following the user's assumption that the target table has an integer `id`. Confirm the actual table identifier and key before synchronizing to Xano; adjust the reference if the workspace differs.
- Keep `status` as text rather than an enum so that the schema does not enforce a lifecycle vocabulary the request did not define. Validation and user-facing status choices are outside this table-only change.
- Follow the existing table convention for a generated `created_at` timestamp if it applies to the target Xano workspace; it is metadata, not a replacement for any requested field.
- Delegate table implementation to the Xano Table Designer, as required by `AGENTS.md`, rather than authoring XanoScript directly.

## Risks / Trade-offs

- [The `subjects` table is not represented in this repository, so its existence and key cannot be independently verified] → Use the user-authorized assumption for the local definition and confirm the actual table and key before synchronizing; if absent, plan that table separately.
- [Free-form status text can contain inconsistent values] → Keep the column as requested and define a shared status vocabulary in a separate product/API decision if validation becomes necessary.
- [Student ownership is not stored directly on this table] → Rely on the associated subject's ownership/access rules; confirm that `subjects` enforces this relationship before exposing task operations.

## Migration Plan

1. Confirm the `subjects` table and its key in the target Xano workspace, updating the local reference if required.
2. Use the Xano Table Designer to synchronize `academic_tasks` with the agreed fields and subject reference.
3. Verify that records cannot reference a missing subject and that the requested values are preserved.
4. If rollback is required, export any task data that must be retained before removing the table.
