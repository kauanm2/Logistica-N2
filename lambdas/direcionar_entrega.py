import json
import os
from datetime import datetime
import locale
from lambdas.utils import calcular_distancia_km


try:
    locale.setlocale(locale.LC_TIME, "pt_BR.UTF-8")
except:
    locale.setlocale(locale.LC_TIME, "Portuguese_Brazil.1252")


def encontrar_centro_mais_proximo(cliente, centros):
    menor_distancia = float('inf')
    centro_mais_proximo = None

    for centro in centros:
        distancia = calcular_distancia_km(
            cliente["lat"], cliente["lon"],
            centro["lat"], centro["lon"]
        )
        if distancia < menor_distancia:
            menor_distancia = distancia
            centro_mais_proximo = centro

    return centro_mais_proximo, menor_distancia


def lambda_handler(pedido):
    # 🔧 Define caminhos absolutos com base neste arquivo
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(base_dir, "..", "data")

    caminho_centros = os.path.join(data_dir, "centros.json")
    caminho_pedidos = os.path.join(data_dir, "pedidos.json")

    # garante que a pasta data exista
    os.makedirs(data_dir, exist_ok=True)

    # carregar centros logísticos
    try:
        with open(caminho_centros, "r", encoding="utf-8") as f:
            centros = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        raise FileNotFoundError(f"Arquivo de centros não encontrado em {caminho_centros}")

    # encontrar centro mais próximo
    centro, distancia = encontrar_centro_mais_proximo(pedido["cliente"], centros)

    # montar registro da entrega
    entrega = {
        "produto": pedido["produto"]["nome"],
        "origem_produto": pedido["produto"]["localizacao"],
        "destino_cliente": pedido["cliente"]["nome"],
        "centro_selecionado": centro["nome"],
        "distancia_cliente_km": round(distancia, 2),
        "data_processamento": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    }

    try:
        with open(caminho_pedidos, "r", encoding="utf-8") as f:
            pedidos = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        pedidos = []

    # adicionar novo pedido
    pedidos.append(entrega)

    # salvar pedidos
    with open(caminho_pedidos, "w", encoding="utf-8") as f:
        json.dump(pedidos, f, ensure_ascii=False, indent=4)

    print(f"🚚 Pedido direcionado ao centro: {centro['nome']}")
    print(f"📢 Notificação enviada para o galpão: {centro['nome']}")

    for k, v in entrega.items():
        print(f"{k}: {v}")

    return entrega
