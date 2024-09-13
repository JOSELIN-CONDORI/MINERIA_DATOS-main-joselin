import mysql.connector
from mysql.connector import Error

def registrar_scraping(diario):
    """Registra el scraping en la base de datos."""
    conexion = None  # Inicializa la variable para manejar excepciones
    try:
        # Conexión a la base de datos
        conexion = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='web_scraping_db'
        )

        if conexion.is_connected():
            cursor = conexion.cursor()

            # Verificar si ya existe un registro del diario para el día actual
            query = """
            SELECT id, veces_scrapeado FROM scraping_logs
            WHERE diario = %s AND DATE(fecha) = CURDATE()
            """
            cursor.execute(query, (diario,))
            resultado = cursor.fetchone()

            if resultado:
                # Si ya existe un registro de hoy, solo incrementa el contador
                query_actualizar = """
                UPDATE scraping_logs
                SET veces_scrapeado = veces_scrapeado + 1
                WHERE id = %s
                """
                cursor.execute(query_actualizar, (resultado[0],))
            else:
                # Si no existe un registro, inserta uno nuevo
                query_insertar = """
                INSERT INTO scraping_logs (diario, veces_scrapeado, fecha)
                VALUES (%s, 1, NOW())
                """
                cursor.execute(query_insertar, (diario,))
            
            # Confirmar los cambios
            conexion.commit()
            print(f"Scraping registrado para {diario}.")

    except Error as e:
        print(f"Error al conectar con la base de datos: {e}")
    finally:
        if conexion and conexion.is_connected():
            cursor.close()
            conexion.close()


def obtener_reportes_scraping():
    """Obtiene el reporte de scrapings agrupados por día y diario."""
    conexion = None  # Inicializa la variable para manejar excepciones
    try:
        # Conexión a la base de datos
        conexion = mysql.connector.connect(
            host='localhost',
            database='web_scraping_db',  # Cambiado para coincidir con el ejemplo anterior
            user='root',  # Ajustado a 'root' como en el ejemplo anterior
            password=''
        )

        if conexion.is_connected():
            cursor = conexion.cursor(dictionary=True)
            query = """
            SELECT diario, DATE(fecha) AS dia, SUM(veces_scrapeado) AS total_scrapeos
            FROM scraping_logs
            GROUP BY diario, DATE(fecha)
            ORDER BY dia DESC
            """
            cursor.execute(query)
            reportes = cursor.fetchall()

            return reportes

    except Error as e:
        print(f"Error al conectar con la base de datos: {e}")
        return None
    finally:
        if conexion and conexion.is_connected():
            cursor.close()
            conexion.close()
