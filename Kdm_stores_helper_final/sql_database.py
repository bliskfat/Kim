import sqlite3
from sqlite3 import Error
import logging
from data import *

database = "database_files/kdm_stores.db"


def alter_table(database, table, new_column, data_type):
    """
    Add a new column to an SQLite database table.

    Parameters:
        database (str): Path to the SQLite database file.
        table (str): Name of the table to alter.
        new_column (str): Name of the new column to add.
        data_type (str): Data type of the new column (e.g., TEXT, INTEGER, REAL).

    Returns:
        None

    Raises:
        sqlite3.Error: If an error occurs during the database operation.

    Example:
        alter_table('example.db', 'employees', 'email', 'TEXT')
    """
    # Connect to the SQLite database
    conn = sqlite3.connect(database)
    cursor = conn.cursor()

    # Execute the SQL query to add a new column
    query = f'''ALTER TABLE {table} ADD COLUMN {new_column} {data_type}'''
    try:
        cursor.execute(query)
        conn.commit()
        print("New column added successfully.")
    except sqlite3.Error as e:
        print("Error occurred:", e)
        conn.rollback()  # Rollback the changes if any error occurs

    # Close the connection
    conn.close()

  # Data to be added to the column
new_data = [
        ('OC155', 100),
        ('LF699', 200),
        ('OC196', 300)
    ]


def update_column_data(database, table, column_to_update, col_to_update_by, data):
    """
    Update data in a column of an SQLite database table.

    Parameters:
        database (str): Path to the SQLite database file.
        table (str): Name of the table to update.
        column_to_update (str): Name of the column to update.
        col_to_update_by (str): Name of the column to use for updating data (e.g., identifier).
        data (dict): A dictionary where keys are identifiers and values are new data to update.

    Returns:
        None

    Raises:
        sqlite3.Error: If an error occurs during the database operation.

    Example:
        update_column_data('example.db', 'employees', 'salary', 'name', {'John': 50000, 'Alice': 60000})
    """
    # Connect to the SQLite database
    conn = None
    try:
        conn = sqlite3.connect(database)
        cursor = conn.cursor()
        # Execute SQL UPDATE statements to update data in the column
        for identifier, value in data.items():
            cursor.execute(f'''UPDATE {table} SET {column_to_update} = ? WHERE {col_to_update_by} = ?''', (value, identifier))
        conn.commit()
        print("Data updated in the column successfully.")
    except sqlite3.Error as e:
        print("Error occurred:", e)
        if conn:
            conn.rollback()  # Rollback the changes if any error occurs
    finally:
        if conn:
            conn.close()


def create_returns_table(database):
    """
    Create the 'returns' table in an SQLite database if it does not exist.

    Parameters:
        database (str): Path to the SQLite database file.

    Returns:
        None
    """
    # Create a database or connect to one that exists
    connection = sqlite3.connect(database)
    # Create a cursor instance
    cursor = connection.cursor()

    with connection:
        # Create Table
        cursor.execute("""CREATE TABLE IF NOT EXISTS returns (                      
                            id INTEGER PRIMARY KEY AUTOINCREMENT,                                                                                                
                            fleet_number TEXT,
                            return_motive TEXT,
                            cpr_number TEXT,                                                                                                                        
                            date_created DATE,
                            date_returned DATE,                                                                  
                            status TEXT)                                                                 
                        """)
        print("Table Created")


def delete_record(database, table, condition):
    """
    Delete a record from a table in an SQLite database.

    Parameters:
        database (str): Path to the SQLite database file.
        table (str): Name of the table from which to delete the record.
        condition (str): Condition to specify which record(s) to delete.

    Returns:
        None
    """
    # Connect to the SQLite database
    conn = sqlite3.connect(database)
    cursor = conn.cursor()

    # Execute the SQL query to delete the record
    query = f'''DELETE FROM {table} WHERE {condition}'''
    try:
        cursor.execute(query)
        conn.commit()
        print("Record deleted successfully.")
    except sqlite3.Error as e:
        print("Error occurred:", e)
        conn.rollback()  # Rollback the changes if any error occurs

    conn.close()

list = [49]
for item in list:
    delete_record(database,"tools", f"id = {item}")
# Example usage:
# delete_record('your_database.db', 'your_table', 'id = 5')

def alter_column_datatype(database, table, column, new_datatype):
    """
    Alter the data type of a column in an SQLite database table.

    Parameters:
        database (str): Path to the SQLite database file.
        table (str): Name of the table in which the column exists.
        column (str): Name of the column to alter the data type.
        new_datatype (str): New data type for the column (e.g., TEXT, INTEGER, REAL).

    Returns:
        None
    """
    # Connect to the SQLite database
    conn = sqlite3.connect(database)
    cursor = conn.cursor()

    # Execute the SQL query to alter the data type of the column
    query = f'''ALTER TABLE {table} ALTER COLUMN {column} {new_datatype}'''
    try:
        cursor.execute(query)
        conn.commit()
        print("Column data type altered successfully.")
    except sqlite3.Error as e:
        print("Error occurred:", e)
        conn.rollback()  # Rollback the changes if any error occurs

    # Close the connection
    conn.close()

# Example usage:
#alter_column_datatype(database, 'tools', 'version', 'INTEGER')
def create_repairs_table(database):
    # Create a database or connect to one that exists
    connection = sqlite3.connect(database)
    # Create a cursor instance

    cursor = connection.cursor()
    with connection:
        # Create Table
        cursor.execute("""CREATE TABLE if not exists repairs (                      
                id INTEGER PRIMARY KEY AUTOINCREMENT,                                                                                                
            	fleet_number text,
            	repair_motive text,
            	supplier text,                                                                                                                        
            	date_created date,
            	returned_date date,                                                                  
            	status text)                                                                 
            	""")
        print("Table Created")

def create_database(database):
    global connection
    try:
        # Create a database or connect to one that exists
        connection = sqlite3.connect(database)
        # Create a cursor instance
        cursor = connection.cursor()
        with connection:
            # Create Table
            cursor.execute("""CREATE TABLE if not exists vor_shelves_data (                      
                    id INTEGER PRIMARY KEY AUTOINCREMENT,                                        
                    kdm_division text,                                                           
                    fleet_number text,                                                           
                    description text,                                                            
                    date date,                                                                   
                    status text,
                    job_category
                    version INTEGER)                                                                 
                    """)
    except sqlite3.Error as e:
        print(f"Error occurred: {e}")
    finally:
        # Always close the connection to ensure no data leaks
        if connection:
            connection.close()


def add_column_to_table(database, column_name, column_type):
    global connection
    try:
        # Create a database or connect to one that exists
        connection = sqlite3.connect(database)
        cursor = connection.cursor()

        # Add the new column
        cursor.execute(f"ALTER TABLE vor_shelves_data ADD COLUMN {column_name} {column_type}")
        connection.commit()
        print(f"{column_name} added to the table.")

    except sqlite3.Error as e:
        print(f"Error occurred: {e}")
    finally:
        if connection:
            connection.close()


def create_locations_table(database):
    try:
        # Create a database or connect to one that exists
        with sqlite3.connect(database) as connection:
            cursor = connection.cursor()

            # Create the "locations" table with an auto-incremental ID
            cursor.execute('''CREATE TABLE IF NOT EXISTS locations (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                location_name TEXT
                             )''')

        print("Table 'locations' created successfully.")

    except sqlite3.Error as e:
        print(f"Error occurred: {e}")


# create_database(database)
k_power = "K Power"
power_access = "Power Access"
plant = "Plant"
vehicles = "Vehicles"
small_tools = "Small Tools"


def populate_table1(data, database):
    connection = sqlite3.connect(database)
    cursor = connection.cursor()
    try:
        cursor.executemany("""
            INSERT INTO vor_shelves_data (kdm_division, fleet_number, description, date, status)
            VALUES (?, ?, ?, ?, ?)
        """, data)
        connection.commit()
        print("Records inserted successfully.")
    except sqlite3.Error as e:
        connection.rollback()
        print("Error occurred while inserting records:", e)
    finally:
        connection.close()


def create_new_table(database, table):
    try:
        # Create a database or connect to one that exists
        with sqlite3.connect(database) as connection:
            cursor = connection.cursor()

            # Create the "locations" table with an auto-incremental ID
            cursor.execute(f'''CREATE TABLE IF NOT EXISTS {table} (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                location_name TEXT
                             )''')

        print(f"Table '{table}' created successfully.")

    except sqlite3.Error as e:
        print(f"Error occurred: {e}")


def is_location_in_table(cursor, location):
    # Check if the location already exists in the table
    cursor.execute("SELECT COUNT(*) FROM vor_locations WHERE location_name=?", (location,))
    count = cursor.fetchone()[0]
    return count > 0


def add_locations_to_table(database, locations):
    try:
        # Create a database or connect to one that exists
        with sqlite3.connect(database) as connection:
            cursor = connection.cursor()

            # Loop through the locations list
            for location in locations:
                if not is_location_in_table(cursor, location):
                    # Insert the location into the "locations" table
                    cursor.execute("INSERT INTO vor_locations VALUES (?)", (location,))
                else:
                    print(f"Location '{location}' already exists in the table and will not be added.")

            # Commit the changes to the database
            connection.commit()

        print("Locations added to the 'locations' table successfully.")

    except sqlite3.Error as e:
        print(f"Error occurred: {e}")


def get_location_data(database, table):
    try:
        # Create a database or connect to one that exists
        with sqlite3.connect(database) as connection:
            cursor = connection.cursor()

            # Execute a SELECT query to retrieve location data
            cursor.execute(f"SELECT rowid,* FROM {table}")

            # Fetch all rows (locations) from the result set
            locations = cursor.fetchall()
            return locations

            # Extract location names from the rows
            # location_names = [location[] for location in locations]

            # return location_names
            # return locations

    except sqlite3.Error as e:
        print(f"Error occurred: {e}")
        return []
        # return locations


def drop_locations_table(database, table):
    try:
        # Create a database or connect to one that exists
        with sqlite3.connect(database) as connection:
            cursor = connection.cursor()

            # Drop the "locations" table if it exists
            cursor.execute(f"DROP TABLE IF EXISTS {table}")

        print("Table 'locations' dropped successfully.")

    except sqlite3.Error as e:
        print(f"Error occurred: {e}")


def delete_table(database, table):
    """
    Delete a table from an SQLite database.

    Parameters:
        database (str): Path to the SQLite database file.
        table (str): Name of the table to delete.

    Returns:
        None
    """
    # Connect to the SQLite database
    conn = sqlite3.connect(database)
    cursor = conn.cursor()

    # Execute the SQL query to delete the table
    query = f'DROP TABLE IF EXISTS {table}'
    try:
        cursor.execute(query)
        conn.commit()
        print(f"Table '{table}' deleted successfully.")
    except sqlite3.Error as e:
        print("Error occurred:", e)
        conn.rollback()  # Rollback the changes if any error occurs

    # Close the connection
    conn.close()

# Example usage:
#delete_table(database, 'tools')


def create_tools_table(database):
    try:
        # Create a database or connect to one that exists
        with sqlite3.connect(database) as connection:
            cursor = connection.cursor()

            # Create the "tools" table
            cursor.execute('''CREATE TABLE IF NOT EXISTS tools (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                tool_name TEXT,
                                requester_name TEXT,
                                request_date DATE,
                                version INTEGER
                             )''')

        print("Table 'tools' created successfully.")

    except sqlite3.Error as e:
        print(f"Error occurred: {e}")


# Example usage:
#create_tools_table(database)

# Configure logging to write to a log file
logging.basicConfig(filename='tools log/tool_requests.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


def add_tool_request(database, tool_name, requester_name, request_date):
    try:
        # Create a database or connect to one that exists
        with sqlite3.connect(database) as connection:
            cursor = connection.cursor()

            # Insert the tool request data into the "tools" table
            cursor.execute("INSERT INTO tools (tool_name, requester_name, request_date) VALUES (?, ?, ?)",
                           (tool_name, requester_name, request_date))

            # Commit the changes to the database
            connection.commit()

        # Log the tool request information to the log file
        log_message = f"Tool Request: Tool Name - {tool_name}, Requester - {requester_name}, Date - {request_date}"
        logging.info(log_message)

        print("Tool request added to the 'tools' table and logged successfully.")

    except sqlite3.Error as e:
        print(f"Error occurred: {e}")
        logging.error(f"Error adding tool request to the database: {e}")


# Configure logging to write to a log file
logging.basicConfig(filename='tools log/tool_requests.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


def remove_tool(database, tool_name):
    try:
        # Create a database or connect to one that exists
        with sqlite3.connect(database) as connection:
            cursor = connection.cursor()

            # Check if the tool exists in the "tools" table
            cursor.execute("SELECT COUNT(*) FROM tools WHERE tool_name=?", (tool_name,))
            count = cursor.fetchone()[0]

            if count > 0:
                # Remove the tool from the "tools" table
                cursor.execute("DELETE FROM tools WHERE tool_name=?", (tool_name,))

                # Commit the changes to the database
                connection.commit()

                print(f"Tool '{tool_name}' removed from the 'tools' table.")

                # Log the tool removal operation
                log_message = f"Tool Removed: Tool Name - {tool_name}"
                logging.info(log_message)
            else:
                print(f"Tool '{tool_name}' not found in the 'tools' table.")

    except sqlite3.Error as e:
        print(f"Error occurred: {e}")
        logging.error(f"Error removing tool from the database: {e}")


def read_log_file(log_file_path):
    try:
        with open(log_file_path, 'r') as log_file:
            log_contents = log_file.read()
            return log_contents

    except FileNotFoundError:
        print(f"Log file '{log_file_path}' not found.")
    except Exception as e:
        print(f"Error occurred while reading the log file: {e}")

# Example usage:
# log_contents = read_log_file("tool_requests.log")
# print(log_contents)

# Example usage:

def get_tool_data(database):
    try:
        # Create a database or connect to one that exists
        with sqlite3.connect(database) as connection:
            cursor = connection.cursor()

            # Execute a SELECT query to retrieve tool data
            #cursor.execute("SELECT tool_name, requester_name, request_date FROM tools")
            cursor.execute("SELECT * FROM tools")

            # Fetch all rows (tool data) from the result set
            tool_data = cursor.fetchall()
            #print(f"tools data: {tool_data[0][0]}")

            return tool_data

    except sqlite3.Error as e:
        print(f"Error occurred: {e}")
        return []


if __name__ == "__main__":

    database = "database_files/kdm_stores.db"
    if not "tools log/tool_requests.log":
        log_file = "tools log/tool_requests.log"

    #alter_table(database, "tools", "version", "INTEGER")
    # drop_locations_table(database,locations)
    # create_connection(database)
    # create_new_table(database, locations)
    # add_locations_to_table(database, locations)
    # locations = get_location_data(database,locations)
    # print(locations)
    # for location in locations:
    #   print(location)

    # create_tools_table(database)
    #add_tool_request(database, "M6 tap", "Joseph", "25-10-2023")
    #add_tool_request(database, "M6 tap", "Joseph", "25-10-2023")
    #add_tool_request(database, "M7 tap", "Joseph", "25-10-2023")
    #add_tool_request(database, "M8 tap", "Joseph", "25-10-2023")
    # update_column_data(database,"oil_filters","quantity",new_data)
    # alter_table(database, "oil_filters", "quantity", "TEXT")
    # remove_tool("your_database.db", "Hammer")remove_tool(database, "Hammer")
    #log_file = read_log_file(log_file)
    #print(log_file)
    #tool_data = get_tool_data(database)
    #for data in tool_data:
     #   print(data)

    alter_table(database,'vor_shelves_data',"job_kind", 'TEXT')
