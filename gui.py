# Handles the GUI window
from tkinter import *
import tkinter.ttk as tk
import sim_window
import ast
import pymunk

# tk initialisation
win = Tk()
win.maxsize(height=700)
win.title("Pyvlov's Dog - Settings")
win.iconbitmap('favicon.ico')
win.resizable(0, 0)
nb = tk.Notebook(win)
nb.pack(fill=BOTH, expand=1)

rules = []
objects = []
simulator_settings = []

# frame initialisation
ru_fr = Frame(win, width=400, height=600)
ob_fr = Frame(win, width=400, height=600)
si_fr = Frame(win, width=400, height=600)
nb.add(ru_fr, text="Rules")
nb.add(ob_fr, text="Objects")
nb.add(si_fr, text="Simulator Settings")

# feedback buttons
bu_fr = Frame(win, width=400, height=50)
bu_fr.pack_propagate(0)
pos_button = Button(bu_fr, text="Reward", bg="green", fg="white", width=27, height=3)
neg_button = Button(bu_fr, text="Punish", bg="red", fg="white", width=27, height=3)

bu_fr.pack()
pos_button.pack(side=LEFT)
neg_button.pack(side=LEFT)

########## rules frame ##########

rules = []


def rules_check():
    rew = False
    pun = False
    for rule in rules:
        r = rule.check("")
        if r == 1:
            rew = True
        elif r == -1:
            pun = True
    return (rew, pun)


class Rule:
    def __init__(self):
        self.frame = Frame(rule_window, width=383)
        self.entry = Entry(self.frame, width=62)

    def __repr__(self):
        return self.entry.get()

    def check(self, inputs):
        try:
            comps = self.entry.get().split(";")
            rule = comps[0]
            component = rule.split(" == ")[0]
            value = rule.split(" == ")[1]

            #TODO make dynamic
            if component == "L Bump":
                if inputs[4] == int(value):
                    print("howdidlydoneighbour")
                    if comps[1] == "punish":
                        return -1
                    elif comps[1] == "reward":
                        return 1

            if component == "R Bump":
                if inputs[5] == int(value):
                    if comps[1] == "punish":
                        return -1
                    elif comps[1] == "reward":
                        return 1

            if component == "LDR":
                if inputs[3] == int(value):
                    if comps[1] == "punish":
                        return -1
                    elif comps[1] == "reward":
                        return 1


        except:
            pass


def ruleadd():
    rules.append(Rule())
    rule_window.create_window(0, (len(rules) - 1) * 23, window=rules[-1].frame, anchor=NW)
    rules[-1].entry.pack(fill=X, padx=4, pady=2)
    rule_window.configure(scrollregion=(0, 0, 383, 23 * len(rules)))


def rulerem():
    rules[-1].entry.forget()
    del (rules[-1])
    rule_window.configure(scrollregion=(0, 0, 383, 23 * len(rules)))


top_menu = Frame(ru_fr, width=400, height=30)
rule_window = Canvas(ru_fr, width=383, height=570)
rule_window.pack_propagate(0)
create_button = Button(top_menu, text="New Rule", command=ruleadd)
remove_button = Button(top_menu, text="Delete Rule", command=rulerem)
scroll = Scrollbar(ru_fr)

top_menu.pack(fill=X)
create_button.pack(side=LEFT, padx=3)
remove_button.pack(side=LEFT, padx=3)
rule_window.pack(side=LEFT, fill=BOTH)
scroll.pack(side=RIGHT, fill=Y)
rule_window.configure(yscrollcommand=scroll.set)
scroll.config(command=rule_window.yview)

########## objects frame ##########

object_types = []


class Obj:
    def __init__(self):
        self.frame = Frame(object_window)
        self.t_fr = Frame(self.frame)
        self.b_fr = Frame(self.frame)
        self.buttons = [Button(self.t_fr, text="Add", command=self.paint_brush),
                        Button(self.t_fr, text="Clear", command=self.clear_obj)]
        self.name = Entry(self.t_fr, width=12)
        self.colour = Entry(self.t_fr)
        self.var = IntVar()
        self.collide = Checkbutton(self.t_fr, text="Collide", variable=self.var)
        self.collide.var = self.var
        self.size = Scale(self.b_fr, orient=HORIZONTAL, label="Size")
        self.alpha = Scale(self.b_fr, orient=HORIZONTAL, to=255, label="Alpha")
        self.alpha.set(255)
        self.input_link = Entry(self.b_fr)



    def paint_brush(self):
        sim_window.paint_brush = object_types.index(self)

    def clear_obj(self):
        sim_window.obj_list[object_types.index(self)].copies = []


def objectadd():
    object_types.append(Obj())
    object_window.create_window(2, (len(object_types) - 1) * 95, width=379, height=93, window=object_types[-1].frame,
                                anchor=NW)
    object_types[-1].t_fr.pack(fill=X)
    object_types[-1].b_fr.pack(fill=X)
    object_types[-1].name.pack(side=LEFT, padx=2, pady=2)
    object_types[-1].colour.pack(side=LEFT, padx=2, pady=2)
    object_types[-1].buttons[0].pack(side=LEFT, padx=2, pady=2)
    object_types[-1].buttons[1].pack(side=LEFT, padx=2, pady=2)
    object_types[-1].collide.pack(side=LEFT, padx=2, pady=2)
    object_types[-1].size.pack(side=LEFT, pady=2)
    object_types[-1].alpha.pack(side=LEFT, pady=2)
    object_types[-1].input_link.pack(side=LEFT, pady=2, padx=15)
    sim_window.obj_list.append(sim_window.Object("", "", 0, 0, 100))
    object_window.configure(scrollregion=(0, 0, 383, 500 if len(object_types) < 6 else len(object_types) * 100))


def objectrem():
    object_window.delete(ALL)
    del (sim_window.obj_list[-1])
    del (object_types[-1])
    for obj in object_types:
        object_window.create_window(2, (object_types.index(obj)) * 95, width=379, height=93,
                                    window=obj.frame,
                                    anchor=NW)
        obj.t_fr.pack(fill=X)
        obj.b_fr.pack(fill=X)
        obj.name.pack(side=LEFT, padx=2, pady=2)
        obj.colour.pack(side=LEFT, padx=2, pady=2)
        obj.buttons[0].pack(side=LEFT, padx=2, pady=2)
        obj.buttons[1].pack(side=LEFT, padx=2, pady=2)
        obj.collide.pack(side=LEFT, padx=2, pady=2)
        obj.size.pack(side=LEFT, pady=2)
        obj.alpha.pack(side=LEFT, pady=2)
        obj.input_link.pack(side=LEFT, pady=2, padx=15)
    sim_window.paint_brush = None
    object_window.configure(scrollregion=(0, 0, 383, 500 if len(object_types) < 6 else len(object_types) * 100))


top_omenu = Frame(ob_fr, width=400, height=30)
object_window = Canvas(ob_fr, width=383, height=570, bg="#999999", scrollregion=(0, 0, 383, 1000))
object_window.pack_propagate(0)
createo_button = Button(top_omenu, text="New Object", command=objectadd)
removeo_button = Button(top_omenu, text="Delete Object", command=objectrem)
scrollo = Scrollbar(ob_fr)
top_omenu.pack(fill=X)
createo_button.pack(side=LEFT, padx=3)
removeo_button.pack(side=LEFT, padx=3)
object_window.pack(side=LEFT)
scrollo.config(command=object_window.yview)
scrollo.pack(side=RIGHT, fill=Y)
object_window.configure(yscrollcommand=scrollo.set)
object_window.configure(yscrollincrement="2")

########## simulator frame ##########
loc_update = 0


def update_loc():
    global t_location
    t_location = location.get()


toggle_frame = Frame(si_fr)
sim_on = Button(toggle_frame, text="Start Simulation", command=sim_window.simon)
sim_off = Button(toggle_frame, text="Stop Simulation", command=sim_window.simoff)
sim_speed = Scale(si_fr, orient=HORIZONTAL, label="Simulation Speed", from_=0, to=0.15, resolution=0.001)
auto_on = Checkbutton(si_fr, text="Automatic Training")
var = IntVar()

dog_lo_frame = Frame(si_fr)
dog_loc_label = Label(dog_lo_frame, text="Save Location")
location = StringVar(win, value="saves\\Default")
dog_location = Entry(dog_lo_frame, width=40, textvariable=location)
t_location = "saves\\Default"
dog_update = Button(dog_lo_frame, text="Generate", command=update_loc)

toggle_frame.pack(pady=2)
sim_on.pack(side=LEFT, pady=2)
sim_off.pack(side=LEFT, pady=2)
sim_speed.pack(pady=2)
auto_on.pack()
dog_lo_frame.pack()
dog_loc_label.pack(side=LEFT)
dog_location.pack(side=LEFT)
dog_update.pack(side=LEFT, padx=3)


def update_gui():
    for rule in rules:
        rule.check(sim_window.var)
    loc_update = 0
    win.update_idletasks()
    win.update()
