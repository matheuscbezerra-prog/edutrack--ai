// Update CLIENTE record
query "cliente/{cliente_id}" verb=PUT {
  api_group = "Authentication"

  input {
    int cliente_id? filters=min:1
    dblink {
      table = "CLIENTE"
    }
  }

  stack {
    db.edit CLIENTE {
      field_name = "id"
      field_value = $input.cliente_id
      enforce_hidden_fields = false
      data = {
        user_id          : $input.user_id
        celular          : $input.celular
        CPF              : $input.CPF
        status_cliente_id: $input.status_cliente_id
      }
    } as $model
  }

  response = $model
  guid = "pur3FTVdRmhcm7Upi7c7szDTE54"
}