from re import compile, IGNORECASE
from time import sleep
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import traceback

from src.data_engineer_jobs_scraping.entities import Job, setup_database
from src.data_engineer_jobs_scraping.helpers import human_scroll
from src.data_engineer_jobs_scraping.login import linkedin_login

# Configuração inicial e login no LinkedIn
driver = linkedin_login()
sleep(10)  # Aguarde o carregamento da página

def run_scraper(page: int = None):
    session = setup_database('duckdb')

    main_url = "https://www.linkedin.com/jobs/search/?keywords=dados"

    if page:
        main_url = main_url + f"&start={page}"

    print("Abrindo página de empregos...")
    # Navegar para a página de busca de vagas no LinkedIn
    driver.get(main_url)
    sleep(1)  # Aguarde o carregamento da página

    print("Arrastrando scroll para o final da página...")
    # Localizar o elemento scrollable (lista de vagas) e realizar scroll
    scrollable_element = driver.find_element(By.CSS_SELECTOR, "#main > div > div.scaffold-layout__list-detail-inner.scaffold-layout__list-detail-inner--grow > div.scaffold-layout__list > div")
    human_scroll(driver, scrollable_element)

    print("Listando as vagas...")
    # Obter o HTML da lista de vagas
    job_list_element = driver.find_element(By.XPATH, '//*[@id="main"]/div/div[2]/div[1]/div/ul')

    html_trecho = job_list_element.get_attribute('outerHTML')
    soup = BeautifulSoup(html_trecho, 'html.parser')

    # Encontrar todas as vagas na lista
    li_items = soup.find_all('li', id=compile('^ember', IGNORECASE))

    #page_button = driver.find_element(By.XPATH, f"//button[@aria-label='Página {page}']")
    #page_button.click()

    print("Iterando sobre as vagas...")
    # Iterar sobre as vagas para extrair informações
    for job in li_items:
        # Extrair o título da vaga
        title = job.find('span', {'aria-hidden': 'true'}).find('strong').get_text(strip=True)
        company = job.find('span', {'class': 'TPHCKUGOZGlriAhISbgBXENNUozRIVIhc'}).get_text(strip=True)
        url = driver.current_url

        # Clicar na vaga para exibir detalhes
        element_id = job['id']
        job_ad = driver.find_element(By.ID, element_id)
        job_ad.click()

        sleep(3)

        # Obter o HTML atualizado e analisar os detalhes da vaga
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")

        list_items = soup.find_all("li", class_="job-details-jobs-unified-top-card__job-insight")
        items = [item.get_text(strip=True) for item in list_items[0].find_all("span", dir="ltr")]
        job_additional_details = " # ".join(items)

        from_and_date_items = (soup
                               .find("div", class_="t-black--light mt2")
                               .find_all("span", class_="tvm__text tvm__text--low-emphasis")
                               )

        job_from = from_and_date_items[0].get_text(strip=True)
        announced_at = " ".join(from_and_date_items[2].get_text().split(" ")[-3:])

        job_details_div = soup.find('div', id='job-details').find('p', {'dir': 'ltr'})
        # Extrair e exibir o texto dos detalhes da vaga
        if job_details_div:
            description = job_details_div.get_text(separator="\n").strip()
            #print("Detalhes da vaga:")
            #print(text)
        else:
            description = None

        job = Job(
            title=title,
            company=company,
            job_from=job_from,
            description=description,
            url=url,
            announced_at=announced_at,
            job_additional_details=job_additional_details
        )

        # se já existe no banco de dados
        if session.query(Job).filter_by(id=job.id).first():
            continue
        else:
            session.add(job)
            session.commit()

    session.close()

try:
    run_scraper()
except:
    print(traceback.format_exc())
    while True:
        continue

for page in [p for p in range(25, 2600, 25)]:
    try:
        run_scraper(page)
        print("Aguardando a próxima página...")
        sleep(20)
    except Exception:
        print(traceback.format_exc())
        while True:
            continue
