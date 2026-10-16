// cadastro cliente
table CLIENTE {
  auth = false

  schema {
    int id
    timestamp created_at?=now {
      visibility = "private"
    }
  
    int user_id?
    text celular? filters=trim
    text CPF? filters=trim
    int status_cliente_id? {
      table = "STATUS.CLIENTE"
    }
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree", field: [{name: "created_at", op: "desc"}]}
  ]

  tags = ["módulo cadastro"]
  guid = "g30HYaD8WwQMvTfFXDMYk9IEZYg"
}