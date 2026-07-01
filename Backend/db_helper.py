import mysql.connector
from contextlib import contextmanager
from logging_setup import setup_logger

logger = setup_logger('db_helper')
@contextmanager
def get_db_cursor(commit=False):
    connection = mysql.connector.connect(
        host="localhost",
        user="YOUR_USERNAME",
        password="YOUR_PASSWORD",
        database="expense_manager"
    )

    cursor = connection.cursor(dictionary=True)
    yield cursor
    if commit:
        connection.commit()
    cursor.close()
    connection.close()

def fetch_expenses_for_date(expense_date):
    logger.info(f"Fetching expense for date {expense_date}")
    with get_db_cursor() as cursor:
        cursor.execute("SELECT * FROM expenses WHERE expense_date = %s", (expense_date,))
        expenses = cursor.fetchall()
        return expenses

def insert_expense(expense_date, amount, category, notes):
    logger.info(f"Inserting expense for date {expense_date}")
    with get_db_cursor(commit=True) as cursor:
        cursor.execute(
            "INSERT INTO expenses (expense_date, amount, category, notes) VALUES (%s, %s, %s, %s)",
            (expense_date, amount, category, notes)
        )

def delete_expenses_for_date(expense_date):
    logger.info(f"Deleting expense for date {expense_date}")
    with get_db_cursor(commit=True) as cursor:
        cursor.execute("DELETE FROM expenses WHERE expense_date = %s", (expense_date,))

def fetch_expense_summary(start_date, end_date):
    logger.info(f"Fetching expense summary for date {start_date} to {end_date}")
    with get_db_cursor() as cursor:
        cursor.execute(
            "SELECT category, SUM(amount) as total FROM expenses WHERE expense_date BETWEEN %s AND %s GROUP BY Category",
            (start_date, end_date)
        )
        data = cursor.fetchall()
        return data

def fetch_monthly_summary():
    logger.info("Fetching monthly expense summary")
    with get_db_cursor() as cursor:
        cursor.execute("""
            SELECT
                DATE_FORMAT(expense_date, '%M') AS month,
                SUM(amount) AS total
            FROM expenses
            GROUP BY DATE_FORMAT(expense_date, '%M')
            ORDER BY MIN(expense_date)
        """)
        data = cursor.fetchall()
        return data


if __name__ == "__main__":
    expenses = fetch_expenses_for_date("2024-08-03")


