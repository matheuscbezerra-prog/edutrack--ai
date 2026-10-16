# Tasks

## 1. Verify the subject dependency

- [x] 1.1 Apply the user-provided assumption that the local Xano workspace has `subjects` with an integer `id`; note that this assumption is not independently verifiable from tracked repository files.

## 2. Create the academic tasks table

- [x] 2.1 Use the Xano Table Designer to create `tables/academic_tasks.xs` with the `id` primary key, requested fields, and integer `subject_id` reference to `subjects`; verify the local definition follows existing table and reference conventions.

- [ ] 2.2 Confirm the actual `subjects` table identifier and key in Xano, adjust the local reference if needed, then synchronize the table definition; verify the target workspace reflects the schema.

## 3. Verify the table requirements

- [ ] 3.1 Verify in Xano that a linked academic task preserves its title, description, due date, status, and subject reference, and that a missing or invalid subject reference is rejected.
