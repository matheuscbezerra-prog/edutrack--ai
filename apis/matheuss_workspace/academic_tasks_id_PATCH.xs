// Edit an academic task belonging to the authenticated user
query "academic_tasks/{id}" verb=PATCH {
  api_group = "Matheus's Workspace"
  auth = "user"

  input {
    int id filters=min:1
    text title? filters=trim
    text description? filters=trim
    date due_date?
    text status? filters=trim
    int subject_id? filters=min:1
  }

  stack {
    // Retrieve existing task
    db.get academic_tasks {
      field_name = "id"
      field_value = $input.id
    } as $existing_task

    // Verify task exists
    precondition ($existing_task != null) {
      error_type = "notfound"
      error = "Academic task not found"
    }

    // Verify authenticated user owns the current subject
    db.get subjects {
      field_name = "id"
      field_value = $existing_task.subject_id
    } as $current_subject

    precondition ($current_subject != null && $current_subject.user_id == $auth.id) {
      error_type = "accessdenied"
      error = "Access denied: you do not own the subject associated with this task"
    }

    // If changing subject_id, verify new subject is also owned by authenticated user
    conditional {
      if ($input.subject_id != null && $input.subject_id != $existing_task.subject_id) {
        db.get subjects {
          field_name = "id"
          field_value = $input.subject_id
        } as $new_subject

        precondition ($new_subject != null && $new_subject.user_id == $auth.id) {
          error_type = "accessdenied"
          error = "Access denied: you do not own the target subject"
        }
      }
    }

    util.get_raw_input {
      encoding = "json"
      exclude_middleware = false
    } as $raw_input

    // Update academic task with provided fields
    db.patch academic_tasks {
      field_name = "id"
      field_value = $input.id
      data = `$input|pick:($raw_input|keys)`|filter_null|filter_empty_text
    } as $updated_task
  }

  response = $updated_task
  tags = ["edutrack", "academic_tasks"]
}

