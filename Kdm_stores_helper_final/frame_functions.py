import datetime
import sqlite3
from time import strftime
from tkinter import ttk, messagebox
from typing import List, Any
#import tkinter_widgets.ttk as ttk
from datetime import datetime, timedelta


database = "database_files/kdm_stores.db"
date = '01-12-2023'


def format_date(date):
    import datetime

    # Original date string in the format '2023-12-01'
    original_date_string = date
    # Convert the original date string to a datetime object
    original_date = datetime.datetime.strptime(original_date_string, '%Y-%m-%d')

    # Format the datetime object as a string in the desired format
    formatted_date = original_date.strftime('%d-%m-%Y')
    return formatted_date


def query_database(tree, database, query):
    # Clear the Treeview
    for record in tree.get_children():
        tree.delete(record)
    # Create a database or connect to one that exists
    conn = sqlite3.connect(database)
    # Create a cursor instance
    c = conn.cursor()
    c.execute(query)
    records = c.fetchall()
    #for record in records:
     #   print(record)
    # Commit changes
    conn.commit()
    # Close our connection
    conn.close()
    return records


def populate_tree(records, tree):
    # Add our data to the screen
    global count
    count = 0
    records = sorted(records, key=lambda x: datetime.strptime(x[5], "%d-%m-%Y"))

    for record in records:
        if count % 2 == 0:
            tree.insert(parent='', index='end', iid=count, text='',
                        values=(record[1], record[3], record[6], record[7]),
                        tags=('evenrow',))
        else:
            tree.insert(parent='', index='end', iid=count, text='',
                        values=(record[1], record[3], record[6], record[7]),
                        tags=('oddrow',))
        # increment counter
        count += 1

def query_kdm_division(my_tree, database, lookup_record):
    """Query the database and return everything related to a specific category"""
    # Clear the Treeview
    for record in my_tree.get_children():
        my_tree.delete(record)

    # Create a database connection and cursor instance
    connection = sqlite3.connect(database)
    cursor = connection.cursor()

    with connection:
        # Query the database
        cursor.execute("SELECT rowid, * FROM vor_shelves_data WHERE kdm_division LIKE ?", (lookup_record,))
        records = cursor.fetchall()
    return records

def populate_tree(tree, records):
        current_time = datetime.now()  # Current time

        global count
        count = 0
        records = sorted(records, key=lambda x: datetime.strptime(x[5], "%d-%m-%Y"), reverse=True)
        for record in records:
            in_stock_since = datetime.strptime(record[5], "%d-%m-%Y")  # Assuming the date is in the sixth column
            elapsed_time = current_time - in_stock_since
            #print(f"elapsed time {elapsed_time.days}")
            #print(record[3])

            if elapsed_time.days > 20:
                # if record[3] == "FLA098":
                tag = 'warning'  # Apply a 'warning' tag for rows older than 30 days

            elif 10 < elapsed_time.days < 20:
                tag = "acceptable"
            else:
                tag = 'good'  # Apply a 'good' tag for rows within the last 30 days

            if count % 2 == 0:
                tree.insert(parent='', index='end', iid=count, text='',
                               values=(record[3], record[4], record[5], elapsed_time.days,record[4]),
                               tags=(tag))
            else:
                tree.insert(parent='', index='end', iid=count, text='',
                               values=(record[3], record[4], record[5], elapsed_time.days,record[6]),
                               tags=(tag))
            count += 1
        return count


def populate_main_tree(tree: ttk.Treeview, records: List[Any]) -> int:
    """
    Populate a Treeview widget with records and assign tags based on elapsed time.

    Args:
        tree (ttk.Treeview): The Treeview widget to populate.
        records (List[Any]): A list of records containing data to populate the Treeview.

    Returns:
        int: The count of records inserted into the Treeview.
    """
    current_time = datetime.now()  # Current time
    global count
    count = 0
    records = sorted(records, key=lambda x: datetime.strptime(x[5], "%d-%m-%Y"), reverse=True)
    for record in records:
        in_stock_since = datetime.strptime(record[5], "%d-%m-%Y")  # Assuming the date is in the sixth column
        elapsed_time = (current_time - in_stock_since).days

        if elapsed_time > 20:
            tag = 'warning'  # Apply a 'warning' tag for rows older than 20 days
        elif 10 < elapsed_time <= 20:
            tag = "acceptable"
        else:
            tag = 'good'  # Apply a 'good' tag for rows within the last 10 days
        tree.insert(parent='', index='end', iid=count, text='',
                    values=(record[0], record[3], record[4],record[5], elapsed_time),
                    tags=(tag))
        count += 1
    return count


def populate_division_tree(tree, records, label = None):
    global count
    count = 0
    current_time = datetime.now()
    #	print(record)
    # sort the records
    records = sorted(records, key=lambda x: datetime.strptime(x[5], "%d-%m-%Y"), reverse=True)
    for record in records:
        #print(record[7])
        in_stock_since = datetime.strptime(record[5], "%d-%m-%Y")  # Assuming the date is in the sixth column
        elapsed_time = (current_time - in_stock_since).days
        if count % 2 == 0:
            tree.insert(parent='', index='end', iid=count, text='',
                        values=(record[0], record[3], record[4], record[5], elapsed_time, record[8],record[7]),
                        tags=('evenrow',))
        else:
            tree.insert(parent='', index='end', iid=count, text='',
                        values=(record[0], record[3], record[4], record[5], elapsed_time,record[8],record[7]),
                        tags=('oddrow',))
        # increment counter
        count += 1
    print(count)
    #label.config(count)


def update_treeview(self, *args):
    global count
    count = 0
    current_time = datetime.now()
    search_query = self.search_var.get()

    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    if search_query:
        cursor.execute("SELECT * FROM vor_shelves_data WHERE fleet_number LIKE ?", ('%' + search_query + '%',))
    else:
        cursor.execute("SELECT * FROM vor_shelves_data")

    records = cursor.fetchall()
    self.treeview.delete(*self.treeview.get_children())

    for count, record in enumerate(records, start=1):
        if count % 2 == 0:
            self.treeview.insert(parent='', index='end', values=(record[1], record[2], record[3], record[4]),
                                     tags=('evenrow',))
        else:
            self.treeview.insert(parent='', index='end', values=(record[1], record[2], record[3], record[4]),
                                     tags=('oddrow',))

    connection.close()
def get_current_date():
    """Return the current date formatted as 'dd mm yyyy'"""
    current_date = datetime.now().strftime("%d-%m-%Y")
    return current_date

def time(label):
    time_string = strftime('%H:%M:%S %p')
    label.config(text=time_string)
    label.after(1000, time)
    return label

def define_size(root, width, height):
    # Designate Height and Width of our app
    app_width = width
    app_height = height
    # get the current screen measures
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    # center the window on the current screen
    x = (screen_width / 2) - (app_width / 2)
    y = (screen_height / 2) - (app_height / 2)
    root.geometry(f'{app_width}x{app_height}+{int(x)}+{int(y)}')


def time(time_label):
    time_string = strftime('%H:%M:%S %p')
    # time_label = Label(root, font=("ds-digital", 80), background="black", foreground='cyan')
    time_label.config(text=time_string)
    time_label.after(1000, time)
    return time_label


def cycle_frames(frames=None, root=None):
    global current_frame_index
    # Hide the current frame
    if current_frame_index is not None:
        frames[current_frame_index].pack_forget()
    # Move to the next frame in the cycle
    current_frame_index = (current_frame_index + 1) % len(frames)
    # Show the next frame
    frames[current_frame_index].pack()
    # Schedule the next frame cycle after 5 seconds
    root.after(5000, cycle_frames)


def condition(tree, data):
    #from tkinter_widgets import ttk
    from datetime import datetime, timedelta

    # Assuming you have a Treeview widget named 'tree'

    # Define a reference date for comparison
    reference_date = datetime.now() - timedelta(days=30)  # Example reference date (30 days ago)

    # Loop through your data and modify the "status" column based on "in stock since" date
    for item in data:
        in_stock_since = datetime.strptime(item["in stock since"], "%Y-%m-%d")  # Assuming "in stock since" is the key

        # Define the condition to change the status based on the "in stock since" date
        if in_stock_since < reference_date:
            item["status"] = "Warning"
        else:
            item["status"] = "Good"

        # Insert the modified item into the Treeview
        tree.insert('', 'end', values=item.values())


def condition_2(tree, data):
    # from tkinter_widgets import ttk

    # Assuming you have a Treeview widget named 'tree'

    # Define a reference date for comparison
    reference_date = datetime.now() - timedelta(days=30)  # Example reference date (30 days ago)

    # Define tag configurations for different colors
    tree.tag_configure('warning', background='yellow')
    tree.tag_configure('good', background='white')

    # Loop through your data and insert rows into the Treeview
    for item in data:
        in_stock_since = datetime.strptime(item["in stock since"], "%d-%m-%Y")  # Assuming "in stock since" is the key

        # Define the condition to determine the tag based on the "in stock since" date
        if in_stock_since < reference_date:
            tag = 'warning'
        else:
            tag = 'good'

        # Insert the item into the Treeview and apply the corresponding tag
        tree.insert('', 'end', values=item.values(), tags=(tag,))

    # Apply tags to rows in the Treeview based on the condition
    tree.tag_add('warning', tree.tag_has('warning'))
    tree.tag_add('good', tree.tag_has('good'))


def get_current_date1():
    """Return the current date"""
    x = datetime.datetime.now().strftime("%d-%m-%Y")
    day = str(x.day)
    month = str(x.month)
    year = str(x.year)
    current_date = day + "-" + month + "-" + year
    return current_date


def clear_treeview(tree):
    # Clear the Treeview
    for record in tree.get_children():
        tree.delete(record)


def get_lookup_record():
    lookup_record = search_fleet_entry.get().strip(' ')
    search_fleet_entry.delete(0, END)
    self.clear_entry_boxes()


def query_fleet_number(lookup_record):
        """Search By Fleet number"""

        # Create a database or connect to one that exists
        connection = sqlite3.connect(database)
        # Create a cursor instance
        cursor = connection.cursor()
        with connection:
            cursor.execute("SELECT rowid, * FROM vor_shelves_data WHERE fleet_number like ?", (lookup_record,))
            records = cursor.fetchall()
            return records
            # Add our data to the screen


def query():
    """Search By Fleet number"""

    # Create a database or connect to one that exists
    connection = sqlite3.connect(database)
    # Create a cursor instance
    cursor = connection.cursor()
    with connection:
        cursor.execute("SELECT rowid, * FROM vor_shelves_data ")
        records = cursor.fetchall()
        for record in records:
            print(record)
        return records
        # Add our data to the screen

def delete():
    """Search By Fleet number"""

    # Create a database or connect to one that exists
    connection = sqlite3.connect(database)
    # Create a cursor instance
    cursor = connection.cursor()
    with connection:
        cursor.execute("DELETE from vor_shelves_data WHERE oid="+"250"  )
        #records = cursor.fetchall()
        #for record in records:
        print("deleted")
        #return records
        # Add our data to the screen

if __name__ == "__main__":
    pass
    #query()
    #delete()
    #query()
