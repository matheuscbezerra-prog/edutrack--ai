// Add CLIENTE record
query cliente verb=POST {
  api_group = "Authentication"

  input {
    dblink {
      table = "CLIENTE"
    }
  }

  stack {
    db.add CLIENTE {
      enforce_hidden_fields = false
      data = {
        created_at       : "now"
        user_id          : $input.user_id
        celular          : $input.celular
        CPF              : $input.CPF
        status_cliente_id: $input.status_cliente_id
      }
    } as $model
  }

  response = $model
}