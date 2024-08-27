import psycopg2


class DBManager():
    "Класс для подключения к БД PostgreSQL "

    def __init__(self, database_name, params):
        self.dbname = database_name
        self.conn = psycopg2.connect(dbname=database_name, **params)
        self.cur = self.conn.cursor()

    def get_companies_and_vacancies_count(self):
        "Функция получает список всех компаний и количество вакансий у каждой компании"
        self.cur.execute(f"SELECT employers.company_name, COUNT(vacancies.vacancy_id) AS vacancy_count FROM employers LEFT JOIN vacancies ON employers.company_id = vacancies.company_id GROUP BY employers.company_id ORDER BY employers.company_name;")
        return self.cur.fetchall()

    def get_all_vacancies(self):
        "Функция получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию"
        self.cur.execute(f"select employers.company_name, vacancies.vacancy_name, vacancies.salary_from,  vacancies.vacancy_url	   from vacancies left join employers using (company_id) order by vacancies.vacancy_name desc")
        return self.cur.fetchall()

    def get_avg_salary(self):
        "Функция получает среднюю зарплату по вакансиям"
        self.cur.execute(f"select AVG(salary_from) as avg_salary from vacancies WHERE salary_from IS NOT NULL")
        return self.cur.fetchall()

    def get_vacancies_with_higher_salary(self):
        "Функция получает список всех вакансий, у которых зарплата выше средней по всем вакансиям"
        self.cur.execute(f"select vacancies.vacancy_name, vacancies.salary_from from vacancies where vacancies.salary_from > (select AVG(salary_from) from vacancies)")
        return self.cur.fetchall()

    def get_vacancies_with_keyword(self, word):
        "Функция получает список всех вакансий, в названии которых содержатся переданные в метод слова"
        query = """SELECT * FROM vacancies
                                WHERE LOWER(vacancy_name) LIKE %s"""
        self.cur.execute(query, ('%' + word.lower() + '%',))
        return self.cur.fetchall()

