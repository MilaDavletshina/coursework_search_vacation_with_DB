import requests
import json
import psycopg2

# Из функции get_employer_id
employer_ids = [10252469, 438441, 5530913, 4536063, 2307097, 1437541, 626544, 800646, 3160848, 4246570]


def get_employer_id():
    "Функция получения id работодателя с сайта hh.ru."
    API = f'https://api.hh.ru/employers'
    params = {"only_with_vacancies": True, "page": 5, "per_page": 10}
    headers = {"User-Agent": "HH-User-Agent"}

    response = requests.get(API, headers=headers, params=params)
    employer = response.json()["items"]

    return employer


# print(get_employer_id())


def get_employer_data():
    "Функция получения данных о работодателе по его id"
    employer_data = []

    for employer_id in employer_ids:
        API_id = f"https://api.hh.ru/employers/{employer_id}"

        responce = requests.get(API_id, ).json()
        employer_data.append(responce)

    return employer_data


def get_vacancies():
    "Функция просмотра вакансии по id работодателя"
    vacancies = []

    for vacancy_id in employer_ids:
        api_key = f"https://api.hh.ru/vacancies/{vacancy_id}"

        responce = requests.get(api_key, ).json()
        vacancies.append(responce)

    return vacancies


def create_database(database_name: str, params: dict):
    """Создание базы данных и таблиц для сохранения данных об организациях и вакансиях."""

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
                emp_id SERIAL PRIMARY KEY,
                employers_id INTEGER,
                name VARCHAR(255) NOT NULL,
                description TEXT,
                area VARCHAR(255),
                open_vacancies INTEGER,
                vacancies_url TEXT
            )
        """)

    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE vacancies (
                vacancies_id SERIAL PRIMARY KEY,
                emp_id INT REFERENCES employers(emp_id),
                name VARCHAR NOT NULL,
                area VARCHAR (255) NOT NULL,
                experience TEXT,
                schedule TEXT
            )
        """)

    conn.commit()
    conn.close()


