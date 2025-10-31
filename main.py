import sys, os
import lambdas.direcionar_entrega

sys.path.append(os.path.dirname(__file__))

from lambdas.receber_pedido import lambda_handler as receber
from lambdas.verificar_produto import lambda_handler as verificar
from lambdas.direcionar_entrega import lambda_handler as direcionar

if __name__ == "__main__":
    cliente = {"nome": "Kauã Miranda", "lat": -22.9068, "lon": -45.1729}
    produto = {"nome": "Notebook Lenovo", "localizacao": {"lat": -23.5505, "lon": -46.6333}}

    pedido = receber(cliente, produto)
    pedido = verificar(pedido)
    entrega = direcionar(pedido)
