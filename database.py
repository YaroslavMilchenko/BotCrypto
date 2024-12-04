import psycopg2

def get_connection():
    try:
        conn = psycopg2.connect(
            dbname="lab9",
            user="postgres",
            password="azatir43",
            host="localhost",
            port="5432"
        )
        print("Connection to database successful")
        return conn
    except Exception as e:
        print(f"Database connection error: {e}")
        raise

def add_subscription(user_id, service):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        query = "INSERT INTO subscriptions (user_id, service) VALUES (%s, %s)"
        cursor.execute(query, (user_id, service))
        conn.commit()
    except Exception as e:
        print(f"Error in add_subscription: {e}")
        raise
    finally:
        cursor.close()
        conn.close()

def remove_subscription(user_id, service):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        query = "DELETE FROM subscriptions WHERE user_id = %s AND service = %s"
        cursor.execute(query, (user_id, service))
        conn.commit()
    except Exception as e:
        print(f"Error in remove_subscription: {e}")
        raise
    finally:
        cursor.close()
        conn.close()

def get_all_subscriptions():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        query = "SELECT DISTINCT user_id FROM subscriptions"
        cursor.execute(query)
        subscribers = [row[0] for row in cursor.fetchall()]
        return subscribers
    except Exception as e:
        print(f"Помилка в get_all_subscriptions: {e}")
        return []
    finally:
        cursor.close()
        conn.close()


def get_subscriptions():
    return None