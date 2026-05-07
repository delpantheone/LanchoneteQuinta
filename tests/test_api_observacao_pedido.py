def test_deve_adicionar_observacao(client):
    r1 = client.post("/clientes", json={"cpf": "11122233344", "nome": "Cliente X"})
    assert r1.status_code == 200
    r2 = client.post(
        "/produtos",
        json={"codigo": "1", "valor": 15, "tipo": 1, "desconto_percentual": 10},
    )
    assert r2.status_code == 200
    cliente = r1.json()
    p1 = r2.json()
    r3 = client.post(
        "/lanchonete/pedidos",
        json={
            "cpf": cliente["cpf"],
            "cod_produto": p1["codigo"],
            "qtd_max_produtos": 10,
        },
    )
    assert r3.status_code == 200
    pedido = r3.json()

    response = client.post(
        f"/lanchonete/pedidos/{pedido['codigo']}/observacao",
        json={"observacao": "Sem cebola"},
    )

    assert response.status_code == 200

    data = response.json()
    assert data["mensagem"] == "Observação adicionada com sucesso"


def test_nao_deve_aceitar_observacao_vazia(client):
    r1 = client.post("/clientes", json={"cpf": "11122233344", "nome": "Cliente X"})
    assert r1.status_code == 200
    r2 = client.post(
        "/produtos",
        json={"codigo": "1", "valor": 15, "tipo": 1, "desconto_percentual": 10},
    )
    assert r2.status_code == 200
    cliente = r1.json()
    p1 = r2.json()
    r3 = client.post(
        "/lanchonete/pedidos",
        json={
            "cpf": cliente["cpf"],
            "cod_produto": p1["codigo"],
            "qtd_max_produtos": 10,
        },
    )
    assert r3.status_code == 200
    pedido = r3.json()

    response = client.post(
        f"/lanchonete/pedidos/{pedido['codigo']}/observacao",
        json={"observacao": ""},
    )

    assert response.status_code == 400

def test_nao_deve_adicionar_observacao_em_pedido_finalizado(client):
    r1 = client.post("/clientes", json={"cpf": "11122233344", "nome": "Cliente X"})
    assert r1.status_code == 200
    r2 = client.post(
        "/produtos",
        json={"codigo": "1", "valor": 15, "tipo": 1, "desconto_percentual": 10},
    )
    assert r2.status_code == 200
    cliente = r1.json()
    p1 = r2.json()
    r3 = client.post(
        "/lanchonete/pedidos",
        json={
            "cpf": cliente["cpf"],
            "cod_produto": p1["codigo"],
            "qtd_max_produtos": 10,
        },
    )
    assert r3.status_code == 200
    pedido = r3.json()

    r4 = client.post(f"/lanchonete/pedidos/{pedido['codigo']}/finalizar")
    assert r4.status_code == 200

    response = client.post(
        "/lanchonete/pedidos/1/observacao",
        json={
            "observacao": "Sem molho"
        }
    )

    assert response.status_code == 400
