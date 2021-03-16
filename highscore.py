# DATABASE assignment 2 - Viktor Stranne & Alexander Röst - vs222my & ar223ni

import mysql.connector
from mysql.connector import errorcode
import random
import string
from random import randrange
import math
import tkinter as tk
from tkinter import *
from tkinter import ttk

gamemode = "normal"
try:
    cnx = mysql.connector.connect(user='root', password='root', host='127.0.0.1', database='videogame_highscore')

    # Used for debugging
    cnx.cursor().execute("DROP TABLE normal")
    cnx.cursor().execute("DROP TABLE hardcore")
    cnx.cursor().execute("DROP TABLE solo")
    cnx.cursor().execute("DROP VIEW equalz")



# Attempt to connect to the database, if there is an error it spits that back at us
except mysql.connector.Error as err:
    cnx = mysql.connector.connect(user='root', password='root', host='127.0.0.1')
    if err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
        print("Creating a database...")
        mycursor = cnx.cursor()
        mycursor.execute("CREATE DATABASE videogame_highscore")
    else:
        print(err)

DB_NAME = "videogame_highscore"

# the tables contains usernames, experience and the respective levels in the different "skills"
# normal accounts have no restrictions, hardcore lose their account upon death, solo's may not interact with others
TABLES = {}
TABLES['normal'] = (
    "CREATE TABLE `normal` ("
    "  `player_name` char(100) ,"
    "  `herbalism_xp` bigint(14) ,"
    "  `attack_xp` bigint(14) ,"
    "  `defence_xp` bigint(14) ,"
    "  `hunting_xp` bigint(14) ,"
    "  `magic_xp` bigint(14) ,"
    "  `archery_xp` bigint(14) ,"
    "  `total_xp` bigint(14) ,"
    "  `herbalism_lvl` bigint(14) ,"
    "  `attack_lvl` bigint(14) ,"
    "  `defence_lvl` bigint(14) ,"
    "  `hunting_lvl` bigint(14) ,"
    "  `magic_lvl` bigint(14) ,"
    "  `archery_lvl` bigint(14) ,"
    "  `total_lvl` bigint(14) ,"
    "  PRIMARY KEY (`player_name`)"
    ") ENGINE=InnoDB")
TABLES['hardcore'] = (
    "CREATE TABLE `hardcore` ("
    "  `player_name` char(100) ,"
    "  `herbalism_xp` bigint(14) ,"
    "  `attack_xp` bigint(14) ,"
    "  `defence_xp` bigint(14) ,"
    "  `hunting_xp` bigint(14) ,"
    "  `magic_xp` bigint(14) ,"
    "  `archery_xp` bigint(14) ,"
    "  `total_xp` bigint(14) ,"
    "  `herbalism_lvl` bigint(14) ,"
    "  `attack_lvl` bigint(14) ,"
    "  `defence_lvl` bigint(14) ,"
    "  `hunting_lvl` bigint(14) ,"
    "  `magic_lvl` bigint(14) ,"
    "  `archery_lvl` bigint(14) ,"
    "  `total_lvl` bigint(14) ,"
    "  PRIMARY KEY (`player_name`)"
    ") ENGINE=InnoDB")
TABLES['solo'] = (
    "CREATE TABLE `solo` ("
    "  `player_name` char(100) ,"
    "  `herbalism_xp` bigint(14) ,"
    "  `attack_xp` bigint(14) ,"
    "  `defence_xp` bigint(14) ,"
    "  `hunting_xp` bigint(14) ,"
    "  `magic_xp` bigint(14) ,"
    "  `archery_xp` bigint(14) ,"
    "  `total_xp` bigint(14) ,"
    "  `herbalism_lvl` bigint(14) ,"
    "  `attack_lvl` bigint(14) ,"
    "  `defence_lvl` bigint(14) ,"
    "  `hunting_lvl` bigint(14) ,"
    "  `magic_lvl` bigint(14) ,"
    "  `archery_lvl` bigint(14) ,"
    "  `total_lvl` bigint(14) ,"
    "  PRIMARY KEY (`player_name`)"
    ") ENGINE=InnoDB")

cnx = mysql.connector.connect(user='root', password='root', host='127.0.0.1', database='videogame_highscore')
# Cursor is a database handler, it helps us execute all commands
cursor = cnx.cursor(buffered=True)
cursor.execute("USE {}".format(DB_NAME))
# Use a for-loop to create the tables using the information in TABLES[]
for table_name in TABLES:
    table_description = TABLES[table_name]
    try:
        print("Creating table {}: ".format(table_name), end='')
        cursor.execute(table_description)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("Table already exists")
        else:
            print(err.msg)
    else:
        print("OK")

# Creating random usernames
# - for this database we can just simulate all data so usernames and their experience points will be randomly generated

# We need first names to use for our usernames, so we picked a few
usernames = {}
first_names = {"Alex", "Viktor", "Emil", "Elijah", "Jacob", "Oscar", "William", "DragonSlayer", "Daniel", "Logan",
               "Samuel", "David", "Isaac", "Asher", "lir"}
chars = string.ascii_letters + string.digits + '!@#%&*()'
# Run the loop 250 times to get 250 "unique names" an example of a name is bAlex2394
for unique in range(250):
    # Random char + random name + 4 random digits
    username_random = "".join(random.choice(chars) for i in range(1))
    username_extra = "".join(random.choice(string.digits) for i in range(4))
    first_name = "".join(random.sample(first_names, 1))
    final_name = username_random + first_name + username_extra
    usernames[unique] = final_name


# This is the equation we decided to use to calculate levels, 13,000,000 xp should equal out to be about 99
def xp_to_level(xp_to_calc):
    return math.ceil(math.log(xp_to_calc / 368599, 1.101141)) + 61


def get_xp():
    # Giving each player a random experience number in all the skills
    ex_points = randrange(100, 13000000)
    return ex_points

# Used to turn the xp into lvl and return the right number
def get_lvl(xp):
    return xp_to_level(xp)


# Inserting values into normal table
for i in range(250):
    values = []
    i1 = get_xp()
    i2 = get_xp()
    i3 = get_xp()
    i4 = get_xp()
    i5 = get_xp()
    i6 = get_xp()
    # For total xp we need to add all the existing xp values
    totalxp = i1 + i2 + i3 + i4 + i5 + i6
    l1 = get_lvl(i1)
    l2 = get_lvl(i2)
    l3 = get_lvl(i3)
    l4 = get_lvl(i4)
    l5 = get_lvl(i5)
    l6 = get_lvl(i6)
    # For total lvl we need to add all the existing lvl values
    totallvl = l1 + l2 + l3 + l4 + l5 + l6
    value = (usernames[i], i1, i2, i3, i4, i5, i6, totalxp, l1, l2, l3, l4, l5, l6, totallvl)
    values.append(value)
    # Normal query for just inserting a bunch of data into our tables
    query = "insert into `normal`(`player_name`,`herbalism_xp`,`attack_xp`,`defence_xp`,`hunting_xp`,`magic_xp`," \
            "`archery_xp`,`total_xp`,`herbalism_lvl`,`attack_lvl`,`defence_lvl`,`hunting_lvl`,`magic_lvl`," \
            "`archery_lvl`,`total_lvl`) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) "

    cursor.executemany(query, values)
    cnx.commit()


# Inserting values into hardcore table
for i in range(250):
    values = []
    i1 = get_xp()
    i2 = get_xp()
    i3 = get_xp()
    i4 = get_xp()
    i5 = get_xp()
    i6 = get_xp()
    totalxp = i1 + i2 + i3 + i4 + i5 + i6
    l1 = get_lvl(i1)
    l2 = get_lvl(i2)
    l3 = get_lvl(i3)
    l4 = get_lvl(i4)
    l5 = get_lvl(i5)
    l6 = get_lvl(i6)
    totallvl = l1 + l2 + l3 + l4 + l5 + l6
    value = (usernames[i], i1, i2, i3, i4, i5, i6, totalxp, l1, l2, l3, l4, l5, l6, totallvl)
    values.append(value)

    query = "insert into `hardcore`(`player_name`,`herbalism_xp`,`attack_xp`,`defence_xp`,`hunting_xp`,`magic_xp`," \
            "`archery_xp`,`total_xp`,`herbalism_lvl`,`attack_lvl`,`defence_lvl`,`hunting_lvl`,`magic_lvl`," \
            "`archery_lvl`,`total_lvl`) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) "

    cursor.executemany(query, values)
    cnx.commit()


# Inserting values into solo table
for i in range(250):
    values = []
    i1 = get_xp()
    i2 = get_xp()
    i3 = get_xp()
    i4 = get_xp()
    i5 = get_xp()
    i6 = get_xp()
    totalxp = i1 + i2 + i3 + i4 + i5 + i6
    l1 = get_lvl(i1)
    l2 = get_lvl(i2)
    l3 = get_lvl(i3)
    l4 = get_lvl(i4)
    l5 = get_lvl(i5)
    l6 = get_lvl(i6)
    totallvl = l1 + l2 + l3 + l4 + l5 + l6
    value = (usernames[i], i1, i2, i3, i4, i5, i6, totalxp, l1, l2, l3, l4, l5, l6, totallvl)
    values.append(value)

    query = "insert into `solo`(`player_name`,`herbalism_xp`,`attack_xp`,`defence_xp`,`hunting_xp`,`magic_xp`," \
            "`archery_xp`,`total_xp`,`herbalism_lvl`,`attack_lvl`,`defence_lvl`,`hunting_lvl`,`magic_lvl`," \
            "`archery_lvl`,`total_lvl`) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) "

    cursor.executemany(query, values)
    cnx.commit()

# Setting up the tkinter root
root = Tk()
# why is this sql here? i think we might need that later
sql = "SELECT player_name,total_lvl,total_xp FROM normal ORDER BY total_xp DESC"
cursor.execute(sql)
rows = cursor.fetchall()

global test
test = ""

# text box in root window
text = Text(root)

# adding of single line text box
edit = Entry(root)
# positioning of text box
"""
    Grid works like this
    column0   column1   column2
    row0       row0       row0
    row1       row1       row1   
    row2       row2       row2
"""
edit.grid(row=0, column=1, padx=4)

# Labels to display text, usually information next to buttons
label1 = Label(root, text="Filter by: ")
label1.grid(row=1, column=0)

label2 = Label(root, text="Filter by gamemode: ")
label2.grid(row=2, column=0)

label3 = Label(root, text="Join normal & hardcore attack lvl:")
label3.grid(row=3, column=0)

label4 = Label(root, text="Players with same total level:")
label4.grid(row=4, column=0)

label5 = Label(root, text=test)
label5.grid(row=1, column=2)
label5.config(font=("Courier", 20))

#Adding some nice style to our program, the red is a nice touch to an otherwise really ugly GUI
s = ttk.Style(root)
s.theme_use("clam")
s.configure("Treeview", background="#8a6d6b",
                fieldbackground="#8a6d6b", foreground="black")

# Dropdown menu for selecting specific xp filters
variableSkill = tk.StringVar(root)
variableSkill.set("Choose any")
w = OptionMenu(root, variableSkill, "Attack xp", "Defence Xp", "Herbalism xp", "Hunting xp", "Magic xp", "Archery xp",
               "Total Xp")
w.grid(row=1, column=1)

variableMode = StringVar(root)
variableMode.set("Normal")
w = OptionMenu(root, variableMode, "Normal", "Hardcore", "Solo")
w.grid(row=2, column=1)

# Creating our treeview ( the table that displays information )
tv = ttk.Treeview(root, columns=(1, 2, 3), show="headings", height="23")
tv.grid(row=8, column=2)
# Setting the heading titles for each column
tv.heading(1, text="Name")
tv.heading(2, text="Total level")
tv.heading(3, text="Total xp")
# Setting the spacing for the columns
ttk.Treeview.column(self=tv, column=1, width=490, anchor=tk.CENTER)
ttk.Treeview.column(self=tv, column=2, width=490, anchor=tk.CENTER)
ttk.Treeview.column(self=tv, column=3, width=490, anchor=tk.CENTER)

for i in rows:
    tv.insert('', 'end', values=i)

# Gets the text from the drop down and makes it right for the sql query
# Attack XP -> attack_xp so it matches our table attribute
def getSkill(string):
    print(string)
    newstring = string.lower().replace(" ", "_")
    return newstring

# This draws out the table for when we pick "Hardcore" in the drop down menu
def drawHardCore():
    sql = "SELECT player_name,total_lvl,total_xp FROM hardcore ORDER BY total_xp DESC"
    cursor.execute(sql)
    rows = cursor.fetchall()

    tv = ttk.Treeview(root, columns=(1, 2, 3), show="headings", height="23")
    tv.grid(row=8, column=2)

    tv.heading(1, text="Name")
    tv.heading(2, text="Total level")
    tv.heading(3, text="Total xp")

    ttk.Treeview.column(self=tv, column=1, width=490, anchor=tk.CENTER)
    ttk.Treeview.column(self=tv, column=2, width=490, anchor=tk.CENTER)
    ttk.Treeview.column(self=tv, column=3, width=490, anchor=tk.CENTER)

    for i in rows:
        tv.insert('', 'end', values=i)

# This draws out the table for when we pick "Normal" in the drop down menu
def drawNormal():
    sql = "SELECT player_name,total_lvl,total_xp FROM normal ORDER BY total_xp DESC"
    cursor.execute(sql)
    rows = cursor.fetchall()

    tv = ttk.Treeview(root, columns=(1, 2, 3), show="headings", height="23")
    tv.grid(row=8, column=2)

    tv.heading(1, text="Name")
    tv.heading(2, text="Total level")
    tv.heading(3, text="Total xp")

    ttk.Treeview.column(self=tv, column=1, width=490, anchor=tk.CENTER)
    ttk.Treeview.column(self=tv, column=2, width=490, anchor=tk.CENTER)
    ttk.Treeview.column(self=tv, column=3, width=490, anchor=tk.CENTER)

    for i in rows:
        tv.insert('', 'end', values=i)

# This draws out the table for when we pick "Solo" in the drop down menu
def drawSolo():
    sql = "SELECT player_name,total_lvl,total_xp FROM solo ORDER BY total_xp DESC"
    cursor.execute(sql)
    rows = cursor.fetchall()

    tv = ttk.Treeview(root, columns=(1, 2, 3), show="headings", height="23")
    tv.grid(row=8, column=2)

    tv.heading(1, text="Name")
    tv.heading(2, text="Total level")
    tv.heading(3, text="Total xp")

    ttk.Treeview.column(self=tv, column=1, width=490, anchor=tk.CENTER)
    ttk.Treeview.column(self=tv, column=2, width=490, anchor=tk.CENTER)
    ttk.Treeview.column(self=tv, column=3, width=490, anchor=tk.CENTER)

    for i in rows:
        tv.insert('', 'end', values=i)

# Used for searching for a specific player in the list, can also search for specific gamemodes
def findPlayer():
    global gamemode
    gamemodestring = getSkill(gamemode)
    # edit.get calls the information from the text input called edit
    username = edit.get()
    cursor = cnx.cursor(buffered=True)
    data = []
    data.append(username)
    # Find what gamemode we're supposed to look at and add the username to the existing query
    if gamemodestring == "normal":
        query = "SELECT * FROM normal WHERE player_name=%s "
    elif gamemodestring == "hardcore":
        query = "SELECT * FROM hardcore WHERE player_name=%s "
    elif gamemodestring == "solo":
        query = "SELECT * FROM solo WHERE player_name=%s "

    cursor.executemany(query, (data,))
    rows = cursor.fetchall()
    # Make sure we find something, otherwise skip printing a blank treeview
    # cursor.rowcount == 0 means it has nothing
    if cursor.rowcount != 0:
        tv = ttk.Treeview(root, columns=(1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15), show="headings",
                          height="23")
        tv.grid(row=8, column=2)
        tv.heading(1, text="Name")
        tv.heading(2, text="Herbalism xp")
        tv.heading(3, text="Attack xp")
        tv.heading(4, text="Defence xp")
        tv.heading(5, text="Hunting xp")
        tv.heading(6, text="Magic xp")
        tv.heading(7, text="Archery xp")
        tv.heading(8, text="Total xp")
        tv.heading(9, text="Herbalism lvl")
        tv.heading(10, text="Attack lvl")
        tv.heading(11, text="Defence lvl")
        tv.heading(12, text="Hunting lvl")
        tv.heading(13, text="Magic lvl")
        tv.heading(14, text="Archery lvl")
        tv.heading(15, text="Total lvl")
        #TODO: Clean this up? maybe use a variable for column id or something, idk not sure if we can clean this up
        ttk.Treeview.column(self=tv, column=1, width=98, anchor=tk.CENTER)
        ttk.Treeview.column(self=tv, column=2, width=98, anchor=tk.CENTER)
        ttk.Treeview.column(self=tv, column=3, width=98, anchor=tk.CENTER)
        ttk.Treeview.column(self=tv, column=4, width=98, anchor=tk.CENTER)
        ttk.Treeview.column(self=tv, column=5, width=98, anchor=tk.CENTER)
        ttk.Treeview.column(self=tv, column=6, width=98, anchor=tk.CENTER)
        ttk.Treeview.column(self=tv, column=7, width=98, anchor=tk.CENTER)
        ttk.Treeview.column(self=tv, column=8, width=98, anchor=tk.CENTER)
        ttk.Treeview.column(self=tv, column=9, width=98, anchor=tk.CENTER)
        ttk.Treeview.column(self=tv, column=10, width=98, anchor=tk.CENTER)
        ttk.Treeview.column(self=tv, column=11, width=98, anchor=tk.CENTER)
        ttk.Treeview.column(self=tv, column=12, width=98, anchor=tk.CENTER)
        ttk.Treeview.column(self=tv, column=13, width=98, anchor=tk.CENTER)
        ttk.Treeview.column(self=tv, column=14, width=98, anchor=tk.CENTER)
        ttk.Treeview.column(self=tv, column=15, width=98, anchor=tk.CENTER)
        for i in rows:
            tv.insert('', 'end', values=i)

# TODO: ADD COMMENTS HERE
def getIndex(string):
    if string=="herbalism_xp":
        return 1
    elif string=="attack_xp":
        return 2
    elif string=="defence_xp":
        return 3
    elif string == "hunting_xp":
        return 4
    elif string == "magic_xp":
        return 5
    elif string == "archery_xp":
        return 6
    elif string == "total_xp":
        return 7

def skillFilter(*args):
    global gamemode
    skill_string = getSkill(variableSkill.get())
    gamemodestring = getSkill(gamemode)
    cursor = cnx.cursor(buffered=True)
    print("This is my skillstring forever hihiih xd:" + skill_string)
    if skill_string == "choose_any":
        return
    else:
        if gamemodestring == "normal":
            cursor = cnx.cursor(buffered=True)
            cursor.execute("SELECT * FROM normal ")

        elif gamemodestring == "hardcore":
            cursor = cnx.cursor(buffered=True)
            cursor.execute("SELECT * FROM hardcore ")

        elif gamemodestring == "solo":
            cursor = cnx.cursor(buffered=True)
            cursor.execute("SELECT * FROM solo ")
        rows = cursor.fetchall()

        tv = ttk.Treeview(root, columns=(1, 2, 3), show="headings", height="23")
        tv.grid(row=8, column=2)

        tv.heading(1, text="Name")
        tv.heading(2, text=skill_string.replace("_", " "))
        skilllvl_string=skill_string.replace("xp", "lvl")
        tv.heading(3, text=skilllvl_string.replace("_", " "))

        ttk.Treeview.column(self=tv, column=1, width=490, anchor=tk.CENTER)
        ttk.Treeview.column(self=tv, column=2, width=490, anchor=tk.CENTER)
        ttk.Treeview.column(self=tv, column=3, width=490, anchor=tk.CENTER)

        index = getIndex(skill_string)
        for i in rows:
            values = []
            values.append(i[0])
            values.append(i[index])
            values.append(i[index+7])
            tv.insert('', 'end', values=values)

# This tells us what is selected in a dropdown menu, used for printing the right table
def selectedDropDown(*args):
    global gamemode
    # check whats selected in the dropdown
    if variableMode.get() == "Normal":
        gamemode = "normal"
        print("normal")
        tv.delete(*tv.get_children())
        drawNormal()
    elif variableMode.get() == "Hardcore":
        gamemode = "hardcore"
        print("hardcore")
        tv.delete(*tv.get_children())
        drawHardCore()
    elif variableMode.get() == "Solo":
        gamemode = "solo"
        print("solo")
        tv.delete(*tv.get_children())
        drawSolo()

# This bool is used to see if the view already exists in the current loop
# This is so that we don't try to create it twice in the same run of the program
# Since we only drop the tables in the beginning for debugging purposes
global viewExist
viewExist = False

# Find player names that have stats in different gamemodes that happen to be the same level
def equalGRÏND():
    global viewExist
    cursor = cnx.cursor(buffered=True)
    if viewExist == False:
        # Here we create and use a view, so that this could be reused later for other purposes
        cursor.execute("CREATE VIEW equalz AS " \
                       "SELECT normal.player_name  FROM normal, hardcore " \
                       "WHERE (normal.herbalism_lvl = hardcore.herbalism_lvl AND normal.player_name=hardcore.player_name) " \
                       "OR (normal.attack_lvl = hardcore.attack_lvl AND normal.player_name=hardcore.player_name) " \
                       "OR (normal.defence_lvl = hardcore.defence_lvl AND normal.player_name=hardcore.player_name) " \
                       "OR (normal.hunting_lvl = hardcore.hunting_lvl AND normal.player_name=hardcore.player_name) " \
                       "OR (normal.magic_lvl = hardcore.magic_lvl AND normal.player_name=hardcore.player_name) " \
                       "OR (normal.archery_lvl = hardcore.archery_lvl AND normal.player_name=hardcore.player_name) ")
        # If the view is already done we run it, otherwise it should have been made by now
        viewExist = True
    # Use the view we made before
    cursor.execute("SELECT * FROM equalz")
    rows = cursor.fetchall()
    tv = ttk.Treeview(root, columns=(1), show="headings", height=23)
    tv.grid(row=8, column=2)
    tv.heading(1, text="Name")
    ttk.Treeview.column(self=tv, column=1, width=1470, anchor=tk.CENTER)
    for i in rows:
        tv.insert('', 'end', values=i)

# Used for joining together data from different tables.
def proveJoining():
    # WE CAN JOIN STUFF, LOOK HERE
    cursor.execute(
        "SELECT normal.player_name, normal.attack_lvl, hardcore.attack_lvl, solo.attack_lvl FROM normal JOIN hardcore "
        "ON normal.player_name = hardcore.player_name JOIN solo ON normal.player_name = solo.player_name")
    rows = cursor.fetchall()
    tv = ttk.Treeview(root, columns=(1, 2, 3, 4), show="headings", height=23)
    tv.grid(row=8, column=2)
    tv.heading(1, text="Normal player")
    tv.heading(2, text="Normal attack lvl")
    tv.heading(3, text="Hardcore attack lvl")
    tv.heading(4, text="Solo attack lvl")

    ttk.Treeview.column(self=tv, column=1, width=365, anchor=tk.CENTER)
    ttk.Treeview.column(self=tv, column=2, width=365, anchor=tk.CENTER)
    ttk.Treeview.column(self=tv, column=3, width=365, anchor=tk.CENTER)
    ttk.Treeview.column(self=tv, column=4, width=365, anchor=tk.CENTER)
    for i in rows:
        tv.insert('', 'end', values=i)

# Groups users together that happen to have the same total level as another user
# Here we only check for the normal table
# TODO: add other tables as well
def proveGrouping():
    # GROUP THING TOGETHER
    cursor.execute("SELECT player_name FROM normal GROUP BY total_lvl")
    rows = cursor.fetchall()
    tv = ttk.Treeview(root, columns=1, show="headings", height=23)
    tv.grid(row=8, column=2)
    tv.heading(1, text="Total lvls")
    ttk.Treeview.column(self=tv, column=1, width=1470, anchor=tk.CENTER)
    for i in rows:
        tv.insert('', 'end', values=i)

# This method is used for finding the average level across all normal players
# TODO: Make these three perhaps into one method? Or atleast atempt cleanup if time allows it
def avgLVLNORMAL():
    global test
    # Find the average total level of all the game modes
    # Use aggregation function AVG for this
    cursor.execute("SELECT AVG(total_lvl) AS average FROM normal")
    rows = cursor.fetchall()

    avgstring = "Average total level for normal:", rows
    test = avgstring
    label5.config(text=test)
    label5.update()

# This method is used for finding the average level across all hardcore players
def avgLVLHARDCORE():
    global test
    # Find the average total level of all the game modes
    cursor.execute("SELECT AVG(total_lvl) AS average FROM hardcore")
    rows = cursor.fetchall()

    avgstring = "Average total level for hardcore:", rows
    test = avgstring
    label5.config(text=test)

# This method is used for finding the average level across all solo players
def avgLVLSOLO():
    global test
    # Find the average total level of all the game modes
    cursor.execute("SELECT AVG(total_lvl) AS average FROM solo")
    rows = cursor.fetchall()

    avgstring = "Average total level for solo:", rows
    test = avgstring
    label5.config(text=test)


# Down here is where we have all of our buttons
# TODO: Make a method for autogenerating buttons? could be neat, not sure how to
butt = Button(root, text='Search for player', command=findPlayer)
butt.grid(row=0, column=0)

butt2 = Button(root, text='COMPARE', command=proveJoining)
butt2.grid(row=3, column=1)

butt3 = Button(root, text='GROUP', command=proveGrouping)
butt3.grid(row=4, column=1)

butt4 = Button(root, text='AVERAGE NORMAL \n TOTAL LVL', command=avgLVLNORMAL)
butt4.grid(row=5, column=0)

butt5 = Button(root, text='AVERAGE HARDCORE \n TOTAL LVL', command=avgLVLHARDCORE)
butt5.grid(row=6, column=0)

butt6 = Button(root, text='AVERAGE SOLO \n TOTAL LVL', command=avgLVLSOLO)
butt6.grid(row=7, column=0)

butt7 = Button(root, text='Equal Grind \n (Normal vs. HC)', command=equalGRÏND)
butt7.grid(row=7, column=1)

# These two lines look for changes in the dropdown menu and then activates the right method to handle the change
variableMode.trace("w", selectedDropDown)
variableSkill.trace("w", skillFilter)

# Add title to the program, size and allow the program to be resized to people preferences
root.title("Highscores")
root.geometry("1800x800")
root.resizable(True, True)
# Start the main GUI loop
root.mainloop()
