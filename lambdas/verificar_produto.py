import json
import os

def lambda_handler(pedido):
    caminho_arquivo = "data/produtos.json"

    # Carrega os produtos existentes
    try:
        with open(caminho_arquivo, "r", encoding="utf-8") as f:
            produtos = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        produtos = []

    produto_encontrado = None
    for p in produtos:
        if p["nome"].lower() == pedido["produto"]["nome"].lower():
            produto_encontrado = p
            break

    # Se o produto não existir, adiciona ao banco
    if not produto_encontrado:
        novo_produto = {
            "nome": pedido["produto"]["nome"],
            "localizacao": pedido["produto"]["localizacao"]
        }
        produtos.append(novo_produto)

        # Salva novamente o JSON atualizado
        os.makedirs(os.path.dirname(caminho_arquivo), exist_ok=True)
        with open(caminho_arquivo, "w", encoding="utf-8") as f:
            json.dump(produtos, f, ensure_ascii=False, indent=4)

        print(f"🆕 Produto '{novo_produto['nome']}' adicionado ao banco de produtos.")

        produto_encontrado = novo_produto
    else:
        print(f"🔎 Produto '{produto_encontrado['nome']}' encontrado no banco.")

    pedido["produto"]["localizacao"] = produto_encontrado["localizacao"]
    return pedido
