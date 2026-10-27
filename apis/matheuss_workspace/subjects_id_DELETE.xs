// Delete a subject record belonging to the authenticated user
query "subjects/{id}" verb=DELETE {
  api_group = "Matheus's Workspace"
  auth = "user"

  input {
    int id filters=min:1
  }

  stack {
    // Retrieve existing subject
    db.get subjects {
      field_name = "id"
      field_value = $input.id
    } as $existing_subject

    // Verify subject exists
    precondition ($existing_subject != null) {
      error_type = "notfound"
      error = "Subject not found"
    }

    // Verify authenticated user owns this subject
    precondition ($existing_subject.user_id == $auth.id) {
      error_type = "accessdenied"
      error = "Access denied: you do not own this subject"
    }

    // Delete subject
    db.del subjects {
      field_name = "id"
      field_value = $input.id
    }
  }

  response = null
  tags = ["edutrack", "subjects"]
}

