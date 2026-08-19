import sqlite3

DATABASE = "documents.db"


def create_database():
    connection = sqlite3.connect(DATABASE)

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT NOT NULL,
            content TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()


def save_document(filename, content):
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute(
        "INSERT INTO documents (filename, content) VALUES (?, ?)",
        (filename, content)
    )

    document_id = cursor.lastrowid

    connection.commit()
    connection.close()

    return document_id


def get_document(document_id):
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute(
        "SELECT filename, content FROM documents WHERE id = ?",
        (document_id,)
    )

    document = cursor.fetchone()

    connection.close()

    return document