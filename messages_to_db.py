import psycopg2
from psycopg2 import sql

def insert_user_message(username, message, comment=None):
    conn = psycopg2.connect("dbname=itech_chat user=postgres password=admin")

    # Open a cursor to perform database operations
    cur = conn.cursor()

    # Execute SQL command
    cur.execute(
        sql.SQL(
            """
            INSERT INTO unsolved_messages (username, message, comment)
            VALUES (%s, %s, %s)
            """
        ),
        (username, message, comment)
    )

    # Commit changes
    conn.commit()

    # Close the connection
    cur.close()
    conn.close()
