from src.entities import setup_database, Job
from typing import List, Type

from src.infra import setup_elasticsearch

session = setup_database('duckdb')

jobs: List[Type[Job]] = session.query(Job).all()
es = setup_elasticsearch()

for i, job in enumerate(jobs):
  job_data = {
    'id': job.id,
    'title': job.title,
    'company': job.company,
    'job_from': job.job_from,
    'job_additional_details': job.job_additional_details,
    'description': job.description,
    'announced_at': job.announced_at,
    'created_at': job.created_at.strftime('%Y-%m-%d %H:%M:%S')
  }
  es.index(index='jobs', document=job_data)
  print(i)
