from dotenv import load_dotenv
from elasticsearch import Elasticsearch
from os import getenv


# Configuração do Elasticsearch
def setup_elasticsearch() -> Elasticsearch:
  load_dotenv()
  es = Elasticsearch(
    hosts=['http://localhost:9200'],
    api_key=getenv('ELASTICSEARCH_API_KEY')
  )
  return es
