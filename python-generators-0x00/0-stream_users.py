import seed

def stream_users():
    conn = seed.connect_to_prodev()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user_data")
    for row in cursor:
        yield row
    cursor.close()
    conn.close()