from src.API.HeadHunterAPI import HeadHunterAPI


def get_data(query, city, experience):
    """Выбор API"""

    managers = [HeadHunterAPI()]
    vacancies = []
    for manager in managers:
        vacancies += manager.get_formatted_data_vacancies(query, city, experience)

    return vacancies


def get_formatted_vacancies(query: str, city: str, experience: str) -> list:
    """Обработка данных """
    vacancies = get_data(query, city, experience)
    formatted_vacancies = [{"name": vac['name'],
                            "id": vac["id"],
                            "employer_id": vac["employer_id"],
                            "salary": vac["salary"],
                            "employer": vac["company"],
                            "vac_url": vac["vac_url"]} for vac in vacancies]

    return formatted_vacancies


