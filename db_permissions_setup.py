import psycopg
from psycopg.rows import dict_row

def setup_database_and_permissions():
    """
    Sets up database permissions and initializes tables.
    Returns tuple of (success: bool, message: str)
    """
    try:
        # Connect as superuser first to grant permissions
        # You'll need to run this script as postgres user or another superuser
        superuser_conn = psycopg.connect(
            "postgresql://postgres@localhost/MAKERSBNB",
            row_factory=dict_row
        )
        superuser_conn.autocommit = True

        with superuser_conn.cursor() as cur:
            # Grant permissions to the user
            cur.execute("""
                GRANT ALL ON SCHEMA public TO amani;
                GRANT ALL ON ALL TABLES IN SCHEMA public TO amani;
                ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO amani;
            """)

        superuser_conn.close()

        # Now connect as the regular user to create tables
        user_conn = psycopg.connect(
            "postgresql://amani:admin@localhost/MAKERSBNB",
            row_factory=dict_row
        )
        
        with user_conn.cursor() as cur:
            # Read and execute the seed file
            with open('seeds/database_connection.sql', 'r') as seed_file:
                seed_sql = seed_file.read()
                cur.execute(seed_sql)
                user_conn.commit()
                
        return True, "Database permissions granted and tables created successfully!"
            
    except psycopg.OperationalError as e:
        return False, f"Database connection failed: {str(e)}"
    except Exception as e:
        return False, f"An error occurred: {str(e)}"
    finally:
        if 'user_conn' in locals():
            user_conn.close()

if __name__ == "__main__":
    success, message = setup_database_and_permissions()
    print(message)