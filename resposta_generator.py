import pandas as pd

class RespostaGenerator:
    """
    Responsável por gerar a resposta HTML formatada para envio por e-mail.
    """
    @staticmethod
    def gerar_resposta(df: pd.DataFrame) -> str:
        import re
        # Filtra apenas linhas onde 'numero' contém um número de telefone (pelo menos 8 dígitos seguidos ou padrão brasileiro)
        df_filtrado = df[df['numero'].astype(str).str.replace(r'\D', '', regex=True).str.len() >= 8]
        html = '''<html><body>
        <p>Prezados,</p>
        <p>Segue abaixo o resultado da verificação solicitada:</p>
        <table border="1" style="border-collapse:collapse;">
        <thead>
        <tr style="background-color:#14395B; color:white; text-align:center;">
            <th>EXCLUIR<br>Nº TEL/E-MAIL</th>
            <th>Status</th>
        </tr>
        </thead>
        <tbody>
'''
        for _, row in df_filtrado.iterrows():
            numero = row.get('numero', '')
            status = row.get('observacao', '')
            if status.lower().startswith('cliente encontrado') or status.lower().startswith('identificado'):
                status_text = 'Identificado e removido'
            else:
                status_text = 'Não identificado na nossa base'
            html += f'<tr style="background-color:#D9E7F6; text-align:center;">'
            html += f'<td>{numero}</td><td>{status_text}</td></tr>'
        html += '</tbody></table>'
        return html
