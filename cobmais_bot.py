import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

class CobmaisBot:
    """
    Responsável por automatizar o login e a pesquisa de números no Cobmais.
    """
    def __init__(self):
        self.driver = None

    def setup_driver(self, headless: bool = False):
        chrome_options = Options()
        chrome_options.add_argument('--start-maximized')
        if headless:
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--disable-gpu')
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)

    def login(self, username: str, password: str):
        self.driver.get('https://app.cobmais.com.br/cob/login')
        print('Aguardando campo de usuário e senha...')
        user_field = WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.NAME, 'Username'))
        )
        pass_field = self.driver.find_element(By.NAME, 'password')
        user_field.send_keys(username)
        pass_field.send_keys(password)
        # Usa seletor alternativo para o botão de login
        login_button = self.driver.find_element(By.ID, 'Login')
        login_button.click()
        time.sleep(5)

    def search_number(self, number: str):
        self.driver.get('https://app.cobmais.com.br/cob/pesquisa')
        # Aguarda o campo de telefone estar disponível
        try:
            telefone_field = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.ID, 'txtTelefone'))
            )
        except Exception:
            print('Campo com id="txtTelefone" não está interagível.')
            raise
        telefone_field.clear()
        telefone_field.send_keys(number)
        # Clica no botão "Pesquisar"
        try:
            pesquisar_btn = self.driver.find_element(By.XPATH, "//button[contains(., 'Pesquisar')]")
        except Exception:
            print('Botão "Pesquisar" não encontrado. Verifique o seletor.')
            raise
        pesquisar_btn.click()
        # Aguarda resultados carregarem
        time.sleep(2)
        try:
            results_table = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'table'))
            )
            try:
                tbody = results_table.find_element(By.TAG_NAME, 'tbody')
                rows = tbody.find_elements(By.TAG_NAME, 'tr')
            except:
                rows = results_table.find_elements(By.TAG_NAME, 'tr')
            # Se não houver linhas de resultado, retorna None
            if not rows or (len(rows) == 1 and 'Visualizando' in rows[0].text):
                return None
            # Considera a primeira linha de dados
            first_data_row = rows[0]
            cells = first_data_row.find_elements(By.TAG_NAME, 'td')
            if len(cells) > 3:
                nome = cells[2].text.strip()
                cpf = cells[3].text.strip()
                if nome and cpf:
                    return {'cpf': cpf, 'nome': nome}
            return None
        except Exception:
            return None

    def quit(self):
        if self.driver:
            self.driver.quit()
