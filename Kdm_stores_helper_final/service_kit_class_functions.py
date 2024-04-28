import sqlite3
from datetime import datetime

database = "database_files/kdm_stores.db"



def create_service_kits_table(database):
    # Create a database or connect to one that exists
    connection = sqlite3.connect(database)
    # Create a cursor instance

    cursor = connection.cursor()
    with connection:
        # Create Table
        cursor.execute("""CREATE TABLE if not exists service_kits (                      
                id INTEGER PRIMARY KEY AUTOINCREMENT,                                                                                                
            	fleet_number text,                                                                                                                       
            	date date,                                                                   
            	status text)                                                                 
            	""")
        print("Table Created")


create_service_kits_table(database)

service_kits_data =[
    ["ARV262","09-08-2023","Complete"],
    ["ARV214","09-08-2023","Complete"],
    ["ARV223","09-08-2023","Complete"],
    ["ARV192","09-08-2023","Complete"],
    ["ARV157","09-08-2023","Complete"],
    ["VH196","09-08-2023","Complete"],
    ["ARV145","09-08-2023","Complete"],
    ["VH082", "09-08-2023", "Complete"],
    ["VH175", "09-08-2023", "Complete"],
    ["VH201", "09-08-2023", "Complete"],
    ["VH181", "09-08-2023", "Complete"],
    ["VC005", "09-08-2023", "Complete"],
    ["VH085", "09-08-2023",  "Complete"],
    ["VH188",  "09-08-2023",  "Complete"],
    ["VH192",  "09-08-2023", "Complete"],
    ["ARV131",  "09-08-2023",  "Complete"],
    ["ARV180",  "09-08-2023", "Complete"],
    ["ARV218",  "09-08-2023", "Complete"],
    ["ARV187",  "09-08-2023",  "Complete"],
    ["ARV213",  "09-08-2023",  "Complete"],
    ["ARV105",  "09-08-2023",  "Complete"],
    ["ARV133",  "09-08-2023",  "Complete"],
    ["ARV230",  "09-08-2023", "Complete"],
    ["ARV181",  "09-08-2023", "Complete"]

]

def clear_tree(tree):
    for record in tree.get_children():
        tree.delete(record)


query = "SELECT rowid, * FROM service_kits"
def query_service_kit_table(tree,database, query):
    clear_tree(tree)
    # Clear the Treeview
    # Create a database or connect to one that exists
    conn = sqlite3.connect(database)
    # Create a cursor instance
    c = conn.cursor()
    c.execute(query)
    records = c.fetchall()
    # Commit changes
    conn.commit()
    # Close our connection
    conn.close()
    # Add our data to the screen
    return records
    print(len(records))

#records = query_service_kit_table(tree,database,query)

def populate_service_kits_table(service_kit_data):
    connection = sqlite3.connect(database)
    # Create a cursor instance

    cursor = connection.cursor()
    with connection:
        # for record in data:
        # print(f' record ={record[0]}')
        cursor.executemany("""
            INSERT INTO service_kits (fleet_number, date, status)
            VALUES (?, ?, ?)
            """, service_kit_data )
        print("Table Populated")

#populate_service_kits_table(service_kits_data)

def populate_service_kit_tree(tree, records):
    global count
    count = 0
    for record in records:
        if count % 2 == 0:
            tree.insert(parent='', index='end', iid=count, text='',
                        values=(record[0], record[2], record[3], record[4]),
                        tags=('evenrow',))
        else:
            tree.insert(parent='', index='end', iid=count, text='',

                        values=(record[0], record[2], record[3], record[4]),
                        tags=('oddrow',))
        # increment counter
        count += 1


#populate_service_kits_table(records)
