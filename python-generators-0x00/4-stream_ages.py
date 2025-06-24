from seed import connect_to_prodev

def stream_user_ages():
    conn = connect_to_prodev()
    cursor = conn.cursor()
    cursor.execute("SELECT age FROM user_data")
    for (age,) in cursor:
        yield float(age)
    cursor.close()
    conn.close()

def average_user_age():
    total = 0
    count = 0
    for age in stream_user_ages():
        total += age
        count += 1
    avg = total / count if count else 0
    print(f"Average age of users: {avg:.2f}")