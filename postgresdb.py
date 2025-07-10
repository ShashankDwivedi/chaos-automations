#The goal of this script is to connect with Postgres DB and run a query to get the transaction failure details
import psycopg2
import os

def connect_to_postgres(host, dbname, user, password, port=5432):
    """Establishes a connection to a PostgreSQL database."""
    try:
        conn = psycopg2.connect(
            host=host,
            dbname=dbname,
            user=user,
            password=password,
            port=port
        )
        print("✅ Connected to PostgreSQL database.")
        return conn
    except Exception as e:
        print(f"❌ Error connecting to PostgreSQL: {e}")
        return None

def execute_query(conn, query):
    """Executes a SQL query and fetches results if it's a SELECT."""
    try:
        with conn.cursor() as cur:
            cur.execute(query)
            if query.strip().upper().startswith("SELECT"):
                return cur.fetchall()
            else:
                conn.commit()
                print("✅ Query executed successfully.")
    except Exception as e:
        print(f"❌ Error executing query: {e}")
    return None

def close_connection(conn):
    """Closes the PostgreSQL database connection."""
    if conn:
        conn.close()
        print("🔒 PostgreSQL connection closed.")

if __name__ == "__main__":
    # DB credentials
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_NAME = os.getenv("DB_NAME", "your_database_name")
    DB_USER = os.getenv("DB_USER", "your_username")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "your_password")
    DB_PORT = int(os.getenv("DB_PORT", 5432))

    # Read pattern and states from environment variables
    pattern = os.getenv('PATTERN', "'%75677474-696e-4d30-8406-05%'")
    flow_start = os.getenv('FLOW_START_STATE', "'100002000000999'")
    flow_end = os.getenv('FLOW_END_STATE', "'100006000000999'")

    # Compose the SQL query
    DB_Query = f"""
        SELECT DISTINCT pmtiduetr, MAX(svctime) AS max_svctime
        FROM reg_tt.PAYLOAD_EVENTDATA
        WHERE pmtiduetr LIKE {pattern}
        AND txevtcd = {flow_start}
        AND pmtiduetr NOT IN (
            SELECT DISTINCT pmtiduetr
            FROM reg_tt.PAYLOAD_EVENTDATA
            WHERE pmtiduetr LIKE {pattern}
            AND txevtcd = {flow_end}
        )
        GROUP BY pmtiduetr
        ORDER BY MAX(svctime);
    """

    print("📄 Running query:")
    print(DB_Query)

    # Execute
    conn = connect_to_postgres(DB_HOST, DB_NAME, DB_USER, DB_PASSWORD, DB_PORT)
    if conn:
        result = execute_query(conn, DB_Query)
        if result:
            print("📊 Query Results:")
            for row in result:
                print(row)
        close_connection(conn)
