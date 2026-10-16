// Query all PAPEL records
query papel verb=GET {
  api_group = "Event Logs"

  input {
  }

  stack {
    db.query PAPEL {
      return = {type: "list"}
    } as $papel
  }

  response = $papel
  guid = "hQ8QJnRPb3exJvXMRuWQcmqiiT8"
}