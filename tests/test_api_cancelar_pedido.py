def test_deve_cancelar_pedido_com_sucesso(client):
    r1 = client.post("/clientes", json={"cpf": "11122233344", "nome": "Cliente X"})
    assert r1.status_code == 200
    r2 = client.post("/produtos", json={"codigo": "1", "valor": 15, "tipo": 1, "desconto_percentual": 10})
    assert r2.status_code == 200
    r3 = client.post("/produtos", json={"codigo": "2", "valor": 10, "tipo": 1, "desconto_percentual": 5})
    assert r2.status_code == 200
    cliente = r1.json()
    p1 = r2.json()
    r4 = client.post("/lanchonete/pedidos", json={"cpf": cliente["cpf"], "cod_produto": p1["codigo"], "qtd_max_produtos": 10})
    assert r4.status_code == 200
    pedido = r4.json()
    p2 = r3.json()
    r5 = client.put(f"/lanchonete/pedidos/{pedido["codigo"]}/itens", json={"cod_produto": p2["codigo"]})
    assert r5.status_code == 200
    
    response = client.post("/lanchonete/pedidos/1/cancelar")

    assert response.status_code == 200

    data = response.json()

    assert data["ok"]
    assert data["mensagem"] == "Pedido cancelado com sucesso"

def test_nao_deve_cancelar_pedido_inexistente(client):
    response = client.post("/lanchonete/pedidos/999/cancelar")
    
    response.status_code == 400

    data = response.json()
    
    data["mensagem"] = "Pedido não encontrado ou não pode ser cancelado"

def test_nao_deve_cancelar_pedido_finalizado(client):
    r1 = client.post("/clientes", json={"cpf": "11122233344", "nome": "Cliente X"})
    assert r1.status_code == 200
    r2 = client.post("/produtos", json={"codigo": "1", "valor": 15, "tipo": 1, "desconto_percentual": 10})
    assert r2.status_code == 200
    cliente = r1.json()
    p1 = r2.json()
    r3 = client.post("/lanchonete/pedidos", json={"cpf": cliente["cpf"], "cod_produto": p1["codigo"], "qtd_max_produtos": 10})
    assert r3.status_code == 200
    pedido = r3.json()
    r3 = client.post(f"/lanchonete/pedidos/{pedido["codigo"]}/finalizar")
    assert r3.status_code == 200
    response = client.post(f"/lanchonete/pedidos/{pedido["codigo"]}/cancelar")
    assert response.status_code == 400

