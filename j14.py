"""
Written by Gerry Benoit, May 27, 2022|June 2,  - took a month to do this to learn TKinter.
©2022 Benoit - you're welcome to use it - provided (a) any improvements are shared
with me; (b) any sales, before or after your own improvements, must shared with me;
(c) maintain my work by including my name and contact info.  Thanks.
"""

import sys
import os
import os.path
from os import system, name
import pathlib
import random
import pydoc

import math
from datetime import datetime
from functools import partial
import configparser
from tkinter import *
from tkvideo import tkvideo
import tkinter as tk
from tkinter import filedialog
from tkinter import font as tkFont
from tkinter import messagebox
from tkinter import scrolledtext
from tkinter import simpledialog
from tkinter import ttk
from tkinter.messagebox import askokcancel, showinfo, WARNING
import mysql.connector
from mysql.connector import Error
from mysql.connector import errorcode
from PIL import Image, ImageTk
import tkinter.messagebox as tkmb
import webbrowser
from pymediainfo import MediaInfo

from createEAD import createEAD  # THE EAD EXTENSION

HOSTVAR = 0
USERVAR = 1
DBPASSWORDVAR = 2 # added here so all #s changed after
DBVAR = 3  # DB TO USE 
DBTABLEVAR = 4   # DB TABLE FIELD NAMES
FLATFILEVAR = 5  # SAVE FLAT FILE FOR INDEX
CBVAR = 6 # CHECKBOXES ON SCREEN

# save to options
SAVETODB = 0
SAVETOFILE = 1
SETCARRYON = 2
DUPLICATE = 3

# search and output options
ANDSEARCH = 0 # 1?
ORSEARCH = 1
RDBMSSEARCH = 2
FLATFILESEARCH = 3
OUTPUTASHTML = 4
OUTPUTASJSON = 5
OUTPUTASVRA = 6
OUTPUTASEAD = 7

#IMPORTANT VAR!
# = []
configuration_setup = False
finalList = []
fullPathImageFileName = []

variables = [] # the list of checkboxes to use for booleans for saving data.
# in the plural, I'm using it a a collection of vars ... in the frucking Checkbox 
# command, the required term is "variable" and then set the var name, there just "var"
runningNumberOfCheckboxesForDB = 0
count = 0
currentImageNo = 0 
cut_off = 6
font_size_to_use = 11
photoImageList = []
imageList = ["card_catalog.png"] # "japanese_scene.png"]
lenFileList = 0
imageChosen = 0
filelister = []
long_text = ""
tagFileToProcess = ""
zutingFileToProcess = ""
listOfCBList_x_Options = []
CBList_x_Options = []
CBListTotal = 0
#tempoOptions
userTagsOptions = []
userTagsNames = []
userTagGroupHeadings = []
userTagsOptionsList = []
dbTableFieldNamesToProcess = ""

# hate to use globals ... 
user = ""
host = ""
database = ""
password = ""
dbTableNameToUse = ""
indexFileName = ""

imageName = ""

listOfTagFiles = []
user_notes = ""
my_val = [] 

zuting_vars = []
chk_list = []
pane_width = 0
pane_height = 0
searchOptionsChoices = ""

def extract_data():
	"""
	function: extract_data
	:param name: The name of foo
	:return: returns user_notes
	"""
	user_notes = text_widget.get('1.0','end-1c')
	return user_notes

# ------------- TEST OF NEW CHECKBAR ------------------ #
class Checkbar(LabelFrame):
	def __init__(self, parent=None, picks=[], side=LEFT, anchor=N+W):
		global clear
		global chk_list
		global count
		global runningNumberOfCheckboxesForDB
		global cut_off
		global font_size_to_use
		#print("class Checkbar\n\tparam:LabelFrame - cut_off and fontsize= ", cut_off, " font: ", font_size_to_use)
		"""
		class Checkbar - calls LabelFrame 
		"""
		#print("class Checkbar()")
		
		#default_CBs = ["Save to RDBMS", "OR tags", "Search RDBMS", "Output as HTML"]
		default_CBs = ["Save to Flat File", "OR tags", "HTML"]
		control_panels = ["Save to", "Search and Output Options"]
		titleFont =  tkFont.Font(family = "SF Pro Rounded Bold", size = 11)
		cbFont = tkFont.Font(family = "PT Sans Regular", size = font_size_to_use) # 10)
		
		add_to_var_list = False

		# ---- test area 
		boxTitle = picks[0]
		# if in the control_panel then use first word for label,
		# all the other terms for display. Remove only first item from list.
		if boxTitle in control_panels:
			add_to_var_list = False
			picks = picks[1:]
			#print("\tcontrolpanel item: boxTitle", boxTitle, " and list: ", picks)
		else:
			#the list is not in the control panel group so show 
			# all the items, except the first (the boxTitle)
			# and the last 'cause it seems to be [] empty.
			add_to_var_list = True
			picks = picks[1:-1]
			#print("\tNOT control panel item: boxTitle", boxTitle, " and list: ", picks)
			
		#print("______________________ TEST: _____________________")

		LabelFrame.__init__(self, parent)
		self.config(text = boxTitle, font = titleFont)
		self.vars = []

		# test area
		pick_count = len(picks) 
		userTagGroupHeadings.append(picks[0]) # the first item is the group title.
		
		grid_column = 0
		row_start = 0
		grid_row = 0
		
		
		###############################
		#cut_off = 6 # usually 6 [testing to set in config panel]
		####################################
		counter = 0
		
		for pick in picks:
			userTagsNames.append(pick)
			var = IntVar()
			chk = Checkbutton(self, text = pick, variable=var, onvalue=1, offvalue=0)
			chk.config(font=cbFont)
			chk.columnconfigure(grid_column, weight = 1)
			chk.rowconfigure(grid_row, weight=1)
			chk.grid(column = grid_column, row = grid_row, sticky="NW")
			#chk.pack(side=side, anchor=anchor, expand=YES)
			self.vars.append(var)
			
			# SELECT / CHECK the default checkboxes
			if pick in default_CBs:
				chk.select()
				
			if add_to_var_list:
				chk_list.append(chk)
				variables.append(var)
				runningNumberOfCheckboxesForDB += 1
				
			# increment counters
			pick_count += 1
			grid_column += 1
			
			# if the # of CBs (pick_count) is > than present limit (cut_off)
			if grid_column > cut_off:
				grid_row += 1
				grid_column = 0
				#pick_number += 1
		#print("Running # of boxes to note: ", runningNumberOfCheckboxesForDB)
		#print("Length of variables = ", len(variables))
		#print("userTagsOptions = ", userTagsOptions)
		
					
	def state(self):
		#print("\tfunction state:\n\tparam: self")
		#print("\treturns: map((lambda var: var.get()), self.vars)")
		"""
		function: state
		:param name: self
		:return: map((lambda var: var.get()), self.vars)
		"""
		return map((lambda var: var.get()), self.vars)
		
# ------END ------- TEST OF NEW CHECKBAR ------------------ #		

def my_upd():
	global vars
	"""
	function: my_upd()
	:global:  vars
	:param name: self
	:return: map((lambda var: var.get()), self.vars)
	"""
	if var.get() == 1:
		var.deselect()
		
def clearallstates():
	#print("function: clearallstates\n\treturns: vars")
	"""
	function: clearallstates()
	:global:  vars
	:param name: 
	:return: prints list of vars
	"""
	global vars
	#print("220 - vars = ", vars)
	
def allstates():
	global userTagsOptions
	global userTagsNames
	global userTagGroupHeadings
	#print("function: allstates()"+\
	#"\t:global:  userTagsOptions, userTagsNames, userTagGroupHeadings"+\
	#"\t::param name: self"+\
	#"\t:return: map((lambda var: var.get()), self.vars")

	list(saveOptions.state())[0] = 1
	
	testl = []
	for i in range(0, len(userTagsOptions)):
		testl += userTagsNames[i]
	
	#print("test of all CBs from allstates() : ", testl, "\n\n")
	#print("testing from that function ... ")
	#print("testoOptions = ", list(testoOptions.state()))

# ___________________________________________________
def click_meX():
	global my_val
	global userTagsOptions
	global userTagsNames
	global chk_list
	global variables
	#print("function: click_meX\n\tglobals: my_val, userTagsOptions,userTagsNames")
	#print("\tchk_list, variables")
	for j in range(0, len(variables)):
		chk_list[j].deselect()

# ******************************************************
# START START
# *****************************************************
win = Tk()					  # CREATE WINDOW

win.title("PIM Tailorable Cataloguer Program, v. 1")
win.resizable(True, True)
win.minsize(1180, 800)

# NEW VERSION
screen_width = win.winfo_screenwidth()
screen_height = win.winfo_screenheight()

window_width = screen_width - 90
window_height = screen_height - 90

# find the center point
center_x = int(screen_width/2 - window_width / 2)
center_y = int(screen_height/2 - window_height / 2)
pane_width = int(window_width/2)
pane_height = int(window_height-90)
# set the position of the window to the center of the screen

win.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

# ------------ end of the root window -------------------------- #

# CHECK BOXES
setCarryOn = BooleanVar()
#setCarryOn.set(True)

makeWebPageOk = BooleanVar()
makeJsonFileOk = BooleanVar()
andSearchTermsOk = BooleanVar()
orSearchTermsOk = BooleanVar()
orSearchTermsOk.set(True)
saveToRDBMSOk = BooleanVar()
saveToRDBMSOk.set(True)

setCarryOn.set(False)
searchUsingRDBMSOk = BooleanVar()
searchUsingTextFileOk = BooleanVar()
saveToFileOptionOk = BooleanVar()
searchUsingTextFileOk = BooleanVar()
# TEST AREA - does nothing but checks CB behaviors.
chkVar = BooleanVar()
chkVar.set(True)

# add the JumpTo #s... that's where imageChosen comes from 
# see  cataloguer-2b-TEST.py

def skipOption(skipValue = False):
	skip = skipValue
	#print("SKIP THIS IMAGE! value of skip is ", skip)
	return skip

def updtcblist():
	#print("function: updtcblist()")
	imageNumberList = []
	for j in range(0, len(imageList)):
		imageNumberList.append(j)
	imageChosen['values'] = imageNumberList
	imageChosen['state'] = 'readonly'
	imageChosen.bind('<<ComboboxSelected>>',getimage_changed)

def getimage_changed(event):
	global currentImageNo

	#print("function: getimage_changed\n\tparams:event\n\tglobal: currentImageNo")
	x = int(imageChosen.get())
	currentImageNo = x
	#print("140 - inside getimage_changed() - the jump to ... ", currentImageNo)
	update_image("jump")


# ******************************************************************************** TAG-PREP RELATED
def list_of_tag_files():
	global filelister
	#("function: list_of_tag_files()")
	#print("***** 174\tlist of tag files: ", filelister)
	#filelister = ['tag1.txt', 'tag2.txt', 'tag3.txt', 'tag4.txt' ]
	#print("\t",filelister, " ", type(filelister))
	return filelister
	
def total_no_of_files():
	#print("function: total_no_of_files")
	i = len(filelister)
	return i


def createListOfTags(fileToUse):
	#print("function: createListOfTags")
	f = open(fileToUse, "r")
	content = f.read()
	content_list = content.split("\n")
	#print("42:\t content_list = ",content_list)
	return content_list
	
# * * * * * * * * * * * * * * * * END OF setupTEST2 * * * *	
def setupTEST():
	global finalList	
	global cut_off
	global font_size_to_use
	#print("function setupTEST()\n\tparams: none")
	DEMO = 1
	TOBY = 2
	NANCY = 3
	STASSI = 4
	VANESSA = 5
	
	HOSTNAME = 0
	DBNAME = 1
	DBUSERNAME = 2
	DBPASSWORDNAME = 3
	DBTABLENAME = 4
	INDEXFILENAME = 5
	CHECKBOXFILENAME = 6

	host_var = StringVar()
	db_var = StringVar()
	db_username_var = StringVar()
	db_password_var = StringVar()
	db_table_name_var = StringVar()
	index_filename_name_var = StringVar()
	checkbox_filename_var = StringVar()
	cut_off_var = StringVar() # should be int but the others aren't so ... 
	font_size_to_use_var = StringVar()
	
	# start cut
	ws = Toplevel(win)
	ws.title('Configuration Window')
	ws.geometry("600x500")

	# _______________________________________________________
	# Add a grid
	mainframe = Frame(ws)
	mainframe.grid(column=0,row=0, sticky=(N,W)) #,E,S) )
	mainframe.columnconfigure(0, weight = 2)
	mainframe.rowconfigure(0, weight = 2)
	mainframe.pack(pady = 50, padx = 50)
	
	# Create a canvas widget. used to work, wtf?
	canvas= Canvas(ws,  width=400, height=300) # 400, 300
	canvas.pack()
	imgtester=ImageTk.PhotoImage(Image.open("japanese_scene.png"))
	canvas.create_image((220,530), image=imgtester) # anchor=CENTER, 220,130
	# ___________________________________________________________
	
	"""
	canvas = Canvas(mainframe, width=380, height=280)
	canvas.pack()
	imgName = os.path.realpath("mattsmirk.jpg")
	img = ImageTk.PhotoImage(Image.open("mattsmirk.jpg")) # "/Users/gb/Documents/j6/demo_images/ahawaii.jpg"))
	#canvas.pack() ORIGINAL KEEP
	# ORIGINAL canvas.create_image(220, 130, image=img, anchor='nw')
	canvas.create_image(220, 130, image=img, anchor=NW )
	"""
	
	# ______________ START OF PRESET DEFAULTS (from drop4.py) _______________

	
	user_defaults = ["Select preset...","demo", "Toby","Nancy", "Stassi", "Vanessa", "The Arts"]
	# individual options.
	host_name = ["localhost", "127.0.0.1"]
	db_name = ["pim", "nancy", "toby", "stassi", "vanessa"]
	db_username_name = ["root", "toby", "nancy", "stassi", "vanessa"]
	db_password_name = ["Antibes1066", "toby", "nancy_pw", "tree", "vanessa_pw"]
	db_table_name = ["demo_db_table", "nancy_table", "toby_table", "stassi_table","vanessa_table"]
	index_filename_name = ["demo_index_1.txt", "nancy_index_1.txt", "toby_index_1.txt","stassi_index_1.txt","vanessa_index_1.txt"]
	checkbox_filename = ["demo_cb_1.txt", "nancy_cb_1.txt", " toby_cb_1.txt","mainemaritime_cb.txt","vanessa_cb_1.txt", "arts_cb_1.txt"]
	cut_off_menu = ["4", "5", "6", "7"] # for cut_off_var
	font_size_to_use_menu = ['8', '9', '10', '11', '12', '13', '14', '15', '16']
	
	#default options.
	# in order: host, db, dbuser, dbpassword, dbtable, index, checkbox
	# in index of the above "individual options" - vital.

	demo_defaults = [ host_name[0], db_name[0], db_username_name[0], db_password_name[0], db_table_name[0], index_filename_name[0], checkbox_filename[0] ]
	Nancy_defaults = [host_name[0], db_name[1], db_username_name[2], db_password_name[2], db_table_name[1], index_filename_name[1], checkbox_filename[1] ]
	Toby_defaults = [host_name[0], db_name[2], db_username_name[1], db_password_name[1], db_table_name[2], index_filename_name[2], checkbox_filename[2] ]
	Stassi_defaults = [host_name[0], db_name[0], db_username_name[3], db_password_name[3], db_table_name[3], index_filename_name[3], checkbox_filename[3] ]
	Vanessa_defaults = [host_name[0], db_name[0], db_username_name[3], db_password_name[4], db_table_name[4], index_filename_name[4], checkbox_filename[4] ]
	
	
	def check(*args):
		#print("\tfunction: checks\n\tparams: *args")
		global cut_off
		# user choice of pre-sets:
		#print(f"variable changed to '{variable.get()}'")
		# THIS SHOULD BE UPDATED FOR python 10.x WITH MATCH statement ... 
		preset_name = variable.get()
		if preset_name == user_defaults[1]: # = "demo":
			host_var.set(demo_defaults[HOSTNAME])
			db_var.set(demo_defaults[DBNAME])
			db_username_var.set(demo_defaults[DBUSERNAME])
			db_password_var.set(demo_defaults[DBPASSWORDNAME])
			db_table_name_var.set(demo_defaults[DBTABLENAME])
			index_filename_name_var.set(demo_defaults[INDEXFILENAME])
			checkbox_filename_var.set(demo_defaults[CHECKBOXFILENAME])
			# set up the rest here...
		elif preset_name == user_defaults[TOBY]:
			host_var.set(Toby_defaults[HOSTNAME])
			db_var.set(Toby_defaults[DBNAME])
			db_username_var.set(Toby_defaults[DBUSERNAME])
			db_password_var.set(Toby_defaults[DBPASSWORDNAME])
			db_table_name_var.set(Toby_defaults[DBTABLENAME])
			index_filename_name_var.set(Toby_defaults[INDEXFILENAME])
			checkbox_filename_var.set(Toby_defaults[CHECKBOXFILENAME])
		elif preset_name == user_defaults[NANCY]: 
			host_var.set(Nancy_defaults[HOSTNAME])
			db_var.set(Nancy_defaults[DBNAME])
			db_username_var.set(Nancy_defaults[DBUSERNAME])
			db_password_var.set(Nancy_defaults[DBPASSWORDNAME])
			db_table_name_var.set(Nancy_defaults[DBTABLENAME])
			index_filename_name_var.set(Nancy_defaults[INDEXFILENAME])
			checkbox_filename_var.set(Nancy_defaults[CHECKBOXFILENAME])
		elif preset_name == user_defaults[STASSI]: 
			host_var.set(Stassi_defaults[HOSTNAME])
			db_var.set(Stassi_defaults[DBNAME])
			db_username_var.set(Stassi_defaults[DBUSERNAME])
			db_password_var.set(Stassi_defaults[DBPASSWORDNAME])
			db_table_name_var.set(Stassi_defaults[DBTABLENAME])
			index_filename_name_var.set(Stassi_defaults[INDEXFILENAME])
			checkbox_filename_var.set(Stassi_defaults[CHECKBOXFILENAME])
		elif preset_name == user_defaults[VANESSA]: 
			host_var.set(Vanessa_defaults[HOSTNAME])
			db_var.set(Vanessa_defaults[DBNAME])
			db_username_var.set(Vanessa_defaults[DBUSERNAME])
			db_password_var.set(Vanessa_defaults[DBPASSWORDNAME])
			db_table_name_var.set(Vanessa_defaults[DBTABLENAME])
			index_filename_name_var.set(Vanessa_defaults[INDEXFILENAME])
			checkbox_filename_var.set(Vanessa_defaults[CHECKBOXFILENAME])
		else: # none
			host_var.get()
			db_var.get()
			db_username_var.get()
			db_password_var.get()
			db_table_name_var.get()
			index_filename_name_var.get()
			checkbox_filename_var.get()
		
	
	def display_selected(choice):
		#print("\tfunction: display_selected\n\tparam: choice")
		choice = variable.get()
		#print(choice)
		
	def closeme4():
		global finalList
		global cut_off
		global font_size_to_use
		#print("\tfunction closeme4()")
		finalList = [
			(host_var.get()).strip(),
			(db_var.get()).strip(),
			(db_username_var.get()).strip(),
			(db_password_var.get()).strip(),
			(db_table_name_var.get()).strip(),
			("searchable_indices/"+index_filename_name_var.get()).strip(),
			("preset_tags_profiles/"+checkbox_filename_var.get()).strip()
		]
		cut_off = int( (cut_off_var.get().strip()) )
		font_size_to_use = int( (font_size_to_use_var.get().strip()) )
		#print("CUT OFF IS SET AT line 52 as ", cut_off, " and font-size-to-use = ", font_size_to_use)
		tagmaker(finalList[6])
		ws.destroy()
	
	# setting variable for Integers
	variable = StringVar()
	variable.trace('w', check)
	variable.set(user_defaults[0])
	
	# creating widget
	dropdown = OptionMenu(mainframe, variable, *user_defaults, command=display_selected)
	# positioning widget
	drowdownLabel = Label(mainframe, width="10", fg="red", text="Pre-sets:")
	
	# 1) DEFINE EACH SETTING NEEDS TO BE SETUP Following the HOST model
	#--- HOST
	host_var.trace('w', check)
	host_var.set('localhost')
	host_names_label = Label(mainframe, width="15", text="Host:")
	host_menu = OptionMenu( mainframe, host_var, *host_name, command=display_selected )
	
	#--- Database DB Setup
	db_var.trace('w', check)
	db_var.set(db_name[0])
	db_names_label = Label(mainframe,  width="15", text="Database Name:")
	db_menu = OptionMenu( mainframe, db_var, *db_name, command=display_selected )
	
	#--- Database DB Setup
	db_username_var.trace('w', check)
	db_username_var.set(db_username_name[0])
	db_usernames_label = Label(mainframe,  width="15", text="DB User Name:")
	db_usernames_menu = OptionMenu( mainframe, db_username_var, *db_username_name, command=display_selected )
	
	#--- Database DB PASSWORD Setup
	db_password_var.trace('w', check)
	db_password_var.set(db_password_name[0])
	db_password_label = Label(mainframe,  width="15", text="DB Password:")
	db_password_menu = OptionMenu( mainframe, db_password_var, *db_password_name, command=display_selected )
	
	#--- Database DB TABLE Setup
	db_table_name_var.trace('w', check)
	db_table_name_var.set(db_table_name[0])
	db_table_name_label = Label(mainframe,  width="15", text="DB Table:")
	db_table_name_menu = OptionMenu( mainframe, db_table_name_var, *db_table_name, command=display_selected )
	
	# -- INDEX File
	index_filename_name_var.trace('w', check)
	index_filename_name_var.set(index_filename_name[0])
	index_filename_name_label = Label(mainframe,  width="15", text="Index file name:")
	index_filename_name_menu = OptionMenu( mainframe, index_filename_name_var, *index_filename_name, command=display_selected )
	
	# checkboxes
	checkbox_filename_var.trace('w', check)
	checkbox_filename_var.set(checkbox_filename[0])
	checkbox_filename_label = Label(mainframe,  width="15", text="Checkbox File:")
	checkbox_filename_menu = OptionMenu( mainframe, checkbox_filename_var, *checkbox_filename, command=display_selected )
	
	cut_off_var.trace('w', check)
	cut_off_var.set(cut_off_menu[2])
	cut_off_label = Label(mainframe, width="15", text="Tags per row:")
	cut_off_menu = OptionMenu(mainframe, cut_off_var, *cut_off_menu, command = display_selected )

	font_size_to_use_var.trace('w', check)
	font_size_to_use_var.set(font_size_to_use_menu[2])
	font_size_to_use_label = Label(mainframe, width="15", text="Font size:")
	font_size_to_use_menu = OptionMenu(mainframe, font_size_to_use_var, *font_size_to_use_menu, command = display_selected )
	
	
	#  2) ADD COMPONENTS TO WINDOW
	drowdownLabel.rowconfigure(0, weight = 1)
	drowdownLabel.columnconfigure(0, weight = 1)
	
	drowdownLabel.grid(row = 0, column = 1, sticky='w')
	dropdown.grid(row = 0, column=2, sticky='w')
	
	# row by row ... 
	Label(mainframe,text="Or select individual controls:").grid(row=1,column=0, columnspan=3, sticky = N+W) #'w')
	host_names_label.grid(row=2, column = 1, sticky=N+W) # 'w')
	host_menu.grid(row=2, column = 2, sticky='w')
	
	db_names_label.grid(row=3, column = 1, sticky='w')
	db_menu.grid(row=3, column = 2, sticky='w')
	
	db_names_label.grid(row=3, column = 1, sticky='w')
	db_menu.grid(row=3, column = 2, sticky='w')
	
	db_usernames_label.grid(row=4, column = 1, sticky='w')
	db_usernames_menu.grid(row=4, column = 2, sticky='w')
	
	db_password_label.grid(row=5, column = 1, sticky='w')
	db_password_menu.grid(row=5, column = 2, sticky='w')
	
	db_table_name_label.grid(row=6, column = 1, sticky='w')
	db_table_name_menu.grid(row=6, column = 2, sticky='w')
	
	index_filename_name_label.grid(row=7, column = 1, sticky='w')
	index_filename_name_menu.grid(row=7, column = 2, sticky='w')
	
	checkbox_filename_label.grid(row=8, column = 1, sticky='w')
	checkbox_filename_menu.grid(row=8, column = 2, sticky='w')
	
	cut_off_label.grid(row=9, column = 1, sticky='w')
	cut_off_menu.grid(row=9, column=2, sticky='w')
	
	font_size_to_use_label.grid(row=10, column = 1, sticky='w')
	font_size_to_use_menu.grid(row = 10, column = 2, sticky='w')

	btn = Button(mainframe,  text = '👍🏼 Okay  🆗 ', fg = "green", bd = '5', command = closeme4).grid(row=11, column=1, rowspan=2)


	def get_file_data(bf):
		#print("\tfunction get_file_data(bf)")
		buttonFileWithPath = os.path.realpath(bf)
		#print("testing 827 buttonFileWithPath: ", buttonFileWithPath)
		try:
			with open(buttonFileWithPath) as f:
				bnames = f.read().splitlines()
			return bnames
		except FileNotFoundError as fnf_error:
			messagebox.showinfo("Information","Sorry, that tag/checkbox file was not located.  Will end script now.  ")
			sys.exit(0)
		###############		
		

	def save_data_to_file(filename, term):
		#print("\tfunction save_data_to_file(filename, term)")
		filename.write(term)

	def tagmaker(tagFileToProcess):
		global finalList 
		#global tagFileToProcess
		global zutingFileToProcess
		global filelister
		global dbTableFieldNames
		global dbTableFieldNamesToProcess

		button_files_list = []
		
		#tagFileToProcess = finalList[6] # getFileToProcess()
		
		#okayToContinueProcessing = check_if_file_ok(tagFileToProcess)
		okayToContinueProcessing = True
		
		fieldnames_file = "FIELDNAMESFILE.txt"
		stoplist = ["START_GROUP", "END_GROUP", ":"]
		f = open("FIELDNAMESFILE.txt", "w")
		# CHECK IF STOP WORDS ARE IN STRING
		anames = get_file_data(tagFileToProcess) 
		for i in anames:
			if not any(test in i for test in stoplist):
				i = i.translate({ord(ch):'_' for ch in "?/: @#$%^&*()=≠±+-'‘’"})
				#print("OKAY TO ADD: ", i)
				#f.write(i + ",\n")  # CHANGED TO REMOVE THE ,
				f.write(i + "\n")  # CHANGED TO REMOVE THE ,
		#print("DONE:.  close f. ")
		f.close()
		# END TEST ___________________________________________
		
		if okayToContinueProcessing:
			randomNumberForName = random.randrange(1,500)
			#print("\t\tcalling get_file_data(tagFileToProcess) ... ")
			
			bnames = get_file_data(tagFileToProcess)  # just added.
			
			#print("\tback (line 460) in tagmaker after calling get_file_data()")
			
			s = ""
			groupcount = 0
			tempfile = "Tag" + str(randomNumberForName)+"_"+str(groupcount) + ".txt"
			listOfTagFiles.append(tempfile)
	
			for i in bnames:
				if i == "START_GROUP":
					tempfile = "Tag" + str(randomNumberForName)+"_"+str(groupcount) + ".txt"
					f = open(tempfile, "a")
					button_files_list.append(tempfile)
					listOfTagFiles.append(tempfile)
				elif i == "END_GROUP":
					save_data_to_file(f, s)
					f.close()
					filelister.append(tempfile)
					listOfTagFiles.append(tempfile)
					#print("\t", len(filelister), tempfile)
					s = ""
					groupcount += 1
				else:
					s += i + "\n"
			messagebox.showinfo("Information","All set!  Configuration complete.\nNow select a folder ... ")
			configuration_setup = True

			CBList_x_Options = showCBOptions()  # WAY BELOW LINE xxx
			
		else:
			messagebox.showinfo("Information","Sorry, the configuration is a no-go.")
			#print("Sorry, configuration is not up-to-date or is wrong. STOP ")

# *************************************************************
def createNewScaledImages():
	global imageName
	global photoImageList
	global fullPathImageFileName
	global currentImageNo
	#print("function: createNewScaledImages()")
	#print("\tglobals: imageName, photoImageList, fullPathImageFIleName, currentImageNo")
	# determine ratio 
	#print("837 - createNewScaledImages() function ----------")
	video_ext = ['.mp3', '.mp4', '.mov', '.wmv', 'mp4', 'mp3', 'mov', 'wmv']
	
	photoImageList[:] = []
	#print("841\tcreateNewScaledImages - how the zut does imageList have a value here?")
	
	for j in range(0, len(imageList)):
		imageName = imageList[j]
		
		#print("TESTING 846 - imageList = ", imageList[j])
		the_file_name, the_file_extension = os.path.splitext(imageList[j])
		#print("*** \t the file extension = ", the_file_extension)
		
		if the_file_extension not in video_ext:
			# print("751: NOT video ", the_file_extension)
			img = Image.open(imageName)
			origHeight = img.size[1]
			origWidth = img.size[0]
			newHeight = 0
			newWidth = 0

			##print("894 \timageName = ", imageName)
			##print("imageName with path: ",  os.path.realpath(imageName)," \n")
			##print("CREATED fullPathImageFileName: ... ")
			fullPathImageFileName.append(os.path.realpath(imageName))
		
			origHeight = img.size[1]
			origWidth = img.size[0]
			newHeight = 0
			newWidth = 0

			srcWidth = img.size[0]
			srcHeight = img.size[1]
			maxWidth = pane_width
			maxHeight = pane_height
			ratio = min(maxWidth / srcWidth, maxHeight / srcHeight)
			img = img.resize( (int(srcWidth * ratio),int(srcHeight * ratio)),Image.ANTIALIAS)
			#img = img.resize( (newWidth, newHeight), Image.ANTIALIAS)
	
			img = ImageTk.PhotoImage(img)
			photoImageList.append(img)
		# VIDEO 
		else:
			#print("780: This is a video file to be resized ... ", imageName)
			# storing a video file name.  It'll be resized before being shown.
			fullPathImageFileName.append(os.path.realpath(imageName))

def callback(selection):
	global currentImageNo
	#print("function: callback\n\tparam: selection")
	#print("898 callback - selection: ", selection)
	#print("currentImageNo = ", currentImageNo)
	#print(" tkvar.get()) = ", tkvar.get() )
	#for i in imageList:
	currentImageNo = imageList.index(selection)
	#update_image("jump")
	canvas.itemconfig(image_container, image = photoImageList[currentImageNo])	
	#print("195 - end of callback selection -------------------------- ") 
	

def loadDirectory():
	global imageList
	global win
	global currentImageNo
	global lenFileList
	global nextImageButton
	global prevImageButton
	global imageChosen
	global finalList
	global fullPathImageFileName
	#print("function: loadDirectory\n\tparams: none")
	#print("\tglobals: imageList, win, currentImageNo, lenFileList")
	#print("\tglobals: nextImageButton, prevImageButton, imageChosen")
	#print("\tfinalList, fullPathImageFileName")
	
	#print("loadDirectory()")
	jumpTo = IntVar()
	
	# clear the file list just in case.
	imageList[:] = []
	
	#video_ext = [".mp4", ".mov", ".wmv", ".webm"]
	okFileTypes = ['.GIF','.gif','.heic','.JPEG','.jpeg','.JPG','.jpg','.mov','.mp3','.mp4','.PNG','.png','.TIF','.tif','.TIFF','.tiff','.webm','.webp','.wmv']
	
	win.attributes("-topmost", False)
	open_file = filedialog.askdirectory()
	for win, directories, files in os.walk(open_file, topdown=False):
		for name in files:
			split_tup = os.path.splitext(name)
			if str(split_tup[1]) in okFileTypes:
				imageList.append(os.path.join(win, name))
		for name in directories:
			if split_tup[1] in okFileTypes:
				imageList.append(os.path.join(win, name))
		if len(imageList) > 0:
			#print("length = ", len(imageList))
			nextImageButton.config(state = 'normal')
			prevImageButton.config(state = 'normal')
			addRecordButton.config(state = 'normal')
			#altAddRecordButton.config(state = 'normal')
			jumpButton = ttk.Button(row2Label, text="Go", command=lambda: setImageNo("jump") )
			jumpButton.config(state = 'normal')
	lenFileList = len(imageList) # -1

	# ORIGINAL
	popupMenu = OptionMenu(row2Label, tkvar, *imageList, command=callback) # update_image("next")) 
	#popupMenu.bind('<<ComboboxSelected>>',change_dropdown)

	# callback)  # was callback
	
	tkvar.set(imageList[0]) # to set to first name?
	currentImageNo = 0
	
	smallerFont12 = tkFont.Font(family = "SF Pro Rounded Light", size = font_size_to_use) # 11)
	popupMenu.config(font = smallerFont12)
	popupMenu.pack(side=LEFT)
	
	
	# JUMP TO BUTTON OPTN
	jumpTo = IntVar()
	imageChosen = ttk.Combobox(row2Label, width=4, textvariable=jumpTo, postcommand = updtcblist)
	imageChosen.pack()
	
	createNewScaledImages()
	
	
# ------------------------------------------------------------
# 
# prep output area. - HTML, JSON, EAD, etc.  Use finalCreateHTML as model.
# 
# ------------------------------------------------------------

def finalCreateHTML(listOfFileNamesForDisplay):
	global imageList
	#print("function: finalCreateHTML\n\tparams: listOfFileNamesForDisplay")

	testl = []
	for i in range(0, len(userTagsOptions)):
		testl += userTagsNames[i]
	
	s = ""
	video_ext = ['.mp4', '.mov', '.wmv', '.webm']
	
	webpageTitle = simpledialog.askstring(title="Title", prompt="What do you want to name your webpage?")
	
	# ORIGINAL totalNoOfImages = len(imageList)
	totalNoOfImages = len(listOfFileNamesForDisplay)
	
	#print("*"*30)
	#print("--- this is in finalCreateHTML --- listOfFileNamesForDisplay = ", listOfFileNamesForDisplay,"\n")
	
	if webpageTitle == "":
		webpageTitle = "Demo Webpage"
	else:
		webpageTitle = webpageTitle.translate({ord(ch):'_' for ch in "?/: @#$%^&*()=≠±+-'‘’"})

	htmlOutput = "webpages/" + webpageTitle + ".html"


	# HERE DIFFERENT TEMPLATES CAN BE USED BASED ON THE VALUE OF templateVariables:
	# THE default is RWD (responsive web design).
	# now using the StringVar - but can be changed to IntVar... 
	selected_template = templateVariables.get()
	
	if selected_template == "RWD":
		# START INDENT HERE FOR RWD:
		column_number = 0
		image_counter = 0
		max_no_of_images_per_row = 2
	
		with open("output_profile_and_templates/htmlHeader8.txt", "r") as f:
			htmlHeaderTags = f.read()
		s = htmlHeaderTags
		
		# alternate left/right - this is the default RWD offering.
		
		for i in range(0, totalNoOfImages):
			if image_counter == 0:
				the_file_name, the_file_extension = os.path.splitext(listOfFileNamesForDisplay[i])
				if the_file_extension in video_ext:
					s += '\n<div class="flex-container">' +\
					'\n\t<div class="flex-item-left">' +\
					'<video controls="controls" preload="metadata">' +\
					'<source id='+str(i)+' src="' + listOfFileNamesForDisplay[i] +'#t=0.1" type="video/mp4" onclick=myPopFunction('+str(i)+')>'+\
					'</video></div>'
				else:
					s += '\n<div class="flex-container">\n\t<div class="flex-item-left">'+\
					'\n\t<img id="'+str(i)+'" src="' + listOfFileNamesForDisplay[i] + '" style="width:100%" '+\
					'onclick="myPopFunction('+str(i)+')">'+\
					'\n</div> <!-- end left div -->'
				image_counter += 1
				
			else:
				if the_file_extension in video_ext:
					s += '\n<div class="flex-container">' +\
					'\n\t<div class="flex-item-left">' +\
					'<video controls="controls" preload="metadata">' +\
					'<source id='+str(i)+' src="' + listOfFileNamesForDisplay[i] +'#t=0.1" type="video/mp4" onclick=myPopFunction('+str(i)+')>'+\
					'</video></div>'
				else:
					s += '\n<div class="flex-item-right">'+\
		  			'\n\t<img id="'+str(i)+'" src="' + listOfFileNamesForDisplay[i] + '" style="width:100%" onclick="myPopFunction('+str(i)+')">'+\
					'\n\t</div> <!-- end right div -->\n</div> <!-- end flex-container div -->\n'
				image_counter = 0
	
		s += "<hr />"
		# ALL DONE WITH IMAGES - UPDATE PAGE TITLE AND CLOSE.
		# update the title of the gallery page galleryName in html
		s += '<script>document.getElementById("galleryName").innerHTML = "'+webpageTitle+'";</script>'
				
		with open("output_profile_and_templates/htmlFooter8.txt", "r") as f:
			htmlFooterTags = f.read()
		
		s += htmlFooterTags
		# END OF RWD TEST 
	try:
		file1 = open(htmlOutput, "w")
		file1.write(s)
		file1.close()
		#print("File done: ", htmlOutput)
		if os.path.exists( (os.path.realpath(htmlOutput))):
			messagebox.showinfo("Information","File Created: "+htmlOutput)
			
		# test of auto opening webpage
		#print("htmlOutput = ", htmlOutput)
		#print("real path = ", os.path.realpath(htmlOutput))
		newhtmlfilepath = "file://"+os.path.realpath(htmlOutput)
		#print("***** newhtmlfilepath = ", newhtmlfilepath)
		
		webbrowser.open(newhtmlfilepath)
	except OSError as err: 
		#print("OS Error {0}". format(err))
		messagebox.showinfo("Information","OS Error {0}". format(err))
# ______________________________________________________________________
# END OF finalCreateHTML
# ______________________________________________________________________

def createHTMLfromFlatFile(): ### createHTML("db", myresult)
	global lenFileList
	global imageList
	# I DON"T THINK THIS IS USED ... 
	#messagebox.showinfo("Information","createHTMLfromFlatFile() - 984")
	#print("function createHTMLfromFlatFile():\n\tparams: none\n\tglobal: lenFileList, imageList")
	
	#print("1084: createHTMLfromFlatFile()")
	s = ""
	htmlHeaderTags = ""
	htmlFooterTags = ""
	file1 = ""
	
	webpageTitle = simpledialog.askstring(title="Title", prompt="What do you want to name your webpage?")
	
	video_ext = [".mp4", ".mov", ".wmv", "webm"]

	# BUILD THE PAGE -------------------------------------------------
	htmlOutput = "webpages/testoutput" + str(random.randint(0, 99)) + ".html"
	#print("htmlOutput file is ", htmlOutput,"\n")

	with open("output_profile_and_templates/htmlHeader8.txt", "r") as f:
		htmlHeaderTags = f.read()
		#print("1016: htmlHeaderTags = ", htmlHeaderTags)
		
	s = htmlHeaderTags + "\n<div class='row'>\n\tr<div class='column'>\n"

	c = 0
	for i in imageList:  # ORIGINAL fileList:
		#print("i = ",i)
		extension = os.path.splitext(i)[1]
		#print("1011 - extension during creating web page - ? ", extension)
		c += 1
		stringC = str(c).strip(" ")
		s+= "<img src=\"" + str(i) + "\" onclick=\"myPopFunction("+str(c)+")\" onclick=\"myUndoPopFunction("+stringC+")\" id=\""+stringC+"\">\n"
		if c % 7 == 0:
			s += "</div>\n<div class=\"column\">"


	with open("output_profile_and_templates/htmlFooter8.txt", "r") as f:
		htmlFooter = f.read()
	   
	s += htmlFooter
	
	print("\n\ns = ", s)
		
	try:
		file1 = open("webpages/"+htmlOutput, "w")
		file1.write(s)
		file1.close()
		if os.path.exists( (os.path.realpath(htmlOutput))):
			messagebox.showinfo("Information","File Created: "+"webpages/"+htmlOutput)
	except OSError as err: 
		#print("OS Error {0}". format(err))
		messagebox.showinfo("Information","OS Error {0}". format(err))
	
	s = ""
	c = 0
	
# --------------------------------------- CREATE JSON
def finalCreateJson(listOfFileNamesForDisplay, query_terms):
	#print("function: finalCreateJson\n\tparams: listOfFileNamesForDisplay")
	#print("\tquery_terms")
	
	messagebox.showinfo("Information","finalCreateJson() 1065")
	#print("listOfFileNamesForDisplay=",listOfFileNamesForDisplay)
	#print("-"*30,"\nthis is finalCreateJson - query_terms:\n",query_terms)
	
	jsonOutput = "testoutput" + str(random.randint(0, 99)) + ".json"
	messagebox.showinfo("Information","Output json to "+jsonOutput)
	jsonHeader = "{\n\t\"results\": {\n\t\t\"date\": \""+datetime.today().strftime('%Y-%m-%d-%H:%M:%S')+"\","
	jsonFooter = "\n\t}\n}"
	s = jsonHeader
	#need to break up the query_terms list into a set of strings?
	query_string = ""
	for t in range(0, len(query_terms)):
		print("t = ", t)
		query_string += query_terms[t]+", "
	query_string = query_string[:-2]
	
	c = 0
	for i in listOfFileNamesForDisplay:
		extension = os.path.splitext(i)[1]
		c += 1
		s += "\n\t\t\"image\": {\n\t\t\t\"name\": \"OUTPUT NAME\","
		s += "\n\t\t\t\"imgNo\": "+str(c)+","
		s += "\n\t\t\t\"searchList\": \""+ query_string +"\","
		s += "\n\t\t\t\"src\": \""+i+"\"," 
		s += "\n\t\t\t\"width\": 100," 
		s += "\n\t\t\t\"height\": 100,"
		s += "\n\t\t\t\"format\": \""+extension+"\""
		s += "\n\t\t}"
	s += jsonFooter
	try:
		file1 = open(jsonOutput, "a")
		file1.write(s)
		file1.close()
	except OSError as err: 
		print("OS Error {0}". format(err))
		messagebox.showinfo("Information","OS Error {0}". format(err))

# ------------------ end finalCreateJson write out.


# ADDED MAY 4, 2022 - to save to MySQL DB!  Hurray
def saveToMySQL(final_query):
	#print("1211 saveToMySQL(final_query)")
	#messagebox.showinfo("Information","saveToMySQL")
	#messagebox.showinfo("Information","saveToMySQL Option "+final_query)
	# TEST TEST TEST KEEP, THO!
	try:
		mydb = mysql.connector.connect(**config)
		mycursor = mydb.cursor()
		# THESE ARE THE DATA TO BE SAVED to TABLE
		mycursor.execute(final_query)
		mydb.commit()
	except Exception as e:
		messagebox.showinformation("Information", e)
	finally:
		mydb.close()

	messagebox.showinfo("Information",str(mycursor.rowcount) + " record added.")

# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
#def getAllRows(query):
def	getAllRows(query, fieldnamesfromfile, searchzut):
	#global searchOptionsChoices
	#messagebox.showinfo("Information", "getAllRows(query)")
	print("\n\nWHAT ARE searchOptionsChoices = ", searchOptionsChoices,"\n\n")
	#print("\n\n\nfunction: getAllRows\n\tparam: query\n\tglobal searchOptionsChoices")
	#print("query = ", query)
	#print("\n"*3)
	# ******* IMPORTANT
	#OUTPUTASHTML = 4
	#OUTPUTASJSON = 5
	#OUTPUTASVRA = 6
	#OUTPUTASEAD = 7
	
	#messagebox.showerror('Info', '1212 getAllRows')
	
	#print("1209 - getAllRows(query) = ", query)
	
	listOfFileNamesForDisplay = []

	"""
	HOSTVAR = 0
	USERVAR = 1
	DBPASSWORDVAR = 2 # added here so all #s changed after
	DBVAR = 3  # DB TO USE 
	DBTABLEVAR = 4   # DB TABLE FIELD NAMES
	FLATFILEVAR = 5  # SAVE FLAT FILE FOR INDEX
	CBVAR = 6 # CHECKBOXES ON SCREEN
	"""
	HOSTNAME = 0
	DBNAME = 1
	DBUSERNAME = 2
	DBPASSWORDNAME = 3
	DBTABLENAME = 4
	INDEXFILENAME = 5
	CHECKBOXFILENAME = 6
	
	config = {
		"user": finalList[DBUSERNAME],
		"password": finalList[DBPASSWORDNAME],
		"host": finalList[HOSTVAR],
		"database": finalList[DBNAME],
		"raise_on_warnings": True
	}

	
	# OLD VERSION - does NOT work now ...
	"""
	config = {
		"user": finalList[USERVAR],
		"password": finalList[DBPASSWORDVAR],
		"host": finalList[HOSTVAR],
		"database": finalList[DBVAR],
		"raise_on_warnings": True
	}
	"""
	print("--------- 1160 test search ------config -- \n", config)
	
	try:
		cnx = mysql.connector.connect(**config)
		print("CONNECTING TO cnx: 1185")
		try:
			cursor = cnx.cursor()
			cursor.execute(query)
			myresult = cursor.fetchall()
			totalNoOfImages = len(myresult)
			messagebox.showinfo("Information","There are {0} records". format(totalNoOfImages))
			#print("TOTAL NO OF IMAGES: " , totalNoOfImages)

		except:
			print("597: Sorry, the query failed.")
			raise
		else:
			#print("\t1227 - this is the else are ... ")
			for (id, filename) in cursor:
				print("-", id, ":", filename)
			#print("1231 - for row in myresult ... ")
			for row in myresult:
				#print("1199: ", str(row[1]))
				#print(str(row[0]))
				listOfFileNamesForDisplay.append(row[1])
		finally:
			cnx.close()
			#print("604: Closing DB connection.")
	except Exception as e:
		messagebox.showinfo("Information","Sorry, DB error {0}". format(e))
		#print("572: Something went wrong:", e)
	else:
		#print("1247 - after search - about to print results and make page")
		#print("1278: getAllRows() -  listOfFileNamesForDisplay - ? ", listOfFileNamesForDisplay)
		#print("\t", type(listOfFileNamesForDisplay))
		# if webpage option created - send there ...
		#print("1281: DB search - calls finalCreateHTML() - different from flat file.")
		#print("\n\n\n\nlistofFileNamesForDisplay: \n", listOfFileNamesForDisplay)
		if searchOptionsChoices[OUTPUTASHTML]:
			#print("***** 1186 - listOfFileNamesForDisplay = ", listOfFileNamesForDisplay)
			finalCreateHTML(listOfFileNamesForDisplay)
		if searchOptionsChoices[OUTPUTASJSON]:
			#print("***** 1225 JSON OPTION - listOfFileNamesForDisplay = ", listOfFileNamesForDisplay)
			finalCreateJSON(listOfFileNamesForDisplay)
		if searchOptionsChoices[OUTPUTASEAD]:
			#print("***** 1225 E A D OPTION - listOfFileNamesForDisplay = ", listOfFileNamesForDisplay)
			#print("need fieldnamesfromfile and searchzut!!!:!")
			#print("fieldnames...", fieldnamesfromfile, searchzut)
			#finalCreateEAD(listOfFileNamesForDisplay)
			#messagebox.showinfo("Information","createEAD() will be here? ")
			createEAD(fieldnamesfromfile, searchzut)

		#print("MORE COOL STUFF TO HAPPEN")
# _________________________________________________________________


# _________________________________________
# S E A R C H
def searchRecords():
	global finalList
	global imageName # = imageList[j]
	global userTagsOptions
	global userTagsNames
	global long_text
	global text_widget
	global fullPathImageFileName
	global currentImageNo
	global variables 
	global searchOptionsChoices

	global imageList

	print("function: searchRecords()\n\tparams: none")
	print("\tglobals: finalList, imageName, userTagOptions, userTagsNames")
	print("\tglobals: long_text, text_widget, fullPathImageFileName")
	print("\tcurrentImageNo, variables, searchOptionsChoices")

	# ******* IMPORTANT
	"""
	ANDSEARCH = 0
	ORSEARCH = 1
	RDBMSSEARCH = 2
	FLATFILESEARCH = 3
	OUTPUTASHTML = 4
	OUTPUTASJSON = 5
	"""
	operand = None
	#print("Test area:","-"*40)
	#print("\n1201\tsearchRecords()")
	#print("\tsearchOptions = ", list(searchOptions.state()))
	searchOptionsChoices = list(searchOptions.state())
	if searchOptionsChoices[ANDSEARCH]:
		#print("\t1365 AND SEARCH")
		operand = " AND "
	if searchOptionsChoices[ORSEARCH]:
		#print("\t1365 OR SEARCH")
		operand = " OR "
	if searchOptionsChoices[RDBMSSEARCH]:
		print("\tRDBMS SEARCH")
	if searchOptionsChoices[FLATFILESEARCH]:
		print("1213 searchRecords() \tFLATFILE SEARCH")
	if searchOptionsChoices[OUTPUTASHTML]:
		print("\tOUTPUT AS HTML")
	if searchOptionsChoices[OUTPUTASJSON]:
		print("\tOUTPUT AS JSON")
	if searchOptionsChoices[OUTPUTASEAD]: #7
		print("\tOUTPUT AS EAD")
		
		
	# list holding matching files temp
	temp_file_matches = []
	

	##################### FLAT FILE SEARCH
	if searchOptionsChoices[FLATFILESEARCH]:
		print("\t***** 1227 - searchOptionsChoices[FLATFILESEARCH]")
		searchzut = []
		fileList = []
		#0 get the terms to be searched (similar to finalAddRecords ...
		# merge the various lists into a single list of 0/1s from each group
		# two-step process - find out which CBs are checked (value = 1)
		# and then match them to the tag name ...
		search_in_flat_file = [] # terms to search for
		combinedCBlists = []
		fieldnamesfromfile = []
		final_matches = [] # the file names that match the search
		tempCBzut = []
		
		
		# THIS PART IS SUPPOSED TO IDENTIFY THE NAMES OF THE FIELDS 
		# BASED ON CHECKBOX STATUS:
		tempCBzut = []
		for i in range(0, len(userTagsOptions)):
			tempCBzut += list(userTagsOptions[i].state())

		#for i in range(0, len(tempCBzut)):
			#i = 0
	
		flatTextFileToUse = finalList[FLATFILEVAR] 
		final_query = ""
		final_CB_options = []
		
		print("\n1215:This section confirms the 0/1 status of individual checkboxes: tempCBzut = ",tempCBzut,"\n")
		
		with open('FIELDNAMESFILE.txt') as f:
			fieldnamesfromfile = f.read().splitlines()
			
		print("1259: confirm all fieldnamesfromfile = ", fieldnamesfromfile)
		
		# merge the various lists into a single list of 0/1s from each group
		for i in range(0, len(userTagsOptions)):
			searchzut += list(userTagsOptions[i].state())
			print("\t1262: searchzut = ", searchzut)

		#now scan that list of 0/1 and get to the index of each "1" value.
		query_terms = [] # ""
		cnt = 0
		for i in range(0, len(searchzut)):
			if searchzut[i] == 1:
				query_terms.append(fieldnamesfromfile[i])

		number_of_hits = 0
		temp_imageList = []
		
		if searchOptionsChoices[ORSEARCH]:
			#print("1291 if searchOptionsChoices[ORSEARCH] for flat file")
			with open(finalList[FLATFILEVAR], "r") as all_index_terms:
				lines = all_index_terms.readlines()
			for line in lines:
				#print("1295: line from file to be searched:", line)
				# --------------------- ANY = "or" --------------------
				if any(hit in line for hit in query_terms):
					#print("query term found in flat file line", line)
					#print("\tType of line = ", type(line))
					templine = line.split("\t")
					#imageList.append(templine[0])
					temp_imageList.append(templine[0])
					#print("..adding this to temp_imageList: ", templine[0])
					number_of_hits += 1
					templine[:] = []
			msg = "There are " + str(number_of_hits) +" hits searching any term in file index."
			messagebox.showinfo("Information", msg)
			#print("ABOUT TO CALL createNewScaledImages()")
			if number_of_hits > 0:
				imageList = temp_imageList
				#print("HERE IS A LIST OF THE HIT(S): as imageList ",imageList) 
				nextImageButton.config(state = 'normal')
				prevImageButton.config(state = 'normal')
				addRecordButton.config(state = 'normal')
	
				# KEEP?! createNewScaledImages()
				#print("1319 - confirm output as html searchOptionsChoices = ", searchOptionsChoices[OUTPUTASHTML])
				if searchOptionsChoices[OUTPUTASHTML] == 1:
					#print("1321 - about to call finalCreateHTML(temp_imageList)")
					#print("temp_imageList = ", temp_imageList)
					finalCreateHTML(temp_imageList)
				if searchOptionsChoices[OUTPUTASJSON] == 1:
					messagebox.showinfo("Information", "This is the call JSON option- calls finalCreateJson")
					#createJson(temp_imageList)
					finalCreateJson(temp_imageList, query_terms)
				### HERE IS WHERE OPTIONS SHOULD BE PLACED - 
				### REMOVE OTHER OUTPUTASEAD, ETC ... 
				if searchOptionsChoices[OUTPUTASEAD] == 1:
					messagebox.showinfo("Information", "This is the call EAD option: not yet available for flatfile indices.")
					#createJson(temp_imageList)
					#finalCreateEAD(temp_imageList, query_terms)
					#createEAD(fieldnamesfromfile, searchzut)
				
				
			
		# AND SEARCH
		if searchOptionsChoices[ANDSEARCH]:
			temp_imageList = []
			with open(finalList[FLATFILEVAR], "r") as all_index_terms:
				lines = all_index_terms.readlines()
			for line in lines:
				# -------------------- if ALL => all -----------
				if all(hit in line for hit in query_terms):
					#print("line = ", line)
					#print("query_terms = ", query_terms)
					#print("ALL HITS HIT!", line)
					number_of_hits += 1
					templine = line.split("\t")
					temp_imageList.append(templine[0])
					#imageList.append(templine[0])
					templine[:] = []
			msg = "There are " + str(number_of_hits) +" hits searching for ALL terms in file index."
			messagebox.showinfo("Information", msg)
			if number_of_hits > 0:
				imageList = temp_imageList
				nextImageButton.config(state = 'normal')
				prevImageButton.config(state = 'normal')
				addRecordButton.config(state = 'normal')
				#createNewScaledImages()
				print("1319 - confirm output as html searchOptionsChoices = ", searchOptionsChoices[OUTPUTASHTML])
				if searchOptionsChoices[OUTPUTASHTML] == 1:
					print("1353 - AND search - about to call finalCreateHTML(temp_imageList)")
					print("temp_imageList = ", temp_imageList)
					finalCreateHTML(temp_imageList)
				if searchOptionsChoices[OUTPUTASJSON] == 1:
					messagebox.showinfo("Information", "This is the call JSON option.")
				if searchOptionsChoices[OUTPUTASEAD] == 1:
					messagebox.showinfo("Information", "This is the call EAD option using AND - but not yet available for flat file search.")
					#createJson(temp_imageList)
					#finalCreateEAD(temp_imageList, query_terms)
					#createEAD(fieldnamesfromfile, searchzut)

	# -- RDBMS -------------------------------------------------
	if searchOptionsChoices[RDBMSSEARCH]:
		#wtf = "1543: searchOptionsChoice: DBVAR = ",finalList[DBVAR], " table: ", finalList[DBTABLEVAR]
		#messagebox.showerror('Info', wtf)
		
		# ################### RDBMS FILE SEARCH	
		# ADDDED SPECIAL SEARCH TESTER 
		searchQuery = "SELECT * FROM "+finalList[DBTABLEVAR]+" WHERE "
		fieldnamesfromfile = []
		searchzut = []
		with open('FIELDNAMESFILE.txt') as f:
			fieldnamesfromfile = f.read().splitlines()
		
		# merge the various lists into a single list of 0/1s from each group
		for i in range(0, len(userTagsOptions)):
			searchzut += list(userTagsOptions[i].state())

		#___________________________________________________________#
		# ############################## RDBMS DATABASE SEARCH  
		#now scan that list of 0/1 and get to the index of each "1" value.
		print("\tsize of searchzut ", len(searchzut))
		cnt = 0
		for i in range(0, len(searchzut)):
			if searchzut[i] == 1:
				searchQuery += fieldnamesfromfile[i]+"="+str(searchzut[i]) + operand 
		
		# clean up extra operand:
		#if searchOptionsChoices[ORSEARCH]:
		searchQuery = searchQuery[:-4]+";"
	
		#print("searchQuery = ", searchQuery)
	
		#print("\n1547 - ran query ... the query has been created; now going to search "+\
		#"and calling getAllRows to complete search and generate page.")
		
		#print("\n***\t->calling getAllRows(searchQuery): 1402 - searchQuery = ", searchQuery)
		getAllRows(searchQuery, fieldnamesfromfile, searchzut)

# ________________________________________

# #######################################
#
# finalAddNewRecord
# 
#########################################

def finalAddNewRecord():
	global finalList
	global imageName # = imageList[j]
	global userTagsOptions
	global userTagsNames
	global long_text
	global text_widget
	global fullPathImageFileName
	global currentImageNo
	global variables 
	global imageName
	global searchOptionsChoices
	""" debugging
	print("function: finalAddNewRecord:\n\tparam: none\n\tglobals: ")
	print("\tfinalList, imageName, userTagsOptions, userTagsNames")
	print("\ttext_widget, fullPathImageFileName, currentImageNo")
	print("\tvariables, imageName")
	print("-1426- error on db user name - test cycle thru finalList:")
	print("HOSTVAR = ", finalList[HOSTVAR])
	print("DB USERVAR = ", finalList[USERVAR])
	print("DB PASSWORD = ", finalList[DBPASSWORDVAR])
	print("DB VAR = ", finalList[DBVAR]) # = 3  # DB TO USE 
	print("DB table = ", finalList[DBTABLEVAR]) # = 4   # DB TABLE FIELD NAMES
	print("flatfile = ", finalList[FLATFILEVAR]) # = 5  # SAVE FLAT FILE FOR INDEX
	"""
	#CBVAR = 6 # CHECKBOXES ON SCREEN

	# ******* IMPORTANT
	
	#messagebox.showinfo("Information","This is finalAddNewRecord()")

# ********************* skipOption is set to True because ADD means add
# and to obey the saveto options (flatfile and rdbms), else skip.
	#messagebox.showinfo("Information","This is finalAddNewRecord - and the skipOption is FALSE")
	skipOption(False)
	#print("skipOption set to False")
	
	#print("----1454 - ---- searchOptionsChoices[OUTPUTASEAD]")
	#for g in range(0, len(searchOptionsChoices)):
		#print(g, " option = ", searchOptionsChoices[g])
	#print("_"*40)
	
	
	userImageName = userImageNameEntry.get()
	userNotes = text_widget.get('1.0','end-1c')
	
	imageNameToSave = fullPathImageFileName[currentImageNo]
	
	# CHECKBOX STATUS: GET THESE VALUES
	# A checkbox that has been checked must be value 1, else 
	#print("\nfinalAddNewRecord\n1483: getting the values of the check boxes ... ? ")
	tempCBzut = []
	for i in range(0, len(userTagsOptions)):
		tempCBzut += list(userTagsOptions[i].state())
	for i in range(0, len(tempCBzut)):
		 i = 0
		 
	#print("\n1537 - Motherfucking check on tempCBzut = ", tempCBzut)

	# SO FAR THIS WORKS - June 22, 7:55 pm
	#print("CHECKING the CHECK BOXES - fix... ", tempCBzut)
	#print("_"*50)

	user_notes = extract_data()
	
	#1 get save options
	saveOptionsListFinal = list(saveOptions.state())
	saveToRDBMS = saveOptionsListFinal[SAVETODB]
	saveToIndexFile = saveOptionsListFinal[SAVETOFILE]
	setCarryOn = saveOptionsListFinal[SETCARRYON]
	final_query = ""
	final_CB_options = []

	
	# 2 if option for FLAT FILE
	# save data to the selected Index flat file
	# check if file available and writable.
	# for now - just default it as ready

	skip_this_image = skipOption()
	#print("THIS IS OPTION IN THE SAVE OPTION AREA WHAT THE FUCK NOW?", skip_this_image)

	# ********************************** FLAT FILE *******x****************
	#if skip_this_image == False:
		#print("flat file save - SKIP IMAGE = ", skip_this_image)
		
	if saveOptionsListFinal[SAVETOFILE] == 1 and skip_this_image == False:
		#print("\tsaveOptionsListFinal[SAVETOFILE]")
		#messagebox.showinfo("Information","Save to flat file option - skip = "+ str(skip_this_image))
		# SAVE FIELD NAMES TO FLAT FILE -------------------- #
		flatTextFileToUse = finalList[FLATFILEVAR]
		tempmsg = "Saving to flat file: "+finalList[FLATFILEVAR]
		messagebox.showinfo("Information", tempmsg)
		fieldnamesfromfile = []
		searchzut = []
		save_to_flat_file =  fullPathImageFileName[currentImageNo] + "\t"
		
		#print("\n 1630 - imageName = ", imageName, "\t", imageList[currentImageNo])
		
		#save_to_flat_file = imageName + "\t"
		#print("1312 - test save_to_flat_file = ", save_to_flat_file)
		
		with open('FIELDNAMESFILE.txt') as f:
			fieldnamesfromfile = f.read().splitlines()
		
		# merge the various lists into a single list of 0/1s from each group
		for i in range(0, len(userTagsOptions)):
			searchzut += list(userTagsOptions[i].state())

		#now scan that list of 0/1 and get to the index of each "1" value.
		#print("\tsize of searchzut ", len(searchzut))
		
		cnt = 0
		for i in range(0, len(searchzut)):
			#print("\n\n\n1925: about to save to flat file")
			if searchzut[i] == 1:
				save_to_flat_file += fieldnamesfromfile[i]+"\t"
		save_to_flat_file += "\n" # ADDED 

		#print("\1649 - \tsave_to_flat_file = ", save_to_flat_file)
		# data should be okay but who the zut knows ... 

		saveToIndexFile = os.path.realpath(flatTextFileToUse)
		
		if os.path.exists( (os.path.realpath(flatTextFileToUse)) ):
			saveToIndexFile = os.path.realpath(flatTextFileToUse)
			
			with open(saveToIndexFile, 'a') as fileindex:
				fileindex.write(save_to_flat_file)
		else:
			tempmsg = "The index file ", saveToIndexFile, " doesn't exist. Creating it now."
			messagebox.showinfo("Information", tempmsg)
			with open(saveToIndexFile, 'a') as fileindex:
				fileindex.write(save_to_flat_file)
			
			
		if not saveOptionsListFinal[SETCARRYON]:
			click_meX()
			text_widget.delete("1.0","end")
			

	# ********************************** RDBMS ***********************
	# 3 if option for RDBMS
	# ADDED skipOption() just in case of auto saving skipped records.
	# JUNE 23, 2022
	
	#messagebox.showinfo("Information","SKIP THIS IMAGE = "+str(skip_this_image))
	
	if saveOptionsListFinal[SAVETODB] == 1:
		#messagebox.showinfo("Information","Save to DB option with skip_this_image = "+str(skip_this_image))
		#print("\n"*10)
		#print("1571: saveOptionsListFinal 0 what the fuck shit is here? 1569")
		HOSTNAME = 0
		DBNAME = 1
		DBUSERNAME = 2
		DBPASSWORDNAME = 3
		DBTABLENAME = 4
		INDEXFILENAME = 5
		CHECKBOXFILENAME = 6
		#print("\tS1524 - AVE TO DB: saveOptionsListFinal[SAVETODB]")
		userImageName = userImageNameEntry.get()
		#messagebox.showinfo("Information",userImageNameEntry.get()+" - "+userImageName+" but finalList = ",finalList[USERVAR])
		
		config = {
			"user": finalList[DBUSERNAME],
			"password": finalList[DBPASSWORDNAME],
			"host": finalList[HOSTVAR],
			"database": finalList[DBNAME],
			"raise_on_warnings": True
		}
		#print("_TEST OF CONFIG ... 1542: ", config)
		# ---------------------------------------- PREPARE THE QUERY
		# a) get list of field names
		# STRINGS!
		# OLD WAY --------------- not sure if still needed
		with open("FIELDNAMESFILE.txt") as f:
			temp_list = f.read()
		
		# because there may be a final extra , ...
		# LIST OF FIELD NAMES FOR THE QUERY
		xtemp_list = temp_list
		xtemp_list = xtemp_list.replace("\n", ",")
		#xtemp_list = xtemp_list[:-1]  # TO REMOVE THE FINAL ,?
		
		# LIST OF FIELD NAMES IN CASE NEED TO CREATE NEW TABLE.
		newtable_list = temp_list.replace("\n", " BOOLEAN,\n")
		newtable_list = newtable_list[:-1]
		newtable_list = newtable_list[:-1]

		#fullPathImageFileName[currentImageNo]). ? imageNameToSave
		###. ADDED userImageName
		#print("USER IMAGE NAME 1636 = ", userImageName)
		
		final_query = "INSERT INTO " + finalList[DBTABLENAME] + " (filename, userImageName, " +\
		xtemp_list + " user_notes) VALUES ('" + fullPathImageFileName[currentImageNo] +"', '" +\
		userImageName+"', "
		
		#print("\n"*4,"_*_"*30,"\nfinal_query for ADD line 1607: \n\t", final_query,"\n----")
		
	
		# ------------------------- the check box values should be set already
		# -------- from tempCBzut above ... 
		#print("1618 - building query - what's the state of CBs?")
		#print("tempCBzut = ", tempCBzut)
	
		# c) get the checkbox Options
		"""
		tempzut = []
		#print("1449 - tempzut = ")
		for i in range(0, len(userTagsOptions)):
			tempzut += list(userTagsOptions[i].state())
			#print("1452 - tempzut =", tempzut)

		for i in range(0, len(tempzut)):  # -1
			final_query += str(tempzut[i])+","
		"""
		
		print("\n UPDATED FINAL QUERY WITH VALUES FROM tempCBzut = ")
		# FIX TO SOMETHING To BE ADDED ... 
		
		#string_ints = [str(int) for int in tempCBzut]
		#str_of_ints = ','.join(string_ints)
		
		#print("\n1641 - processing tempCBzut for SQL final_query: \n")
		# ********************** HERE - idiot.
		
		# stupid but if it works ...
		for i in range(0, len(tempCBzut)):
			final_query += str(tempCBzut[i])+","
			#final_query += str(i)+","
		#print("\n1650: ", final_query)
		#final_query = final_query[:-1] # for the final , added above.
		#final_query += str_of_ints # tempCBzut
		#print("\n* * * * * 1675\n\tWhat is final_query now? ", final_query)
		final_query += "'"+user_notes+"');"
		#print("\n\n\nFINAL_QUERY 1654\n", final_query,"\n*****\n")
		#print("_"*40, "1641 add to DB effort ... \n")
		
		# --------------------------------------- PREPARE THE TABLE AND DB
		final_database = finalList[DBNAME] # databaseToUseVar.get(DBVAR)
		final_db_table_to_use =  finalList[DBTABLENAME]

		create_new_table = "CREATE TABLE " + final_db_table_to_use +" ("+\
		"id INT UNSIGNED AUTO_INCREMENT NOT NULL PRIMARY KEY, "+\
		"filename VARCHAR(255) NOT NULL, "+\
		"userImageName VARCHAR(25) NULL DEFAULT 'No name',"+\
		newtable_list +\
		",\nuser_notes TEXT,"+\
		"\ncreated_on DATETIME DEFAULT CURRENT_TIMESTAMP);"
		
		okToUseTable = False
		
		stmt = "SHOW TABLES LIKE '"+final_db_table_to_use+"';"
		try:
			cnx = mysql.connector.connect(**config)
			print("OPENED CONNECTION TO DB to test for Table")
			try:
				#messagebox.showinfo("Information","DB Connected: testing for table.")
				cursor = cnx.cursor()
				cursor.execute(stmt)
				result = cursor.fetchone()
				#messagebox.showinfo("Information",result)
				print("1552 - result = ", result)
				if result:
					#messagebox.showinfo("Information","The table "+final_db_table_to_use+" exists.")
					okToUseTable = True
				else:
					#print("\n*** Creating that table now ... ", final_db_table_to_use)
					messagebox.showinfo("Information","Creating the table "+final_db_table_to_use)
					#print("COMMAND FOR create_new_table: ", create_new_table)
					cursor.execute(create_new_table)
					okToUseTable = True
			except:
				print("Sorry, the query failed.", stmt)
				messagebox.showinfo("Information","Sorry, the query to create new table failed.")
				raise
			finally:
				cnx.close()
		except Exception as e:
			messagebox.showinfo("Information", e)
		else:
			#print("Time to add records.", final_query)
			if okToUseTable:
				#print("\nfinal_query = ", final_query)
				#print("\n\t->calling now finalSaveToMySQL")
				# TEST:
				if skip_this_image == False:
					finalSaveToMySQL(final_query, **config)
				#else:
					#messagebox.showinfo("Information","Image is being skipped - not saved to DB.")
			else:
				messagebox.showinfo("Information","Sorry, can't create table.")
				#print("\nSorry - table failed so no record can be saved.")


	# ADDED IF SET CARRY ON IS NOT SELECTED, CLEAR CBs
	if setCarryOn is False: 
		#print("1849 - setCarryOn is false")
		messagebox.showinfo("Information","SET CARRY ON - clear.")
		click_meX()
		clearToTextInput()

# #######################################
#
#		   END END END 
# 
#####################################################################
def finalSaveToMySQL(final_query, **config):
	global text_widget
	print("\n"*4)
	#print("What  now? finalSaveToMySQL:")
	#messagebox.showinfo("Information","finalSaveToMySQL")
	#print("function: finalSaveToMySQL\n\tparams: final_query\n\t**config")
	#print("\tfinal_query = ", final_query,"\n\tglobal: text_widget")

	tempSearchOptions = list(searchOptions.state())
	tempSaveOptions = list(saveOptions.state())
	try:
		mydb = mysql.connector.connect(**config)
		mycursor = mydb.cursor()
		# THESE ARE THE DATA TO BE SAVED to TABLE
		mycursor.execute(final_query)
		mydb.commit()
	except Exception as e:
		messagebox.showinfo("Information", e)
	finally:
		mydb.close()
	#if str(mycursor.rowcount) > 0: 
	if mycursor.rowcount > 0:
		messagebox.showinfo("Information",str(mycursor.rowcount) + " record added.")
		#print("1831 - after record added test tempSaveOptions - set carry on: ",tempSaveOptions[SETCARRYON])
		#print("--wtf? check of tempSearchOptions: ")
		#print("0 = tempSaveOptions ", tempSaveOptions[0], " <> ", tempSaveOptions[SAVETODB])
		#print("1 = tempSaveOptions SAVETOFILE ", tempSaveOptions[1], " <> ", tempSaveOptions[SAVETOFILE])
		#print("2 = tempSaveOptions SETCARRYON ", tempSaveOptions[2], " <> ", tempSaveOptions[SETCARRYON])
		if tempSaveOptions[SETCARRYON] == 0:
			click_meX()
			#print("TESTING extract data")
			#print("TEXT WIDGET:global text_widget", text_widget)
			text_widget.delete("1.0","end")
			#extract_data()
			#clearToTextInput()
	else: 
		messagebox.showinfo("Information", "Sorry, the record could not be saved.")

# ____________________________________________________	
def quitScript():
	print("function: quitScript()")
	fullPathImageName = []
	imageList = []
	for i in range(0, len(listOfTagFiles)):
		fileToKill = os.path.realpath(listOfTagFiles[i])
		#print("fileToKill = ", fileToKill, " ", type(fileToKill))
		if os.path.exists(fileToKill):
			os.remove(fileToKill)
	sys.exit(0)
# ____________________________________________________

#optionsFrame = Frame(win, bg="white", width = pane_width)  # LEFT & RIGHT PANELS
# **** LEFT PANEL
optionsFrame = Frame(win, width = pane_width)
# **** RIGHT PANEL 
imageFrame = Frame(win, width = pane_width)

optionsFrame.pack_propagate(0)
imageFrame.pack_propagate(0)

# ********************************************************** 
#							LEFT SIDE: CONTROL BUTTONS 
#							and CHECKBOXES
# **********************************************************

tkvar = StringVar(win)
#imageList = ["Dropdox box for images in selected folder"]

# -------------------------- ROW 0, COL 0 -----------------------
row1Label = LabelFrame(optionsFrame, text = "Configure, Select Folder, Prev|Next")
row1Label.grid(row=0,column=0, padx= 12, pady = 12, sticky=N+W+E+S)
row1Label.pack(side=TOP, fill = BOTH, expand = FALSE)

# ************************** SCROLLING WINDOW ***********	
# Create the text widget
rowTextLabel = LabelFrame(optionsFrame, text = "Notes")
# MOVED OUTSIDE OF FUNCT
text_widget = Text(rowTextLabel, height=3, width = pane_width-100, wrap='word')
pt11 = tkFont.Font(family = "PT Sans Regular", size = 11)
text_widget.config(font = pt11)

# -------------------  BUTTONS & CONTROLS CONFIG BUTTON ------------
#KEEP!
configureButton = Button(row1Label, text=" 🧰 ", command = setupTEST)
configureButton.pack(side=LEFT)

selectFolderButton = Button(row1Label,  text=" 📂 ", command=loadDirectory)
selectFolderButton.pack(side=LEFT)
prevImageButton = Button(row1Label, text="\u25c0 ", command=lambda:update_image("prev"), state = DISABLED)
prevImageButton.pack(side=LEFT) 
nextImageButton = Button(row1Label,  text=" \u25b6", command=lambda:update_image("next"), state = DISABLED)
#button= ttk.Button(optionsFrame, text="Next Image",
#command=lambda:update_image("next"))
nextImageButton.pack(side=LEFT)

# * #* #*# * #* #* #* #* #* #* #* *# *# *# *# *# *# *# *# *# *# *# *# *# 
#ORIGINAL IS BELOW!  KEEP
#addRecordButton = Button(row1Label, text="Add Record",command=addNewRecord, state = DISABLED)
# ADD RECORD BUttoN
addRecordButton = Button(row1Label, text="Add Record",command=finalAddNewRecord, state = DISABLED)
addRecordButton.pack(side=LEFT, padx=5, pady=5)

# SEARCH BUTTON
searchButton = Button(row1Label, text="Search",command=searchRecords)
searchButton.pack(side=LEFT, padx=5, pady=5)

testButton = Button(row1Label, text="Stop Video") #,command=stopVideo)
#testButton.pack(side=LEFT, padx=5, pady=5)

# CLEAR CHECK BOXES BUTTON
clearCheckBoxes = Button(row1Label, text = "Clear", command=click_meX)
clearCheckBoxes.pack(side=LEFT)  # top, bottom, left, right

# QUIT BUTTON
quitButton = Button(row1Label, text="Quit",command=quitScript)
quitButton.pack(side=RIGHT)


# --------- ROW 1, COL 0   :: DROPDOWN BOX OF IMAGE OPTIONS   -------------
templateOptionsFont = tkFont.Font(family = "PT Sans Regular", size = font_size_to_use) # 10)
row2Label = LabelFrame(optionsFrame, text = "Optional Image File Name", width = pane_width-20)
row2Label.grid(row = 1, column=0 , sticky=N+E+W)
row2Label.config(font = templateOptionsFont)
row2Label.pack(side=TOP, fill = BOTH, expand = FALSE)

# TEST OF ADDING NAME BOX: 
#Label(row2Label,text="Name").pack(side=LEFT)
userImageNameEntry = Entry(row2Label, width="15")
userImageNameEntry.insert(0, 'Name')
userImageNameEntry.bind("<FocusIn>", lambda args: userImageNameEntry.delete('0','end'))
userImageNameEntry.config(font=templateOptionsFont,foreground='blue')
userImageNameEntry.pack(side=LEFT)

######  MOVED FROM 995 TEST -----
templateOptions = ["RWD", "RWD with notes", "Scrolly1", "Other"]
templateVariables = StringVar(optionsFrame)
templateVariables.set( templateOptions[0]) 
templateChoice = OptionMenu(row2Label, templateVariables, *templateOptions)
templateChoice.config(font = templateOptionsFont)
templateChoice.pack(side = RIGHT, fill = X)
###


# -------------- ROW 3 -------- USER CREATED TAGS --------- 
tagLabelFrame = LabelFrame(optionsFrame, text = "TAGS")
tagLabelFrame.grid(row=0,column=0, sticky=N+W+E+S)
tagLabelFrame.pack(side=TOP, fill = BOTH, expand = FALSE)
tagLabelFrame.pack_propagate(0)

### ADDED FOR DB ACCESS
saveOptionsList = ["Save to", "Save to RDBMS", "Save to Flat File", "Set Carry On", "Duplicate"]
saveOptions = Checkbar(optionsFrame, saveOptionsList)
saveOptions.pack(side = TOP, fill = X)


# TEMPLATE:
searchOptionsList = ["Search and Output Options", 'AND tags', 'OR tags', 'Search RDBMS', 'Index File', "HTML", "JSON", "VRA", "EAD"]
searchOptions = Checkbar(optionsFrame, searchOptionsList)
searchOptions.pack(side = TOP, fill = X)


# TEMPLATE FOR OUTPUT - just added June 5, 2022, 7:04 pm!
"""
templateOptions = ["RWD", "RWD with notes", "Scrolly1", "Other"]
templateVariables = StringVar(optionsFrame)
templateVariables.set( templateOptions[0]) 
templateChoice = OptionMenu(optionsFrame, templateVariables, *templateOptions)
templateChoice.pack(side = RIGHT, fill = X)
"""

def showCBOptions():
	global finalList 
	#global long_text
	global text_widget
	#print("function: showCBOptions()\n\treturns: CBList_x_Options")
	
	def clearToTextInput():
		#print("function: showCBOptions().clearToTextInput\n\treturns:")
		text_widget.delete("1.0","end")
		#btn=Button(optionsFrame,height=1,width=10, text="Clear",command=clearToTextInput)
		#btn.pack()
	
	#print("\n","-"*50,"\tshowCBOptions line 1664 and finalList ", finalList) 
	for cnt in range(0, len(filelister)):
		testoOptionsList = createListOfTags(filelister[cnt])	
		# a list of tags ... 
		testoOptions = Checkbar(optionsFrame, testoOptionsList)
		testoOptions.pack(side=TOP, fill = X)
		userTagsOptions.append(testoOptions)
		userTagsOptionsList.append(testoOptionsList)
		userTagsNames.append(userTagGroupHeadings[cnt])
		#print("1160 \t Adding testoOptions ", len(userTagsOptions))
	cnt = 3
	

	rowTextLabel.grid(row= (cnt+1), column=0, padx= 13, pady = 13, sticky=N+W+E+S)
	rowTextLabel.pack(side=TOP, fill = X, expand = FALSE)

	# data/buttons for this row:
	# MOVED OUTSIDE OF FUNCT
	#text_widget = Text(rowTextLabel, height=5, width = pane_width-22, wrap='word')
	largerFont16 = tkFont.Font(family = "SF Pro Rounded Light", size = 11)
	#text_widget.config(font = largerFont16)
	
	scroll_bar = tk.Scrollbar(rowTextLabel)
	scroll_bar.pack(side=RIGHT)
	text_widget.pack(side=LEFT)
	long_text = """Notes"""
	text_widget.insert(END, long_text)

	btn=Button(optionsFrame, height=1,width=10, text="Clear Notes",command=clearToTextInput)
	btn.config(font = largerFont16)
	btn.pack()
	
	return CBList_x_Options
# ******************************************************* ------------------------------------------
# ***			  IMAGE AREA 
# *******************************************************------------------------------------------
optionsFrame.grid(row = 0,column = 0, sticky="nsew")
#Create a canvas and add the image into it
# find the center point
canvas= Canvas(imageFrame, width=pane_width, height=screen_height)
canvas.pack(side=TOP, fill="both", expand=True)

video_label = Label(canvas)
video_label.pack()

# TEST OF VIDEO:  THIS WORKS but ... 
# move to option to control images versus videos appearing in the canvas ... 
#def showVideo():
#	video_label = Label(canvas)
#	video_label.pack()
#	player = tkvideo("testmovie.mp4", video_label, loop=1, size = (500,350))
#	player.play()


#rightFrame.pack()

#Define function to update the image
def update_image(direction):
	#print("function: update_image(direction)")
	#messagebox.showinfo("Information","update the goddamned fucking image! direction = "+direction)
	global currentImageNo
	global imageName
	global photoImageList
	global fullPathImageFileName
	global video_label
	
	skipOption(True)  # ADDED TO SKIP AUTO ADD TO RDBMS AND FLAT FILE - 
	#messagebox.showinfo("Information","Skipping this record.  ")

	video_extensions = [".mp4"]
	the_file_name, the_file_extension = os.path.splitext((fullPathImageFileName[currentImageNo]))

	# THIS can still screw up 'cause it'll cause image to be skipped ahead
	# 1 makingthings off ... 
	if direction == "next":
		currentImageNo += 1
		if currentImageNo == len(photoImageList):
			currentImageNo = 0
			#print("Resetting to top of the list.")
	elif direction == "jump":
		print("JUMPTO currentImageNo ", currentImageNo)
	else: # previous
		currentImageNo = currentImageNo - 1
		if currentImageNo < 0:
			currentImageNo = 0
			tkmb.showinfo(title='Info', message='Already at the start of the file list.')

	imageName = photoImageList[currentImageNo]
	
	
	#print("\n"*3,"checking images 2002: ")
	#print("currentImageNo = ", currentImageNo)
	#print("imageName from list = ", imageName,"\n-------------- 2004")

	# ************ 
	the_file_name, the_file_extension = os.path.splitext((fullPathImageFileName[currentImageNo]))
	#print("Line 2191: currentImageNo: ", currentImageNo, " name: ", the_file_name, " ext ", the_file_extension)
	
	if the_file_extension not in video_extensions:
		#video_label.destroy()
		video_label.pack_forget()
		#video_label.destroy()
		canvas.itemconfig(image_container, image = photoImageList[currentImageNo])
		# return the video_label just in case?
	else:
		# TRY THIS? canvas.itemconfig(image_container, image = "")
		# KEEP THESE TWO LINES, too.
		# ### video_label = Label(canvas)
		#print("line 2131 - video and canvas test")
		canvas.itemconfig(image_container, image = None)
		video_label.pack_forget()
		video_label = Label(canvas)
		# TEST video_label.pack()
		
		# testButton = Button(row1Label, text="Stop Video",command=stopVideo)
		#KEEP testButton.pack(side=LEFT, padx=5, pady=5)
		#KEEP testButton.bind('<Button-1>', lambda event: video_label.destroy())
		#### WORKS!  nextImageButton.bind('<Button-1>', lambda event: video_label.destroy())
		#video_label = Label(canvas)
		#video_label.pack()
		video_label.pack_forget()
		movieToShow = fullPathImageFileName[currentImageNo] # testmovie.mp4
		
		# RESIZE THE VIDEO TO FIT SCREEN
		#print("movie file name: ", movieToShow)

		# ORIGINAL KEEP:
		media_info = MediaInfo.parse(movieToShow)

		for track in media_info.tracks:
			#print("1882 - for track in media_info ... ")
			if track.track_type == 'Video':
				#print("1884 - TRACK.TRACK_TYPE = Video")
				#print ("Resolution {}x{}".format(track.width, track.height))	
				srcWidth = track.width
				srcHeight = track.height
				maxWidth = pane_width
				maxHeight = pane_height
			
				ratio = min(maxWidth / srcWidth, maxHeight / srcHeight)
				videoWidth = int(srcWidth * ratio)
				videoHeight = int(srcHeight * ratio)
				#print(videoWidth, " ", videoHeight)
				#print("NEW width x height = ", (int(srcWidth * ratio), int(srcHeight * ratio)))

				#print("2188 VIDEO:\t ", movieToShow)
				player = tkvideo(movieToShow, video_label, loop=1, size = (videoWidth,videoHeight))
		
		video_label.pack()
		player.play()
	

# determine ratio 
for j in range(0, len(imageList)):
	imageName = imageList[j]
	img = Image.open(imageName)   # TEST WTF?
	#print("1895 ### imageName = ", imageName)
	origHeight = img.size[1]
	origWidth = img.size[0]
	newHeight = 0
	newWidth = 0

	srcWidth = img.size[0]
	srcHeight = img.size[1]
	maxWidth = pane_width
	maxHeight = pane_width
	ratio = min(maxWidth / srcWidth, maxHeight / srcHeight)
	img = img.resize( (int(srcWidth * ratio),int(srcHeight * ratio)),Image.ANTIALIAS)
	#img = img.resize( (newWidth, newHeight), Image.ANTIALIAS)
	
	img = ImageTk.PhotoImage(img) 
	photoImageList.append(img)
	#print("RATIO 1196: ratio ",ratio, " w x h = ", int(srcWidth * ratio),"x",int(srcHeight * ratio))


# PRELOAD FOR TESTING - MAY REMOVE
img0= PhotoImage(file="card_catalog.png") # japanese_scene.png")


image_container = canvas.create_image(0,0, anchor=NW, image = img0) 

# RIGHT SIDE IS CALLED imageFrame
imageFrame.grid(row=0,column=1, sticky="nsew")
imageFrame.grid_rowconfigure(0, weight=1)
imageFrame.grid_columnconfigure(0, weight=1)

# ******************************************************* ------------------------------------------
# ***															  END   IMAGE AREA 
# *******************************************************-----------------------------

if __name__ == '__main__':
	print("__main__")
	win.rowconfigure(0, weight=1)
	win.columnconfigure(0, weight=1)
	win.columnconfigure(1, weight=1)

	win.mainloop()
