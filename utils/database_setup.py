import psycopg2


def connect_to_db():
    """Подключение к БД"""
    conn = psycopg2.connect(dbname='hh.ru vacancies',
                            user='postgres',
                            password='admin',
                            host='localhost',
                            port='5432')
    return conn


def create_employers_table(cursor):
    """Создание таблицы employers"""
    create_table_sql = """
    CREATE TABLE employers (
        employer_id SERIAL PRIMARY KEY,
        employer_name VARCHAR(200) NOT NULL
    );
    """
    cursor.execute(create_table_sql)


def create_vacancies_table(cursor):
    """Создание vacancies employers"""
    create_table_sql = """
        CREATE TABLE vacancies (
            vacancy_id SERIAL PRIMARY KEY,
    		employer_id INTEGER,
            FOREIGN KEY (employer_id) REFERENCES employers(employer_id),
            vacancy_name VARCHAR(200) NOT NULL,
            salary_from INTEGER DEFAULT 0, 
            salary_to INTEGER DEFAULT 0, 
            currency TEXT,
            url_vacancy TEXT
        )
        """

    cursor.execute(create_table_sql)


def insert_employers_data(cursor, vacancies):
    """Заполнение таблицы employers"""
    for item in vacancies:
        cursor.execute("SELECT EXISTS(SELECT 1 FROM employers WHERE employer_id = %s)", (item['employer_id'],))
        exists = cursor.fetchone()[0]

        # Если employer_id уже существует, пропускаем вставку
        if exists:
            print("Запись уже существует")
        else:
            # Выполняем INSERT
            cursor.execute("INSERT INTO employers (employer_id, employer_name) VALUES (%s, %s)",
                           (item['employer_id'], item['employer']))


def insert_vacancies_data(cursor, vacancies):
    """Заполнение таблицы vacancies"""
    for item in vacancies:
        if item['salary'] is not None:
            salary_from = item['salary'].get('from')
            salary_to = item['salary'].get('to')
            currency = item['salary'].get('currency')
        else:
            salary_from = None
            salary_to = None
            currency = None
        cursor.execute("INSERT INTO vacancies (vacancy_id, employer_id, vacancy_name, salary_from, "
                       "salary_to, currency, url_vacancy)"
                       "VALUES (%s, %s, %s, %s, %s, %s, %s)",
                       (item['id'], item['employer_id'], item['name'], salary_from, salary_to, currency,
                        item['vac_url']))


def add_data_to_db(vacancies):
    """Добавление таблицы в БД"""
    try:
        with connect_to_db() as conn:
            with conn.cursor() as cur:
                create_employers_table(cur)
                create_vacancies_table(cur)

                insert_employers_data(cur, vacancies)
                insert_vacancies_data(cur, vacancies)
    finally:
        conn.close()