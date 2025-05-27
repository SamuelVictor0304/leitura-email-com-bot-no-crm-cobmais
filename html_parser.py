from bs4 import BeautifulSoup
import pandas as pd
from io import StringIO
from typing import Optional
import re

class HtmlParser:
    """
    Responsável por extrair a tabela de números do corpo HTML do e-mail.
    """
    def extract_table(self, html_content: str) -> Optional[pd.DataFrame]:
        soup = BeautifulSoup(html_content, 'html.parser')
        tables = soup.find_all('table')
        for table in tables:
            df = pd.read_html(StringIO(str(table)))[0]
            # Verifica se alguma coluna parece ser de número
            for col in df.columns:
                if isinstance(col, str) and col.strip().lower() in ['numero', 'número', 'telefone', 'contato']:
                    # Remove o número (61) 2099-6565 se existir
                    def normaliza_numero(num):
                        import re
                        return re.sub(r'\D', '', str(num))
                    numero_ignorado = normaliza_numero('(61) 2099-6565')
                    df = df[df[col].apply(lambda x: normaliza_numero(x) != numero_ignorado)].reset_index(drop=True)
                    return df
        # Se não encontrar tabela válida, extrai números do texto bruto
        text = soup.get_text(separator=' ')
        # Regex para pegar números de telefone brasileiros (8+ dígitos)
        numeros = re.findall(r'(\d{2,3}[\s-]?)?(\d{4,5}[\s-]?\d{4})', text)
        numeros_extraidos = []
        def normaliza_numero(num):
            import re
            return re.sub(r'\D', '', str(num))
        numero_ignorado = normaliza_numero('(61) 2099-6565')
        for match in numeros:
            # Junta os grupos e remove espaços/hífens
            numero = ''.join(match).replace(' ', '').replace('-', '')
            if len(numero) >= 8 and normaliza_numero(numero) != numero_ignorado:
                numeros_extraidos.append(numero)
        if numeros_extraidos:
            df = pd.DataFrame({'numero': numeros_extraidos})
            return df
        return None
