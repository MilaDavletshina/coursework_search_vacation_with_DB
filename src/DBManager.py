import psycopg2


class DBManager():
    "Класс для подключения к БД PostgreSQL "

    def __init__(self, database_name, params):
        self.dbname = database_name
        self.conn = psycopg2.connect(dbname=database_name, **params)
        self.cur = self.conn.cursor()

    def get_companies_and_vacancies_count(self):
        "Функция получает список всех компаний и количество вакансий у каждой компании"
        self.cur.execute(f"select name, open_vacancies from employers where open_vacancies is not null")
        return self.cur.fetchall()


    def get_all_vacancies(self):
        "Функция получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию"
        pass

    def get_avg_salary(self):
        "Функция получает среднюю зарплату по вакансиям"
        pass

    def get_vacancies_with_higher_salary(self):
        "Функция получает список всех вакансий, у которых зарплата выше средней по всем вакансиям"
        pass

    def get_vacancies_with_keyword(self):
        "Функция получает список всех вакансий, в названии которых содержатся переданные в метод слова"
        pass

