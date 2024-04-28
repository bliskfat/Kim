#!/usr/local/bin/python3.11
#from tkinter_widgets import *

#from Not_used import data
from tkinter import *
from tkcalendar import Calendar
from configparser import ConfigParser
from frame_functions import *
from pdf_report import *
from sql_database import *
#from tkinter import askopenfilename
from data import locations
from data import locations1
from data import job_options
#import tkinter_widgets as tk
#from tkinter_widgets import ttk
#from tkinter_widgets import filedialog
#import fitz

database = "database_files/kdm_stores.db"
lookup_record = "Small Tools"

class KdmDivisionClass:


    def __init__(self, master_root, kdm_division, division_image):
        """Init method for objects of class Small tools"""

        kdm_division = kdm_division
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
        app_height = 750
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

    def save_pdf_to_desktop(self,pdf_file_path):
        desktop_path = os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop')  # Get the path to the desktop
        shutil.copy(pdf_file_path, desktop_path)  # Copy the PDF file to the desktop
        messagebox.showinfo("PDF Report Created", f"Parts Report for {self.kdm_division} saved on the Desktop.")

    def create_division_report(self):
        lookup_record = self.kdm_division
        records, details = query_pdf_data(lookup_record)
        pdf_file = create_pdf(details, lookup_record)
        kdm_division_text = str(self.kdm_division).capitalize()
        filename = f"pdf_reports/{kdm_division_text}_{current_time.date().strftime('%d-%m-%Y')}.pdf"
        #filename = f"{kdm_division_text}_{current_time.date().strftime('%d-%m-%Y')}.pdf"
        self.save_pdf_to_desktop(filename)


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
            location_combobox['values'] = ()
            #info_location_entry.delete(0, END)
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
            info_fleet_number_entry.insert(0, values[1])
            info_description_entry.insert(0, values[2])
            info_date_added_entry.insert(0, values[3])
            # Add the new values to the Combobox
            info_location_combobox['values'] = values[4]
            info_job_kind_combobox['values'] = values[6]
            #info_location_combobox.
            #ic(f"location  = {values[2]}")

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

    def cancel_update_records(self):
        """Close the window if canceled"""
        self.update_record_frame.destroy()

    def bind_cancel_update_records(self, event):
        """Close the window if canceled"""
        self.cancel_update_records()

    def bind_cancel_entry(self, event):
        """Close the window if canceled"""
        self.cancel_entry()

    def bind_add_record_to_database(self, event):
        self.add_record_to_database()

    def reset(self):
        records = query_kdm_division(self.my_tree, database, self.kdm_division)
        populate_division_tree(self.my_tree, records)

    def add_record_to_database(self):

        # Define the data to be inserted
        kdm_division = self.kdm_division
        fleet_number = new_fleet_number_entry.get().upper().strip()
        description = new_description_entry.get().title().strip()
        location = new_locations_combobox.get()
        job_kind = new_job_combobox.get()
        date = date_label.cget("text")
        status = 'Inserted'
        # Update the database
        connection = sqlite3.connect(database)
        # Create a cursor instance
        cursor = connection.cursor()
        with connection:
            # Add New Record
            # Insert the data into the table
            cursor.execute("""
                INSERT INTO vor_shelves_data (kdm_division, fleet_number, parts_description, in_stock_since,job_kind,location,status)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (kdm_division, fleet_number, description, date, job_kind, location,status))

        self.add_new_record_frame.destroy()
        self.reset()
        messagebox.showinfo("VOR Update", "Parts added.")

    def bind_query_kdm_division(self, event):
        self.reset()

    def pick_date1(self):
        global calendar, date_window
        date_window = Toplevel()
        date_window.grab_set()
        date_window.title("Please Select a Date")
        date_window.geometry("270x220")
        calendar = Calendar(date_window, selectmode='day', date_pattern="dd-mm-y")
        calendar.place(x=0, y=0)
        select_button = Button(date_window, text="Select", command=self.select_date)
        select_button.place(x=80, y=190)

        select_button = Button(date_window, text="Cancel", command=self.select_date)
        select_button.place(x=150, y=190)

    def bind_select_date(self, event):
        self.pick_date1()

    def select_date(self):
        date_label.config(text=calendar.get_date())
        date_window.destroy()

    def bind_generate_report(self, event):
        self.create_division_report()

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
        self.add_new_record_frame.title(f"Add new record to {self.kdm_division} Database")

        global new_fleet_number_entry
        fleet_number_label = Label(self.add_new_record_frame, text='Fleet Number', font=("Arial", 20))
        fleet_number_label.grid(row=2, column=0, padx=10, pady=10)
        new_fleet_number_entry = Entry(self.add_new_record_frame, font=("Arial", 20))
        new_fleet_number_entry.grid(row=2, column=1, padx=10, pady=10)

        global new_description_entry
        description_label = Label(self.add_new_record_frame, text="Parts Description", font=("Arial", 20))
        description_label.grid(row=4, column=0, padx=10, pady=10)
        new_description_entry = Entry(self.add_new_record_frame,font=("Arial", 20))
        new_description_entry.grid(row=4, column=1, padx=10, pady=10)

        global new_location_entry
        location_label = Label(self.add_new_record_frame, text="Bin Location", font=("Arial", 20))
        #location_label.grid(row=5, column=0, padx=10, pady=10)
        new_location_entry = Entry(self.add_new_record_frame)
        #new_location_entry.grid(row=5, column=1, padx=10, pady=10)

        #location = data.locations

        global new_locations_combobox
        new_locations_label = Label(self.add_new_record_frame, text="Bin Location", font=("Arial", 20))
        new_locations_label.grid(row=5, column=0, padx=10, pady=10)
        # Create the combobox
        new_locations_combobox = ttk.Combobox(self.add_new_record_frame, values=locations,font=("Arial", 20))
        new_locations_combobox.grid(row=5, column=1, padx=10, pady=10)

        global new_job_combobox
        new_job_label = Label(self.add_new_record_frame, text="Job Kind", font=("Arial", 20))
        new_job_label.grid(row=6, column=0, padx=10, pady=10)
        # Create the combobox
        new_job_combobox = ttk.Combobox(self.add_new_record_frame, values=job_options, font=("Arial", 20))
        new_job_combobox.grid(row=6, column=1, padx=10, pady=10)

        global clicked
        clicked = StringVar()
        # clicked.set(name_options[0])
        global date_label

        def select_date():
            date_label.config(text=calendar.get_date())
            date_window.destroy()

        def bind_select_date(event):
            select_date()

        def pick_date():
            global calendar, date_window
            date_window = Toplevel()
            date_window.grab_set()
            date_window.title("Select Date")
            date_window.geometry("400x350")
            calendar = Calendar(date_window, selectmode='day', date_pattern="dd-mm-y",font=("Arial", 20), borderwidth=2)
            #calendar.set_date_range(None, date.today())
            calendar.pack()
            confirm_button = Button(date_window, text="Confirm Date", command=select_date,font=("Arial", 20))
            confirm_button.bind("<Return>", bind_select_date)
            confirm_button.pack(pady=20)

        def bind_pick_date(event):
            pick_date()

        current_date = datetime.now().strftime("%d-%m-%Y")
        global new_date_entry
        new_date_label = Label(self.add_new_record_frame, text="Date Received", font=("Arial", 20))
        new_date_label.grid(row=7, column=0, padx=10, pady=10)

        date_label = Label(self.add_new_record_frame,text=current_date, font=("Arial", 20))
        #date_label = Label(root, text=current_date)
        date_label.grid(row=7, column=1, padx=10, pady=10)

        select_button = Button(self.add_new_record_frame, text="Change Date", command=pick_date,font=("Arial", 20))
        select_button.bind("<Return>", bind_pick_date)
        select_button.grid(row=7, column=2, padx=10, pady=10)
        current_date = get_current_date()
        add_button = Button(self.add_new_record_frame, text="Add Record", command=self.add_record_to_database,
                            font=("Arial", 20))
        add_button.bind("<Return>", self.bind_add_record_to_database)
        add_button.grid(row=8, column=1, padx=20, pady=10)

        cancel_button = Button(self.add_new_record_frame, text="Cancel", command=self.cancel_entry, font=("Arial", 20))
        cancel_button.bind("<Return>", self.bind_cancel_entry)
        cancel_button.grid(row=8, column=2, padx=10, pady=10)

    global update_date
    update_date = None
    def frame_update_func(self):
        selected_item = self.my_tree.focus()
        if selected_item:
            flee_number = update_fleet_number_entry.get().upper().strip()
            description = update_description_entry.get().title().strip()
            date = update_date_label.cget("text")
            location = update_locations_combobox.get()
            job_kind = updated_job_combobox.get()
            oid = database_id_entry.get()

            self.my_tree.item(selected_item, values=(oid, flee_number, description))

            with sqlite3.connect(database) as connection:
                cursor = connection.cursor()
                cursor.execute("""UPDATE vor_shelves_data 
                SET fleet_number = ?,parts_description = ?,in_stock_since = ? ,location = ? , job_kind = ?
                WHERE oid = ?
                """, (flee_number, description, date,location,job_kind, oid))

            self.clear_entry_boxes()
            messagebox.showinfo("Vor Small Tools Update", "Record Updated.")
            self.reset()
            self.update_record_frame.destroy()
        else:
            messagebox.showinfo("Vor Small Tools Update", "Please select a record to update.")

    def update_details_frame(self):
        """Update the details"""
        selected = self.my_tree.focus()
        if not selected:
            # If no record is selected, prompt the user to select one
            messagebox.showinfo("Select Record", "Please select a record in the Treeview to update.")
            return

        global update_record_frame
        app_width: int = 800
        app_height = 400
        self.update_record_frame = Toplevel(self.window)
        screen_width = self.update_record_frame.winfo_screenwidth()
        screen_height = self.update_record_frame.winfo_screenheight()
        # This will center the app on the screen
        x = (screen_width / 2) - (app_width / 2)
        y = (screen_height / 2) - (app_height / 2)

        #selected = self.my_tree.focus()
        #if not selected:
            # If no record is selected, prompt the user to select one
          #  messagebox.showinfo("Select Record", "Please select a record in the Treeview to update.")
           # return

        # Grab record values from the tree
        values = self.my_tree.item(selected, 'values')
        self.update_record_frame.geometry(f'{app_width}x{app_height}+{int(x)}+{int(y)}')
        self.update_record_frame.title(f"Update Record {self.kdm_division} Database")
        frame = self.update_record_frame

        global update_fleet_number_entry
        update_fleet_number_label = Label(frame, text='Fleet Number', font=("Arial", 20))
        update_fleet_number_label.grid(row=2, column=0, padx=10, pady=10)
        update_fleet_number_entry = Entry(frame, font=("Arial", 20))
        # insert the value correspondent to the fleet number
        update_fleet_number_entry.insert(0, values[1])
        update_fleet_number_entry.grid(row=2, column=1, padx=10, pady=10)

        global update_description_entry
        update_description_label = Label(frame, text="Parts Description", font=("Arial", 20))
        update_description_label.grid(row=4, column=0, padx=10, pady=10)
        update_description_entry = Entry(frame, font=("Arial", 20))
        update_description_entry.insert(0, values[2])
        update_description_entry.grid(row=4, column=1, padx=10, pady=10)

        global update_location_entry
        update_location_label = Label(frame, text="Bin Location", font=("Arial", 20))
        #location_label.grid(row=5, column=0, padx=10, pady=10)
        update_location_entry = Entry(frame, font=("Arial", 20))
        #new_location_entry.grid(row=5, column=1, padx=10, pady=10)
        #locations = get_location_data(database,"vor_locations")
        #print(f"locations{locations}")

        global update_locations_combobox
        update_locations_label = Label(frame, text="Bin Location", font=("Arial", 20))
        update_locations_label.grid(row=5, column=0, padx=10, pady=10)
        # Create the combobox
        update_locations_combobox = ttk.Combobox(frame, values=locations,font=("Arial", 20))
        #update_locations_combobox['values'] = values[4]
        update_locations_combobox.set(values[6])
        update_locations_combobox.grid(row=5, column=1, padx=10, pady=10)

        global updated_job_combobox
        updated_job_combobox_label = Label(frame, text="Job Kind", font=("Arial", 20))
        updated_job_combobox_label.grid(row=6, column=0, padx=10, pady=10)
        # Create the combobox
        updated_job_combobox = ttk.Combobox(frame, values=job_options, font=("Arial", 20))
        updated_job_combobox.set(values[5])
        updated_job_combobox.grid(row=6, column=1, padx=10, pady=10)

        global clicked
        clicked = StringVar()
        # clicked.set(name_options[0])
        global date_label

        def select_date():
            update_date_label.config(text=calendar.get_date())
            global update_date
            update_date = calendar.get_date()
            date_window.destroy()

        def bind_select_date(event):
            select_date()

        def pick_date():
            global calendar, date_window
            date_window = Toplevel()
            date_window.grab_set()
            date_window.title("Alter Date")
            date_window.geometry("400x450")
            calendar = Calendar(date_window, selectmode='day', date_pattern="dd-mm-y",font=("Arial", 20), borderwidth=2)
            #calendar.set_date_range(None, date.today())
            calendar.pack()
            confirm_button = Button(date_window, text="Confirm Date", command=select_date,font=("Arial", 20))
            confirm_button.bind("<Return>", bind_select_date)
            confirm_button.pack(pady=20)

        def bind_pick_date(event):
            pick_date()
        # get the current date and format it into the day-month-year format
        current_date = datetime.now().strftime("%d-%m-%Y")
        global update_date_label
        update_date_label = Label(frame, text="Date Received", font=("Arial", 20))
        update_date_label.grid(row=7, column=0, padx=10, pady=10)
        old_date = values[3]
        update_date_label = Label(frame,text=old_date, font=("Arial", 20))
        #date_label = Label(root, text=current_date)
        update_date_label.grid(row=7, column=1, padx=10, pady=10)

        select_button = Button(frame, text="Select Date", command=pick_date,font=("Arial", 20))
        select_button.bind("<Return>", bind_pick_date)
        select_button.grid(row=7, column=2, padx=10, pady=10)
        current_date = get_current_date()

        update_button = Button(frame, text="Update", command=self.frame_update_func,
                            font=("Arial", 20))
        update_button.bind("<Return>", self.frame_update_func)
        update_button.grid(row=8, column=1, padx=20, pady=10)

        cancel_button = Button(frame, text="Cancel", command=self.cancel_update_records, font=("Arial", 20))
        cancel_button.bind("<Return>", self.bind_cancel_update_records)
        cancel_button.grid(row=8, column=2, padx=10, pady=10)

    def remove_one(self):
        """Remove one item from the database"""
        selected_to_delete = self.my_tree.focus()
        if not selected_to_delete:
            messagebox.showinfo("Select Record", "Please select a record in the Treeview to delete.")
            return
        confirmation = messagebox.askyesno("Delete Item", "Delete Item?")
        if confirmation == YES:
            #selected_to_delete = self.my_tree.selection()[0]
            self.my_tree.delete(selected_to_delete)
            # Create a database or connect to one that exists
            connection = sqlite3.connect(database)
            # Create a cursor instance
            cursor = connection.cursor()
            # Delete From Database
            with connection:
                cursor.execute("DELETE from vor_shelves_data WHERE oid=" + database_id_entry.get())
            # Clear The Entry Boxes
            self.clear_entry_boxes()
            # Add a little message box for fun
            messagebox.showinfo("Deleted!", "Your Record Has Been Deleted!")
            self.reset()

    def search_by_fleet_number(self, *args):
        """Search By Fleet number"""
        lookup_record = search_fleet_entry.get().strip(' ')
        division = self.kdm_division
        #lookup_record = self.search_var.get().strip(' ')
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
            # this will return everything that matches the search criteria
            cursor.execute("SELECT rowid, * FROM vor_shelves_data WHERE fleet_number like ?",
                          ('%' + lookup_record + '%',))
            records = cursor.fetchall()
            # Add our data to the screen
        return records

    def bind_search_by_feet_number(self, event):
        records = self.search_by_fleet_number()
        populate_division_tree(self.my_tree, records)

    def bind_query_kdm_division(self, event):
        """Bind function to query the database"""
        self.reset()

    def update_details(self):
        selected_item = self.my_tree.focus()
        flee_number = info_fleet_number_entry.get().upper().strip()
        description = info_description_entry.get().title().strip()
        date = info_date_added_entry.get()
        location = info_locations_combobox.get()
        job_kind = info_job_kind_combobox.get()
        oid = database_id_entry.get()

        self.my_tree.item(selected_item, values=(oid, flee_number, description))

        with sqlite3.connect(database) as connection:
            cursor = connection.cursor()
            cursor.execute("""UPDATE vor_shelves_data 
            SET fleet_number = ?,parts_description = ?,in_stock_since = ? ,location = ?,job_kind = ?
            WHERE oid = ?
            """, (flee_number, description, date,location, job_kind,oid))

        self.clear_entry_boxes()
        messagebox.showinfo(f"Vor {kdm_division} Update", "Record Updated.")
        self.reset()

    def bind_update_details(self, event):
        self.update_details()

    def frame(self):
        global main_frame
        main_frame = Frame(self.window, width=1200, height=700)
        main_frame.pack()

        global items_qty_label
        items_qty_label = Label(main_frame, text="", font=("Arial", 30))
        #items_qty_label.config(text=)
        items_qty_label.grid(row=0, column=0, padx=10, pady=10)

        global search_fleet_entry
        search_fleet_number_label = Label(main_frame, text="Search Fleet Number", font=("Arial", 30))
        search_fleet_number_label.grid(row=0, column=1, padx=10, pady=10)

        # set up the dynamic search
        search_fleet_entry = Entry(main_frame)
        search_fleet_entry.bind("<Return>", self.bind_search_by_feet_number)
        search_fleet_entry.grid(row=0, column=2, padx=10, pady=10)
        # set up the reset button
        reset_button = Button(main_frame, text="Reset", command=self.reset, font=("Arial", 20))
        reset_button.bind("<Return>", self.bind_query_kdm_division)
        reset_button.grid(row=0, column=4, padx=10, pady=10)
        # setup tree frame
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
                            rowheight=22,
                             fieldbackground="#D3D3D3")

        self.style.configure("Treeview.Heading", font=("Arial", 15))  # Set the font size here for the column headings
        # configure the rows in the tree
        self.style.configure("Treeview", font=("Arial", 15))  # Set the font size here
        # Change Selected Color #347083
        self.style.map('Treeview',
                       background=[('selected', self.saved_highlight_color)])
        self.blue = "blue"
        self.gray = "lightgray"
        self.white = "white"

        self.my_tree.tag_configure('oddrow', background=self.gray)
        self.my_tree.tag_configure('evenrow', background=self.white)

        visible_items = 20  # Adjust the number of items visible in the treeview
        self.my_tree["height"] = visible_items

        self.my_tree['columns'] = (
            "id", "fleet_number", "parts_description", "in_stock_since", "status", "job_type","location")

        # Format Our Columns
        self.my_tree.column("#0", width=0, stretch=NO)
        self.my_tree.column("id",width=0 ,stretch=NO)
        self.my_tree.column("fleet_number", anchor=W, width=180)
        self.my_tree.column("parts_description", anchor=W, width=350)
        self.my_tree.column("in_stock_since", anchor=CENTER, width=150)
        self.my_tree.column("status", anchor=CENTER, width=175)
        self.my_tree.column("job_type", width=130, stretch=NO)
        self.my_tree.column("location", width=150)

        # Create Headings
        self.my_tree.heading("#0", text="", anchor=W)
        self.my_tree.heading("id", text="ID", anchor=W)
        self.my_tree.heading("fleet_number", text="Fleet Number", anchor=W)
        self.my_tree.heading("parts_description", text="Parts Description", anchor=W)
        self.my_tree.heading("in_stock_since", text="In Stock Since", anchor=CENTER)
        self.my_tree.heading("status", text="Days In Stock", anchor=CENTER)
        self.my_tree.heading("job_type", text="Job Type", anchor=CENTER)
        self.my_tree.heading("location", text="Location", anchor=CENTER)

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
        #database_id_label.grid(row=0, column=6, padx=10, pady=10)
        database_id_entry = Entry(information_frame)
        #database_id_entry.grid(row=0, column=7, padx=10, pady=10)

        global division_entry
        division_label = Label(information_frame, text=second_column_name)
        # division_label.grid(row=0, column=0, padx=10, pady=10)
        division_entry = Entry(information_frame)
        # division_entry.grid(row=0, column=1, padx=10, pady=10)

        global info_fleet_number_entry
        fleet_number_label = Label(information_frame, text=third_column_name)
        #fleet_number_label.grid(row=0, column=0, padx=10, pady=10)
        info_fleet_number_entry = Entry(information_frame)
        #info_fleet_number_entry.grid(row=0, column=1, padx=10, pady=10)

        global info_description_entry
        description_label = Label(information_frame, text=fifth_column_name)
        #description_label.grid(row=0, column=2, padx=10, pady=10)
        info_description_entry = Entry(information_frame)
        #info_description_entry.grid(row=0, column=3, padx=10, pady=10)

        # clicked = StringVar()
        # clicked.set(options[0])

        global info_date_added_entry
        date_added_label = Label(information_frame, text=seventh_column_name)
        #date_added_label.grid(row=0, column=4, padx=10, pady=10)
        info_date_added_entry = Entry(information_frame)
        #info_date_added_entry.grid(row=0, column=5, padx=10, pady=10)


        global info_locations_combobox
        location_label = Label(information_frame, text="VOR-Location")
        #location_label.grid(row=0, column=6, padx=10, pady=10)
        # Create the combobox
        info_locations_combobox = ttk.Combobox(information_frame, values=locations)
        #info_locations_combobox.grid(row=0, column=7, padx=10, pady=10)

        global info_job_kind_combobox
        #job_options = ["Select Job...", "O/S", "VOR", "Breakdown", "Cat B"]
        info_job_kind_label = Label(information_frame, text="Job Kind")
        # location_label.grid(row=0, column=6, padx=10, pady=10)
        # Create the combobox
        info_job_kind_combobox = ttk.Combobox(information_frame, values=job_options)
        # info_locations_combobox.grid(row=0, column=7, padx=10, pady=10)

        global info_location_entry
        info_location_label = Label(information_frame, text="Location")
        #info_location_label.grid(row=0, column=6, padx=10, pady=10)
        info_location_entry = Entry(information_frame)
        #info_location_entry.grid(row=0, column=7, padx=10, pady=10)

        # Item Info Frame
        update_button = Button(information_frame, text="Update Record", command=self.update_details)
        update_button.bind("<Return>", self.bind_update_details)
        #update_button.grid(row=1, column=0, padx=10, pady=10)

        # Command Frame
        command_frame = LabelFrame(self.window, text="Commands", font=("Arial", 30))
        command_frame.pack(fill="x", expand="yes", padx=20)

        # Add Buttons
        add_new_button = Button(command_frame, text="Add New Record",
                                command=self.add_new_record_window, font=("Arial", 15))
        add_new_button.bind()
        add_new_button.grid(row=0, column=0, padx=10, pady=10)

        # update Button
        update_button = Button(command_frame, text="Update Record",command=self.update_details_frame, font=("Arial", 15))
        update_button.bind()
        update_button.grid(row=0, column=1, padx=10, pady=10)

        remove_selected_button = Button(command_frame, text="Remove Selected",command=self.remove_one, font=("Arial", 15))
        remove_selected_button.bind()
        remove_selected_button.grid(row=0, column=2, padx=10, pady=10)

        clear_entry_button = Button(command_frame, text="Clear Entry Boxes",command=self.clear_entry_boxes, font=("Arial", 15))
        #clear_entry_button.grid(row=0, column=7, padx=10, pady=10)

        generate_report_button = Button(command_frame, text="Generate Report",command=self.create_division_report, font=("Arial", 15))
        generate_report_button.grid(row=0, column=8, padx=10, pady=10)

        # Bind the treeview
        self.my_tree.bind("<ButtonRelease-1>", self.select_record)
        self.my_tree.bind("<Return>", self.select_record)
        self.my_tree.bind("<Up>", self.select_record)
        self.my_tree.bind("<Down>", self.select_record)

        self.my_tree.bind("<R>", self.bind_generate_report)


        def update():
            records = query_kdm_division(self.my_tree, database, self.kdm_division)
            populate_division_tree(self.my_tree, records)
            # self.master_root.after(1000, update)

        update()

if __name__ == "__main__":
    root = Tk()
    global kdm_division
    kdm_division = "Plant"
    division_image = "images/plant.png"
    # division_image = "images/small.png"
    KdmDivisionClass(root, kdm_division, division_image)
    root.mainloop()
