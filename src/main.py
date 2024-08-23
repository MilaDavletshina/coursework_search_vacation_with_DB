from src.utils import get_hh_data, create_database, save_data_to_database
from config import config


def main():
    employer_ids = ['10008770', '5667343', '10252469', '3522689', '960654', '11281625', '1568931', '1518573', '2792723', '10608879']
    params = config()

    data = get_hh_data(employer_ids)
    create_database('hh', params)
    save_data_to_database(data, 'hh', params)
    print(get_hh_data(employer_ids))


if __name__ == '__main__':
    main()
