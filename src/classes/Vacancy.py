from typing import List


class Vacancy:
    def __init__(self, name: str, salary: dict, employer: str, vac_url: str, id, employer_id):
        self.name = name
        self.salary = salary
        self.employer = employer
        self.vac_url = vac_url
        self.id = id
        self.employer_id = employer_id

    def to_dict(self) -> dict:
        """
        Словарь вакансий
        """
        vacancies = {
            "name": self.name,
            "ID": self.id,
            "employer_id": self.employer_id,
            "salary": self.salary,
            "employer": self.employer,
            "vac_url": self.vac_url
        }
        return vacancies

    def check_value_salary(self) -> list[dict | str]:
        """
        проверка значений словаря salary
        """
        vacancies = self.to_dict()
        salary_info = vacancies['salary']

        if not salary_info or salary_info == "None" or salary_info == 0:
            vacancies['salary'] = 0
            return [vacancies, "Нет данных по зарплате"]

        result = {}

        if salary_info.get("from") is not None and salary_info.get("from") != 0:
            result["from"] = {
                "salary": salary_info['from'],
                "currency": salary_info['currency']
            }

        if salary_info.get("to") is not None and salary_info.get("to") != 0:
            result["to"] = {
                "salary": salary_info['to'],
                "currency": salary_info['currency']
            }

        if result:
            return [vacancies, result]

        return [vacancies, "Некорректные данные по зарплате"]

    def __repr__(self):
        """
        Вывод данных
        """
        vacancy = self.to_dict()
        salary_info = self.check_value_salary()[1]
        if isinstance(salary_info, dict):
            salary_str = ", ".join(
                [f"{key.capitalize()}: {value['salary']} {value['currency']}" for key, value in salary_info.items()])
        else:
            salary_str = salary_info

        return f"Вакансия: {vacancy['name']}\n" \
               f"ID: {vacancy['ID']}\n" \
               f"Зарплата: {salary_str}\n" \
               f"Компания: {vacancy['employer']}\n" \
               f"Ссылка на вакансию: {vacancy['vac_url']}\n"
