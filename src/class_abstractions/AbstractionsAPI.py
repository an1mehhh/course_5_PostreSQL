from abc import ABC, abstractmethod
import requests


class AbstractionsAPI(ABC):

    @abstractmethod
    def get_vacancies(self, search_query: str, city: str = None, experience: str = None):
        pass

    @abstractmethod
    def get_formatted_data_vacancies(self, search_query: str, city: str = None, experience: str = None) -> list:
        pass