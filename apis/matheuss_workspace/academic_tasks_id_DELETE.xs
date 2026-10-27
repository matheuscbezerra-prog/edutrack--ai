// Delete an academic task belonging to the authenticated user
query "academic_tasks/{id}" verb=DELETE {
  api_group = "Matheus's Workspace"
  auth = "user"

  input {
    int id filters=min:1
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

    // Verify authenticated user owns the associated subject
    db.get subjects {
      field_name = "id"
      field_value = $existing_task.subject_id
    } as $subject

    precondition ($subject != null && $subject.user_id == $auth.id) {
      error_type = "accessdenied"
      error = "Access denied: you do not own the subject associated with this task"
    }

    // Delete academic task
    db.del academic_tasks {
      field_name = "id"
      field_value = $input.id
    }
  }

  response = null
  tags = ["edutrack", "academic_tasks"]
}

