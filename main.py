import MySQLdb as mysql
import pandas as pd
import numpy as np
import csv
import matplotlib.pyplot as plt


class DatabaseConnection:
    def __init__(self, host, user, password, database):
        """
        Constructor de la clase DatabaseConnection.
        Inicializa los parámetros de conexión a la base de datos y variables para la conexión y cursor.
        """
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.db = None
        self.cursor = None

    def connect(self):
        """
        Establece la conexión con la base de datos y crea un cursor para ejecutar consultas.
        Maneja errores de conexión e informa si hay problemas al conectar.
        """
        try:
            self.db = mysql.connect(self.host, self.user, self.password, self.database)
            self.cursor = self.db.cursor()
            print("Conexión a la base de datos establecida.")
        except mysql.Error as e:
            print("Error al conectar a la base de datos:", e)
            exit(1)

    def create_table(self):
        """
        Crea la tabla EmployeePerformance en la base de datos.
        Primero elimina cualquier tabla existente con ese nombre para evitar conflictos.
        """
        try:
            self.cursor.execute("DROP TABLE IF EXISTS EmployeePerformance")
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS EmployeePerformance (
                    id INT,
                    employee_id INT,
                    depart VARCHAR(255),
                    performance_score REAL,
                    years_with_company INT,
                    salary REAL
                )
            """)
            print("Tabla eliminada y creada correctamente.")
        except mysql.Error as e:
            print("Error al crear la tabla:", e)
            exit(1)

    def close(self):
        """
        Cierra la conexión a la base de datos si está abierta.
        """
        if self.db:
            self.db.close()
            print("Conexión a la base de datos cerrada.")

    def import_csv_to_db(self, csv_file):
        """
        Importa datos desde un archivo CSV a la tabla EmployeePerformance.
        Lee el archivo CSV, prepara los datos e inserta los registros en la base de datos.
        """
        try:
            with open(csv_file, 'r', newline='', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile)
                next(reader)  # Omitir la primera fila (cabeceras)
                datos = list(reader)

            insertar = """
            INSERT INTO EmployeePerformance (id, employee_id, depart, performance_score, years_with_company, salary)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            self.cursor.executemany(insertar, datos)
            self.db.commit()
            print("Datos importados correctamente a la base de datos.")
        except mysql.Error as e:
            self.db.rollback()
            print("Error al importar datos:", e)

    def fetch_data(self):
        """
        Extrae todos los datos de la tabla EmployeePerformance y los devuelve como un DataFrame de pandas.
        """
        try:
            query = "SELECT * FROM EmployeePerformance"
            df = pd.read_sql(query, self.cursor.connection)
            print("Datos extraídos correctamente.")
            return df
        except mysql.Error as e:
            print("Error al extraer datos:", e)
            exit(1)


class DataAnalysis:
    def __init__(self, df):
        """
        Constructor de la clase DataAnalysis.
        Inicializa el atributo df con el DataFrame proporcionado.
        """
        self.df = df

    def calculate_statistics(self):
        """
        Calcula estadísticas descriptivas para las columnas performance_score y salary,
        agrupadas por departamento. También cuenta el número de empleados por departamento.
        """
        depart_group = self.df.groupby('depart')

        # Estadísticas del rendimiento
        stats = depart_group['performance_score'].agg(['mean', 'median', 'std']).rename(
            columns={'mean': 'Media', 'median': 'Mediana', 'std': 'Desviación estándar'})
        print("Estadísticas del rendimiento por departamento:\n", stats)

        # Estadísticas del salario
        salary_stats = self.df[['salary']].agg(['mean', 'median', 'std']).rename(
            columns={'mean': 'Media', 'median': 'Mediana', 'std': 'Desviación estándar'})
        print("Estadísticas del salario:\n", salary_stats)

        # Número de empleados por departamento
        empleados = depart_group.size().reset_index(name='Número de empleados')
        print("Número total de empleados por departamento:\n", empleados)

    def calculate_correlations(self):
        """
        Calcula la correlación entre years_with_company y performance_score,
        y entre salary y performance_score.
        """
        correlacion_years_perf = self.df['years_with_company'].corr(self.df['performance_score'])
        correlacion_salary_perf = self.df['salary'].corr(self.df['performance_score'])

        print("Correlación entre years_with_company y performance_score:", correlacion_years_perf)
        print("Correlación entre salary y performance_score:", correlacion_salary_perf)

    def histograma_perfomance(self):
        """
        Genera un histograma de performance_score para cada departamento.
        """
        depart_group = self.df.groupby('depart')
        fig, ax = plt.subplots()
        for depart, data in depart_group:
            data['performance_score'].plot(kind='hist', ax=ax, label=depart, alpha=0.6, bins=15)
        ax.set_xlabel('performance_score')
        ax.set_ylabel('Frecuencia')
        ax.set_title('Histograma del performance_score por departamento')
        ax.legend(title='Departamento')
        plt.show()

    def yearsCompany_vs_perfomance(self):
        """
        Genera un gráfico de dispersión de years_with_company vs. performance_score.
        """
        fig, ax = plt.subplots()
        ax.scatter(self.df['years_with_company'], self.df['performance_score'], alpha=0.6)
        ax.set_xlabel('years_with_company')
        ax.set_ylabel('performance_score')
        ax.set_title('Gráfico de dispersión de years_with_company vs. performance_score')
        plt.show()

    def salary_vs_perfomance(self):
        """
        Genera un gráfico de dispersión de salary vs. performance_score.
        """
        fig, ax = plt.subplots()
        ax.scatter(self.df['salary'], self.df['performance_score'], alpha=0.6)
        ax.set_xlabel('salary')
        ax.set_ylabel('performance_score')
        ax.set_title('Gráfico de dispersión de salary vs. performance_score')
        plt.show()


def main():
    """
    Función principal que realiza las siguientes operaciones:
    - Establece la conexión con la base de datos.
    - Crea la tabla necesaria.
    - Importa datos desde un archivo CSV.
    - Extrae los datos en un DataFrame.
    - Realiza el análisis de datos.
    - Cierra la conexión a la base de datos.
    """
    db = DatabaseConnection("localhost", "root", "", "CompanyData")
    db.connect()
    db.create_table()
    db.import_csv_to_db('datos.csv')
    df = db.fetch_data()

    data_analysis = DataAnalysis(df)
    data_analysis.calculate_statistics()
    data_analysis.calculate_correlations()
    data_analysis.histograma_perfomance()
    data_analysis.yearsCompany_vs_perfomance()
    data_analysis.salary_vs_perfomance()

    db.close()


if __name__ == "__main__":
    main()
