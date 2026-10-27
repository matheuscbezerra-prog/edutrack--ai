// Add a new academic task linked to an owned subject
query academic_tasks verb=POST {
  api_group = "Matheus's Workspace"
  auth = "user"

  input {
    text title filters=trim
    text description? filters=trim
    date due_date
    text status?="pending" filters=trim
    int subject_id filters=min:1
  }

  stack {
    // Verify subject exists
    db.get subjects {
      field_name = "id"
      field_value = $input.subject_id
    } as $subject

    precondition ($subject != null) {
      error_type = "notfound"
      error = "Referenced subject not found"
    }

    // Verify authenticated user owns the referenced subject
    precondition ($subject.user_id == $auth.id) {
      error_type = "accessdenied"
      error = "Access denied: you do not own the referenced subject"
    }

    // Add new academic task
    db.add academic_tasks {
      enforce_hidden_fields = false
      data = {
        title      : $input.title
        description: $input.description
        due_date   : $input.due_date
        status     : $input.status
        subject_id : $input.subject_id
        created_at : "now"
      }
    } as $new_task
  }

  response = $new_task
  tags = ["edutrack", "academic_tasks"]
}

