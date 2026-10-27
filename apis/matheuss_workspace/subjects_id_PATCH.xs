// Edit a subject record belonging to the authenticated user
query "subjects/{id}" verb=PATCH {
  api_group = "Matheus's Workspace"
  auth = "user"

  input {
    int id filters=min:1
    text name? filters=trim
    text teacher? filters=trim
    int hours? filters=min:0
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

    util.get_raw_input {
      encoding = "json"
      exclude_middleware = false
    } as $raw_input

    // Update subject record with provided fields
    db.patch subjects {
      field_name = "id"
      field_value = $input.id
      data = `$input|pick:($raw_input|keys)`|filter_null|filter_empty_text
    } as $updated_subject
  }

  response = $updated_subject
  tags = ["edutrack", "subjects"]
}

