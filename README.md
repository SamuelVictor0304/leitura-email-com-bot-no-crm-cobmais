# Automação de Verificação de Números - Outlook + Cobmais

Este projeto automatiza o processo de verificação de números telefônicos/e-mails recebidos por e-mail e gera uma resposta pronta com a situação de cada número, utilizando a base de dados do CRM Cobmais.

## Requisitos

- Python 3.8 ou superior
- Microsoft Outlook Desktop instalado
- Google Chrome instalado
- Acesso ao Cobmais

## Instalação

1. Clone este repositório
2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Crie um arquivo `.env` na raiz do projeto com suas credenciais:
```
COBMAIS_USERNAME=seu_usuario
COBMAIS_PASSWORD=sua_senha
```

## Uso

1. Certifique-se de que o Outlook Desktop está aberto
2. Execute o script:
```bash
python main.py
```

3. O script irá:
   - Ler o último e-mail com assunto "Solicitação de Verificação"
   - Extrair a tabela com os números
   - Verificar cada número no Cobmais
   - Gerar uma resposta formatada
   - Copiar a resposta para a área de transferência

4. Cole a resposta no Outlook e envie

## Formato do E-mail de Entrada

O e-mail deve conter uma tabela HTML com as seguintes colunas:
- numero: Número telefônico ou e-mail a ser verificado
- cpf: Será preenchido automaticamente
- nome: Será preenchido automaticamente
- observacao: Será preenchido automaticamente

## Observações

- O script deve ser executado manualmente quando necessário
- Certifique-se de que o Outlook está aberto antes de executar
- As credenciais do CRM devem ser mantidas seguras no arquivo .env 
