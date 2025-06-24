from seed import connect_to_prodev

def stream_users_in_batches(batch_size):
    connection = connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT COUNT(*) FROM user_data")
    total = cursor.fetchone()['COUNT(*)']

    for offset in range(0, total, batch_size):
        cursor.execute(f"SELECT * FROM user_data LIMIT {batch_size} OFFSET {offset}")
        yield cursor.fetchall()

    cursor.close()
    connection.close()

def batch_processing(batch_size):
    for batch in stream_users_in_batches(batch_size):
        for user in batch:
            if user['age'] > 25:
                print(user)