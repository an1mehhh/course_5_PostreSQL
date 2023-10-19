import requests

from src.class_abstractions.AbstractionsAPI import AbstractionsAPI


class HeadHunterAPI(AbstractionsAPI):

    def __init__(self):
        self.url = "https://api.hh.ru"

    @staticmethod
    def _get_experience(experience: str = None) -> str:
        match int(experience):
            case 1:
                return "noExperience"
            case 2:
                return "between1And3"
            case 3:
                return "between3And6"
            case 4:
                return "moreThan6"
            case 5:
                return None
            case _:
                print("Ошибка ввода")
                return "between1And3"

    def _get_city(self, city: str) -> str:
        if len(city) == 0:
            return None
        else:
            response = requests.get(f"{self.url}/areas").json()
            city = city.lower().title()

            for area in response:
                for country in area["areas"]:
                    for region in country["areas"]:
                        if region["name"] == city:
                            return region["id"]

    def get_vacancies(self, search_query: str, city: str = None, experience: str = None) -> list:

        response = requests.get(f"https://api.hh.ru/vacancies",
                                params={"text": search_query,
                                        "area": self._get_city(city),
                                        "experience": self._get_experience(experience),
                                        "per_page": 100})
        if response.status_code == 200:
            data = response.json()
            return data.get("items", [])
        else:
            print(f"Request failed with status code: {response.status_code}")

    def get_formatted_data_vacancies(self, search_query: str, city: str = None, experience: str = None) -> list:

        data_vacancies = self.get_vacancies(search_query, city, experience)
        vacancies = []
        for vac in data_vacancies:
            vacancies.append({
                "id": vac.get("id", "Нет данных."),
                "employer_id": vac.get("employer", "Нет данных.").get("id"),
                "name": vac.get('name', 'Нет данных.'),
                "company": vac.get('employer', 'Нет данных.').get('name', 'Нет данных.'),
                "experience": vac.get('experience', 'Нет данных.').get('name', 'Нет данных.'),
                "city": vac.get('area', {}).get('name', 'Нет данных.'),
                "vac_url": vac.get('alternate_url'),
                "salary": vac.setdefault("salary"),
            })

        return vacancies
