// Query all subjects for the authenticated user
query subjects verb=GET {
  api_group = "Matheus's Workspace"
  auth = "user"

  input {
  }

  stack {
    // Retrieve subjects belonging exclusively to the authenticated user
    db.query subjects {
      where = $db.subjects.user_id == $auth.id
      sort = {
        created_at: "desc"
      }
      return = {type: "list"}
    } as $user_subjects
  }

  response = $user_subjects
  tags = ["edutrack", "subjects"]
}

