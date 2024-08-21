from config import config
from utils import get_employer_data, get_vacancies, create_database


def main():

    # employer_data = get_employer_data
    # vacancies_data = get_vacancies
    params = config()
    create_database("hh", params)


if __name__ == '__main__':
    main()
