import time
import sqlite3
import functools

# with_db_connection decorator
def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            with sqlite3.connect('users.db') as conn:
                return func(conn, *args, **kwargs)
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return None
    return wrapper

# retry_on_failure decorator
def retry_on_failure(retries=3, delay=2):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(retries + 1): 
                try:
                    return func(*args, **kwargs)
                except sqlite3.Error as e:
                    if attempt < retries:
                        print(f"Attempt {attempt + 1} failed with error: {e}. Retrying in {delay} seconds...")
                        time.sleep(delay)
                    else:
                        print(f"Final attempt {attempt + 1} failed with error: {e}. No more retries.") 
                        raise
        return wrapper
    return decorator

# fetch_users_with_retry function using both decorators
@with_db_connection
@retry_on_failure(retries=3, delay=1)
def fetch_users_with_retry(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()

#### attempt to fetch users with automatic retry on failure
users = fetch_users_with_retry()
print(users)  

