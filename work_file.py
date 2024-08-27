# def get_hh_data(employer_ids: List[str]) -> List[Dict[str, Any]]:
#     "Функция получения данных о вакансии и компании по отдельности с сайта hh.ru."
#     params = {"page": 1, "per_page": 10}
#     data = []
#     vacancies = []
#     employers = []
#
#     for employer_id in employer_ids:
#         # получаем данные о компаниях
#         api_url_emp = f"https://api.hh.ru/employers?text={employer_id}"
#         employer_info = requests.get(api_url_emp, ).json()
#         employers.append(employer_info)
#
#         for employer in employer_info['items']:
#             employer_id = employer['id']
#
#             # получаем данные о вакансии
#             api_url = f"https://api.hh.ru/vacancies/{employer_id}"
#             vacancies_info = requests.get(api_url, params=params).json()
#             vacancies.append(vacancies_info)
#
#     data.append({
#         'employers': employers,
#         'vacancies': vacancies
#     })
#     return data


# def create_database(database_name: str, params: dict):
#     """Создание базы данных и таблиц для сохранения данных о работодателе и вакансиях."""
#
#     conn = psycopg2.connect(dbname='postgres', **params)
#     conn.autocommit = True
#     cur = conn.cursor()
#
#     cur.execute(f"DROP DATABASE {database_name}")
#     cur.execute(f"CREATE DATABASE {database_name}")
#
#     conn.close()
#
#     conn = psycopg2.connect(dbname=database_name, **params)
#
#     with conn.cursor() as cur:
#         cur.execute("""
#             CREATE TABLE employers (
#                 employer_id integer,
#                 employer_name VARCHAR(255) NOT NULL,
#                 vacancies_url TEXT,
#                 primary key (employer_id),
#                 unique (employer_name)
#             )
#         """)
#
#     with conn.cursor() as cur:
#         cur.execute("""
#             CREATE TABLE vacancies (
#                 vacancy_name VARCHAR NOT NULL,
#                 salary_from INT,
#                 experience TEXT,
#                 schedule TEXT,
#                 employer_id integer,
#                 employer_name VARCHAR(255) NOT NULL,
#                 foreign key(employer_id) REFERENCES employers(employer_id),
#                 foreign key(employer_name) REFERENCES employers(employer_name)
#             )
#         """)
#
#     conn.commit()
#     conn.close()


# def save_data_to_database(data: list[dict[str, Any]], database_name: str, params: dict) -> None:
#     """Сохранение данных в базу данных."""
#
#     conn = psycopg2.connect(dbname=database_name, **params)
#
#     with conn.cursor() as cur:
#         for i in data:
#             employers_data = i['employers']
#             for emp in employers_data:
#                 cur.execute(
#                     """
#                     INSERT INTO employers (employer_id, employer_name, vacancies_url)
#                     VALUES (%s, %s, %s)
#                     """,
#                     (emp[0]['id'], emp[0]['name'], emp[0]['vacancies_url'])
#                 )
#
#                 cur.execute("SELECT employer_id FROM employers WHERE employer_name = %s", (emp[0]['name'],))
#
#                 # employer_id = cur.fetchone()[0]
#                 # employer_name = emp['name']
#
#                 vacancies_data = i['vacancies']
#                 for vac in vacancies_data:
#                     if vac['salary'] is None:
#                         cur.execute(
#                             """
#                             INSERT INTO vacancies (employer_id, employer_name, vacancy_name, salary_from, experience, schedule)
#                             VALUES (%s, %s, %s, %s, %s, %s)
#                             """,
#                             (emp[0]['id'], emp[0]['name'], vac['name'], 0, vac['experience']['name'], vac['schedule']['name'])
#                         )
#                     else:
#                         cur.execute(
#                             """
#                             INSERT INTO vacancies (employer_id, employer_name, vacancy_name, salary_from, experience, schedule)
#                             VALUES (%s, %s, %s, %s, %s, %s)
#                             """,
#                             (emp[0]['id'], emp[0]['name'], vac['name'], vac['salary']['from'],
#                             vac['experience']['name'], vac['schedule']['name'])
#                         )
#     conn.commit()
#     conn.close()
