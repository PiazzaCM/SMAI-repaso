# advanced-data-analysis

Aquí tienes un ejemplo de README que explica el código en detalle:

---

# README

Este proyecto contiene un script en Python para gestionar datos de rendimiento de empleados desde una base de datos MySQL, calcular estadísticas descriptivas y generar visualizaciones. A continuación, se detalla el funcionamiento del código y cómo utilizarlo.

## Requisitos

- Python 3.x
- Paquetes: `MySQLdb`, `pandas`, `numpy`, `csv`, `matplotlib`
- Una base de datos MySQL en funcionamiento con un usuario que tenga permisos adecuados

## Instalación

1. **Instala las dependencias**:
   Asegúrate de tener las bibliotecas necesarias instaladas. Puedes instalarlas usando pip:
   ```bash
   pip install mysqlclient pandas numpy matplotlib
   ```

2. **Configura la base de datos**:
   Crea una base de datos MySQL llamada `CompanyData` antes de ejecutar el script. Asegúrate de tener un archivo CSV llamado `datos.csv` con los datos de los empleados.

## Código

### Funciones

1. **`connect_db()`**:
   Conecta a la base de datos MySQL y devuelve el objeto de conexión y el cursor.
   ```python
   def connect_db():
       try:
           db = mysql.connect("localhost", "root", "", "CompanyData")
           cursor = db.cursor()
           return db, cursor
       except mysql.Error as e:
           print("Error al conectar a la base de datos:", e)
           exit(1)
   ```

2. **`create_table(cursor)`**:
   Crea la tabla `EmployeePerformance` en la base de datos, eliminando cualquier tabla existente con el mismo nombre.
   ```python
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
   ```

3. **`import_csv_to_db(cursor, db, csv_file)`**:
   Importa datos desde un archivo CSV a la tabla `EmployeePerformance`.
   ```python
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
   ```

4. **`fetch_data(cursor)`**:
   Extrae todos los datos de la tabla `EmployeePerformance` y los carga en un DataFrame de pandas.
   ```python
   def fetch_data(cursor):
       try:
           query = "SELECT * FROM EmployeePerformance"
           df = pd.read_sql(query, cursor.connection)
           print("Datos extraídos correctamente.")
           return df
       except mysql.Error as e:
           print("Error al extraer datos:", e)
           exit(1)
   ```

5. **`calculate_statistics(df)`**:
   Calcula y muestra estadísticas descriptivas del rendimiento y del salario por departamento.
   ```python
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
   ```

6. **`calculate_correlations(df)`**:
   Calcula y muestra la correlación entre `years_with_company` y `performance_score`, así como entre `salary` y `performance_score`.
   ```python
   def calculate_correlations(df):
       correlacion_years_perf = df['years_with_company'].corr(df['performance_score'])
       correlacion_salary_perf = df['salary'].corr(df['performance_score'])
       
       print("Correlación entre years_with_company y performance_score:", correlacion_years_perf)
       print("Correlación entre salary y performance_score:", correlacion_salary_perf)
   ```

7. **`histograma_perfomance(df)`**:
   Genera un histograma del `performance_score` para cada departamento.
   ```python
   def histograma_perfomance(df):
       depart_group = df.groupby('depart')
       fig, ax = plt.subplots()
       for depart, data in depart_group:
           data['performance_score'].plot(kind='hist', ax=ax, label=depart, alpha=0.6, bins=15)
       ax.set_xlabel('performance_score')
       ax.set_ylabel('Frecuencia')
       ax.set_title('Histograma del performance_score por departamento')
       ax.legend(title='Departamento')
       plt.show()
   ```

8. **`yearsCompany_vs_perfomance(df)`**:
   Genera un gráfico de dispersión de `years_with_company` frente a `performance_score`.
   ```python
   def yearsCompany_vs_perfomance(df):
       fig, ax = plt.subplots()
       ax.scatter(df['years_with_company'], df['performance_score'], alpha=0.6)
       ax.set_xlabel('years_with_company')
       ax.set_ylabel('performance_score')
       ax.set_title('Gráfico de dispersión de years_with_company vs. performance_score')
       plt.show()  
   ```

9. **`salary_vs_perfomance(df)`**:
   Genera un gráfico de dispersión de `salary` frente a `performance_score`.
   ```python
   def salary_vs_perfomance(df):
       fig, ax = plt.subplots()
       ax.scatter(df['salary'], df['performance_score'], alpha=0.6)
       ax.set_xlabel('salary')
       ax.set_ylabel('performance_score')
       ax.set_title('Gráfico de dispersión de salary vs. performance_score')
       plt.show()
   ```

### Función Principal

La función principal coordina el flujo de trabajo del script, desde la conexión a la base de datos, la creación de la tabla, la importación de datos, la extracción de datos, hasta el cálculo de estadísticas y la generación de visualizaciones.

```python
def main():
    db, cursor = connect_db()
    create_table(cursor)
    import_csv_to_db(cursor, db, 'datos.csv')
    df = fetch_data(cursor)
    
    calculate_statistics(df)
    calculate_correlations(df)

    histograma_perfomance(df)
    yearsCompany_vs_perfomance(df)
    salary_vs_perfomance(df)
    
    db.close()

if __name__ == "__main__":
    main()
```

## Ejecución

1. **Prepara el entorno**: Asegúrate de que la base de datos MySQL esté en funcionamiento y de tener el archivo `datos.csv` en el mismo directorio que el script.
2. **Ejecuta el script**:
   ```bash
   python nombre_del_script.py
   ```

Este README proporciona una guía completa para entender y ejecutar el script de Python, incluyendo la configuración, el propósito de cada función y cómo ejecutar el código para obtener los resultados deseados.

---