import requests
import psycopg2
from typing import List, Dict, Any


def get_hh_data(employer_ids: List[str]) -> List[Dict[str, Any]]:
    "Функция получения данных с сайта hh.ru."

    for employer_id in employer_ids:
        params = {"text": {employer_id}, "page": 1, "per_page": 20}
        api = f'https://api.hh.ru/vacancies'
        response = requests.get(api, params=params)

    return response.json().get("items", [])


def create_database(database_name: str, params: dict):
    """Создание базы данных и таблиц для сохранения данных о работодателе и вакансиях."""

    conn = psycopg2.connect(dbname='postgres', **params)
    conn.autocommit = True
    cur = conn.cursor()

    cur.execute(f"DROP DATABASE {database_name}")
    cur.execute(f"CREATE DATABASE {database_name}")

    conn.close()

    conn = psycopg2.connect(dbname=database_name, **params)

    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE employers (
                company_id serial primary key,
                company_name VARCHAR(255) NOT NULL,
                company_url TEXT
            )
        """)

    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE vacancies (
                vacancy_id serial primary key,
                company_id INT REFERENCES employers (company_id),
                vacancy_name VARCHAR NOT NULL,
                salary_from INT,
                experience TEXT,
                requirement TEXT,
                schedule TEXT,
                vacancy_url TEXT               
            )
        """)

    conn.commit()
    conn.close()


def save_data_to_database(data: list[dict[str, Any]], database_name: str, params: dict) -> None:
    """Сохранение данных в базу данных."""

    conn = psycopg2.connect(dbname=database_name, **params)

    with conn.cursor() as cur:
        for i in data:
            cur.execute(
                """
                INSERT INTO employers (company_name, company_url)
                VALUES (%s, %s)
                RETURNING company_id;
                """,
                (i["employer"]["name"], i["employer"]["url"])
                )

            company_id = cur.fetchone()[0]

            if i['salary'] is None:
                cur.execute(
                    """
                    INSERT INTO vacancies (company_id, vacancy_name, salary_from, experience, requirement, schedule, vacancy_url)                        
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """,
                    (company_id,
                     i["name"],
                     0,
                     i["experience"]["name"],
                     i["snippet"]["requirement"],
                     i["schedule"]["name"],
                     i["employer"]["vacancies_url"])
                    )
            else:
                cur.execute(
                    """
                    INSERT INTO vacancies (company_id, vacancy_name, salary_from, experience, requirement, schedule, vacancy_url)                        
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """,
                    (company_id,
                     i["name"],
                     i["salary"]["from"],
                     i["experience"]["name"],
                     i["snippet"]["requirement"],
                     i["schedule"]["name"],
                     i["employer"]["vacancies_url"])
                    )

    conn.commit()
    conn.close()

