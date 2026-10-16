// informações de pedido
table PAPEL {
  auth = false

  schema {
    int id
    timestamp created_at?=now {
      visibility = "private"
    }
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree", field: [{name: "created_at", op: "desc"}]}
  ]

  tags = ["módulo cadastro"]
  guid = "TIZ7feLZ8nqZR4cCnxRqwqWBzC0"
}