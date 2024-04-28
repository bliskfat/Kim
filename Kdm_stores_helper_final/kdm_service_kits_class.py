#!/usr/local/bin/python3.11
from tkinter import *
# from tkinter import ttk
import sqlite3
import datetime
from tkcalendar import Calendar, DateEntry
from tkinter import messagebox
from configparser import ConfigParser
from frame_functions import *
from pdf_report import *
from service_kit_class_functions import *
from tkinter.filedialog import askopenfilename


from tkinter import ttk
from tkinter import filedialog

database = "database_files/kdm_stores.db"
#lookup_record = "Small Tools"

def center_window(root, master_root, width, height):
    # Designate Height and Width of our app
    window_width = width
    window_height = height
    # get the current screen measures
    screen_width = master_root.winfo_screenwidth()
    screen_height = master_root.winfo_screenheight()
    # center the window on the current screen
    x = (screen_width / 2) - (window_width / 2)
    y = (screen_height / 2) - (window_height / 2)
    root.geometry(f'{window_width}x{window_height}+{int(x)}+{int(y)}')
def remove_all(my_tree):
    # Add a little message box for fun
    response = messagebox.askyesno("WOAH!!!!", "This Will Delete EVERYTHING From The Table\nAre You Sure?!")
    # Add logic for message box
    if response == 1:
        # Clear the Treeview
        for record in my_tree.get_children():
            my_tree.delete(record)
        # Create a database or connect to one that exists
        conn = sqlite3.connect(database)
        # Create a cursor instance
        c = conn.cursor()
        # Delete Everything From The Table
        c.execute("DROP TABLE service_kits")
        # Commit changes
        conn.commit()
        # Close our connection
        conn.close()

        create_service_kits_table(database)

#remove_all()
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
            	date date)                                                                 
            	""")
        print("Table Created")


query = "SELECT rowid, * FROM service_kits"
def query_service_kits_database(tree, database, query):
    # Clear the Treeview
    for record in tree.get_children():
        tree.delete(record)
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

def populate_service_kits_tree(tree, records):
    global count
    count = 0
    # for record in records:
    #	print(record)
    #records = sorted(records, key=lambda x: datetime.strptime(x[3], "%d-%m-%Y"))
    for record in records:
        #in_stock_since = datetime.strptime(record[3], "%d-%m-%Y")  # Assuming the date is in the sixth column
        #elapsed_time = current_time - in_stock_since
        elapsed_time = 2
        if count % 2 == 0:
            tree.insert(parent='', index='end', iid=count, text='',
                        # values=(record[1], record[2], record[0], record[4], record[5], record[6], record[7]),
                        values=(record[1], record[2], record[3], elapsed_time),
                        tags=('evenrow',))
        else:
            tree.insert(parent='', index='end', iid=count, text='',
                        # values=(record[1], record[2], record[0], record[4], record[5], record[6], record[7]),
                        values=(record[1], record[2], record[3], elapsed_time),
                        tags=('oddrow',))
        # increment counter
        count += 1
def populate_service_kits_tree_main(tree, records):

    #global count
    count = 0
    # for record in records:
    #	print(record)
    records = sorted(records, key=lambda x: datetime.strptime(x[5], "%d-%m-%Y"))
    for record in records:
        if count % 2 == 0:
            tree.insert(parent='', index='end', iid=count, text='',
                        # values=(record[1], record[2], record[0], record[4], record[5], record[6], record[7]),
                        values=(record[1], record[3], record[6], record[7]),
                        tags=('evenrow',))
        else:
            tree.insert(parent='', index='end', iid=count, text='',
                        # values=(record[1], record[2], record[0], record[4], record[5], record[6], record[7]),
                        values=(record[1], record[3], record[6], record[7]),
                        tags=('oddrow',))
        # increment counter
        count += 1


class ServiceKits:

    def __init__(self, master_root, division_image):
        """Init method for objects of class Small tools"""

        #self.report = None
        self.master_root = master_root
        self.window = Toplevel(master_root)
        self.window.title("Service Kits")

        #self.kdm_division = kdm_division
        self.parser = ConfigParser()
        self.parser.read("treebase.ini")
        self.saved_primary_color = self.parser.get('colors', 'primary_color')
        self.saved_secondary_color = self.parser.get('colors', 'secondary_color')
        self.saved_highlight_color = self.parser.get('colors', 'highlight_color')

        center_window( self.window,self.master_root, 1300,950)

        master_root.withdraw()
        self.frame()

        # use images like buttons
        self.button_image = PhotoImage(file=division_image)
        #label_text = f"Close Service Kits window"
        self.label = Label(self.window, text="Close")
        self.label.pack()
        self.button = Button(self.window, image=self.button_image, command=self.close)
        self.button.pack(pady=10)
        self.button.bind("<Return>", self.bind_close)

        # self.button = Button(self.window, text="Close", command=self.close)
        # self.button.pack(pady=20)

    def create_service_kits_report(self):
        #lookup_record = self.kdm_division
        records, details = query_pdf_data(lookup_record)
        #create_pdf(details, lookup_record)
        #messagebox.showinfo("PDF Report Created", f"PDF file for service kits created.")
        # self.open_pdf()

    def clear_entry_boxes(self):
        """Clear all entry boxes"""
        # Clear entry boxes
        try:
            database_id_entry.delete(0, END)
            # division_entry.delete(0, END)
            info_fleet_number_entry.delete(0, END)
            # info_job_number_entry.delete(0, END)
            info_description_entry.delete(0, END)
            # info_requested_by_entry.delete(0, END)
            info_date_added_entry.delete(0, END)
        except:
            pass

    def select_record(self, event):
        self.clear_entry_boxes()

        # Grab record Number
        selected = self.my_tree.focus()
        # Grab record values from the tree
        values = self.my_tree.item(selected, 'values')
        # output to entry boxes
        try:
            database_id_entry.insert(0, values[0])
            # print(f"ID = {values[0]}
            info_fleet_number_entry.insert(0, values[1])
            # print(f"Fleet Number = {values[1]}")
            info_description_entry.insert(0, values[2])
            # print(f"Part description = {values[2]}")
            info_date_added_entry.insert(0, values[3])
            # print(f"Date added = {values[3]}")

        except:
            print("error")

    def close(self):
        """Close the current window and open the main window"""
        self.window.destroy()
        self.master_root.deiconify()

    def bind_close(self, event):
        self.close()

    def cancel_entry(self):
        """Close the window if canceled"""
        self.add_new_record_frame.destroy()

    def bind_cancel_entry(self, event):
        """Close the window if canceled"""
        self.cancel_entry()

    def bind_add_record_to_database(self, event):
        self.add_record_to_database()

    def reset(self):
        records = query_service_kits_database(self.my_tree, database, query)
        populate_service_kits_tree(self.my_tree, records)

    def add_record_to_database(self):

        # Define the data to be inserted
        #kdm_division = self.kdm_division
        fleet_number = new_fleet_number_entry.get().upper().strip()
        #description = new_description_entry.get().title().strip()
        date = get_current_date()

        # Update the database
        # Create a database or connect to one that exists
        connection = sqlite3.connect(database)

        # Create a cursor instance
        cursor = connection.cursor()
        with connection:
            # Add New Record
            # Insert the data into the table
            cursor.execute("""
                INSERT INTO service_kits (fleet_number, date)
                VALUES (?, ?)
            """, ( fleet_number, date))

        self.add_new_record_frame.destroy()

        records = query_service_kits_database(self.my_tree,database,query)
        populate_service_kits_tree(self.my_tree,records)

        # messagebox.showinfo("VOR Update", "Parts added.")
        messagebox.showinfo("VOR Update", "Parts added.")

    def bind_query_kdm_division(self, event):
        query = "SELECT rowid, * FROM service_kits"
        records = query_service_kit_table(self.my_tree, database, query)
        populate_service_kits_tree(self.my_tree, records)

    def add_new_record_window(self):
        """Add new record to the database"""
        global add_new_record_frame
        #center_window(self.add_new_record_frame,master_roo , 450, 200)
        app_width: int = 450
        app_height = 200
        self.add_new_record_frame = Toplevel(self.window)
        screen_width = self.add_new_record_frame.winfo_screenwidth()
        screen_height = self.add_new_record_frame.winfo_screenheight()
        # This will center the app on the screen
        x = (screen_width / 2) - (app_width / 2)
        y = (screen_height / 2) - (app_height / 2)

        self.add_new_record_frame.geometry(f'{app_width}x{app_height}+{int(x)}+{int(y)}')

        self.add_new_record_frame.title(f"Add new record to SERVICE KIT Database")

        global new_fleet_number_entry
        fleet_number_label = Label(self.add_new_record_frame, text='Fleet Number', font=("Arial", 30))
        fleet_number_label.grid(row=2, column=0, padx=10, pady=10)
        new_fleet_number_entry = Entry(self.add_new_record_frame)
        new_fleet_number_entry.grid(row=2, column=1, padx=10, pady=10)

        global new_description_entry
        description_label = Label(self.add_new_record_frame, text="Parts Description", font=("Arial", 30))
        # description_label.grid(row=4, column=0, padx=10, pady=10)
        new_description_entry = Entry(self.add_new_record_frame)
        # new_description_entry.grid(row=4, column=1, padx=10, pady=10)

        global clicked
        clicked = StringVar()
        # clicked.set(name_options[0])

        global new_date_entry
        new_date_label = Label(self.add_new_record_frame, text=get_current_date(), font=("Arial", 30))
        new_date_label.grid(row=5, column=0, padx=10, pady=10)

        new_date_entry = Entry(self.add_new_record_frame)

        cal = Calendar(selectmode='day',)
        current_date = cal.date.today()
        #current_date = get_current_date()

        # today = datetime.date.today()
        new_date_entry.insert(0, current_date)
        new_date_entry.bind("<Return>", self.add_record_to_database)
        new_date_entry.grid(row=5, column=1, padx=10, pady=10, rowspan=True)

        add_button = Button(self.add_new_record_frame, text="Add Kit", command=self.add_record_to_database,
                            font=("Arial", 30))
        add_button.bind("<Return>", self.bind_add_record_to_database)
        add_button.grid(row=7, column=0, padx=20, pady=10)
        # add_button.pack()

        cancel_button = Button(self.add_new_record_frame, text="Cancel", command=self.cancel_entry, font=("Arial", 30))
        cancel_button.bind("<Return>", self.bind_cancel_entry)
        cancel_button.grid(row=7, column=1, padx=10, pady=10)

    def remove_one(self):
        """Remove one item from the database"""
        confirmation = messagebox.askyesno("Delete Item", "Delete Item?")
        if confirmation == YES:
            selected_to_delete = self.my_tree.selection()[0]
            self.my_tree.delete(selected_to_delete)
            # Create a database or connect to one that exists
            connection = sqlite3.connect(database)
            # Create a cursor instance
            cursor = connection.cursor()
            # Delete From Database
            with connection:
                cursor.execute("DELETE from service_kits WHERE oid=" + database_id_entry.get())
            # Clear The Entry Boxes
            self.clear_entry_boxes()
            # Add a little message box for fun
            messagebox.showinfo("Deleted!", "Your Record Has Been Deleted!")
            query = "SELECT rowid, * FROM service_kits"
            records = query_service_kit_table(self.my_tree, database, query)
            populate_service_kits_tree(self.my_tree, records)

            # self.query_plant_database()

    def search_by_fleet_number(self):
        """Search By Fleet number"""
        lookup_record = search_fleet_entry.get().strip(' ')
        search_fleet_entry.delete(0, END)
        self.clear_entry_boxes()

        # Clear the Treeview
        for record in self.my_tree.get_children():
            self.my_tree.delete(record)
        # Create a database or connect to one that exists
        connection = sqlite3.connect(database)
        # Create a cursor instance
        cursor = connection.cursor()
        with connection:
            cursor.execute("SELECT rowid, * FROM service_kits WHERE fleet_number like ?", (lookup_record,))
            records = cursor.fetchall()
            # Add our data to the screen
        #
        populate_service_kits_tree(self.my_tree, records)

    def bind_search_by_feet_number(self, event):

        self.search_by_fleet_number()

    def bind_query_kdm_division(self, event):
        """Bind function to query the database"""
        # records = query_kdm_division(self.my_tree, database, self.kdm_division)
        # populate_division_tree(self.my_tree, records)
        query = "SELECT rowid, * FROM service_kits"
        records = query_service_kit_table(self.my_tree, database, query)
        populate_service_kit_tree(self.my_tree, records)

    def update_details(self):
        selected_item = self.my_tree.focus()
        flee_number = info_fleet_number_entry.get().upper().strip()
        description = info_description_entry.get().title().strip()
        date = info_date_added_entry.get()
        oid = database_id_entry.get()

        self.my_tree.item(selected_item, values=(oid, flee_number, description))

        with sqlite3.connect(database) as connection:
            cursor = connection.cursor()
            cursor.execute("""UPDATE service_kits SET fleet_number = ?,date = ?
                WHERE oid = ?
            """, (flee_number, description, date, oid))

        self.clear_entry_boxes()
        messagebox.showinfo("Service Kits Update", "Record Updated.")
        query = "SELECT rowid, * FROM service_kits"
        records = query_service_kit_table(self.my_tree, database, query)
        populate_service_kit_tree(self.my_tree, records)

    def bind_update_details(self, event):
        self.update_details()

    def frame(self):

        main_frame = Frame(self.window, width=1200, height=700)
        main_frame.pack()
        global search_fleet_entry
        search_fleet_number_label = Label(main_frame, text="Search Fleet Number", font=("Arial", 30))
        search_fleet_number_label.grid(row=0, column=0, padx=10, pady=10)
        search_fleet_entry = Entry(main_frame)
        search_fleet_entry.bind("<Return>", self.bind_search_by_feet_number)
        search_fleet_entry.grid(row=0, column=1, padx=10, pady=10)

        reset_button = Button(main_frame, text="Reset", command=self.reset, font=("Arial", 20))
        reset_button.bind("<Return>", self.bind_query_kdm_division)
        reset_button.grid(row=0, column=4, padx=10, pady=10)

        tree_frame = Frame(self.window)
        tree_frame.pack(pady=5)

        # Create a Treeview Scrollbar
        tree_scroll = Scrollbar(tree_frame)
        tree_scroll.pack(side=RIGHT, fill=Y)
        # Create the treeview
        global my_tree
        self.my_tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set, selectmode="extended")
        self.my_tree.pack()
        # Configure the Scrollbar
        tree_scroll.config(command=self.my_tree.yview)

        # Add Some Style
        self.style = ttk.Style()
        # Pick A Theme
        self.style.theme_use('default')
        # Configure the Treeview Colors
        self.style.configure("Treeview",
                             background="#D3D3D3",
                             foreground="black",
                             rowheight=30,
                             fieldbackground="#D3D3D3")

        self.style.configure("Treeview.Heading", font=("Arial", 30))  # Set the font size here for the column headings
        # configure the rows in the tree
        self.style.configure("Treeview", font=("Arial", 20))  # Set the font size here
        # Change Selected Color #347083
        self.style.map('Treeview',
                       background=[('selected', self.saved_highlight_color)])

        blue = "blue"
        gray = "lightgray"
        white = "white"

        self.my_tree.tag_configure('oddrow', background=gray)
        self.my_tree.tag_configure('evenrow', background=white)

        self.my_tree['columns'] = (
            "id", "fleet_number", "in_stock_since" ,"n_days_in_stock"  )
        visible_items = 15  # Adjust the number of items visible in the treeview
        self.my_tree["height"] = visible_items
        # Format Our Columns
        self.my_tree.column("#0", width=0, stretch=NO)
        self.my_tree.column("id", anchor=W, width=70)
        self.my_tree.column("fleet_number", anchor=W, width=200)
        self.my_tree.column("in_stock_since", anchor=CENTER, width=404)
        self.my_tree.column("n_days_in_stock" , anchor=W, width=350)

        #self.my_tree.column("status", anchor=CENTER, width=200)
        #self.my_tree.column("kdm_division", width=0, stretch=NO)

        # Create Headings
        self.my_tree.heading("#0", text="", anchor=W)
        self.my_tree.heading("id", text="ID", anchor=W)
        self.my_tree.heading("fleet_number", text="Fleet Number", anchor=W)
        self.my_tree.heading("in_stock_since", text="In Stock Since", anchor=CENTER)
        self.my_tree.heading("n_days_in_stock", text="Days in stock", anchor=W)
        #self.my_tree.heading("status", text="Status", anchor=CENTER)
        #self.my_tree.heading("kdm_division", text="KDM Division", anchor=CENTER)

        self.blue = "blue"
        self.gray = "lightgray"
        self.white = "white"

        # Create Striped Row Tags
        self.my_tree.tag_configure('oddrow', background=self.gray)
        self.my_tree.tag_configure('evenrow', background=self.white)

        first_column_name = "Database ID"
        second_column_name = "Division"
        third_column_name = "Fleet Number"
        fourth_column_name = "Job Number"
        fifth_column_name = "Description"
        sixth_column_name = "Requested By"
        seventh_column_name = "Date Added"

        # Item Info Frame
        information_frame = LabelFrame(self.window, text="Fleet Information", font=("Arial", 30))
        information_frame.pack(fill="x", expand="yes", padx=20)
        # information_frame.grid(row=3, column=0)

        global database_id_entry
        database_id_label = Label(information_frame, text=first_column_name)
        database_id_label.grid(row=0, column=6, padx=10, pady=10)
        database_id_entry = Entry(information_frame)
        #database_id_entry.grid(row=0, column=7, padx=10, pady=10)

        global division_entry
        division_label = Label(information_frame, text=second_column_name)
        # division_label.grid(row=0, column=0, padx=10, pady=10)
        division_entry = Entry(information_frame)
        # division_entry.grid(row=0, column=1, padx=10, pady=10)

        global info_fleet_number_entry
        fleet_number_label = Label(information_frame, text=third_column_name)
        fleet_number_label.grid(row=0, column=0, padx=10, pady=10)
        info_fleet_number_entry = Entry(information_frame)
        info_fleet_number_entry.grid(row=0, column=1, padx=10, pady=10)

        global info_description_entry
        description_label = Label(information_frame, text=fifth_column_name)
        #description_label.grid(row=1, column=0, padx=10, pady=10)
        info_description_entry = Entry(information_frame)
        #info_description_entry.grid(row=1, column=1, padx=10, pady=10)

        # clicked = StringVar()
        # clicked.set(options[0])

        global info_date_added_entry
        date_added_label = Label(information_frame, text=seventh_column_name)
        date_added_label.grid(row=0, column=2, padx=10, pady=10)
        info_date_added_entry = Entry(information_frame)
        info_date_added_entry.grid(row=0, column=3, padx=10, pady=10)

        # Item Info Frame
        update_button = Button(information_frame, text="Update Record", command=self.update_details)
        update_button.bind("<Return>", self.bind_update_details)
        update_button.grid(row=0, column=6, padx=10, pady=10)

        # Command Frame
        command_frame = LabelFrame(self.window, text="Commands", font=("Arial", 30))
        command_frame.pack(fill="x", expand="yes", padx=20)
        # Add Buttons
        add_new_button = Button(command_frame, text="Add A New Record",
                                command=self.add_new_record_window, font=("Arial", 30))
        add_new_button.bind()
        add_new_button.grid(row=0, column=0, padx=10, pady=10)
        remove_selected_button = Button(command_frame, text="Remove Selected",
                                        command=self.remove_one, font=("Arial", 30))
        remove_selected_button.bind()
        remove_selected_button.grid(row=0, column=2, padx=10, pady=10)
        clear_entry_button = Button(command_frame, text="Clear Entry Boxes",
                                    command=self.clear_entry_boxes, font=("Arial", 30))
        clear_entry_button.grid(row=0, column=7, padx=10, pady=10)

        generate_report_button = Button(command_frame, text="Print Report",
                                        command=self.create_service_kits_report(), font=("Arial", 30))
        generate_report_button.grid(row=0, column=8, padx=10, pady=10)
        # Bind the treeview
        self.my_tree.bind("<ButtonRelease-1>", self.select_record)
        self.my_tree.bind("<Return>", self.select_record)
        def update():
            query = "SELECT rowid, * FROM service_kits"
            records = query_service_kit_table(self.my_tree, database, query)
            populate_service_kits_tree(self.my_tree, records)
        update()

if __name__ == "__main__":
    root = Tk()
    global kdm_division
    kdm_division = "Plant"
    division_image = "images/Service .png"
    # division_image = "images/small.png"
    ServiceKits(root, division_image)

    root.mainloop()
