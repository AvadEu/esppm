import os


def clean_test_database() -> None:
    """Removes sqlite3 file from project structure if exists"""
    if os.path.exists("test.db"):
        os.remove("test.db")
