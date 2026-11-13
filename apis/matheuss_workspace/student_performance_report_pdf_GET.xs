// Download student academic performance report as PDF
query "student/performance_report_pdf" verb=GET {
  api_group = "Matheus's Workspace"
  auth = "user"

  input {
  }

  stack {
    // Retrieve authenticated student record
    db.get user {
      field_name = "id"
      field_value = $auth.id
      output = ["id", "name", "email", "created_at"]
    } as $student

    // Ensure student exists
    precondition ($student != null) {
      error_type = "notfound"
      error = "Student record not found"
    }

    // Retrieve subjects owned by authenticated student
    db.query subjects {
      where = $db.subjects.user_id == $auth.id
      sort = {
        created_at: "desc"
      }
      return = {type: "list"}
    } as $student_subjects

    // Retrieve academic tasks associated with student's subjects
    db.query academic_tasks {
      join = [
        {
          table = "subjects"
          where = $db.academic_tasks.subject_id == $db.subjects.id
        }
      ]
      where = $db.subjects.user_id == $auth.id
      sort = {
        created_at: "desc"
      }
      return = {type: "list"}
    } as $student_tasks

    // Set HTTP headers to instruct client to download PDF attachment
    util.set_header {
      value = "Content-Type: application/pdf"
      duplicates = "replace"
    }

    util.set_header {
      value = "Content-Disposition: attachment; filename=\"relatorio_desempenho.pdf\""
      duplicates = "replace"
    }

    // Prepare consolidated report payload
    var $report {
      value = {
        student : $student
        subjects: $student_subjects
        tasks   : $student_tasks
      }
    }
  }

  response = $report
  tags = ["edutrack", "reports"]
}
