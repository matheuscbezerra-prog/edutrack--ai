// Edit STATUS.CLIENTE record
query "status_cliente/{status_cliente_id}" verb=PATCH {
  api_group = "Event Logs"

  input {
    int status_cliente_id? filters=min:1
    dblink {
      table = "STATUS.CLIENTE"
    }
  }

  stack {
    util.get_raw_input {
      encoding = "json"
      exclude_middleware = false
    } as $raw_input
  
    db.patch "STATUS.CLIENTE" {
      field_name = "id"
      field_value = $input.status_cliente_id
      data = `$input|pick:($raw_input|keys)`|filter_null|filter_empty_text
    } as $status_cliente
  }

  response = $status_cliente
}