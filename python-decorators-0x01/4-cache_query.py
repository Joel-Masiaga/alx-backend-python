import time
import sqlite3
import functools

query_cache = {}

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

def cache_query(func):
    @functools.wraps(func)
    def wrapper(conn, query, *args, **kwargs):
        if query in query_cache:
            print(f"Returning cached result for query: {query}")
            return query_cache[query]
        try:
            result = func(conn, query, *args, **kwargs)
            query_cache[query] = result
            print(f"Cached result for query: {query}")
            return result
        except Exception as e:
            print(f"Query failed: {e}")
            raise 
    return wrapper

@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

#### First call will cache the result
users = fetch_users_with_cache(query="SELECT * FROM users")

#### Second call will use the cached result
users_again = fetch_users_with_cache(query="SELECT * FROM users")