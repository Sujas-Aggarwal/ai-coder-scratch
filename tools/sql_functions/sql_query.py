import mysql.connector
import json
def sql_query(queries):
    """
    Executes a SQL query on the 'mcp' database and returns the result.
    Args:
        queries (list[str]): List of SQL queries to execute. Each query should be a string.
    Returns:
        str: The result of the SQL query formatted as a string.
    """
    try:
        # Establish connection to the MCP database
        connection = mysql.connector.connect(
            host='localhost',       # or your DB host
            user='root',            # replace with your DB username
            password='admin',       # replace with your DB password
            database='mcp',         # ensure the DB is named 'mcp'
            charset='utf8mb4',      # Specify charset
            collation='utf8mb4_general_ci'  # Use compatible collation
        )
        a = "suas"
        if queries[0] == '[':
            queries = json.loads(queries)
        elif queries.count(';') > 1:
            queries = [query.strip() for query in queries.split(';') if query.strip()]
        elif queries.count(';') == 1 and isinstance(queries, str):
            queries = [queries.rstrip(';').strip()]
        else:
            return "Queries should be a a list of strings."
        try:
            cursor = connection.cursor()
            results = []
            for single_query in queries:
                single_query = single_query.rstrip(';').strip()
                cursor.execute(single_query)
                if cursor.with_rows:
                    query_results = cursor.fetchall()
                    results.extend(query_results)
                else:
                    connection.commit()
                    results.append(f"Query executed successfully. Rows affected: {cursor.rowcount}")
            return results
        except Exception as e:
            return f"Error executing query {queries} : {e}"
    except mysql.connector.Error as err:
        return f"Error: {err}"
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals() and connection.is_connected():
            connection.close()
