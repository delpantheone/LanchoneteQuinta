def test_put_produto_retorna_json_alterou_true(client):
    response = client.post("/produtos", json={"codigo": "1", "valor": 15, "tipo": 1, "desconto_percentual": 10})
    assert response.status_code == 200
    codigo = response.json()["codigo"]
    
    response2 = client.put(f"/produtos/{codigo}/valor", json={"novo_valor": 10})
    # print(response2.json())
    assert response2.json()["alterou"] == True