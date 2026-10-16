// Query all CLIENTE records
query cliente verb=GET {
  api_group = "Event Logs"

  input {
  }

  stack {
    db.query CLIENTE {
      return = {type: "list"}
    } as $cliente
  }

  response = $cliente
  guid = "qbtjLgBS99KdcnSNmtoXjp8XATY"
}