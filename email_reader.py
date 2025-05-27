import win32com.client
from typing import Optional

class EmailReader:
    """
    Responsável por ler e-mails do Outlook Desktop e extrair o corpo HTML do e-mail relevante.
    """
    def __init__(self):
        self.outlook = win32com.client.Dispatch("Outlook.Application")
        self.namespace = self.outlook.GetNamespace("MAPI")

    def get_latest_relevant_email(self, subject_filter: str) -> Optional[str]:
        """
        Retorna o corpo HTML do e-mail mais recente cujo assunto contém o filtro fornecido.
        """
        inbox = self.namespace.GetDefaultFolder(6)  # 6 = Inbox
        messages = inbox.Items
        messages.Sort("[ReceivedTime]", True)
        for message in messages:
            try:
                if subject_filter in message.Subject:
                    return message.HTMLBody
            except Exception:
                continue
        return None
