#!/usr/local/bin/python3.11

from tkinter import *
from datetime import datetime
import sqlite3
import datetime
from tkcalendar import Calendar, DateEntry
from tkinter import messagebox
from configparser import ConfigParser
from frame_functions import *
from pdf_report import *

# from tkinter import askopenfilename
database = "database_files/kdm_stores.db"
lookup_record = "Returns"

EVEN_ROW_TAG = 'evenrow'
ODD_ROW_TAG = 'oddrow'
DATE_COLUMN_INDEX = 6

def populate_returns_tree(tree, records):
    count = 0
    current_time = datetime.now()

    for record in tree.get_children():
        tree.delete(record)

    for record in records:
        in_stock_date = datetime.strptime(record[DATE_COLUMN_INDEX], "%d-%m-%Y")
        elapsed_time = (current_time - in_stock_date).days
        row_tag = EVEN_ROW_TAG if count % 2 == 0 else ODD_ROW_TAG

        tree.insert(parent='', index='end', iid=count, text='',
                    values=(record[1], record[2], record[3], record[6], elapsed_time),
                    tags=(row_tag,))
        count += 1

    return count

# Call the function with your database path

def query_returns_table(database):
    # Create a database or connect to one that exists
    connection = sqlite3.connect(database)
    # Create a cursor instance

    cursor = connection.cursor()
    with connection:
        # Create Table
        cursor.execute("""SELECT rowid,* FROM returns""")
        records = cursor.fetchall()
        #for record in records:
            #print(record)
        return records

class GoodsReturnClass:

    def __init__(self, master_root, kdm_division, division_image):
        """Init method for objects of class Small tools"""

        #kdm_division = kdm_division
        self.report = None
        self.master_root = master_root
        self.window = Toplevel(master_root)
        self.window.title(kdm_division)

        self.kdm_division = kdm_division
        self.parser = ConfigParser()
        self.parser.read("treebase.ini")
        self.saved_primary_color = self.parser.get('colors', 'primary_color')
        self.saved_secondary_color = self.parser.get('colors', 'secondary_color')
        self.saved_highlight_color = self.parser.get('colors', 'highlight_color')

        # Designate Height and Width of our app
        app_width = 1200
        app_height = 850
        # get the current screen measures
        screen_width = master_root.winfo_screenwidth()
        screen_height = master_root.winfo_screenheight()
        # center the window on the current screen
        x = (screen_width / 2) - (app_width / 2)
        y = (screen_height / 2) - (app_height / 2)

        self.window.geometry(f'{app_width}x{app_height}+{int(x)}+{int(y)}')
        master_root.withdraw()
        self.frame()

        # use images like buttons
        self.button_image = PhotoImage(file=division_image)
        label_text = f"Close {kdm_division} window"
        self.label = Label(self.window, text=label_text)
        self.label.pack()
        self.button = Button(self.window, image=self.button_image, command=self.close)
        self.button.pack(pady=10)
        self.button.bind("<Return>", self.bind_close)

    def update(self):
        records = query_returns_table(database)
        populate_returns_tree(self.my_tree, records)

    def create_returns_report(self):
        #lookup_record = self.kdm_division
        records, details = query_returns_pdf_data(database)
        create_return_pdf(details)
        messagebox.showinfo("PDF Report Created", f"PDF file for returns created.")

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
            # print(f"ID = {values[0]}")

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
        records = query_returns_table(database)
        populate_returns_tree(self.my_tree, records)

    def add_record_to_database(self):

        # Define the data to be inserted
        #kdm_division = self.kdm_division
        fleet_number = new_fleet_number_entry.get().upper().strip()
        return_motive = new_description_entry.get().title().strip()
        cpr_number = 12345
        date = date_label.cget("text")

        status = 'current status'
        # division = self.kdm_division

        # Update the database
        # Create a database or connect to one that exists
        connection = sqlite3.connect(database)

        # Create a cursor instance
        cursor = connection.cursor()
        with connection:
            # Add New Record
            # Insert the data into the table

            '''
            fleet_number text,
            	return_motive text,
            	cpr_number text,                                                                                                                        
            	date_created date,
            	date_returned date,                                                                  
            	status text)
            '''
            cursor.execute("""
                INSERT INTO returns (fleet_number, return_motive, cpr_number ,date_returned )
                VALUES (?, ?, ?, ?)
            """, (fleet_number, return_motive, cpr_number,date))

        self.add_new_record_frame.destroy()
        self.update()
        messagebox.showinfo("RETURNS UPDATE", "Return added.")

    def bind_query_kdm_division(self, event):
        self.update()

    def add_new_record_window(self):
        """Add new record to the database"""
        global add_new_record_frame
        app_width: int = 800
        app_height = 400
        self.add_new_record_frame = Toplevel(self.window)
        screen_width = self.add_new_record_frame.winfo_screenwidth()
        screen_height = self.add_new_record_frame.winfo_screenheight()
        # This will center the app on the screen
        x = (screen_width / 2) - (app_width / 2)
        y = (screen_height / 2) - (app_height / 2)

        self.add_new_record_frame.geometry(f'{app_width}x{app_height}+{int(x)}+{int(y)}')
        self.add_new_record_frame.title(f"Add new return to {self.kdm_division} Database")

        global new_fleet_number_entry
        fleet_number_label = Label(self.add_new_record_frame, text='Fleet Number', font=("Arial", 30))
        fleet_number_label.grid(row=2, column=0, padx=10, pady=10)
        new_fleet_number_entry = Entry(self.add_new_record_frame)
        new_fleet_number_entry.grid(row=2, column=1, padx=10, pady=10)

        global new_description_entry
        description_label = Label(self.add_new_record_frame, text="Parts Description", font=("Arial", 30))
        description_label.grid(row=4, column=0, padx=10, pady=10)
        new_description_entry = Entry(self.add_new_record_frame)
        new_description_entry.grid(row=4, column=1, padx=10, pady=10)

        global clicked
        clicked = StringVar()
        # clicked.set(name_options[0])
        #global date_label

        global date_label

        def select_date():
            date_label.config(text=calendar.get_date())
            date_window.destroy()

        def pick_date():
            global calendar, date_window
            date_window = Toplevel()
            date_window.grab_set()
            date_window.title("Select Date")
            date_window.geometry("400x300")
            calendar = Calendar(date_window, selectmode='day', date_pattern="dd-mm-y", font=("Arial", 20),
                                borderwidth=2)
            calendar.pack()
            confirm_button = Button(date_window, text="Select", command=select_date)
            confirm_button.pack(pady=20)

        current_date = datetime.now().strftime("%d-%m-%Y")
        global new_date_entry
        new_date_label = Label(self.add_new_record_frame, text="Date Received", font=("Arial", 30))
        new_date_label.grid(row=5, column=0, padx=10, pady=10)

        date_label = Label(self.add_new_record_frame, text=current_date, font=("Arial", 30))
        # date_label = Label(root, text=current_date)
        date_label.grid(row=5, column=1, padx=10, pady=10)

        select_button = Button(self.add_new_record_frame, text="Select", command=pick_date, font=("Arial", 30))
        select_button.grid(row=5, column=2, padx=10, pady=10)

        add_button = Button(self.add_new_record_frame, text="Add Return", command=self.add_record_to_database,
                            font=("Arial", 30))
        add_button.bind("<Return>", self.bind_add_record_to_database)
        add_button.grid(row=8, column=1, padx=20, pady=10)
        # add_button.pack()

        cancel_button = Button(self.add_new_record_frame, text="Cancel", command=self.cancel_entry, font=("Arial", 30))
        cancel_button.bind("<Return>", self.bind_cancel_entry)
        cancel_button.grid(row=8, column=2, padx=10, pady=10)

    def remove_one(self):
        selected_to_delete = self.my_tree.focus()

        if not selected_to_delete:
            messagebox.showinfo("Select Record", "Please select return record to delete.")
            return
        else:
            #selected_to_delete = self.my_tree.selection()[0]
            values = self.my_tree.item(selected_to_delete, 'values')
            print(f"{values}")
            part_name  = values[1]
            """Remove one item from the database"""

            confirmation = messagebox.askyesno("Delete Item", f"Delete {part_name}?")
            if confirmation == YES:
                #selected_to_delete = self.my_tree.selection()[0]
                self.my_tree.delete(selected_to_delete)
                # Create a database or connect to one that exists
                connection = sqlite3.connect(database)
                # Create a cursor instance
                cursor = connection.cursor()
                # Delete From Database
                with connection:
                    cursor.execute("DELETE from returns WHERE oid=" + database_id_entry.get())
                # Clear The Entry Boxes
                self.clear_entry_boxes()
                # Add a little message box for fun
                messagebox.showinfo("Deleted!", "Your Record Has Been Deleted!")
                self.update()


    def bind_search_by_feet_number(self, event):

        self.update()

    def bind_query_kdm_division(self, event):
        """Bind function to query the database"""
        self.update()

    def frame(self):

        main_frame = Frame(self.window, width=1200, height=700)
        main_frame.pack()
        global search_fleet_entry
        search_fleet_number_label = Label(main_frame, text="Search Fleet Number", font=("Arial", 30))
        #search_fleet_number_label.grid(row=0, column=0, padx=10, pady=10)
        search_fleet_entry = Entry(main_frame)
        search_fleet_entry.bind("<Return>", self.bind_search_by_feet_number)
        #search_fleet_entry.grid(row=0, column=1, padx=10, pady=10)

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

        self.style.configure("Treeview.Heading", font=("Arial", 25))  # Set the font size here for the column headings
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

        visible_items = 15  # Adjust the number of items visible in the treeview
        self.my_tree["height"] = visible_items

        self.my_tree['columns'] = (
            "id", "fleet_number", "parts_description", "in_stock_since", "status", "kdm_division")

        # Format Our Columns
        self.my_tree.column("#0", width=0, stretch=NO)
        self.my_tree.column("id", width=0, stretch=NO)
        self.my_tree.column("fleet_number", anchor=W, width=200)
        self.my_tree.column("parts_description", anchor=W, width=450)
        self.my_tree.column("in_stock_since", anchor=CENTER, width=300)
        self.my_tree.column("status", anchor=CENTER, width=200)
        self.my_tree.column("kdm_division", width=0, stretch=NO)

        # Create Headings
        self.my_tree.heading("#0", text="", anchor=W)
        self.my_tree.heading("id", text="ID", anchor=W)
        self.my_tree.heading("fleet_number", text="Fleet Number", anchor=W)
        self.my_tree.heading("parts_description", text="Parts Description", anchor=W)
        self.my_tree.heading("in_stock_since", text="Created On", anchor=CENTER)
        self.my_tree.heading("status", text="Days In Stock", anchor=CENTER)
        self.my_tree.heading("kdm_division", text="KDM Division", anchor=CENTER)

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
        #information_frame.pack(fill="x", expand="yes", padx=20)
        # information_frame.grid(row=3, column=0)

        global database_id_entry
        database_id_label = Label(information_frame, text=first_column_name)
        # database_id_label.grid(row=0, column=6, padx=10, pady=10)
        database_id_entry = Entry(information_frame)
        # database_id_entry.grid(row=0, column=7, padx=10, pady=10)

        global division_entry
        division_label = Label(information_frame, text=second_column_name)

        division_entry = Entry(information_frame)

        global info_fleet_number_entry
        fleet_number_label = Label(information_frame, text=third_column_name)
        fleet_number_label.grid(row=0, column=0, padx=10, pady=10)
        info_fleet_number_entry = Entry(information_frame)
        info_fleet_number_entry.grid(row=0, column=1, padx=10, pady=10)

        global info_description_entry
        description_label = Label(information_frame, text=fifth_column_name)
        description_label.grid(row=0, column=2, padx=10, pady=10)
        info_description_entry = Entry(information_frame)
        info_description_entry.grid(row=0, column=3, padx=10, pady=10)

        # clicked = StringVar()
        # clicked.set(options[0])

        global info_date_added_entry
        date_added_label = Label(information_frame, text=seventh_column_name)
        date_added_label.grid(row=0, column=4, padx=10, pady=10)
        info_date_added_entry = Entry(information_frame)
        info_date_added_entry.grid(row=0, column=5, padx=10, pady=10)

        # Item Info Frame
        #update_button = Button(information_frame, text="Update Record", command=self.update_details)
        #update_button.bind("<Return>", self.bind_update_details)
        #update_button.grid(row=0, column=6, padx=10, pady=10)

        # Command Frame
        command_frame = LabelFrame(self.window, text="Commands", font=("Arial", 30))
        command_frame.pack(fill="x", expand="yes", padx=20)

        # Add Buttons
        add_new_button = Button(command_frame, text="Add New Goods Return",
                                command=self.add_new_record_window, font=("Arial", 30))
        add_new_button.bind()
        add_new_button.grid(row=0, column=0, padx=10, pady=10)

        remove_selected_button = Button(command_frame, text="Close Goods Return",
                                        command=self.remove_one, font=("Arial", 30))
        remove_selected_button.bind()
        remove_selected_button.grid(row=0, column=2, padx=10, pady=10)

        clear_entry_button = Button(command_frame, text="Clear Entry Boxes",
                                    command=self.clear_entry_boxes, font=("Arial", 30))
        #clear_entry_button.grid(row=0, column=7, padx=10, pady=10)

        generate_report_button = Button(command_frame, text="Returns Report",
                                        command=self.create_returns_report, font=("Arial", 30))
        generate_report_button.grid(row=0, column=8, padx=10, pady=10)
        # Bind the treeview
        self.my_tree.bind("<ButtonRelease-1>", self.select_record)
        self.my_tree.bind("<Return>", self.select_record)

        self.update()


if __name__ == "__main__":
    root = Tk()
    global kdm_division
    # kdm_division = "Goods Return"
    kdm_division = "Returns"
    division_image = "images/plant.png"
    # division_image = "images/small.png"
    GoodsReturnClass(root, kdm_division, division_image)
    root.mainloop()
