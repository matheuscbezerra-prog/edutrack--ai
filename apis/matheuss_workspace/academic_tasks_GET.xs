// Query all academic tasks belonging to subjects owned by the authenticated user
query academic_tasks verb=GET {
  api_group = "Matheus's Workspace"
  auth = "user"

  input {
    int subject_id? filters=min:1
  }

  stack {
    db.query academic_tasks {
      join = [
        {
          table = "subjects"
          where = $db.academic_tasks.subject_id == $db.subjects.id
        }
      ]
      where = ($db.subjects.user_id == $auth.id) && ($input.subject_id == null || $db.academic_tasks.subject_id == $input.subject_id)
      sort = {
        created_at: "desc"
      }
      return = {type: "list"}
    } as $user_tasks
  }

  response = $user_tasks
  tags = ["edutrack", "academic_tasks"]
}

