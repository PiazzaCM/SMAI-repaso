import MySQLdb as mysql
import pandas as pd
import numpy as np
import csv
import matplotlib.pyplot as plt

#funcion para conectar a la base de datos
def connect_db():
    try:
        db = mysql.connect("localhost", "root", "", "CompanyData")
        cursor = db.cursor()
        return db, cursor
    except mysql.Error as e:
        print("Error al conectar a la base de datos:", e)
        exit(1)


#funcion para crear la tabla
def create_table(cursor):
    try:
        cursor.execute("DROP TABLE IF EXISTS EmployeePerformance")
        cursor.execute("""
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


#funcion para importar datos desde un archivo CSV a la base de datos
def import_csv_to_db(cursor, db, csv_file):
    try:
        with open(csv_file, 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  
            datos = list(reader)

        insertar = """
        INSERT INTO EmployeePerformance (id, employee_id, depart, performance_score, years_with_company, salary)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.executemany(insertar, datos)
        db.commit()
        print("Datos importados correctamente a la base de datos.")
    except mysql.Error as e:
        db.rollback()
        print("Error al importar datos:", e)


#funcion para extraer datos de la base de datos
def fetch_data(cursor):
    try:
        query = "SELECT * FROM EmployeePerformance"
        df = pd.read_sql(query, cursor.connection)
        print("Datos extraídos correctamente.")
        return df
    except mysql.Error as e:
        print("Error al extraer datos:", e)
        exit(1)


#funcion para calcular estadisticas
def calculate_statistics(df):
    depart_group = df.groupby('depart')
    
    # Estadísticas del rendimiento
    stats = depart_group['performance_score'].agg(['mean', 'median', 'std']).rename(
        columns={'mean': 'Media', 'median': 'Mediana', 'std': 'Desviación estándar'})
    print("Estadísticas del rendimiento por departamento:\n", stats)
    
    # Estadísticas del salario
    salary_stats = df[['salary']].agg(['mean', 'median', 'std']).rename(
        columns={'mean': 'Media', 'median': 'Mediana', 'std': 'Desviación estándar'})
    print("Estadísticas del salario:\n", salary_stats)
    
    # Número de empleados por departamento
    empleados = depart_group.size().reset_index(name='Número de empleados')
    print("Número total de empleados por departamento:\n", empleados)


#funcion para calcular correlaciones
def calculate_correlations(df):
    correlacion_years_perf = df['years_with_company'].corr(df['performance_score'])
    correlacion_salary_perf = df['salary'].corr(df['performance_score'])
    
    print("Correlación entre years_with_company y performance_score:", correlacion_years_perf)
    print("Correlación entre salary y performance_score:", correlacion_salary_perf)




#funcion principal
def main():
    db, cursor = connect_db()
    create_table(cursor)
    import_csv_to_db(cursor, db, 'datos.csv')
    df = fetch_data(cursor)
    
    calculate_statistics(df)
    calculate_correlations(df)

    
    db.close()

if __name__ == "__main__":
    main()
