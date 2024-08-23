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
        # получаем данные о компании
        api_url_emp = f"https://api.hh.ru/employers/{employer_id}"
        employer_info = requests.get(api_url_emp, ).json()
        employers.append(employer_info)

        # получаем данные о вакансии
        api_url = f"https://api.hh.ru/vacancies/{employer_id}"
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
        cur.execute("""
            CREATE TABLE employers (
                employer_id SERIAL PRIMARY KEY, 
                employer_name VARCHAR(255) NOT NULL, 
                area VARCHAR (255) NOT NULL, 
                vacancies_url TEXT, 
                trusted TEXT, 
                open_vacancies INT
            )
        """)

    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE vacancies (
                vacancy_id SERIAL PRIMARY KEY,
                employer_id INT REFERENCES employers(employer_id),
                vacancy_name VARCHAR NOT NULL,
                salary_from TEXT,
                experience TEXT,
                schedule TEXT
            )
        """)

    conn.commit()
    conn.close()


def save_data_to_database(data: list[dict[str, Any]], database_name: str, params: dict) -> None:
    """Сохранение данных в базу данных."""

    conn = psycopg2.connect(dbname=database_name, **params)

    with conn.cursor() as cur:
        for i in data:
            employers_data = i['employers']
            for emp in employers_data:
                cur.execute(
                    """
                    INSERT INTO employers (employer_name, area, vacancies_url, trusted, open_vacancies)
                    VALUES (%s, %s, %s, %s, %s)
                    RETURNING employer_id
                    """,
                    (emp['name'], emp['area']['name'], emp['vacancies_url'], emp['trusted'], emp['open_vacancies'])
                )
                employer_id = cur.fetchone()[0]
            vacancies_data = i['vacancies']
            for vac in vacancies_data:
                if vac['salary'] is None:
                    cur.execute(
                        """
                        INSERT INTO vacancies (employer_id, vacancy_name, salary_from, experience, schedule)
                        VALUES (%s, %s, %s, %s, %s)
                        """,
                        (employer_id, vac['name'], 0,
                        vac['experience']['name'], vac['schedule']['name'])
                    )
                else:
                    cur.execute(
                        """
                        INSERT INTO vacancies (employer_id, vacancy_name, salary_from, experience, schedule)
                        VALUES (%s, %s, %s, %s, %s)
                        """,
                        (employer_id, vac['name'], vac['salary']['from'],
                        vac['experience']['name'], vac['schedule']['name'])
                    )
    conn.commit()
    conn.close()



