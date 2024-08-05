import MySQLdb as mysql

# Conexión a la base de datos
try:
    db = mysql.connect("localhost", "root", "", "CompanyData")
    cursor = db.cursor()

    # Eliminar tabla si existe
    cursor.execute("DROP TABLE IF EXISTS EmployeePerformance")
    db.commit()
    print("Tabla eliminada correctamente.")

    # Crear tabla EmployeePerformance si no existe
    crear = """
    CREATE TABLE IF NOT EXISTS EmployeePerformance (
        id INT,
        employee_id INT,
        depart VARCHAR(255),
        performance_score REAL,
        years_with_company INT,
        salary REAL
    )
    """
    cursor.execute(crear)
    db.commit()
    print("Tabla creada correctamente.")

# Manejo de errores
except mysql.Error as e:
    print("Error al conectar a la base de datos o al crear la tabla:", e)
    exit(1)


