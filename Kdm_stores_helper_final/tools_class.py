#!/usr/local/bin/python3.11
#from tkinter_widgets import *
#from icecream import ic
from tkinter import *
import sqlite3
import datetime
from datetime import date
from tkcalendar import Calendar, DateEntry
from tkinter import messagebox
from configparser import ConfigParser
from frame_functions import *
from pdf_report import *
from sql_database import *
#from tkinter import askopenfilename

#import tkinter_widgets as tk
#from tkinter_widgets import ttk
#from tkinter_widgets import filedialog
#import fitz

database = "database_files/kdm_stores.db"
lookup_record = "Small Tools"


class ToolsClass:

    def __init__(self, master_root, tools_image):
        """Init method for objects of class Small tools"""

        #kdm_division = kdm_division
        self.unique_id_counter = 0
        self.report = None
        self.master_root = master_root
        self.window = Toplevel(master_root)
        tools_text = "Tools Management"
        self.window.title(tools_text)
        self.parser = ConfigParser()
        self.parser.read("treebase.ini")
        self.saved_primary_color = self.parser.get('colors', 'primary_color')
        self.saved_secondary_color = self.parser.get('colors', 'secondary_color')
        self.saved_highlight_color = self.parser.get('colors', 'highlight_color')

        # Designate Height and Width of our app
        app_width = 1400
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
        self.button_image = PhotoImage(file=tools_image)
        label_text = f"Close {tools_text} window"
        self.label = Label(self.window, text=label_text)
        self.label.pack()
        self.button = Button(self.window, image=self.button_image, command=self.close)
        self.button.pack(pady=10)
        self.button.bind("<Return>", self.bind_close)

    def get_unique_id(self):
        self.unique_id_counter += 1
        return self.unique_id_counter
    def update1(self):
        # pass
        records = get_tool_data(database)
        self.populate_tools_tree(self.my_tree, records)

    def update(self):
        # pass
        records = get_tool_data(database)
        self.populate_tools_tree(self.my_tree, records)
        #self.add_new_record_frame.destroy()
        #self.master_root.after(1000, self.update)
    def remove_tool1(self):
        selected = self.my_tree.focus()
        values = self.my_tree.item(selected, 'values')
        print(f"values{values[0]}")
        tool_name = values[0]
        x = self.my_tree.selection()[0]
        self.my_tree.delete(x)

        try:
            # Create a database or connect to one that exists
            with sqlite3.connect(database) as connection:
                cursor = connection.cursor()

                # Check if the tool exists in the "tools" table
                cursor.execute("SELECT COUNT(*) FROM tools WHERE tool_name=?", (tool_name,))
                count = cursor.fetchone()[0]

                if count > 0:
                    # Remove the tool from the "tools" table
                    cursor.execute("DELETE from tools WHERE oid ?" + database_id_entry.get())
                    #cursor.execute("DELETE from tools WHERE oid=?" (x,))
                    #cursor.execute("DELETE FROM tools WHERE tool_name=?", (tool_name,))

                    # Commit the changes to the database
                    connection.commit()

                    print(f"Tool '{tool_name}' removed from the 'tools' table.")
                    self.update()
                    # Log the tool removal operation
                    log_message = f"Tool Removed: Tool Name - {tool_name}"
                    logging.info(log_message)
                    self.update()
                else:
                    print(f"Tool '{tool_name}' not found in the 'tools' table.")


        except sqlite3.Error as e:
            print(f"Error occurred: {e}")
            logging.error(f"Error removing tool from the database: {e}")

    def clear_entry_boxes(self):
        database_id_entry.delete(0, END)

    def select_record(self, event):
        """
            Selects a record from the tree view and populates entry boxes with its values.

            This method retrieves the selected record from the tree view and extracts its values. It then populates the entry boxes
            with the values of the selected record, allowing for easy editing. Additionally, it prints the values to the console for
            debugging purposes.

            Args:
                event: The event object that triggered the selection (e.g., a mouse click).

            Returns:
                None
            """
        self.clear_entry_boxes()
        # Grab record Number
        selected = self.my_tree.focus()
        # Grab record values from the tree
        values = self.my_tree.item(selected, 'values')
        print(values)
        # output to entry boxes
        try:
            database_id_entry.insert(0, values[0])
            #id = database_id_entry.insert(0, values[0])
            print(f"the id is {database_id_entry.get()}")

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


    def populate_tools_tree(self, tree, records):
        """
           Populates the tree view widget with tool records.

           This method clears the existing records from the tree view and then iterates through the provided records to add them
           to the tree view. It calculates the elapsed time since the tool has been in stock and adds each record to the tree view
           with appropriate formatting. Additionally, it assigns tags to alternate rows for visual distinction.

           Args:
               tree: The tree view widget to populate.
               records: A list of tuples containing tool records, where each tuple represents a single record.

           Returns:
               None
           """

        for record in tree.get_children():
            tree.delete(record)
        current_time = datetime.now()

        for count, record in enumerate(records, start=1):
            in_stock_since = datetime.strptime(record[3], "%d-%m-%Y")
            elapsed_time = (current_time - in_stock_since).days

            # Check if the item with the same identifier already exists
            if tree.exists(count):
                pass
                # Handle this situation, e.g., by updating the existing item
                # or generating a unique identifier
                # count = get_unique_id()

            row_tag = 'evenrow' if count % 2 == 0 else 'oddrow'
            tree.insert(parent='', index='end', iid=count, text='',
                        values=(record[0], record[1], record[2], record[3], elapsed_time),
                        tags=(row_tag,))
    def populate_tools_tree2(self, tree, records):
        current_time = datetime.now()

        for count, record in enumerate(records, start=1):
            in_stock_since = datetime.strptime(record[3], "%d-%m-%Y")
            elapsed_time = (current_time - in_stock_since).days

            # Check if the item with the same identifier already exists
            if tree.exists(count):
                pass
                # Handle this situation, e.g., by updating the existing item
                # or generating a unique identifier
                #count = get_unique_id()
            if count % 2 == 0:
                tree.insert(parent='', index='end', iid=count, text='',
                            values=(record[0], record[1], record[2], record[3], elapsed_time),
                            tags=('evenrow',))
            else:
                tree.insert(parent='', index='end', iid=count, text='',
                            values=(record[0], record[1], record[2], record[3], elapsed_time),
                            tags=('oddrow',))

    def bind_add_tool(self,event):
        self.add_tool_request()

    def add_tool_request(self):
        """
            Adds a tool request to the database.

            This method retrieves the tool name, requester name, and request date from the input fields in the tool request window.
            It then inserts this information into the 'tools' table in the database. Additionally, it logs the tool request information
            to a log file. Finally, it updates the GUI and destroys the tool request window.

            Returns:
                None
            """
        tool_name = tool_entry.get()
        requester_name = requested_by_entry.get()
        request_date = date_label.cget("text")

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
            self.update()
            self.add_new_record_frame.destroy()

        except sqlite3.Error as e:
            print(f"Error occurred: {e}")
            logging.error(f"Error adding tool request to the database: {e}")

    def bind_query_kdm_division(self, event):
        self.update()

    def pick_date1(self):
        global calendar, date_window
        date_window = Toplevel()
        date_window.grab_set()
        date_window.title("Please Select a Date")
        date_window.geometry("250x220")
        calendar = Calendar(date_window, selectmode='day', date_pattern="dd-mm-y")
        calendar.place(x=0, y=0)
        select_button = Button(date_window, text="Select", command=self.select_date)
        select_button.place(x=80, y=190)

    def bind_select_date(self, event):
        self.pick_date1()

    def select_date(self):
        date_label.config(text=calendar.get_date())
        date_window.destroy()

    def book_tool_out_window(self):

        """
          Opens a window for booking a tool out.

          This method creates a new window for booking a tool out. It provides fields for entering the tool name and the person
          who is requesting the tool. The window is centered on the screen.

          Returns:
              None
          """
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
        self.add_new_record_frame.title(f"Book took out")

        global tool_entry
        tool_name = Label(self.add_new_record_frame, text='Tool Name', font=("Arial", 30))
        tool_name.grid(row=2, column=0, padx=10, pady=10)
        tool_entry = Entry(self.add_new_record_frame)
        tool_entry.grid(row=2, column=1, padx=10, pady=10)

        global requested_by_entry
        requested_by_label = Label(self.add_new_record_frame, text="Requested By", font=("Arial", 30))
        requested_by_label.grid(row=4, column=0, padx=10, pady=10)
        requested_by_entry = Entry(self.add_new_record_frame)
        requested_by_entry.grid(row=4, column=1, padx=10, pady=10)

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
            """
               Opens a window for selecting a date.

               This function creates a new window for selecting a date using a calendar widget. The user can select a date from the calendar.
               A confirm button is provided to finalize the selection. The selected date can then be used for further processing.

               Returns:
                   None
               """
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
        new_date_label = Label(self.add_new_record_frame, text="Date Received", font=("Arial", 30))
        new_date_label.grid(row=6, column=0, padx=10, pady=10)

        date_label = Label(self.add_new_record_frame,text=current_date, font=("Arial", 30))
        #date_label = Label(root, text=current_date)
        date_label.grid(row=6, column=1, padx=10, pady=10)

        select_button = Button(self.add_new_record_frame, text="Select", command=pick_date,font=("Arial", 30))
        select_button.bind("<Return>", bind_pick_date)
        select_button.grid(row=6, column=2, padx=10, pady=10)
        current_date = get_current_date()
        add_button = Button(self.add_new_record_frame, text="Add Record", command=self.add_tool_request,
                            font=("Arial", 30))
        add_button.bind("<Return>", self.bind_add_tool)
        add_button.grid(row=7, column=1, padx=20, pady=10)

        cancel_button = Button(self.add_new_record_frame, text="Cancel", command=self.cancel_entry, font=("Arial", 30))
        cancel_button.bind("<Return>", self.bind_cancel_entry)
        cancel_button.grid(row=7, column=2, padx=10, pady=10)
    global update_date
    update_date = None


    def remove_one(self):

        """
           Remove one item from the database.

           This method prompts the user to confirm the return of a tool. If confirmed, the selected tool is deleted from the database
           and the associated entry in the GUI tree view is removed. Additionally, a log message is generated and displayed confirming
           the return of the tool. Finally, entry boxes are cleared and a message box is shown to inform the user that the tool has
           been marked as returned.

           Returns:
               None
           """

        confirmation = messagebox.askyesno("Confirm Return", "Mark Tool as returned Today??")
        if confirmation == YES:
            selected_to_delete = self.my_tree.selection()[0]
            tool_name = "tool"
            #print(f"selected {selected_to_delete}")
            # Create a database or connect to one that exists
            connection = sqlite3.connect(database)
            # Create a cursor instance
            cursor = connection.cursor()
            # Delete From Database
            with connection:
                cursor.execute("DELETE from tools WHERE oid =" + database_id_entry.get())
                self.my_tree.delete(selected_to_delete)
                log_message = f"Tool returned: Tool Name - {selected_to_delete}"
                print(f"log message ={log_message}")
                logging.info(log_message)
            # Clear The Entry Boxes
            self.clear_entry_boxes()
            # Add a little message box for fun
            messagebox.showinfo("Tool Return", "Tool marked as returned.")
            self.update()

    def frame(self):

        main_frame = Frame(self.window, width=1200, height=700)
        main_frame.pack()

        reset_button = Button(main_frame, text="Reset", command=self.update, font=("Arial", 20))
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
                            rowheight=30,
                             fieldbackground="#D3D3D3")

        self.style.configure("Treeview.Heading", font=("Arial", 25))  # Set the font size here for the column headings
        # configure the rows in the tree
        self.style.configure("Treeview", font=("Arial", 20))  # Set the font size here
        # Change Selected Color #347083
        self.style.map('Treeview',
                       background=[('selected', self.saved_highlight_color)])
        self.blue = "blue"
        self.gray = "lightgray"
        self.white = "white"

        self.my_tree.tag_configure('oddrow', background=self.gray)
        self.my_tree.tag_configure('evenrow', background=self.white)

        visible_items = 15  # Adjust the number of items visible in the treeview
        self.my_tree["height"] = visible_items

        first_column_name = "id"
        second_column_name = "fleet_number"
        third_column_name = "parts_description"
        fourth_column_name = "in_stock_since"
        fifth_column_name = "status"
        sixth_column_name = "kdm_division"
        #seventh_column_name = "Date Added"

        self.my_tree['columns'] = (f"{first_column_name}", f"{second_column_name}",
                                   f"{third_column_name}", f"{fourth_column_name}",
                                   f"{fifth_column_name}", f"{sixth_column_name}")

        # Format Our Columns
        self.my_tree.column("#0", width=0, stretch=NO)
        self.my_tree.column(first_column_name,width=100 ,stretch=NO)
        self.my_tree.column(second_column_name, anchor=W, width=400)
        self.my_tree.column(third_column_name, anchor=W, width=200)
        self.my_tree.column(fourth_column_name, anchor=CENTER, width=200)
        self.my_tree.column(fifth_column_name, anchor=CENTER, width=200)
        self.my_tree.column(sixth_column_name, width=0, stretch=NO)
        #self.my_tree.column("location", width=150)

        # Create Headings
        self.my_tree.heading("#0", text="", anchor=W)
        self.my_tree.heading("id", text="ID", anchor=W)
        self.my_tree.heading("fleet_number", text="Tool Description", anchor=W)
        self.my_tree.heading("parts_description", text="Requested By", anchor=W)
        self.my_tree.heading("in_stock_since", text="Date Requested", anchor=CENTER)
        self.my_tree.heading("status", text="Days Out", anchor=CENTER)
        self.my_tree.heading("kdm_division", text="KDM Division", anchor=CENTER)
        #self.my_tree.heading("location", text="Location", anchor=CENTER)

        # Create Striped Row Tags
        self.my_tree.tag_configure('oddrow', background=self.gray)
        self.my_tree.tag_configure('evenrow', background=self.white)
        # Item Info Frame
        information_frame = LabelFrame(self.window, text="Fleet Information", font=("Arial", 30))
        information_frame.pack(fill="x", expand="yes", padx=20)
        # information_frame.grid(row=3, column=0)

        global database_id_entry
        database_id_label = Label(information_frame, text=first_column_name)
        #database_id_label.grid(row=0, column=6, padx=10, pady=10)
        database_id_entry = Entry(information_frame)
        #database_id_entry.grid(row=0, column=7, padx=10, pady=10)

        # clicked = StringVar()
        # clicked.set(options[0])

        # Command Frame
        command_frame = LabelFrame(self.window, text="Commands", font=("Arial", 30))
        command_frame.pack(fill="x", expand="yes", padx=20)

        # Add Buttons
        add_new_button = Button(command_frame, text="Book Tool Out",
                                command=self.book_tool_out_window, font=("Arial", 30))
        add_new_button.bind()
        add_new_button.grid(row=0, column=0, padx=10, pady=10)

        # update Button
        update_button = Button(command_frame, text="Mark Tool as Returned",
                                command=self.remove_one, font=("Arial", 30))
        update_button.bind()
        update_button.grid(row=0, column=1, padx=10, pady=10)

        remove_selected_button = Button(command_frame, text="Returned",
                                        command=self.remove_one, font=("Arial", 30))
        remove_selected_button.bind()
        #remove_selected_button.grid(row=0, column=2, padx=10, pady=10)
        # Bind the treeview
        self.my_tree.bind("<ButtonRelease-1>", self.select_record)
        self.my_tree.bind("<Return>", self.select_record)
        self.my_tree.bind("<Up>", self.select_record)
        self.my_tree.bind("<Down>", self.select_record)
        #self.my_tree.bind()
        self.update()
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

                    return tool_data

            except sqlite3.Error as e:
                print(f"Error occurred: {e}")
                return []


if __name__ == "__main__":
    tool_image = ("images/tools_2.png")
    root = Tk()
    root.title("Kdm Division Selection")
    tools = ToolsClass(root,tool_image)

    root.mainloop()