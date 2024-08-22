import requests
import psycopg2
from typing import List, Dict, Any


def get_hh_data(employer_ids: List[str]) -> List[Dict[str, Any]]:
    "Функция получения данных с сайта hh.ru."

    params = {"page": 0, "per_page": 0}
    data = []
    vacancies = []
    employers = []

    for employer_id in employer_ids:
        api_url = f"https://api.hh.ru/vacancies/{employer_id}"

        # получаем данные о компании
        employer_info = requests.get(api_url, ).json()
        employers.append(employer_info['employer'])

        # получаем данные о вакансии
        vacancies_info = requests.get(api_url, params=params).json()
        vacancies.append(vacancies_info)

    data.append({
        'employers': employers,
        'vacancies': vacancies
    })
    return data


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
        cur.execute("""CREATE TABLE employers (employer_id SERIAL PRIMARY KEY, name VARCHAR(255) NOT NULL, vacancies_url TEXT, trusted TEXT)""")

    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE vacancies (
                vacancy_id SERIAL PRIMARY KEY,
                employer_id INT REFERENCES employers(employer_id),
                name VARCHAR NOT NULL,
                area VARCHAR (255) NOT NULL,
                salary_from TEXT,
                experience TEXT,
                schedule TEXT
            )
        """)

    conn.commit()
    conn.close()


def save_data_to_database(data: list[dict[str, Any]], database_name: str, params: dict) -> None:
    """Сохранение данных о работодателе в базу данных."""

    conn = psycopg2.connect(dbname=database_name, **params)

    with conn.cursor() as cur:
        for i in data:
            employers_data = i['employers']
            for emp in employers_data:
                cur.execute(
                    """
                    INSERT INTO employers (name, vacancies_url, trusted)
                    VALUES (%s, %s, %s)
                    RETURNING employer_id
                    """,
                    (emp['name'], emp['vacancies_url'], emp['trusted'])
                )
            employer_id = cur.fetchone()[0]
            vacancies_data = i['vacancies']
            for vac in vacancies_data:
                if vac['salary'] is None:
                    cur.execute(
                        """
                        INSERT INTO vacancies (employer_id, name, area, salary_from, experience, schedule)
                        VALUES (%s, %s, %s, %s, %s, %s)
                        """,
                        (employer_id, vac['name'], vac['area']['name'], 0,
                         vac['experience']['name'], vac['schedule']['name'])
                    )
                else:
                    cur.execute(
                        """
                        INSERT INTO vacancies (employer_id, name, area, salary_from, experience, schedule)
                        VALUES (%s, %s, %s, %s, %s, %s)
                        """,
                        (employer_id, vac['name'], vac['area']['name'], vac['salary']['from'],
                         vac['experience']['name'], vac['schedule']['name'])
                    )
    conn.commit()
    conn.close()



