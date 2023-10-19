class DBManager:
    """
    Класс DBManager для работы с данными в БД
    """
    def __init__(self, connection):
        self.connection = connection
        self.cursor = connection.cursor()

    def get_companies_and_vacancies_count(self):
        """получает список всех компаний и количество вакансий у каждой компании."""
        query = """
        SELECT employers.employer_name, COUNT(vacancies.vacancy_id) AS vacancy_count
        FROM employers
        LEFT JOIN vacancies ON employers.employer_id = vacancies.employer_id
        GROUP BY employers.employer_name;
        """
        self.cursor.execute(query)
        return [print(row) for row in self.cursor.fetchall()]

    def get_all_vacancies(self):
        """получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию."""
        query = """SELECT employers.employer_name, vacancies.vacancy_name, vacancies.salary_from, 
        vacancies.salary_to, vacancies.url_vacancy FROM employers JOIN vacancies ON employers.employer_id = 
        vacancies.employer_id;"""
        self.cursor.execute(query)
        return [print(row) for row in self.cursor.fetchall()]

    def get_avg_salary(self):
        """получает среднюю зарплату по вакансиям."""
        query = """
        SELECT AVG((salary_from + salary_to) / 2) AS average_salary
        FROM vacancies
        """
        self.cursor.execute(query)
        result = self.cursor.fetchone()
        return result[0] if result else 0

    def get_vacancies_with_higher_salary(self):
        """получает список всех вакансий, у которых зарплата выше средней по всем вакансиям."""
        avg_salary = self.get_avg_salary()
        query = f"""
        SELECT vacancy_id, employer_id, vacancy_name, salary_from, salary_to, currency, url_vacancy
        FROM vacancies
        WHERE (salary_from + salary_to) / 2 > {avg_salary};;
        """
        self.cursor.execute(query)
        return [print(row) for row in self.cursor.fetchall()]

    def get_vacancies_with_keyword(self, keyword):
        """получает список всех вакансий, в названии которых содержатся переданные в метод слова, например python."""
        query = f"""
        SELECT vacancy_id, employer_id, vacancy_name, salary_from, salary_to, currency, url_vacancy
        FROM vacancies
        WHERE vacancy_name LIKE '%{keyword}%';;
        """
        self.cursor.execute(query)
        return [print(row) for row in self.cursor.fetchall()]

    def close(self):
        """закрытие БД"""
        self.cursor.close()
        self.connection.close()
