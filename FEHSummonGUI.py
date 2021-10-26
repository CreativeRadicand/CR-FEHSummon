from tkinter import *
import FEHSummonFunctions
from PIL import ImageTk,Image

import math

root = Tk()
root.geometry("800x600")
root.title("Fire Emblem Heroes: Sadness Simulator")

# These will be the functions that result in the clicking of the widgets:

def bTypeUpdate():
    global base_pullrate
    base_pullrate = FEHSummonFunctions.pullrate_dict[b_type.get()]
    i = 0
    while i <= 5:
        pull_rate[i].config(text = "{:.2f}".format(base_pullrate[i]) + "%")
        i += 1
    
def simulateButton():
    # We need to be able to check whether or not we have the correct sets of values.
    
    # Criteria 1: We must have a fivestar unit.
    fivestar_check = 0
    i = 0
    global fivestar_focus
    while i <= 3:
        if int(fivestar_focus[i].get()) >= 1:
            fivestar_check = 1
        i += 1
            
    # Criteria 2: If we have a 4* rate, then there must be a 4$ focus
    fourstar_check = 1
    global pull_rate
    global fourstar_focus
    if base_pullrate[2] > 0:
        fourstar_check = 0
        i = 0
        while i <= 3:
            if int(fourstar_focus[i].get()) >= 1:
                fourstar_check = 1
            i += 1
    
    # Criteria 3: The order priority must make sense
    priority_check = 1
    order = [-1, -1, -1, -1]
    global summon_priority
    i = 0
    while i <= 3:
        order[int(summon_priority[i].get())] = i
        i += 1;
    i = 0
    while i <= 3:
        if order[i] == -1:
            priority_check = 0
        i += 1
    
    global warning_label
    if fourstar_check == 0 or fivestar_check == 0 or priority_check == 0:
        warning_label.config(text = "Error had occured.")
    else:
        warning_label.config(text = "Everything is clear.")
    
    return

# This is the GUI that will house the prediction of number of copies of heroes.

banner_type_frame = LabelFrame(root, text="Banner Type:")
banner_type_frame.grid(row=0, column=1, padx = 20, pady=20, sticky=S)

base_pullrate_frame = LabelFrame(root, text="Base Banner Chances:")
base_pullrate_frame.grid(row=0, column=2, padx=20, pady=20, sticky=S)

fivestar_focus_frame = LabelFrame(root, text="5 Star Focus")
fivestar_focus_frame.grid(row=0, column=3, padx=20, pady=20, sticky=S)

fourstar_focus_frame = LabelFrame(root, text="4 Star Focus")
fourstar_focus_frame.grid(row=0, column=4, padx=20, pady=20, sticky=S)

summon_priority_frame = LabelFrame(root, text="Summon Priority")
summon_priority_frame.grid(row=0, column=5, padx=20, pady=20, sticky=S)

warning_label = Label(root, text="")
warning_label.grid(row=1, column=2, padx=10, pady=10, columnspan=3)

simulation_frame = LabelFrame(root, text="Simulation (max 100 000)")
simulation_frame.grid(row=2, column=2, padx=20, pady=20, columnspan=3)

b_type = IntVar()

i = 0
b_type_radio = []
while i <= 5:
    b_type_radio.append(Radiobutton(banner_type_frame, text=FEHSummonFunctions.bannertype_dict[i], variable=b_type, value=i, command=bTypeUpdate))
    b_type_radio[i].grid(row=i, column=0, sticky=W)
    i += 1



base_pullrate = FEHSummonFunctions.pullrate_dict[0]
i = 0
pull_type = []
pull_rate = []
while i <= 5:
    pull_type.append(Label(base_pullrate_frame, text=FEHSummonFunctions.rarity_dict[i], anchor=W, padx=10))
    pull_rate.append(Label(base_pullrate_frame, text="{:.2f}".format(base_pullrate[i]) + "%", anchor=E, padx=10))
    pull_type[i].grid(row=i, column=0, sticky=W)
    pull_rate[i].grid(row=i, column=1, sticky=E)
    i += 1
    
i = 0
fivestar_focus = []
fivestar_focus_spinbox=[]
while i <= 3:
    fivestar_focus.append(StringVar())
    fivestar_focus_spinbox.append(Spinbox(fivestar_focus_frame, from_=0, to=20, textvariable=fivestar_focus[i], width=5))
    fivestar_focus_spinbox[i].grid(row=i, column=0, padx=10, pady=10, sticky=E)
    i += 1;
    
i = 0
fourstar_focus = []
fourstar_focus_spinbox=[]
while i <= 3:
    fourstar_focus.append(StringVar())
    fourstar_focus_spinbox.append(Spinbox(fourstar_focus_frame, from_=0, to=20, textvariable=fourstar_focus[i], width=5))
    fourstar_focus_spinbox[i].grid(row=i, column=0, padx=10, pady=10, sticky=E)
    i += 1;

i = 0
summon_priority = []
summon_priority_label=[]
summon_priority_spinbox=[]
Label(summon_priority_frame, text="0 - Highest Priority", anchor = E).grid(row=0, column=0, columnspan=2)
while i <= 3:
    summon_priority.append(StringVar())
    summon_priority_spinbox.append(Spinbox(summon_priority_frame, from_=0, to=3, textvariable=summon_priority[i], width=5))
    summon_priority_label.append(Label(summon_priority_frame, text=FEHSummonFunctions.color_dict[i]))
    summon_priority_label[i].grid(row=i+1, column=0, padx=5, pady=5)
    summon_priority_spinbox[i].grid(row=i+1, column=1, padx=5, pady=5)
    i += 1;
    
simulation_count = StringVar()
simulation_label = Label(simulation_frame, text="Simulations")
simulation_label.grid(row=0, column=0,sticky=W, padx=5)
simulation_spinbox = Spinbox(simulation_frame, from_=1, to=100000, textvariable=simulation_count, width=10)
simulation_spinbox.grid(row=1, column=0, sticky=W, padx=5, pady=5)
simulation_button = Button(simulation_frame, text="Commence Sadness", command=simulateButton)
simulation_button.grid(row=0, column=1, rowspan=2, sticky=E, padx=5)




root.mainloop()