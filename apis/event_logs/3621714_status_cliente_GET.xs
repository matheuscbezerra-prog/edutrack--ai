// Query all STATUS.CLIENTE records
query status_cliente verb=GET {
  api_group = "Event Logs"

  input {
  }

  stack {
    db.query "STATUS.CLIENTE" {
      return = {type: "list"}
    } as $status_cliente
  }

  response = $status_cliente
}