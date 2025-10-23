import requests
import time
import os
import math

# 🔒 Variáveis de ambiente (você define no Render)
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Configurações
VARIACAO = 500  # diferença em dólares para avisar
API_URL = "https://api.coinbase.com/v2/prices/spot?currency=USD"

def get_btc_price():
    """Obtém o preço atual do Bitcoin pela API da Coinbase"""
    try:
        r = requests.get(API_URL)
        data = r.json()
        return float(data["data"]["amount"])
    except Exception as e:
        print("Erro ao buscar preço:", e)
        return None

def arredondar_preco(preco):
    """Arredonda o preço para múltiplos de 500"""
    return round(preco / VARIACAO) * VARIACAO

def send_message(text):
    """Envia mensagem para o Telegram"""
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": text}
    try:
        requests.post(url, data=payload)
    except Exception as e:
        print("Erro ao enviar mensagem:", e)

def main():
    """Loop principal do bot"""
    ultimo_preco = get_btc_price()
    if ultimo_preco:
        ultimo_preco = arredondar_preco(ultimo_preco)
        send_message(f"🚀 Bot iniciado! Preço atual do Bitcoin: ${int(ultimo_preco):,}")

    while True:
        time.sleep(30)  # verifica a cada 30 segundos
        preco_atual = get_btc_price()
        if preco_atual:
            preco_atual = arredondar_preco(preco_atual)
            if preco_atual != ultimo_preco:
                emoji = "🟢" if preco_atual > ultimo_preco else "🔴"
                send_message(f"{emoji} ${int(preco_atual):,}")
                ultimo_preco = preco_atual

if __name__ == "__main__":
    main()
