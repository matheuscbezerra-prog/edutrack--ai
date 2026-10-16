query CEP verb=GET {
  api_group = "Authentication"

  input {
    // CEP A SER PESQUISADO
    text CEP? filters=trim
  }

  stack {
  }

  response = null
  tags = ["módulo cadastro"]
  guid = "X1gSJogjaLJr3zE1Yf0iKehtP0I"
}