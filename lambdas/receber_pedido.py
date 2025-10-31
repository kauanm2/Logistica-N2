from datetime import datetime

def lambda_handler(cliente, produto):
    print(f"📦 Pedido recebido: {produto['nome']} para {cliente['nome']}")
    return {
        "cliente": cliente,
        "produto": produto,
        "data_pedido": datetime.now().isoformat(timespec="seconds")
    }
