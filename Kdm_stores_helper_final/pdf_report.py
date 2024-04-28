import sqlite3
import os
from datetime import datetime
from time import strftime
from tkinter import filedialog
from fpdf import FPDF
import shutil


#from pdf import current_time

database = "database_files/kdm_stores.db"
lookup_record = "K Power"
current_time = datetime.now()


def query_returns_pdf_data(database = None):
    database = "database_files/kdm_stores.db"
    # Create a database or connect to one that exists
    connection = sqlite3.connect(database)
    # Create a cursor instance

    cursor = connection.cursor()
    with connection:
        # Create Table
        cursor.execute("""SELECT rowid,* FROM returns""")
        records = cursor.fetchall()
        details = []
        columns = ["Fleet Number", "Parts Description", "Return created on", "Days waiting"]
        details.append(columns)
        #print(details)
        current_time = datetime.now()
        for row in records:
            in_stock_since = datetime.strptime(row[6],"%d-%m-%Y")
            #print(f"elapsed time: {in_stock_since}")
            elapsed_time = (current_time - in_stock_since).days
            fleet_number = row[3]
            parts_desc = row[4]
            in_stock_since = row[5]
            number_of_days = elapsed_time
            item = [fleet_number, parts_desc, in_stock_since, number_of_days]
            details.append(item)
            #print(details)
        # sort the results
        records = sorted(records, key=lambda x: datetime.strptime(x[6], "%d-%m-%Y"), reverse=False)
        # sort the results
        details = sorted(details[1:], key=lambda x: x[-1], reverse=True)
        # add the header to the file
        details.insert(0, columns)
        return records, records

def create_return_pdf(data):
    current_time = datetime.now()
    col_widths = [30, 80, 40, 40]  # Adjust column widths as needed
    pdf = FPDF()
    # Create the directory if it doesn't exist
    os.makedirs("pdf_reports", exist_ok=True)
    filename = f"pdf_reports/returns_{current_time.date().strftime('%d-%m-%Y')}.pdf".lower()
    pdf.add_page()
    pdf.image("images/kdm_logo.png", 60, 5, 100)
    pdf.ln(20)
    pdf.set_font("Arial", size=10)
    pdf.cell(1)
    pdf.cell(100, 8, f'Returns  -  Report Created on {current_time}', border=False, ln=1, align='C')

    for row in data:
        for i in range(len(row)):
            pdf.cell(col_widths[i], 10, str(row[i]), border=1)
        pdf.ln()

    pdf.set_y(-12)
    pdf.set_font('helvetica', 'I', 8)
    pdf.cell(0, 10, f'Page {pdf.page_no()}/{{nb}}', align='C')
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=False, margin=0)
    pdf.output(filename)
    #print(f"File {filename} created.")

def query_pdf_data(lookup_record):
    """Query the database and return everything related to a specific category"""
    database = "database_files/kdm_stores.db"
    # Create a database connection and cursor instance
    connection = sqlite3.connect(database)
    cursor = connection.cursor()
    with connection:
        # Query the database
        cursor.execute("SELECT rowid, * FROM vor_shelves_data WHERE kdm_division LIKE ?", (lookup_record,))
        records = cursor.fetchall()
        #print("record", records[7])
        details = []
        columns = ["Fleet Number", "Parts Description", "In Stock Since", "Days in stock", "Job Kind"]
        #columns = ["Fleet Number", "Parts Description", "In Stock Since", "Days in stock"]

        details.append(columns)
        current_time = datetime.now()
        for row in records:
            in_stock_since = datetime.strptime(row[5], "%d-%m-%Y")
            elapsed_time = (current_time - in_stock_since).days
            fleet_number = row[3]
            parts_desc = row[4]
            in_stock_since = row[5]
            job_kind = row[8]

            number_of_days = elapsed_time
            item = [fleet_number, parts_desc, in_stock_since, number_of_days,job_kind]
            details.append(item)
        # sort the results
        records = sorted(records, key=lambda x: datetime.strptime(x[5], "%d-%m-%Y"), reverse=False)
        # sort the results
        # Filter out None values
        #details = [detail for detail in details if detail is not 'NoneType']
        #details = sorted(details[1:], key=lambda x: x[-1],reverse=True)
        # Sort the details by elapsed time (number of days)
        details = sorted(details[1:], key=lambda x: x[3], reverse=True)
        #print(details[1:])
        # add the header to the file
        details.insert(0, columns)
    return records, details

def delete_file_if_exists(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)
        print(f"File '{file_path}' deleted.")
    else:
        print(f"File '{file_path}' does not exist.")


def create_pdf(data, kdm_division):
    current_date = datetime.now()
    current_date = current_date.date().strftime('%d-%m-%Y')
    current_time = strftime('%H:%M:%S %p')
    current_week = datetime.now()
    weekday = current_week.strftime('%A')
    #col_widths = [30, 80, 30, 30, 20]  # Adjust column widths as needed
    #hidind the last column, not needed now
    col_widths = [30, 75, 30, 30, 30]  # Adjust column widths as needed
    pdf = FPDF()
    # Create the directory if it doesn't exist
    os.makedirs("pdf_reports", exist_ok=True)
    filename = f"pdf_reports/{kdm_division}_{current_date}.pdf"
    delete_file_if_exists(filename)
    filename = f"pdf_reports/{kdm_division}_{current_date}.pdf".lower()
    pdf.add_page()
    pdf.image(f"images/{kdm_division}.png", 20, 5, 40)
    pdf.image("images/kdm_logo.png", 60, 5, 100)
    pdf.image(f"images/{kdm_division}.png", 150, 5, 40)
    pdf.ln(20)
    pdf.set_font("Arial", size=10)
    pdf.cell(1)
    pdf.cell(100, 8, f'.               {kdm_division}    - Report Created on {weekday} {current_date}        {current_time}', border=False, ln=1, align='C')

    for row in data:
        for i in range(len(row)):
            pdf.cell(col_widths[i], 7, str(row[i]), border=1)
        pdf.ln()

    # Add empty cells after all data is inserted
    for _ in range(10):
        for width in col_widths:
            pdf.cell(width, 7, "", border=1)
        pdf.ln()

    pdf.set_y(-12)
    pdf.set_font('helvetica', 'I', 8)
    #pdf.cell(0, 1, f'Page {pdf.page_no()}/{{nb}}', align='C')
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=1)
    pdf.output(filename)
    return pdf
    #print(f"File {filename} created.")

def save_pdf_to_desktop(pdf_file_path):
    desktop_path = os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop')  # Get the path to the desktop
    shutil.copy(pdf_file_path, desktop_path)  # Copy the PDF file to the desktop
