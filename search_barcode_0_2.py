#python virsion 3.7
#install these modules
import mysql.connector
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

#table name
table_name="barcode_info"

#database setting
def connect_db():
	try:
		mydb = mysql.connector.connect(
		host="localhost",
		port=3306,
		user="root",
		passwd="1234",
		database="SBtable"
		)
		mycursor = mydb.cursor()

		return mycursor,mydb
	except Exception as e:
		print(e)
		return False

def run_db(mycursor,mydb,sql):
	try:
		mycursor.execute(sql)
		mydb.commit()
		clear_entries()
		show_All()
		mydb.close()
		return True
	except Exception as e:
		messagebox.showerror("ERROR",str(e))
		print(e)
		return False


#if you want to check the log,
#delete '#' on the print(txt)
def chk_log(txt):
	#print(txt)
	pass


#this function is making query using <<combo_box's values>>
#it will be use at the SQL
def make_query(list_value,txt):
	where_query=''
	for v,e in zip(combo_box['values'],list_value):
		where_query+=(str(v)+ " = '" + str(e) +txt)
	
	where_query=where_query[:-(len(txt)-1)]
	return where_query


#show all data in table
def show_All():
	tree.delete(*tree.get_children())
	mycursor,mydb = connect_db()
	mycursor.execute("SELECT * FROM "+table_name)
	chk_log("All data -----")
	for row in mycursor:
		chk_log(row)
		tree.insert("",tk.END, values=row)
	mydb.close()

def chk_freezer_number():
	print(entries[1].get())
	return False if "F" in entries[1].get() or "R" in entries[1].get() else True

#insert new item into database
def add_item():
	result=messagebox.askquestion("ADD","are you sure?")
	if(result):

		chk=False
		for e in entries:
			if(e.get()==''):
				chk=True
		fchk=chk_freezer_number()
		print('fchk - ',fchk)
		chk= chk or fchk
		print('chk ',chk)
		if(chk):
			messagebox.showerror("INPUT ERROR","THERE IS BLANK OR CHECK FREEZER NUMBER")
		else:
			tmpquery=''
			for i in entries:
				tmpquery+="'"+i.get()+"',"
			mycursor,mydb=connect_db()
			sql="INSERT INTO "+table_name+" VALUES("+tmpquery[:-1]+")"
			chk_log("-> "+sql+" <-")
			db_report=run_db(mycursor,mydb,sql)
			if(db_report):
				messagebox.showinfo("SUCESS","DONE!")
			else:
				messagebox.showerror("ERROR","FAIL")
		
	else:
		pass

#edit data in table
def edit_item():
	curItem=tree.focus()
	currInd=tree.index(tree.focus())
	tmp=list(tree.item(curItem).values())[2]
	lst=[]
	for e in entries:
		lst.append(e.get())
	chk_log("insert value -----")
	chk_log(lst)
	result=messagebox.askquestion("EDIT","are you sure?")
	if(result):
		chk=False
		for e in entries:
			if(e.get()==''):
				chk=True
		if(chk):
			messagebox.showerror("INPUT ERROR","THERE ARE BLANK")
		else:
			chk_log('ok')
			mycursor,mydb=connect_db()
			where_query=make_query(tmp,"' and ")
			#chk_log(where_query)
			set_query=make_query(lst,"' , ")
			#chk_log(set_query)
			sql="UPDATE "+table_name +" SET "+set_query +" WHERE "+where_query
			chk_log("EDIT -> "+sql+" <-")
			db_report=run_db(mycursor,mydb,sql)
			if(db_report):
				messagebox.showinfo("SUCESS","DONE!")
			else:
				messagebox.showerror("ERROR","FAIL")
		
	else:
		pass


#delete data from table
def del_item():
	result=messagebox.askquestion("DELETE","are you sure?", icon='warning')
	if(result):
		curItem=tree.focus()
		tmp=list(tree.item(curItem).values())[2]

		mycursor,mydb=connect_db()
		where_query=make_query(tmp,"' and ")
		sql="DELETE FROM "+table_name+" WHERE "+where_query
		chk_log("-> "+sql+" <-")
		db_report=run_db(mycursor,mydb,sql)
		if(db_report):
			messagebox.showinfo("SUCESS","DONE!")
		else:
			messagebox.showerror("ERROR","FAIL")
		
	else:
		pass


#search data in table
def search_item():
	if search_txt.get() == '':
		show_All()
	else:
		tree.delete(*tree.get_children())
		mycursor,mydb=connect_db()
		chk_log("search ->"+search_txt.get())
		mycursor.execute("SELECT * FROM "+table_name +" WHERE "+combo_box.get()+" LIKE '%"+search_txt.get()+"%'")
		chk_log("----- search result -----")
		for row in mycursor:
			chk_log(row)
			tree.insert("",tk.END, values=row)

		mydb.close()


#clear text boxes on the left side
def clear_entries():
	for i in entries:
		i.delete(0,'end')


#event bind (double click)
def leftClick(event):
	
	curItem = tree.focus()
	currInd = tree.index(tree.focus())
	tmp=list(tree.item(curItem).values())[2]
	clear_entries()


#these for test
	print('1', list(tree.item(curItem).values())[1])
	print('2', list(tree.item(curItem).values())[2])
	print('3', list(tree.item(curItem).values())[3])

	for i in range(0,len(combo_box['values'])):
		entries[i].insert(0,str(tmp[i])) 
	return True


def EnterClick(event):
	search_item()



#codes under here are all for GUI
############################### G U I - S T A R T ###############################

root = tk.Tk()
L_FONT=('Futura',9, 'bold')
B_FONT=('Futura', 10, 'bold')

height= 350
width=1230

#frame and application set
root.title('SEARCH SAMPLE LOCATION')
root.geometry(str(width)+'x'+str(height))
frame_top=tk.Frame(root,height=80,width=width)
frame_top.pack(side='top',fill='both')
frame_left=tk.Frame(root,height=height,width=width/2+120)
frame_left.pack(side='left',fill='y')
frame_right=tk.Frame(root,height=height, width=width/2-120)
frame_right.pack(side='right',fill='y')

############################### W I D G E T S ###############################
#treeView setting
tree= ttk.Treeview(frame_left, column=("SAMPLE BARCODE NUMBER", "FREEZE NUMBER","BOX NUMBER", "RACK NUMBER", "WELL NUMBER"), show='headings')
tree.heading("#1", text="SAMPLE BARCODE NUMBER")
tree.heading("#2", text="FREEZE NUMBER")
tree.heading("#3", text="BOX NUMBER")
tree.heading("#4", text="RACK NUMBER")
tree.heading("#5", text="WELL NUMBER")

#tree with scrollbar 
#tree bind with event(doubleclick)
vsb = ttk.Scrollbar(frame_left, orient="vertical")
vsb.configure(command=tree.yview)
tree.configure(yscrollcommand=vsb.set)
tree.bind("<ButtonRelease-1>", leftClick)

#widgets in the frame_top 
logo=tk.PhotoImage(file='logo.png')
title= tk.Label(frame_top,image=logo ,font=L_FONT)
search_txt=tk.Entry(frame_top, width='35')
search_btn=tk.Button(frame_top, text="FIND", font= B_FONT, command=search_item)
root.bind("<Return>", EnterClick)
combo_box = ttk.Combobox(frame_top, font=B_FONT,width=22)

#this is important bc I use this values when i make SQL in this application
combo_box['values']=["sample_barcode_number","freezer_number", "rack_number", "box_number","well_number"]
#set default value
combo_box.set(combo_box['values'][0])


#widgets in frame_right
add_btn=tk.Button(frame_right, text="ADD", font= B_FONT, command=add_item)
edit_btn=tk.Button(frame_right, text="EDIT", font= B_FONT, command=edit_item)
del_btn=tk.Button(frame_right, text="DELETE", font= B_FONT, command=del_item)

#these are entries when we want to chage,insert,delete data from the table
entries=[]
for i in range(0,len(combo_box['values'])):
	entries.append(tk.Entry(frame_right))



############################### P A C K I N G ###############################
 #pack at frame_top
title.pack(side='left',padx="15",pady="8")
combo_box.pack(side="left", padx="5")
search_txt.pack(side="left",padx="5")
search_btn.pack(side="left",padx="5")

#pack at frame_left
tree.pack(fill='both',side="left",padx="5",pady="5")
vsb.pack(side='right',fill='y')

#pack at frame_right
for i in range(0,len(combo_box['values'])):
	tk.Label(frame_right, text=combo_box['values'][i]).pack(fill='x',pady="5")
	entries[i].pack(fill='x')

add_btn.pack(side="left",fill='x')
edit_btn.pack(side="left",fill='x')
del_btn.pack(side="left",fill='x')



#open application
show_All()
root.mainloop()
