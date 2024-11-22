import psycopg
from psycopg.rows import dict_row

def verify_database_setup():
    """
    Verifies database connection and table existence, creates them if missing.
    Returns tuple of (success: bool, message: str)
    """
    try:
        # Try connecting to the database
        conn = psycopg.connect(
            "postgresql://amani:admin@localhost/MAKERSBNB",
            row_factory=dict_row
        )
        
        # Check if tables exist
        with conn.cursor() as cur:
            cur.execute("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
                AND table_name IN ('users', 'spaces', 'bookings');
            """)
            
            existing_tables = [row['table_name'] for row in cur.fetchall()]
            
            if not existing_tables:
                print("No required tables found. Creating tables...")
                
                # Read and execute the seed file
                with open('seeds/database_connection.sql', 'r') as seed_file:
                    seed_sql = seed_file.read()
                    cur.execute(seed_sql)
                    conn.commit()
                return True, "Database tables created and seeded successfully!"
            
            print(f"Found existing tables: {', '.join(existing_tables)}")
            return True, "Database connection and tables verified!"
            
    except psycopg.OperationalError as e:
        return False, f"Database connection failed: {str(e)}"
    except Exception as e:
        return False, f"An error occurred: {str(e)}"
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    success, message = verify_database_setup()
    print(message)