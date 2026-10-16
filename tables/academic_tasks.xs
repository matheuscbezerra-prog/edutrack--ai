// Stores academic tasks associated with a subject.
table academic_tasks {
  auth = false

  schema {
    int id {
      description = "Unique identifier for the academic task"
    }

    text title {
      description = "Title of the academic task"
    }

    text description {
      description = "Details about the academic task"
    }

    date due_date {
      description = "Date by which the academic task is due"
    }

    text status {
      description = "Current status of the academic task"
    }

    int subject_id {
      table = "subjects"
      description = "Reference to the subject associated with the task"
    }

    timestamp created_at?=now {
      description = "Timestamp when the academic task was created"
      visibility = "private"
    }
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree", field: [{name: "created_at", op: "desc"}]}
  ]
  guid = "a5g91ITbN3hIsbpmku1qYAdYaRc"
}
