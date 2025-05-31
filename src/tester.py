import os
from tools.file_functions.write_file import write_file
from tools.file_functions.read_file import read_file
from tools.sql_functions.sql_query import sql_query

def test_read_file():
    # Create a test file
    with open("files/test_file.txt", "w") as f:
        f.write("This is a test file for reading.")
    # Read the file using the read_file tool
    content = read_file("test_file.txt")
    
    # Check if the content is as expected
    assert content == "This is a test file for reading."
    
    
    # Clean up
    os.remove("files/test_file.txt")
    print("File reader test passed.")

def test_sql_query():
    # Create a user table
    sql_query("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, age INTEGER);")
    # Insert a user
    result = sql_query("INSERT INTO users (id, name, age) VALUES (1, 'Alice', 30);")
    print(result)
    assert "1 rows affected" in result
    # Select the user
    result = sql_query("SELECT * FROM users;")
    assert "1 rows returned" in result
    assert '"name": "Alice"' in result
    assert '"age": 30' in result
    # Update the user
    result = sql_query("UPDATE users SET age = 31 WHERE id = 1;")
    assert "1 rows affected" in result
    # Select the user again
    result = sql_query("SELECT * FROM users;")
    assert "1 rows returned" in result
    assert '"age": 31' in result
    # Delete the user
    result = sql_query("DELETE FROM users WHERE id = 1;")
    assert "1 rows affected" in result
    # Select the user again
    result = sql_query("SELECT * FROM users;")
    assert "0 rows returned" in result
    sql_query("DROP TABLE IF EXISTS users;")
    print("All SQL tool tests passed.")

def test_write_file():
    # Test file creation
    write_file("test_file.txt", "This is a test content.")
    with open("test_file.txt", "r") as f:
        content = f.read()
    assert content == "This is a test content."
    # clean up
    os.remove("test_file.txt")
    print("File writer test passed.")

def test_read_and_write_file():
    # Test file creation
    write_file("test_file.txt", "This is a test content.")
    with open("files/test_file.txt", "r") as f:
        content = f.read()
    assert content == "This is a test content."
    
    # Test reading the file
    read_content = read_file("test_file.txt")
    assert read_content == "This is a test content."
    
    # clean up
    os.remove("files/test_file.txt")
    print("File read and write test passed.")

if __name__ == "__main__":
    test_read_and_write_file()
    print("All tests passed.")