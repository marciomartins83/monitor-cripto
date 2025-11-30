import os
import smtplib
import requests
from email.mime.text import MIMEText
from datetime import datetime

# --- SUAS CONFIGURAÇÕES AQUI ---
VALOR_ALVO_BRL = 25000.00  # <--- COLOCA AQUI O VALOR DO ETH PARA VENDER (EM REAIS)
EMAIL_DESTINO = "seu_email_aqui@gmail.com" # <--- QUEM VAI RECEBER O AVISO
# -------------------------------

def verificar_preco():
    # API da CoinGecko (Gratuita e sem chave)
    url = "https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=brl"
    
    try:
        response = requests.get(url, timeout=10)
        dados = response.json()
        preco_atual = float(dados['ethereum']['brl'])
        
        hora_agora = datetime.now().strftime("%d/%m/%Y %H:%M")
        print(f"[{hora_agora}] ETH Atual: R$ {preco_atual:.2f} | Alvo: R$ {VALOR_ALVO_BRL:.2f}")

        # Lógica: Se o preço atual for MAIOR ou IGUAL ao alvo, dispara o email
        if preco_atual >= VALOR_ALVO_BRL:
            enviar_email(preco_atual)
        else:
            print("Ainda não atingiu o alvo. Segue o jogo.")
            
    except Exception as e:
        print(f"Erro ao buscar preço: {e}")

def enviar_email(preco_atual):
    # Pega as credenciais das Secrets do GitHub (Segurança)
    email_remetente = os.environ.get('EMAIL_USER')
    senha_app = os.environ.get('EMAIL_PASS') # Senha de App do Google

    if not email_remetente or not senha_app:
        print("ERRO: Credenciais de e-mail não configuradas nas Secrets!")
        return

    assunto = f"🚀 VENDA AGORA! ETH bateu R$ {preco_atual:.2f}"
    corpo = f"""
    Fala Marcio!
    
    O Ethereum atingiu o preço que você queria.
    
    Meta: R$ {VALOR_ALVO_BRL:.2f}
    Atual: R$ {preco_atual:.2f}
    
    Corre pra vender!
    """
    
    msg = MIMEText(corpo)
    msg['Subject'] = assunto
    msg['From'] = email_remetente
    msg['To'] = EMAIL_DESTINO

    try:
        # Configuração para Gmail
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(email_remetente, senha_app)
        server.send_message(msg)
        server.quit()
        print(">> E-mail de alerta enviado com sucesso!")
    except Exception as e:
        print(f"Erro ao enviar e-mail: {e}")

if __name__ == "__main__":
    verificar_preco()
