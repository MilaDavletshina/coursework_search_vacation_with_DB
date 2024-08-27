from config import config
from src.db_manager import DBManager
from src.utils import create_database, get_hh_data, save_data_to_database


def main():
    employer_ids = [
        "Яндекс",
        "Mail.ru",
        "Google",
        "Microsoft",
        "Facebook",
        "Apple",
        "Twitter",
        "Amazon",
        "Uber",
        "Airbnb",
    ]
    params = config()

    data = get_hh_data(employer_ids)

    create_database("hh", params)
    save_data_to_database(data, "hh", params)

    db = DBManager("hh", params)

    # # Вариант №1:
    #     print("Предлагаем Вашему вниманию следующую информацию на выбор:")
    #     print()
    #     print(f"1 - Список компаний и количество вакансий у каждой компании\n"
    #           f"2 - Список вакансий\n"
    #           f"3 - Средняя заработная плата по вакансиям\n"
    #           f"4 - Список вакансий с заработной платой выше средней\n"
    #           f"5 - Список вакансий по заданному слову")
    #
    #     user_input = int(input("Ведите ваш выбор: "))
    #
    #     if user_input == 1:
    #         emp_vac = db.get_companies_and_vacancies_count()
    #         print(f"Список компаний и количество вакансий у каждой компании: {emp_vac}")
    #     elif user_input == 2:
    #         all_vac = db.get_all_vacancies()
    #         print(f"Список вакансий: {all_vac}")
    #     elif user_input == 3:
    #         avg_salary = db.get_avg_salary()
    #         print(f"Средняя заработная плата по вакансиям: {avg_salary}")
    #     elif user_input == 4:
    #         salary_higher_than_avg = db.get_vacancies_with_higher_salary()
    #         print(f"Список вакансий с заработной платой выше средней: {salary_higher_than_avg}")
    #     elif user_input == 5:
    #         word = input("введите слово: ").lower()
    #         vac_word = db.get_vacancies_with_keyword(word)
    #         print(f"Список вакансий, в названии которых содержится переданное слово: {vac_word}")
    #     else:
    #         print("Попробуйте еще раз")

    # Вариант №2:
    print("Предлагаем Вашему вниманию следующую информацию:")
    print()

    emp_vac = db.get_companies_and_vacancies_count()
    print(f"Список компаний и количество вакансий у каждой компании: {emp_vac}")
    print()

    all_vac = db.get_all_vacancies()
    print(f"Список вакансий: {all_vac}")
    print()

    avg_salary = db.get_avg_salary()
    print(f"Средняя заработная плата по вакансиям: {avg_salary}")
    print()

    salary_higher_than_avg = db.get_vacancies_with_higher_salary()
    print(f"Список вакансий с заработной платой выше средней: {salary_higher_than_avg}")
    print()

    print("Список вакансий по заданному слову")
    word = input("введите слово: ").lower()
    vac_word = db.get_vacancies_with_keyword(word)
    print(
        f"Список вакансий, в названии которых содержится переданное слово: {vac_word}"
    )


if __name__ == "__main__":
    main()
