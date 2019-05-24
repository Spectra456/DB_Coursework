from tkinter import *
from tkinter import ttk
import cx_Oracle
import os
os.environ["NLS_LANG"] = "RUSSIAN_RUSSIA.AL32UTF8"

def button_clicked():
    try:
        ip = 'localhost'
        port = 32118
        SID = 'XE'
        dsn_tns = cx_Oracle.makedsn(ip, port, SID)
        db = cx_Oracle.connect(textLogin.get(), textPassword.get(), dsn_tns)
        root.withdraw()
        libraryWin.update()
        libraryWin.deiconify()
        db.close()
    except:
        labelError.config(text='Wrong login or password')



def selectItem(a):
    global selected_tuple
    curItem = listBox.focus()
    selected_tuple = listBox.item(curItem).get('values')
    print(selected_tuple)
    e1.delete(0, END)
    e1.insert(END, selected_tuple[1])
    e2.delete(0, END)
    e2.insert(END, selected_tuple[2])
    e3.delete(0, END)
    e3.insert(END, selected_tuple[3])
    e4.delete(0, END)
    e4.insert(END, selected_tuple[4])
    e5.delete(0, END)
    e5.insert(END, selected_tuple[5])

def show():
    listBox.delete(*listBox.get_children())
    ip = 'localhost'
    port = 32118
    SID = 'XE'
    dsn_tns = cx_Oracle.makedsn(ip, port, SID)
    db = cx_Oracle.connect('spectra', '12345', dsn_tns)
    cursor = db.cursor()

    cursor.execute('SELECT * FROM clients')

    tempList = cursor.fetchall()

    for (id, name, last, father, serial, num) in tempList:
        listBox.insert("", "end", values=(id, name, last, father, serial, num))
    db.close()


def update_command():
    ip = 'localhost'
    port = 32118
    SID = 'XE'
    dsn_tns = cx_Oracle.makedsn(ip, port, SID)
    db = cx_Oracle.connect('spectra', '12345', dsn_tns)
    cursor = db.cursor()

    sql = """UPDATE clients SET first_name= :first, last_name= :second, father_name= :third, passport_serial= :fourth, passport_num= :fifty WHERE id= trunc(:sixty)"""
    print(cursor.execute(sql, {'first': str(name_text.get()), 'second': str(last_text.get()),
                               'third': str(father_text.get()), 'fourth': str(serial_text.get()),
                               'fifty': str(num_text.get()), 'sixty': int(selected_tuple[0])}))
    db.commit()
    listBox.delete(*listBox.get_children())
    cursor.execute('SELECT * FROM clients')

    tempList = cursor.fetchall()

    for (id, name, last, father, serial, num) in tempList:
        listBox.insert("", "end", values=(id, name, last, father, serial, num))
    db.close()


def insert_command():
    ip = 'localhost'
    port = 32118
    SID = 'XE'
    dsn_tns = cx_Oracle.makedsn(ip, port, SID)
    db = cx_Oracle.connect('spectra', '12345', dsn_tns)
    cursor = db.cursor()

    sql = """INSERT INTO CLIENTS (FIRST_NAME, LAST_NAME, FATHER_NAME, PASSPORT_SERIAL, PASSPORT_NUM) VALUES
     ( :first, :second, :third, :fourth, :fifty)"""
    print(cursor.execute(sql, {'first': str(name_text.get()), 'second': str(last_text.get()),
                               'third': str(father_text.get()), 'fourth': str(serial_text.get()),
                               'fifty': str(num_text.get())}))
    db.commit()
    listBox.delete(*listBox.get_children())
    cursor.execute('SELECT * FROM clients')

    tempList = cursor.fetchall()

    for (id, name, last, father, serial, num) in tempList:
        listBox.insert("", "end", values=(id, name, last, father, serial, num))
    db.close()


def delete_command():
    ip = 'localhost'
    port = 32118
    SID = 'XE'
    dsn_tns = cx_Oracle.makedsn(ip, port, SID)
    db = cx_Oracle.connect('spectra', '12345', dsn_tns)
    cursor = db.cursor()

    sql = """DELETE FROM clients WHERE id= trunc(:sixty)"""
    print(cursor.execute(sql, {'sixty': int(selected_tuple[0])}))
    db.commit()
    listBox.delete(*listBox.get_children())
    cursor.execute('SELECT * FROM clients')

    tempList = cursor.fetchall()

    for (id, name, last, father, serial, num) in tempList:
        listBox.insert("", "end", values=(id, name, last, father, serial, num))
    db.close()


# --- LOGIN ------
root1 = Tk()
root1.withdraw()
root = Toplevel(root1)
libraryWin = Toplevel(root)
libraryWin.withdraw()
style = ttk.Style(root)
style.configure('listBoxType.Treeview', rowheight=41)

style1 = ttk.Style(root)
style1.configure('listBox.Treeview', rowheight=15)

libraryWin.geometry('900x500')
libraryWin.resizable(False, False)
root.geometry('200x300+500+200')
root.resizable(False, False)

root["bg"] = "white"
root.title('Login')

button = Button(root, text=u"Login", command=button_clicked,bg="white")
button.pack()
textLogin = Entry(root, bg="white")
textLogin.pack()
textPassword = Entry(root, bg="white",show="*")
textPassword.pack()
label1 = Label(root,text="Login", fg="black", bg="white")
label1.pack()
label2 = Label(root,text="Password", fg="black", bg="white")
label2.pack()
labelError = Label(root,text="", fg="red", bg="white")
labelError.pack()
label1.place(y=75,x=5)
textLogin.place(y=100, x=4)
textPassword.place(y=150, x=4)
label2.place(y=127,x=5)
labelError.place(y=250, x=20)
button.place(x=40, y = 200)
button.config(height=1, width=10)
# ----------- Clients ------------


tabControl = ttk.Notebook(libraryWin)
tab1 = ttk.Frame(tabControl)
tab2 = ttk.Frame(tabControl)
tab3 = ttk.Frame(tabControl)
tab4 = ttk.Frame(tabControl)
tab5 = ttk.Frame(tabControl)



tabControl.add(tab1, text='Clients')
tabControl.add(tab2, text='Books')
tabControl.add(tab3, text='Books type')
tabControl.add(tab4, text='Journal')
tabControl.add(tab5, text='Features')


tabControl.pack(expand=1, fill="both")

cols = ('ID', 'First name', 'Last name', 'Father Name', 'Passport serial', 'Passport num')
width = (40,160,165,165,165,165)
listBox = ttk.Treeview(tab1, columns=cols, show='headings')
listBox.pack()

# set column headings
for i, col in enumerate(cols):
    listBox.column(col,width=width[i],stretch=0, anchor=CENTER)
    listBox.heading(col, text=col)
    listBox.grid(row=1, column=0)



listBox.bind('<<TreeviewSelect>>', selectItem)

l1 = Label(tab1, text="Name", bg='gray91')
l1.grid()
l1.place(x=0, y=220)

name_text = StringVar()
e1 = Entry(tab1, textvariable=name_text,highlightbackground ='gray91')
e1.grid()
e1.place(x=0, y=240)

l2 = Label(tab1, text="Last name", bg='gray91')
l2.grid()
l2.place(x=200, y=220)

last_text = StringVar()
e2 = Entry(tab1, textvariable=last_text,highlightbackground ='gray91')
e2.grid()
e2.place(x=200, y=240)

l3 = Label(tab1, text="Father name", bg='gray91')
l3.grid()
l3.place(x=400, y=220)

father_text = StringVar()
e3 = Entry(tab1, textvariable=father_text,highlightbackground ='gray91')
e3.grid()
e3.place(x=400, y=240)

l4 = Label(tab1, text="Passport serial", bg='gray91')
l4.grid()
l4.place(x=0, y=270)

serial_text = StringVar()
e4 = Entry(tab1, textvariable=serial_text,highlightbackground ='gray91')
e4.grid()
e4.place(x=0, y=290)

l5 = Label(tab1, text="Passport num", bg='gray91')
l5.grid()
l5.place(x=200, y=270)

num_text = StringVar()
e5 = Entry(tab1, textvariable=num_text,highlightbackground ='gray91')
e5.grid()
e5.place(x=200, y=290)


showbutton = Button(tab1, text="Show", command=show,highlightbackground ='gray91')
showbutton.pack()
showbutton.place(x=600, y = 390)
showbutton.config(height=1, width=18)

update = Button(tab1, text="Update", width=15, command=update_command,highlightbackground ='gray91')
update.pack()
update.place(x=600, y = 240)
update.config(height=1, width=18)

delete = Button(tab1, text="Delete", width=15, command=delete_command,highlightbackground ='gray91')
delete.pack()
delete.place(x=600, y = 290)
delete.config(height=1, width=18)

insert = Button(tab1, text="Insert", width=15, command=insert_command,highlightbackground ='gray91')
insert.pack()
insert.place(x=600, y = 340)
insert.config(height=1, width=18)

# BOOKS

def selectItemBooks(a):
    global selected_tupleBooks
    curItem = listBoxBooks.focus()
    selected_tupleBooks = listBoxBooks.item(curItem).get('values')
    print(selected_tupleBooks)
    e1Books.delete(0, END)
    e1Books.insert(END, selected_tupleBooks[1])
    e2Books.delete(0, END)
    e2Books.insert(END, selected_tupleBooks[2])
    e3Books.delete(0, END)
    e3Books.insert(END, selected_tupleBooks[3])

def showBooks():
    listBoxBooks.delete(*listBoxBooks.get_children())
    ip = 'localhost'
    port = 32118
    SID = 'XE'
    dsn_tns = cx_Oracle.makedsn(ip, port, SID)
    db = cx_Oracle.connect('spectra', '12345', dsn_tns)
    cursor = db.cursor()

    cursor.execute('SELECT * FROM Books')

    tempList = cursor.fetchall()

    for (id, name, count, type) in tempList:
        listBoxBooks.insert("", "end", values=(id, name, count, type))
    db.close()

def update_commandBooks():
    ip = 'localhost'
    port = 32118
    SID = 'XE'
    dsn_tns = cx_Oracle.makedsn(ip, port, SID)
    db = cx_Oracle.connect('spectra', '12345', dsn_tns)
    cursor = db.cursor()
    print(typeBooks_text.get().rsplit(' ', 1)[0])
    sql = """UPDATE books SET name= :first, cnt= trunc(:second), type_id= trunc(:third) WHERE id= trunc(:fourth)"""
    print(cursor.execute(sql, {'first': str(name_textBooks.get()), 'second': int(cnt_text.get()),
                               'third': int(typeBooks_text.get().rsplit(' ', 1)[0]), 'fourth': int(selected_tupleBooks[0])}))
    db.commit()
    listBoxBooks.delete(*listBoxBooks.get_children())
    cursor.execute('SELECT * FROM books')

    tempList = cursor.fetchall()

    for (id, name, cnt, type) in tempList:
        listBoxBooks.insert("", "end", values=(id, name, cnt, type))
    db.close()

def delete_commandBooks():
    ip = 'localhost'
    port = 32118
    SID = 'XE'
    dsn_tns = cx_Oracle.makedsn(ip, port, SID)
    db = cx_Oracle.connect('spectra', '12345', dsn_tns)
    cursor = db.cursor()

    sql = """DELETE FROM books WHERE id= trunc(:sixty)"""
    print(cursor.execute(sql, {'sixty': int(selected_tupleBooks[0])}))
    db.commit()
    listBoxBooks.delete(*listBoxBooks.get_children())
    cursor.execute('SELECT * FROM books')

    tempList = cursor.fetchall()

    for (id, name, count, type) in tempList:
        listBoxBooks.insert("", "end", values=(id, name, count, type))
    db.close()

def insert_commandBooks():
    ip = 'localhost'
    port = 32118
    SID = 'XE'
    dsn_tns = cx_Oracle.makedsn(ip, port, SID)
    db = cx_Oracle.connect('spectra', '12345', dsn_tns)
    cursor = db.cursor()

    sql = """INSERT INTO books (NAME, CNT, TYPE_ID) VALUES
     ( :first, trunc(:second), trunc(:third))"""
    print(cursor.execute(sql, {'first': str(name_textBooks.get()), 'second': int(cnt_text.get()),
                               'third': int(typeBooks_text.get().rsplit(' ', 1)[0])}))
    db.commit()
    listBoxBooks.delete(*listBoxBooks.get_children())
    cursor.execute('SELECT * FROM books')

    tempList = cursor.fetchall()

    for (id, name, cnt, type) in tempList:
        listBoxBooks.insert("", "end", values=(id, name, cnt, type))
    db.close()


def typelist():
    ip = 'localhost'
    port = 32118
    SID = 'XE'
    dsn_tns = cx_Oracle.makedsn(ip, port, SID)
    db = cx_Oracle.connect('spectra', '12345', dsn_tns)
    cursor = db.cursor()

    cursor.execute('SELECT DISTINCT id, name FROM book_types')

    tempList = cursor.fetchall()

    e3Books['values'] = tempList

colsBooks = ('ID', 'Name', 'Count', 'Type')
widthBooks = (40,200,200,200)
listBoxBooks = ttk.Treeview(tab2, columns=colsBooks, show='headings', style = 'listBoxType.Treeview')
listBoxBooks.pack()

# set column headings
for i, col in enumerate(colsBooks):
    listBoxBooks.column(col,width=widthBooks[i],stretch=0, anchor=CENTER)
    listBoxBooks.heading(col, text=col)
    listBoxBooks.grid(row=1, column=0)


listBoxBooks.bind('<<TreeviewSelect>>', selectItemBooks)

l1Books = Label(tab2, text="Name", bg='gray91')
l1Books.grid()
l1Books.place(x=645, y=0)

name_textBooks = StringVar()
e1Books = Entry(tab2, textvariable=name_textBooks,highlightbackground ='gray91')
e1Books.grid()
e1Books.place(x=645, y=20)

l2Books = Label(tab2, text="Count", bg='gray91')
l2Books.grid()
l2Books.place(x=645, y=60)

cnt_text = StringVar()
e2Books = Entry(tab2, textvariable=cnt_text,highlightbackground ='gray91')
e2Books.grid()
e2Books.place(x=645, y=80)

l3Books = Label(tab2, text="Type of book", bg='gray91')
l3Books.grid()
l3Books.place(x=645, y=120)


typeBooks_text = StringVar()
e3Books = ttk.Combobox(tab2, textvariable=typeBooks_text, postcommand =typelist)
e3Books.grid()
e3Books.config(height=5, width=19)
e3Books.place(x=645, y=140)

showbuttonBooks = Button(tab2, text="Show", width=15, command=showBooks,highlightbackground ='gray91')
showbuttonBooks.pack()
showbuttonBooks.place(x=645, y = 190)
showbuttonBooks.config(height=1, width=18)

updateBooks = Button(tab2, text="Update", width=15, command=update_commandBooks,highlightbackground ='gray91')
updateBooks.pack()
updateBooks.place(x=645, y = 240)
updateBooks.config(height=1, width=18)

deleteBooks = Button(tab2, text="Delete", width=15, command=delete_commandBooks,highlightbackground ='gray91')
deleteBooks.pack()
deleteBooks.place(x=645, y = 290)
deleteBooks.config(height=1, width=18)

insertBooks = Button(tab2, text="Insert", width=15, command=insert_commandBooks, highlightbackground ='gray91')
insertBooks.pack()
insertBooks.place(x=645, y = 340)
insertBooks.config(height=1, width=18)

# BOOKS TYPE

def selectItemType(a):
    global selected_tupleType
    curItem = listBoxType.focus()
    selected_tupleType = listBoxType.item(curItem).get('values')
    print(selected_tupleType)
    e1Type.delete(0, END)
    e1Type.insert(END, selected_tupleType[1])
    e2Type.delete(0, END)
    e2Type.insert(END, selected_tupleType[2])
    e3Type.delete(0, END)
    e3Type.insert(END, selected_tupleType[3])
    e4Type.delete(0, END)
    e4Type.insert(END, selected_tupleType[4])

def showType():
    listBoxType.delete(*listBoxType.get_children())
    ip = 'localhost'
    port = 32118
    SID = 'XE'
    dsn_tns = cx_Oracle.makedsn(ip, port, SID)
    db = cx_Oracle.connect('spectra', '12345', dsn_tns)
    cursor = db.cursor()

    cursor.execute('SELECT * FROM book_types')

    tempList = cursor.fetchall()

    for (id, name, count, fine, days) in tempList:
        listBoxType.insert("", "end", values=(id, name, count, fine, days))
    db.close()

def update_commandType():
    ip = 'localhost'
    port = 32118
    SID = 'XE'
    dsn_tns = cx_Oracle.makedsn(ip, port, SID)
    db = cx_Oracle.connect('spectra', '12345', dsn_tns)
    cursor = db.cursor()

    sql = """UPDATE book_types SET name= :first, cnt= trunc(:second), fine= trunc(:third), day_count= trunc(:fifth)  WHERE id= trunc(:fourth)"""
    print(cursor.execute(sql, {'first': str(name_textType.get()), 'second': int(cntType.get()),
                               'third': int(fine_Type.get()), 'fourth': int(selected_tupleType[0]),
                               'fifth': int(dayCount_Type.get())}))
    db.commit()
    listBoxType.delete(*listBoxType.get_children())
    cursor.execute('SELECT * FROM book_types')

    tempList = cursor.fetchall()

    for (id, name, count, fine, days) in tempList:
        listBoxType.insert("", "end", values=(id, name, count, fine, days))
    db.close()

def delete_commandType():
    ip = 'localhost'
    port = 32118
    SID = 'XE'
    dsn_tns = cx_Oracle.makedsn(ip, port, SID)
    db = cx_Oracle.connect('spectra', '12345', dsn_tns)
    cursor = db.cursor()

    sql = """DELETE FROM book_types WHERE id= trunc(:sixty)"""
    print(cursor.execute(sql, {'sixty': int(selected_tupleType[0])}))
    db.commit()
    listBoxType.delete(*listBoxType.get_children())
    cursor.execute('SELECT * FROM book_types')

    tempList = cursor.fetchall()

    for (id, name, count, fine, days) in tempList:
        listBoxType.insert("", "end", values=(id, name, count, fine, days))
    db.close()

def insert_commandType():
    ip = 'localhost'
    port = 32118
    SID = 'XE'
    dsn_tns = cx_Oracle.makedsn(ip, port, SID)
    db = cx_Oracle.connect('spectra', '12345', dsn_tns)
    cursor = db.cursor()

    sql = """INSERT INTO book_types (NAME, CNT, FINE, DAY_COUNT) VALUES
     ( :first, trunc(:second), trunc(:third), trunc(:fourth))"""
    print(cursor.execute(sql, {'first': str(name_textType.get()), 'second': int(cntType.get()),
                               'third': int(fine_Type.get()),'fourth': int(dayCount_Type.get())}))
    db.commit()
    listBoxType.delete(*listBoxType.get_children())
    cursor.execute('SELECT * FROM book_types')

    tempList = cursor.fetchall()

    for (id, name, count, fine, days) in tempList:
        listBoxType.insert("", "end", values=(id, name, count, fine, days))
    db.close()

colsType = ('ID', 'Name', 'Count', 'Fine', 'Days')
widthType = (40,400,65,65,65)
listBoxType = ttk.Treeview(tab3, columns=colsType, show='headings', style = 'listBoxType.Treeview')
listBoxType.pack()

# set column headings
for i, col in enumerate(colsType):
    listBoxType.column(col,width=widthType[i],stretch=0, anchor=CENTER)
    listBoxType.heading(col, text=col)
    listBoxType.grid(row=1, column=0)


listBoxType.bind('<<TreeviewSelect>>', selectItemType)

l1Type = Label(tab3, text="Name", bg='gray91')
l1Type.grid()
l1Type.place(x=645, y=0)

name_textType = StringVar()
e1Type = Entry(tab3, textvariable=name_textType,highlightbackground ='gray91')
e1Type.grid()
e1Type.place(x=645, y=20)

l2Type = Label(tab3, text="Count", bg='gray91')
l2Type.grid()
l2Type.place(x=645, y=60)

cntType = StringVar()
e2Type = Entry(tab3, textvariable=cntType,highlightbackground ='gray91')
e2Type.grid()
e2Type.place(x=645, y=80)

l3Type = Label(tab3, text="Fine", bg='gray91')
l3Type.grid()
l3Type.place(x=645, y=120)

fine_Type = StringVar()
e3Type = Entry(tab3, textvariable=fine_Type,highlightbackground ='gray91')
e3Type.grid()
e3Type.place(x=645, y=140)

l4Type = Label(tab3, text="Days", bg='gray91')
l4Type.grid()
l4Type.place(x=645, y=180)

dayCount_Type = StringVar()
e4Type = Entry(tab3, textvariable=dayCount_Type,highlightbackground ='gray91')
e4Type.grid()
e4Type.place(x=645, y=200)

showbuttonType = Button(tab3, text="Show", width=15, command=showType,highlightbackground ='gray91')
showbuttonType.pack()
showbuttonType.place(x=645, y = 270)
showbuttonType.config(height=1, width=18)

updateType = Button(tab3, text="Update", width=15, command=update_commandType,highlightbackground ='gray91')
updateType.pack()
updateType.place(x=645, y = 310)
updateType.config(height=1, width=18)

deleteType = Button(tab3, text="Delete", width=15, command=delete_commandType,highlightbackground ='gray91')
deleteType.pack()
deleteType.place(x=645, y = 350)
deleteType.config(height=1, width=18)

insertType = Button(tab3, text="Insert", width=15, command=insert_commandType, highlightbackground ='gray91')
insertType.pack()
insertType.place(x=645, y = 390)
insertType.config(height=1, width=18)

# JOURNAL

def bookList():

    ip = 'localhost'
    port = 32118
    SID = 'XE'
    dsn_tns = cx_Oracle.makedsn(ip, port, SID)
    db = cx_Oracle.connect('spectra', '12345', dsn_tns)
    cursor = db.cursor()

    cursor.execute('SELECT DISTINCT id,name FROM Books')

    tempList = cursor.fetchall()

    e1Journal['values'] = tempList

def clientList():

    ip = 'localhost'
    port = 32118
    SID = 'XE'
    dsn_tns = cx_Oracle.makedsn(ip, port, SID)
    db = cx_Oracle.connect('spectra', '12345', dsn_tns)
    cursor = db.cursor()

    cursor.execute('SELECT DISTINCT id, first_name, last_name, father_name FROM clients')

    tempList = cursor.fetchall()

    e2Journal['values'] = tempList
    e1Features['values'] = tempList
def selectItemJournal(a):
    global selected_tupleJournal
    curItem = listBoxJournal.focus()
    selected_tupleJournal = listBoxJournal.item(curItem).get('values')
    print(selected_tupleJournal)
    e1Journal.delete(0, END)
    e1Journal.insert(END, selected_tupleJournal[1])
    e2Journal.delete(0, END)
    e2Journal.insert(END, selected_tupleJournal[2])
    e4Journal.delete(0, END)
    e4Journal.insert(END, selected_tupleJournal[5])


def showJournal():
    listBoxJournal.delete(*listBoxJournal.get_children())
    ip = 'localhost'
    port = 32118
    SID = 'XE'
    dsn_tns = cx_Oracle.makedsn(ip, port, SID)
    db = cx_Oracle.connect('spectra', '12345', dsn_tns)
    cursor = db.cursor()

    cursor.execute('SELECT * FROM journal')

    tempList = cursor.fetchall()

    for (id, book_id, client_id, date_beg,date_end, date_ret) in tempList:
        listBoxJournal.insert("", "end", values=(id, book_id, client_id, date_beg,date_end, date_ret))
    db.close()

def update_commandJournal():
    ip = 'localhost'
    port = 32118
    SID = 'XE'
    dsn_tns = cx_Oracle.makedsn(ip, port, SID)
    db = cx_Oracle.connect('spectra', '12345', dsn_tns)
    cursor = db.cursor()
    sql = """UPDATE journal SET book_id= trunc(:first), client_id= trunc(:second), date_ret= to_date(:third, 'yyyy-mm-dd hh24:mi:ss')  WHERE id= trunc(:fourth)"""
    print(cursor.execute(sql, {'first': int(bookJournal.get().rsplit(' ', 1)[0]), 'second': int(clientJournal.get().rsplit(' ', 3)[0]),
                               'third': str(dateRetJournal.get()), 'fourth': int(selected_tupleJournal[0]),
                               }))
    db.commit()
    listBoxJournal.delete(*listBoxJournal.get_children())
    cursor.execute('SELECT * FROM journal')

    tempList = cursor.fetchall()

    for (id, book_id, client_id, date_beg,date_end, date_ret) in tempList:
        listBoxJournal.insert("", "end", values=(id, book_id, client_id, date_beg,date_end, date_ret))
    db.close()

def delete_commandJournal():
    ip = 'localhost'
    port = 32118
    SID = 'XE'
    dsn_tns = cx_Oracle.makedsn(ip, port, SID)
    db = cx_Oracle.connect('spectra', '12345', dsn_tns)
    cursor = db.cursor()

    sql = """DELETE FROM journal WHERE id= trunc(:sixty)"""
    print(cursor.execute(sql, {'sixty': int(selected_tupleJournal[0])}))
    db.commit()
    listBoxJournal.delete(*listBoxJournal.get_children())
    cursor.execute('SELECT * FROM journal')

    tempList = cursor.fetchall()

    for (id, book_id, client_id, date_beg,date_end, date_ret) in tempList:
        listBoxJournal.insert("", "end", values=(id, book_id, client_id, date_beg,date_end, date_ret))
    db.close()

def insert_commandJournal():
    ip = 'localhost'
    port = 32118
    SID = 'XE'
    dsn_tns = cx_Oracle.makedsn(ip, port, SID)
    db = cx_Oracle.connect('spectra', '12345', dsn_tns)
    cursor = db.cursor()

    sql = """INSERT INTO JOURNAL (BOOK_ID, CLIENT_ID, DATE_BEG, DATE_END, DATE_RET) VALUES
    (trunc(:first), trunc(:second), SYSDATE ,SYSDATE + (SELECT day_count FROM book_types
    JOIN Books ON books.type_id = book_types.id
    WHERE Books.id = 1) , to_date(:third, 'yyyy-mm-dd hh24:mi:ss'))"""

    print(cursor.execute(sql, {'first': int(bookJournal.get().rsplit(' ', 1)[0]), 'second': int(clientJournal.get().rsplit(' ', 3)[0]),
                               'third': dateRetJournal.get()}))
    db.commit()
    listBoxJournal.delete(*listBoxJournal.get_children())
    cursor.execute('SELECT * FROM journal')

    tempList = cursor.fetchall()

    for (id, book_id, client_id, date_beg, date_end, date_ret) in tempList:
        listBoxJournal.insert("", "end", values=(id, book_id, client_id, date_beg, date_end, date_ret))
    db.close()


colsJournal = ('ID', 'Book ID', 'Client ID', 'Begin date', 'End date', 'Return date')
widthJournal = (40,80,80,150,150,150)
listBoxJournal = ttk.Treeview(tab4, columns=colsJournal, show='headings', style = 'listBoxType.Treeview')
listBoxJournal.pack()

# set column headings
for i, col in enumerate(colsJournal):
    listBoxJournal.column(col,width=widthJournal[i],stretch=0, anchor=CENTER)
    listBoxJournal.heading(col, text=col)
    listBoxJournal.grid(row=1, column=0)

listBoxJournal.bind('<<TreeviewSelect>>', selectItemJournal)

l1Journal = Label(tab4, text="Book", bg='gray91')
l1Journal.grid()
l1Journal.place(x=655, y=0)

bookJournal = StringVar()
e1Journal = ttk.Combobox(tab4, textvariable=bookJournal, postcommand =bookList)
e1Journal.grid()
e1Journal.config(height=5, width=19)
e1Journal.place(x=655, y=20)

l2Journal = Label(tab4, text="Client", bg='gray91')
l2Journal.grid()
l2Journal.place(x=655, y=50)

clientJournal = StringVar()
e2Journal = ttk.Combobox(tab4, textvariable=clientJournal, postcommand =clientList)
e2Journal.grid()
e2Journal.config(height=5, width=19)
e2Journal.place(x=655, y=70)

l4Journal = Label(tab4, text="Return date", bg='gray91')
l4Journal.grid()
l4Journal.place(x=655, y=100)

dateRetJournal = StringVar()
e4Journal = Entry(tab4, textvariable=dateRetJournal,highlightbackground ='gray91')
e4Journal.grid()
e4Journal.place(x=655, y=120)

showbuttonJournal = Button(tab4, text="Show", width=15, command=showJournal,highlightbackground ='gray91')
showbuttonJournal.pack()
showbuttonJournal.place(x=655, y = 270)
showbuttonJournal.config(height=1, width=18)

updateJournal = Button(tab4, text="Update", width=15, command=update_commandJournal,highlightbackground ='gray91')
updateJournal.pack()
updateJournal.place(x=655, y = 310)
updateJournal.config(height=1, width=18)

deleteJournal = Button(tab4, text="Delete", width=15, command=delete_commandJournal,highlightbackground ='gray91')
deleteJournal.pack()
deleteJournal.place(x=655, y = 350)
deleteJournal.config(height=1, width=18)

insertJournal = Button(tab4, text="Insert", width=15, command=insert_commandJournal, highlightbackground ='gray91')
insertJournal.pack()
insertJournal.place(x=655, y = 390)
insertJournal.config(height=1, width=18)

# FEATURES

def booksCount(event):

    ip = 'localhost'
    port = 32118
    SID = 'XE'
    dsn_tns = cx_Oracle.makedsn(ip, port, SID)
    db = cx_Oracle.connect('spectra', '12345', dsn_tns)
    cursor = db.cursor()

    sql = """SELECT COUNT(*) FROM clients
                    JOIN journal ON journal.client_id = clients.id
                    WHERE clients.id = trunc(:first) AND journal.date_ret IS NULL"""
    cursor.execute(sql, {'first': int(clientFeatures.get().rsplit(' ', 3)[0])})

    temp = cursor.fetchall()
    cntBook.config(text=str('Amount of books: ') + str(temp[0][0]))
#####
    sql = """SELECT SUM(fine*(-EXTRACT(day FROM (date_end - date_ret)))) from journal
             JOIN book_types ON journal.book_id = book_types.id
             AND (EXTRACT(day FROM (date_end - date_ret)) < 0) AND client_id = trunc(:first)"""
    cursor.execute(sql, {'first': int(clientFeatures.get().rsplit(' ', 3)[0])})

    temp = cursor.fetchall()
    fineClient.config(text=str('Fine: ') + str(temp[0][0]))

    pass


def showFine():
    ip = 'localhost'
    port = 32118
    SID = 'XE'
    dsn_tns = cx_Oracle.makedsn(ip, port, SID)
    db = cx_Oracle.connect('spectra', '12345', dsn_tns)
    cursor = db.cursor()

    cursor.execute("""SELECT MAX(fine*(-EXTRACT(day FROM (date_end - date_ret)))) from journal
                        JOIN book_types ON journal.book_id = book_types.id
                        AND (EXTRACT(day FROM (date_end - date_ret)) < 0)""")

    temp = cursor.fetchall()
    maxFine.config(text=str('Maximum fine: ') + str(temp[0][0]))
    showTop()


def showTop():
    listBoxTop.delete(*listBoxTop.get_children())
    ip = 'localhost'
    port = 32118
    SID = 'XE'
    dsn_tns = cx_Oracle.makedsn(ip, port, SID)
    db = cx_Oracle.connect('spectra', '12345', dsn_tns)
    cursor = db.cursor()

    cursor.execute("""(SELECT books.name from (SELECT book_id,
                      COUNT(*) AS Cnt
                      FROM journal
                      GROUP BY book_id
                      ORDER BY CNT DESC)
                      JOIN Books ON Books.id = book_id
                      WHERE rownum <= 3)""")

    tempList = cursor.fetchall()

    for (book) in tempList:
        listBoxTop.insert("", "end", values=(book))
    db.close()

cntBook = Label(tab5, text="", bg='gray91')
cntBook.grid()
cntBook.place(x=310, y=20)

fineClient = Label(tab5, text="", bg='gray91')
fineClient.grid()
fineClient.place(x=450, y=20)

l1Features = Label(tab5, text="Client", bg='gray91')
l1Features.grid()
l1Features.place(x=0, y=0)

clientFeatures = StringVar()
e1Features = ttk.Combobox(tab5, textvariable=clientFeatures, postcommand =clientList)
e1Features.grid()
e1Features.bind("<<ComboboxSelected>>", booksCount)
e1Features.config(height=5, width=30)
e1Features.place(x=0, y=20)

showMaxFine = Button(tab5, text="Update", width=15, command=showFine,highlightbackground ='gray91')
showMaxFine.pack()
showMaxFine.place(x=770, y = 16)
showMaxFine.config(height=1, width=5)

maxFine = Label(tab5, text="", bg='gray91')
maxFine.grid()
maxFine.place(x=600, y=20)


top = Label(tab5, text="Top 3 books", bg='gray91')
top.grid()
top.place(x=0, y=80)

colsTop = ('books')
widthTop = (200)
listBoxTop = ttk.Treeview(tab5, columns=colsTop, show='headings', style = 'listBox.Treeview')
listBoxTop.pack()
listBoxTop.place(x=0, y=100)



# set column headings
for i, col in enumerate(colsJournal):
    listBoxJournal.column(col,width=widthJournal[i],stretch=0, anchor=CENTER)
    listBoxJournal.heading(col, text=col)
    listBoxJournal.grid(row=1, column=0)

root1.mainloop()
