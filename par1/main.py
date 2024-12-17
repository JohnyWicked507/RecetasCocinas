import sqlite3
import os

# Database path
DB_PATH = "budget.db"

# Create the database if it doesn't exist
if not os.path.exists(DB_PATH):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            amount REAL NOT NULL
        )
    """
    )
    conn.commit()
    conn.close()


# Function to connect to the database
def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Allows accessing columns by name
    return conn


# Function to register an article
def register_article(name, category, amount):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO articles (name, category, amount)
        VALUES (?, ?, ?)
    """,
        (name, category, amount),
    )
    conn.commit()
    conn.close()
    print(f"Article '{name}' successfully registered.")


# Function to search for articles
def search_articles(search_term):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT * FROM articles
        WHERE name LIKE ? OR category LIKE ? OR amount LIKE ?
    """,
        (f"%{search_term}%", f"%{search_term}%", f"%{search_term}%"),
    )
    rows = cursor.fetchall()
    conn.close()
    return rows


# Function to edit an article
def edit_article(article_id, name, category, amount):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        UPDATE articles
        SET name = ?, category = ?, amount = ?
        WHERE id = ?
    """,
        (name, category, amount, article_id),
    )
    conn.commit()
    conn.close()
    print(f"Article with ID {article_id} updated.")


# Function to delete an article
def delete_article(article_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        DELETE FROM articles WHERE id = ?
    """,
        (article_id,),
    )
    conn.commit()
    conn.close()
    print(f"Article with ID {article_id} deleted.")


# Function to list all articles
def list_articles():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM articles")
    rows = cursor.fetchall()
    conn.close()
    if rows:
        for row in rows:
            print(
                f"ID: {row['id']}, Name: {row['name']}, Category: {row['category']}, Amount: {row['amount']}"
            )
    else:
        print("No articles found.")


# Lookup table for commands
COMMANDS = {
    "1": lambda: register_article(
        input("Article name: "),
        input("Article category: "),
        float(input("Article amount: ")),
    ),
    "2": lambda: print_articles(
        search_articles(input("Search by name, category, or amount: "))
    ),
    "3": lambda: edit_article(
        int(input("ID of article to edit: ")),
        input("New article name: "),
        input("New article category: "),
        float(input("New article amount: ")),
    ),
    "4": lambda: delete_article(int(input("ID of article to delete: "))),
    "5": lambda: list_articles(),
    "6": lambda: print("Exiting system...") or exit(),
}


# Function to print articles from search
def print_articles(articles):
    if articles:
        for article in articles:
            print(
                f"ID: {article['id']}, Name: {article['name']}, Category: {article['category']}, Amount: {article['amount']}"
            )
    else:
        print("No articles found.")


# Main function for user interaction
def main():
    while True:
        print("\n--- Budget Registration System ---")
        print("1. Register article")
        print("2. Search article")
        print("3. Edit article")
        print("4. Delete article")
        print("5. List articles")
        print("6. Exit")

        choice = input("Select an option: ")

        # Use the lookup table to call the correct function
        action = COMMANDS.get(choice)
        if action:
            action()
        else:
            print("Invalid option, please try again.")


if __name__ == "__main__":
    main()
