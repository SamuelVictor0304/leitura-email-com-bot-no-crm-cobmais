def preencher_observacao(df, resultado_dict):
    """
    Atualiza o DataFrame com os resultados da busca no Cobmais.
    resultado_dict deve ser um dicionário no formato {index: {'cpf': ..., 'nome': ..., 'encontrado': True/False}}
    """
    for idx, resultado in resultado_dict.items():
        if resultado.get('encontrado'):
            df.at[idx, 'cpf'] = resultado['cpf']
            df.at[idx, 'nome'] = resultado['nome']
            df.at[idx, 'observacao'] = 'Cliente encontrado'
        else:
            df.at[idx, 'observacao'] = 'Cliente não identificado'
    return df
