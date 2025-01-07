from re import compile, IGNORECASE
from time import sleep
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

# Importações do projeto
from src.data_engineer_jobs_scraping.helpers import human_scroll, parse_relative_date
from src.data_engineer_jobs_scraping.login import linkedin_login

# Configuração inicial e login no LinkedIn
driver = linkedin_login()
sleep(10)  # Aguarde o carregamento da página

# Exibir o título da página atual
print("Página atual:", driver.title)

# Navegar para a página de busca de vagas no LinkedIn
driver.get("https://www.linkedin.com/jobs/search/?keywords=dados")
sleep(6)  # Aguarde o carregamento da página

# Localizar o elemento scrollable (lista de vagas) e realizar scroll
scrollable_element = driver.find_element(
    By.CSS_SELECTOR,
    "#main > div > div.scaffold-layout__list-detail-inner.scaffold-layout__list-detail-inner--grow > div.scaffold-layout__list > div"
)
human_scroll(driver, scrollable_element)

# Obter o HTML da lista de vagas
job_list_element = driver.find_element(By.XPATH, '//*[@id="main"]/div/div[2]/div[1]/div/ul')
html_trecho = job_list_element.get_attribute('outerHTML')
soup = BeautifulSoup(html_trecho, 'html.parser')

# Encontrar todas as vagas na lista
li_items = soup.find_all('li', id=compile('^ember', IGNORECASE))

# Iterar sobre as vagas para extrair informações
for job in li_items:
    try:
        # Extrair o título da vaga
        title = job.find('span', {'aria-hidden': 'true'}).find('strong')
        if title:
            print("Título da vaga:", title.get_text(strip=True))

        # Clicar na vaga para exibir detalhes
        element_id = job['id']
        job_ad = driver.find_element(By.ID, element_id)
        job_ad.click()
        sleep(2)  # Aguarde o carregamento dos detalhes da vaga

        # Obter o HTML atualizado e analisar os detalhes da vaga
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        job_details_div = soup.find('div', id='job-details').find('p', {'dir': 'ltr'})

        list_items = soup.find_all("li", class_="job-details-jobs-unified-top-card__job-insight")
        for item in [list_items[0]]: # Extrair a localidade, senioridade e período de trabalho
            spans = item.find_all("span", dir="ltr")
            for span in spans[:3]:
                print(span.get_text(strip=True))

        from_and_date_items = (soup
                               .find("div", class_="t-black--light mt2")
                               .find_all("span", class_="tvm__text tvm__text--low-emphasis")
                               )

        job_from = from_and_date_items[0].get_text(strip=True)
        raw_estimated_announcement_date = " ".join(from_and_date_items[2].get_text().split(" ")[-3:])
        print(raw_estimated_announcement_date)
        print(job_from)
        print(parse_relative_date(raw_estimated_announcement_date))

        # Extrair e exibir o texto dos detalhes da vaga
        if job_details_div:
            text = job_details_div.get_text(separator="\n").strip()
            print("Detalhes da vaga:")
            print(text)
        else:
            print("Detalhes da vaga não encontrados.")
        break

    except Exception as e:
        print(f"Erro ao processar a vaga: {e}")
        break  # Remova isso para continuar mesmo após erros

# Encerrar a execução com uma pausa longa para depuração (se necessário)
sleep(90)
