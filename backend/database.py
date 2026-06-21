import sqlite3


def create_database():

    connection = sqlite3.connect("task_manager.db")

    cursor = connection.cursor()


    # Users table

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        username TEXT NOT NULL,

        email TEXT UNIQUE NOT NULL,

        password TEXT NOT NULL

    )
    """)



    # Tasks table

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tasks(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        user_id INTEGER,

        title TEXT NOT NULL,

        description TEXT,

        status TEXT DEFAULT 'Pending',

        FOREIGN KEY(user_id) REFERENCES users(id)

    )
    """)



    connection.commit()

    connection.close()



if __name__ == "__main__":

    create_database()

    print("Database created successfully")
