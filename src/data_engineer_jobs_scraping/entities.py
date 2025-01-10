from datetime import datetime
from hashlib import sha256

from sqlalchemy import create_engine, Column, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

Base = declarative_base()

class Job(Base):
    __tablename__ = 'jobs'

    id = Column(String, primary_key=True)  # Chave primária
    title = Column(String, nullable=False)
    company = Column(String, nullable=False)
    job_from = Column(String, nullable=False)
    job_additional_details = Column(String, nullable=True)
    description = Column(Text, nullable=True)
    announced_at = Column(Text, nullable=True)
    created_at = Column(DateTime, nullable=False)

    def __init__(self,
                 title: str,
                 company: str,
                 job_from: str,
                 job_additional_details: str,
                 description: str,
                 announced_at: str):
        self.id = self.generate_id(title, company, announced_at)
        self.title = title
        self.company = company
        self.job_from = job_from
        self.job_additional_details = job_additional_details
        self.description = description
        self.announced_at = announced_at
        self.created_at = datetime.now()

    def __str__(self):
        return (f"ID: {self.id}\n"
                f"Job Title: {self.title}\n"
                f"Company: {self.company}\n"
                f"Job from: {self.job_from}\n"
                f"Job additional details: {self.job_additional_details}\n"
                f"Description: {self.description}\n"
                f"Announced at: {self.announced_at}\n"
                f"Created at: {self.created_at.strftime('%Y-%m-%d')}")

    @staticmethod
    def generate_id(title: str, company: str, announced_at: str) -> str:
        hash_input = f"{title}#{company}#{announced_at}"
        return sha256(hash_input.encode('utf-8')).hexdigest()

# Criar a base de dados e a tabela
def setup_database(db: str) -> Session:
    # Criar o engine do SQLite
    dbs_mapping = {
        'duckdb': 'duckdb:///jobs.duckdb',
        'sqlite': 'sqlite:///jobs.db'
    }

    engine = create_engine(dbs_mapping.get(db))

    # Criar as tabelas definidas no modelo, se ainda não existirem
    Base.metadata.create_all(engine)

    # Retornar uma sessão para interagir com o banco de dados
    Session = sessionmaker(bind=engine)
    return Session()
