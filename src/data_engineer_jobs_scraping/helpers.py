from time import sleep
from datetime import date, datetime, timedelta

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement


def human_scroll(driver: WebDriver, element: WebElement = None, step=200, delay=0.1):
  if element:  # Scroll em um elemento específico
    last_height = driver.execute_script("return arguments[0].scrollHeight;", element)
    current_position = 0
    while current_position < last_height:
      current_position += step
      driver.execute_script("arguments[0].scrollTop = arguments[1];", element, current_position)
      sleep(delay)
  else:  # Scroll na página principal
    last_height = driver.execute_script("return document.body.scrollHeight")
    current_position = driver.execute_script("return window.pageYOffset")
    while current_position < last_height:
      current_position += step
      driver.execute_script("window.scrollTo(0, arguments[0]);", current_position)
      sleep(delay)


def parse_relative_date(relative_date: str) -> date:
  """
  Converte uma string relativa de tempo em uma data absoluta.

  Args:
      relative_date (str): Exemplo "há 1 mês", "há 3 semanas", "há 3 dias".

  Returns:
      datetime.date: Data correspondente ao tempo relativo informado.
  """
  # Obter a data atual
  today = datetime.today().date()

  # Mapear palavras para os intervalos de tempo
  time_units = {
    "mês": 30,  # Aproximado como 30 dias
    "meses": 30,
    "semana": 7,
    "semanas": 7,
    "dia": 1,
    "dias": 1
  }

  # Remover a palavra "há" e espaços extras
  cleaned_str = relative_date.replace("há", "").strip()

  # Separar o número e a unidade
  parts = cleaned_str.split(" ")
  if len(parts) != 2:
    raise ValueError(f"Formato inválido: {relative_date}. Use strings como 'há 3 dias', 'há 1 mês'.")

  # Obter o valor e a unidade
  try:
    value = int(parts[0])
  except ValueError:
    raise ValueError(f"Não foi possível interpretar o número: {parts[0]}")

  unit = parts[1]
  if unit not in time_units:
    raise ValueError(f"Unidade de tempo desconhecida: {unit}")

  # Calcular a data
  days_to_subtract = value * time_units[unit]
  calculated_date = today - timedelta(days=days_to_subtract)

  return calculated_date


def parse_job_details(details_list):
  """
  Parseia os detalhes de uma vaga do LinkedIn a partir de uma lista de strings,
  mapeando informações como local de trabalho, tipo de emprego e senioridade.
  """
  mapping = {
    "Remoto": "local_de_trabalho",
    "Híbrido": "local_de_trabalho",
    "Presencial": "local_de_trabalho",
    "Tempo integral": "tipo_de_emprego",
    "Meio período": "tipo_de_emprego",
    "Freelance": "tipo_de_emprego",
    "Contrato": "tipo_de_emprego",
    "Estágio": "tipo_de_emprego",
    "Temporário": "tipo_de_emprego",
    "Estagiário": "senioridade",
    "Júnior": "senioridade",
    "Pleno": "senioridade",
    "Sênior": "senioridade",
    "Gerente": "senioridade",
    "Diretor": "senioridade"
  }

  # Estrutura inicial para armazenar os resultados
  parsed_details = {"local_de_trabalho": None, "tipo_de_emprego": None, "senioridade": None}

  # Itera sobre cada detalhe e aplica o mapeamento
  for detail in details_list:
    for key, category in mapping.items():
      if key in detail:
        parsed_details[category] = key

  return parsed_details

