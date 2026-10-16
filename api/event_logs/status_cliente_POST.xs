// Add STATUS.CLIENTE record
query status_cliente verb=POST {
  api_group = "Event Logs"

  input {
    dblink {
      table = "STATUS.CLIENTE"
    }
  }

  stack {
    db.add "STATUS.CLIENTE" {
      enforce_hidden_fields = false
      data = {created_at: "now"}
    } as $status_cliente
  }

  response = $status_cliente
  guid = "BUhkmVgWMWQ7vyDhLottbza5oW0"
}