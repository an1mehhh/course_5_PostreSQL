from src.classes.DBManager import DBManager
from src.classes.Vacancy import Vacancy
from utils.database_setup import connect_to_db, add_data_to_db
from utils.utils import get_formatted_vacancies


def get_user_input(prompt: str, options=None):
    """
    Функция для получения ввода пользователя с опциональным ограничением по вариантам ответа.
    """
    while True:
        user_input = input(prompt)
        if options is None or user_input in options:
            return user_input
        else:
            print("Пожалуйста, введите корректный вариант.")


def methots_to_dbmanager(user_input, db):
    match int(user_input):
        case 1:
            db.get_companies_and_vacancies_count()
        case 2:
            db.get_all_vacancies()
        case 3:
            print(db.get_avg_salary())
        case 4:
            db.get_vacancies_with_higher_salary()
        case 5:
            keyword = input("Введите слово:")
            db.get_vacancies_with_keyword(keyword)
        case _:
            print("Ошибка ввода")


def user_interaction():
    """
    Консольный интерфейс для пользователя
    """

    city = input("Введите свой город:\n")
    query = input("Введите название профессии:\n")
    experience = get_user_input("Выберите требуемый опыт работы:\n"
                                "1. Без опыта\n"
                                "2. От 1 до 3 лет\n"
                                "3. От 3 до 6 лет\n"
                                "4. Более 6 лет\n")

    vacancies = get_formatted_vacancies(query, city, experience)
    vacancy_objects = [Vacancy(**vac) for vac in vacancies]

    # Вывод всех вакансий
    for vac in vacancy_objects:
        print(vac)

    while True:
        user_input = get_user_input("Что мне сделать?\n"
                                    "1. Создать таблицу в БД и внести данные.\n"
                                    "2. Проверить методы класса DBManager.\n"
                                    "3. exit\n")

        if user_input == "1":
            add_data_to_db(vacancies)

        elif user_input == "2":
            user_input = get_user_input("Какой метод проверим?\n"
                                        "1. get_companies_and_vacancies_count() — получает список всех компаний и "
                                        "количество вакансий у каждой компании.\n"
                                        "2. get_all_vacancies() — получает список всех вакансий с указанием "
                                        "названия компании, названия вакансии и зарплаты и ссылки на вакансию.\n"
                                        "3. get_avg_salary() — получает среднюю зарплату по вакансиям.\n"
                                        "4. get_vacancies_with_higher_salary() — получает список всех вакансий, "
                                        "у которых зарплата выше средней по всем вакансиям.\n"
                                        "5. get_vacancies_with_keyword() — получает список всех вакансий, "
                                        "в названии которых содержатся переданные в метод слова, например python.\n")

            if user_input:
                db = DBManager(connect_to_db())
                methots_to_dbmanager(user_input, db)
                continue
            else:
                break

        elif user_input == "3":
            print("До свидания!")
            break

        else:
            print("Ошибка ввода")
            break


if __name__ == "__main__":
    user_interaction()
