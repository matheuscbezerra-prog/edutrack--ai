// Create a new subject for the authenticated user
query subjects verb=POST {
  api_group = "Matheus's Workspace"
  auth = "user"

  input {
    text name filters=trim
    text teacher filters=trim
    int hours filters=min:0
  }

  stack {
    // Add new subject record associated with authenticated user
    db.add subjects {
      enforce_hidden_fields = false
      data = {
        name      : $input.name
        teacher   : $input.teacher
        hours     : $input.hours
        user_id   : $auth.id
        created_at: "now"
      }
    } as $new_subject
  }

  response = $new_subject
  tags = ["edutrack", "subjects"]
}

