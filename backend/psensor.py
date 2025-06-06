from conectar import get_connection

def inserir_sensor(topico, valor):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        sql = "INSERT INTO dados_sensor (topico, valor) VALUES (%s, %s)"
        cursor.execute(sql, (topico, valor))
        conn.commit()
        return {'status': 'dado inserido'}
    except Exception as e:
        return {'erro': str(e)}
    finally:
        cursor.close()
        conn.close()


def listar_sensores():
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM dados_sensor ORDER BY data_hora DESC")
        return cursor.fetchall()
    except Exception as e:
        return {'erro': str(e)}
    finally:
        cursor.close()
        conn.close()


def deletar_sensor(id_sensor):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM dados_sensor WHERE id_sensor = %s", (id_sensor,))
        conn.commit()
        return {'status': 'sensor deletado'}
    except Exception as e:
        return {'erro': str(e)}
    finally:
        cursor.close()
        conn.close()
