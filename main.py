import os
from dotenv import load_dotenv
import pandas as pd
import pyperclip
from email_reader import EmailReader
from html_parser import HtmlParser
from cobmais_bot import CobmaisBot
from resposta_generator import RespostaGenerator
from utils.helpers import preencher_observacao

load_dotenv()

SUBJECT_FILTER = "ENC: OUVIDORIA: EXCLUSÃO DE TELEFONES/ E-MAILS / SMS"

if __name__ == "__main__":
    # 1. Ler e-mail
    reader = EmailReader()
    html_content = reader.get_latest_relevant_email(SUBJECT_FILTER)
    if not html_content:
        print("Nenhum e-mail relevante encontrado.")
        exit(1)

    # 2. Extrair tabela
    parser = HtmlParser()
    df = parser.extract_table(html_content)
    if df is None:
        print("Não foi possível extrair a tabela do e-mail.")
        exit(1)

    # 3. Garantir colunas extras
    for col in ['cpf', 'nome', 'observacao']:
        if col not in df.columns:
            df[col] = ""

    # Diagnóstico: mostrar colunas extraídas
    print('Colunas extraídas da tabela:', list(df.columns))
    # Ajuste automático: tenta renomear coluna parecida
    numero_col = None
    for col in df.columns:
        if isinstance(col, str) and col.strip().lower() in ['numero', 'número', 'telefone', 'contato']:
            df.rename(columns={col: 'numero'}, inplace=True)
            numero_col = 'numero'
            break
    # Se não encontrou, tenta usar a primeira coluna se ela for o número
    if 'numero' not in df.columns:
        # Se a primeira coluna for int ou string, assume que é o número
        first_col = df.columns[0]
        print(f"Ajuste automático: usando a primeira coluna '{first_col}' como 'numero'.")
        df.rename(columns={first_col: 'numero'}, inplace=True)

    # Remove o número (61) 2099-6565 do DataFrame, independente do formato
    def normaliza_numero(num):
        import re
        return re.sub(r'\D', '', str(num))
    numero_ignorado = normaliza_numero('(61) 2099-6565')
    df = df[df['numero'].apply(lambda x: normaliza_numero(x) != numero_ignorado)].reset_index(drop=True)

    # 4. Login e pesquisa no Cobmais
    cobmais = CobmaisBot()
    cobmais.setup_driver(headless=True)
    try:
        username = os.getenv("COBMAIS_USERNAME")
        password = os.getenv("COBMAIS_PASSWORD")
        if not username or not password:
            print("Credenciais não encontradas no .env")
            exit(1)
        cobmais.login(username, password)
        resultados = {}
        for idx, row in df.iterrows():
            numero_pesquisado = str(row['numero'])
            print(f"Pesquisando número no Cobmais: {numero_pesquisado}")
            result = cobmais.search_number(numero_pesquisado)
            if result:
                resultados[idx] = {'cpf': result['cpf'], 'nome': result['nome'], 'encontrado': True}
            else:
                resultados[idx] = {'encontrado': False}
        df = preencher_observacao(df, resultados)
    finally:
        cobmais.quit()

    # 5. Gerar resposta e copiar
    resposta = RespostaGenerator.gerar_resposta(df)
    pyperclip.copy(resposta)
    print("Resposta gerada e copiada para a área de transferência!")
    # Atualiza o arquivo index.html com a nova resposta
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(resposta)
    print("Arquivo index.html atualizado com a última resposta.")