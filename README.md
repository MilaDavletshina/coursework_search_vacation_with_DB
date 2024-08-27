# Курсовая работа Coursework_search_vacancy_with_DB
## Программа для получения данных о компаниях и вакансиях с сайта hh.ru, проектирования таблиц в БД PostgreSQL и загрузка полученных данных в созданные таблицы.
### Описание:
Программа получает информацию о вакансиях с платформы hh.ru по названию компании.

Возможности:
- Получение списка компаний и количество вакансий у каждой компании;
- Получение списка вакансий;
- Получение средней заработной платы по вакансиям;
- Получение списка вакансий с заработной платой выше средней;
- Получение списка вакансий по заданному слову.

### Докуметнация:
- Данные загружаются с платформы `hh.ru`, используя `api` сервис;
- Все данные выгружаются в `json` формате;
- Взаимодействие с пользователем через консоль;
- Используется версия `python 3.12`;
- Установлено `poetry`.