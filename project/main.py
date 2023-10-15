import tkinter as tk
from tkinter import ttk
import sqlite3

class Main(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.init_main()
        self.db = db
        self.view_records()

    def init_main(self): #создаем функцию для открытия главного окна
        toolbar = tk.Frame(bg='#d7d8e0', bd=2)
        toolbar.pack(side=tk.TOP, fill=tk.X)
        
        self.add_img = tk.PhotoImage(file='./img/add.png') #создаем кнопку для добавления сотрудников
        btn_open_dialog = tk.Button(toolbar, bg='#d7d8e0', bd=0, image=self.add_img, command=self.open_dialog)
        btn_open_dialog.pack(side=tk.LEFT)

        self.tree = ttk.Treeview(self, columns=('ID', 'name', 'phone', 'email', 'salary'), height=45, show='headings') #говорим, какие используем данные для заголовков

        self.tree.column("ID", width=30, anchor=tk.CENTER) #задаем параметры столбцов
        self.tree.column("name", width=300, anchor=tk.CENTER)
        self.tree.column("phone", width=150, anchor=tk.CENTER)
        self.tree.column("email", width=150, anchor=tk.CENTER)
        self.tree.column("salary", width=150, anchor=tk.CENTER)

        self.tree.heading("ID", text='ID') #красиво называем столбцы
        self.tree.heading("name", text='full name')
        self.tree.heading("phone", text='telephone number')
        self.tree.heading("email", text='E-mail addres')
        self.tree.heading("salary", text='salary')

        self.tree.pack(side=tk.LEFT) #выравниваем

        self.update_img = tk.PhotoImage(file='./img/update.png') #создаем кнопку для изменения сотрудников
        btn_edit_dialog = tk.Button(toolbar, bg='#d7d8e0', bd=0, image=self.update_img, command=self.open_update_dialog)
        btn_edit_dialog.pack(side=tk.LEFT)

        self.delete_img = tk.PhotoImage(file='./img/delete.png') #создаем кнопку для удаления сотрудников
        btn_delete = tk.Button(toolbar, bg='#d7d8e0', bd=0, image=self.delete_img, command=self.delete_records)
        btn_delete.pack(side=tk.LEFT)

        self.search_img = tk.PhotoImage(file='./img/search.png') #создаем кнопку для поиска сотрудников
        btn_search = tk.Button(toolbar, bg='#d7d8e0', bd=0, image=self.search_img, command=self.open_search_dialog)
        btn_search.pack(side=tk.LEFT)

    def records(self, name, phone, email, salary): #создаем записи
        self.db.insert_data(name, phone, email, salary)
        self.view_records()

    def view_records(self): #показываем записи из бд
        self.db.cursor.execute('''SELECT * FROM db''')
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db.cursor.fetchall()]
        
    def open_dialog(self): #открываем окно добавления сотрудников
        Child()

    def open_update_dialog(self): #открываем окно изменения сотрудников
        Update()

    def update_record(self, name, phone, email, salary): #обновляем записи о сотрудниках
        self.db.cursor.execute(
            '''UPDATE db SET name = ?, phone = ?, email = ?, salary = ? WHERE ID = ?''', (name, phone, email, salary, self.tree.set(self.tree.selection() [0], '#1')))
        self.db.conn.commit()
        self.view_records()

    def delete_records(self): #удаляем записи из бд
        for selection_item in self.tree.selection():
            self.db.cursor.execute('''DELETE FROM db WHERE ID=?''', (self.tree.set(selection_item, '#1')))
        self.db.conn.commit()
        self.view_records()

    def open_search_dialog(self): #открываем окно поиска
        Search()

    def search_records(self, name): #ищем данные о сотруднике по его имени 
        name = '%' + name + '%'
        self.db.cursor.execute('''SELECT * FROM db WHERE name LIKE ?''', (name,))

        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db.cursor.fetchall()]



class Child(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_child()
        self.view = app

    def init_child(self): #задаем все-все-все параметры окна добавления 
        self.title('Add')
        self.geometry('400x220')
        self.resizable(False, False)

        self.grab_set()
        self.focus_set()

        label_name = tk.Label(self, text='full name:') #показывает что нужно вводить при добавлении сотрудника
        label_name.place(x=50, y=50)
        label_phone = tk.Label(self, text='telephone number:')
        label_phone.place(x=50, y=80)
        label_email = tk.Label(self, text='E-mail addres:')
        label_email.place(x=50, y=110)
        label_salary = tk.Label(self, text='salary:')
        label_salary.place(x=50, y=140)

        self.entry_name = ttk.Entry(self) #место для заполнения данных
        self.entry_name.place(x=200, y=50)
        self.entry_phone = ttk.Entry(self)
        self.entry_phone.place(x=200, y=80)
        self.entry_email = ttk.Entry(self)
        self.entry_email.place(x=200, y=110)
        self.entry_salary = ttk.Entry(self)
        self.entry_salary.place(x=200, y=140)

        self.btn_cancel = ttk.Button(self, text='Close', command=self.destroy) #закрытие окна
        self.btn_cancel.place(x=300, y=170)

        self.btn_ok = ttk.Button(self, text='Add') #добавление
        self.btn_ok.place(x=220, y=170)

        self.btn_ok.bind('<Button-1>', lambda event:
                          self.view.records(self.entry_name.get(),
                                            self.entry_phone.get(),
                                            self.entry_email.get(),
                                            self.entry_salary.get()))



class Update(Child):
    def __init__(self):
        super().__init__()
        self.init_edit()
        self.view = app
        self.db = db
        self.default_data()

    def init_edit(self): #функция для изменения данных
        self.title('Edit position')
        btn_edit = ttk.Button(self, text= 'Edit')
        btn_edit.place(x=205, y=170)
        btn_edit.bind('<Button-1>', lambda event:
                      self.view.update_record(self.entry_name.get(),
                                              self.entry_phone.get(),
                                              self.entry_email.get(),
                                              self.entry_salary.get()))
        btn_edit.bind('<Button-1>', lambda event:
                      self.destroy(), add='+')
        self.btn_ok.destroy()

    def default_data(self): #заполняем поля, которые будем изменять, уже имеющимися данными (так, при изменении одного параметра остальные сохранятся прежними)
        self.db.cursor.execute(
            'SELECT * FROM db WHERE ID=?', self.view.tree.set(self.view.tree.selection()[0], '#1'))
        row = self.db.cursor.fetchone()
        self.entry_name.insert(0, row[1])
        self.entry_phone.insert(0, row[2])
        self.entry_email.insert(0, row[3])
        self.entry_salary.insert(0, row[4])



class Search(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.init_search()
        self.view = app

    def init_search(self): #функция для открытия окна поиска
        self.title('Search for contact')
        self.geometry('300x100')
        self.resizable(False, False)

        label_search = tk.Label(self, text='Name: ') #даем понять, что нам нужно имя
        label_search.place(x=50, y=20)

        self.entry_search = tk.Entry(self) #место для вписывания имени
        self.entry_search.place(x=105, y=20, width=150)

        btn_cancel = ttk.Button(self, text='Close', command=self.destroy) #кнопка закрытия
        btn_cancel.place(x=185, y=50)

        btn_search = ttk.Button(self, text='Find') #кнопка поиска
        btn_search.place(x=105, y=50)

        btn_search.bind('<Button-1>', lambda event:
                          self.view.search_records(self.entry_search.get()))
        btn_search.bind('<Button-1>', lambda event:self.destroy(), add='+')



class DB:
    def __init__(self): #создание бд для хранения записей
        self.conn = sqlite3.connect('db.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute(
            '''CREATE TABLE IF NOT EXISTS db (
                ID INTEGER PRIMARY KEY,
                name TEXT,
                phone TEXT,
                email TEXT,
                salary TEXT
            )'''
        )
        self.conn.commit()

    def insert_data(self, name, phone, email, salary): #функция заполнения бд введенными записями
        self.cursor.execute('''INSERT INTO db (name, phone, email, salary) VALUES(?, ?, ?, ?)''', (name, phone, email, salary))
        self.conn.commit()



if __name__ == '__main__': #открытие всей программы
    root = tk.Tk()
    db = DB()
    app = Main(root)
    app.pack()
    root.title('List of company employees')
    root.geometry('810x450')
    root.resizable(False, False)
    root.mainloop()