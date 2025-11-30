import os
import smtplib
import requests
from email.mime.text import MIMEText
from datetime import datetime

# --- SUAS CONFIGURAÇÕES ---
VALOR_ALVO_BRL = 21787.00  # Meta de venda (Topo recente + 5%)
EMAIL_DESTINO = "marcioramos1983@gmail.com" # Seu e-mail
# --------------------------

def verificar_preco():
    # API da CoinGecko
    url = "https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=brl"
    
    try:
        response = requests.get(url, timeout=10)
        dados = response.json()
        preco_atual = float(dados['ethereum']['brl'])
        
        hora_agora = datetime.now().strftime("%d/%m/%Y %H:%M")
        print(f"[{hora_agora}] ETH Atual: R$ {preco_atual:.2f} | Alvo: R$ {VALOR_ALVO_BRL:.2f}")

        # Lógica: Manda e-mail SEMPRE, mas muda o assunto e o texto
        if preco_atual >= VALOR_ALVO_BRL:
            # CENÁRIO DE VENDA (Meta atingida)
            assunto = f"🚀 VENDA AGORA! ETH bateu R$ {preco_atual:.2f}"
            mensagem_extra = "O Ethereum atingiu sua meta! Corre pra negociar e realizar o lucro."
            enviar_email(preco_atual, assunto, mensagem_extra)
        else:
            # CENÁRIO DE HOLD (Ainda não chegou)
            # Calcula quanto falta em porcentagem
            falta = VALOR_ALVO_BRL - preco_atual
            porcentagem = (falta / preco_atual) * 100
            
            assunto = f"📊 Relatório Diário: ETH a R$ {preco_atual:.2f}"
            mensagem_extra = f"Ainda não atingiu o alvo. Faltam R$ {falta:.2f} (+{porcentagem:.1f}%) para a meta. Segue o jogo."
            enviar_email(preco_atual, assunto, mensagem_extra)
            
    except Exception as e:
        print(f"Erro ao buscar preço: {e}")

def enviar_email(preco_atual, assunto_email, mensagem_corpo):
    # Pega as credenciais das Secrets do GitHub
    email_remetente = os.environ.get('EMAIL_USER')
    senha_app = os.environ.get('EMAIL_PASS')

    if not email_remetente or not senha_app:
        print("ERRO: Credenciais de e-mail não configuradas nas Secrets!")
        return

    corpo = f"""
    Fala Marcio!
    
    Resumo diário do seu monitoramento:
    
    -----------------------------------
    🎯 Meta de Venda: R$ {VALOR_ALVO_BRL:.2f}
    💎 Preço Atual:   R$ {preco_atual:.2f}
    -----------------------------------
    
    Mensagem do Robozão:
    {mensagem_corpo}
    """
    
    msg = MIMEText(corpo)
    msg['Subject'] = assunto_email
    msg['From'] = email_remetente
    msg['To'] = EMAIL_DESTINO

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(email_remetente, senha_app)
        server.send_message(msg)
        server.quit()
        print(f">> E-mail enviado: {assunto_email}")
    except Exception as e:
        print(f"Erro ao enviar e-mail: {e}")

if __name__ == "__main__":
    verificar_preco()
