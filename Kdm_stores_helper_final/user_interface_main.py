from time import strftime

#from Not_used.info_board_class import InfoWhiteBoard
from kdm_division_info_class import *
#from division_class import *
from kdm_service_kits_class import *
from returns_class import *
from tools_class import *
from PIL import Image
from tkinter import Tk, Label
from PIL import Image, ImageTk


root = Tk()
root.title("Kdm Division Selection")
# Designate Height and Width of our app
define_size(root, 1250, 830)


def select_small_tools():
    KdmDivisionClass(root, "Small Tools", "images/small_tools.png")


def bind_selected_small_tools(event):
    select_small_tools()



def select_k_power():
    KdmDivisionClass(root, "K Power", "images/kpower.png")


def bind_selected_k_power(event):
    select_k_power()


def select_power_access():
    KdmDivisionClass(root, "Power Access", "images/power access.png")


def bind_selected_power_access(event):
    select_power_access()


def select_plant():
    KdmDivisionClass(root, "Plant","images/plant.png")


def bind_selected_plant(event):
    select_plant()


def selected_service_kits():
    service_image = "images/Service .png"
    ServiceKits(root, service_image)


def bind_selected_service_kits(event):
    selected_service_kits()


def select_lorrybay():
    KdmDivisionClass(root, "Vehicles", "images/lorry bay.png")


def bind_selected_lorrybay(event):
    select_lorrybay()


def selected_tools():
    ToolsClass(root,"images/tools_2.png")

def bind_selected_tools(event):
    selected_tools()


def selected_used_parts():
    pass
    #output_label.config(text=" ")
    #output_label.config(text="Used parts Selected")
    # used_parts_blob = UsedPartsBlob(root)
    # used_parts_blob = UsedPartsBlobCopy(root)
    # used_parts_blob = UsedPartsRefactored(root)


def bind_selected_used_parts(event):
    selected_used_parts()


def select_information_board():
    kdm_division = "Small Tools"
    division_image = "images/resized_image.png"
    GoodsReturnClass(root,kdm_division, division_image)


def bind_information_board(event):
    select_information_board()


# Define images
#kdm_logo = PhotoImage(file="images/kdm_logo.png")
kdm_logo = Image.open("images/kdm_logo.png")
kdm_logo = ImageTk.PhotoImage(kdm_logo)

#small_tools_button_image = PhotoImage(file="images/small_tools.png")
small_tools_button_image = Image.open("images/small_tools.png")
small_tools_button_image = ImageTk.PhotoImage(small_tools_button_image)

#kpower_button_image = PhotoImage(file="images/kpower.png")
kpower_button_image = Image.open("images/kpower.png")
kpower_button_image = ImageTk.PhotoImage(kpower_button_image)

#power_access_button_image = PhotoImage(file="images/power access.png")
power_access_button_image = Image.open("images/power access.png")
power_access_button_image = ImageTk.PhotoImage(power_access_button_image)

#plant_button_image = PhotoImage(file="images/plant.png")
plant_button_image = Image.open("images/plant.png")
plant_button_image = ImageTk.PhotoImage(plant_button_image)

#lorrybay_button_image = PhotoImage(file="images/lorry bay.png")
lorrybay_button_image = Image.open("images/lorry bay.png")
lorrybay_button_image = ImageTk.PhotoImage(lorrybay_button_image)

#service_kit_button_image = PhotoImage(file="images/Service .png")
service_kit_button_image = Image.open("images/Service .png")
service_kit_button_image = ImageTk.PhotoImage(service_kit_button_image)

tools_button_image = Image.open("images/tools_4.png")
tools_button_image = ImageTk.PhotoImage(tools_button_image)

used_part_button_image = Image.open("images/used_parts_2.png")
used_part_button_image = ImageTk.PhotoImage(used_part_button_image)
def resize_image(image, width, heigth):
    from PIL import Image
    original_image = Image.open(image)
    # Define the desired width and height
    new_width = width
    new_height = heigth
    # Resize the image
    resized_image = original_image.resize((new_width, new_height))
    resized_image.save("images/resized_image.png")
    print("image resized.")
    #return resized_image.save("images/resized_image.png")

#image = resize_image(image,180,100)
original_image = Image.open("images/returns.png")

# Define the desired width and height
new_width = 180
new_height = 100

# Resize the image
#resized_image = original_image.resize((new_width, new_height))
#resized_image.save("images/resized_image.png")
#blueboard_button_image = PhotoImage(file="images/resized_image.png")
blueboard_button_image = Image.open("images/resized_image.png")
blueboard_button_image = ImageTk.PhotoImage(blueboard_button_image)
# Define Frames
general_frame = Frame(root,background="darkblue")
general_frame.pack(pady=10, padx=10)

logo_frame = Frame(general_frame, background="darkblue")
logo_frame.grid(row=0, column=0, pady=10)

kdm_logo_image = Label(logo_frame, image=kdm_logo)
kdm_logo_image.grid(row=0, column=1, pady=30, padx=30)

division_frame = Frame(general_frame,background="darkgray")
division_frame.grid(row=1, column=0)

tools_and_spares_frame = Frame(general_frame, bg='lightgrey',)
tools_and_spares_frame.grid(row=2, column=0, pady=30)

used_parts_frame = Frame(general_frame, bg='lightgrey', )
used_parts_frame.grid(row=3, column=0, pady=10)

service_kits_frame = Frame(general_frame, bg='lightgrey', )
service_kits_frame.grid(row=4, column=0, pady=10)

time_label = Label(logo_frame, font=("Arial", 30))

def time():
    time_string = strftime('%H:%M:%S %p')
    # time_label = Label(root, font=("ds-digital", 80), background="black", foreground='cyan')
    time_label.config(text=time_string)
    time_label.after(1000, time)
    return time_label

time()
time_label.grid(row=0, column=0)
time_label.after(1000, time)

time_label.grid(row=0, column=0)
date = datetime.now().strftime("%d-%m-%Y")
date_label = Label(logo_frame, text=date, font=("Arial", 30),pady=10, padx=20)
date_label.grid(row=0, column=3)

# use images like buttons in Division Frame
small_tools_button = Button(division_frame, image=small_tools_button_image, command=select_small_tools)
small_tools_button.grid(row=2, column=0, padx=20)
small_tools_button.bind("<Return>", bind_selected_small_tools)
small_tools_label = Label(division_frame, text="Small Tools",font=("Arial", 30))
small_tools_label.grid(row=3, column=0)

kpower_button = Button(division_frame, image=kpower_button_image, command=select_k_power)
kpower_button.grid(row=2, column=1, padx=20)
kpower_button.bind("<Return>", bind_selected_k_power)
kpower_label = Label(division_frame, text="K-Power",font=("Arial", 30))
kpower_label.grid(row=3, column=1)

power_access_button = Button(division_frame, image=power_access_button_image, command=select_power_access)
power_access_button.grid(row=2, column=2, padx=20)
power_access_button.bind("<Return>", bind_selected_k_power)
power_access_label = Label(division_frame, text="Power Access",font=("Arial", 30))
power_access_label.grid(row=3, column=2)

plant_image_button = Button(division_frame, image=plant_button_image, command=select_plant)
plant_image_button.grid(row=2, column=3, padx=20)
plant_image_button.bind("<Return>", bind_selected_plant)
plant_label = Label(division_frame, text="Plant",font=("Arial", 30))
plant_label.grid(row=3, column=3)

lorrybay_image_button = Button(division_frame, image=lorrybay_button_image, command=select_lorrybay)
lorrybay_image_button.grid(row=2, column=4, padx=20, pady=20)
lorrybay_image_button.bind("<Return>", bind_selected_lorrybay)
lorry_bay_label = Label(division_frame, text="Lorrybay",font=("Arial", 30), pady=5)
lorry_bay_label.grid(row=3, column=4)

# tools set up
tools_button = Button(division_frame, image=tools_button_image, command=selected_tools)
tools_button.grid(row=4, column=3, padx=10)
tools_button.bind("<Return>", bind_selected_tools)
tools_label = Label(division_frame, text="Tools")
tools_label.grid(row=5, column=3)

# used parts set up
used_parts_button = Button(used_parts_frame, image=used_part_button_image, command=selected_used_parts)
used_parts_button.grid(row=4, column=2, padx=10, pady=10)
used_parts_button.bind("<Return>", bind_selected_used_parts)
used_parts_label = Label(used_parts_frame, text="Used Parts")
used_parts_label.grid(row=5, column=2)

service_kit_image_button = Button(division_frame, image=service_kit_button_image, command=selected_service_kits)
service_kit_image_button.grid(row=4, column=2, padx=10)
service_kit_image_button.bind("<Return>", bind_selected_service_kits)
service_kits_label = Label(division_frame, text="Service Kits")
service_kits_label.grid(row=5, column=2)

# use images like buttons in Division Frame
board_button = Button(division_frame, image=blueboard_button_image, command=select_information_board, width=180, height=100)
board_button.grid(row=4, column=1, padx=10, pady=20)
board_button.bind("<Return>", bind_information_board)
board_button_label = Label(division_frame, text="Goods Returns")
board_button_label.grid(row=5, column=1)

root.mainloop()

