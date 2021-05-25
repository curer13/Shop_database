import time
from tkinter import *
from tkinter.ttk import Progressbar
import pyodbc

server = 'localhost'
database = 'market'
username = 'sa'
password = 'Abz09jvv1'

db = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=' +
                    'localhost' + ';DATABASE=' + 'shop' + ';UID=' + 'sa' + ';PWD=' + 'Abz09jvv1')

db.autocommit = True

mycursor = db.cursor()

costumers = []
result = mycursor.execute('select costumer_id from costumers')
for x in result:
    x = str(x)
    x = x.replace('(', '')
    x = x.replace(', )', '')
    costumers.append(x)

costumers_login = {}
result = mycursor.execute('select login, password from custs_login')
for x,y in result:
    costumers_login[x] = y

admin_login = {}
result = mycursor.execute('select login, password from admins')
for x,y in result:
    admin_login[x] = y

def register(event):
    global entry_name, entry_address, entry_login, entry_password
    registration = Toplevel(root)
    registration.title('Registration')
    registration.geometry('300x200')
    registration.configure(bg = 'floral white')
    label_name = Label(registration, text='Name', bg = 'floral white', font = ('Lucida', 10, 'bold'), fg = 'bisque4')
    label_address = Label(registration, text='Address', bg = 'floral white', font = ('Lucida', 10, 'bold'), fg = 'bisque4')
    label_login = Label(registration, text='Login', bg='floral white', font=('Lucida', 10, 'bold'), fg='bisque4')
    label_password = Label(registration, text='Password', bg='floral white', font=('Lucida', 10, 'bold'), fg='bisque4')
    entry_name = Entry(registration, bg = 'bisque4', fg = 'floral white')
    entry_address = Entry(registration, bg = 'bisque4', fg = 'floral white')
    entry_login = Entry(registration, bg = 'bisque4', fg = 'floral white')
    entry_password = Entry(registration, bg = 'bisque4', fg = 'floral white')
    button = Button(registration, text='Register', bg = 'bisque4', font = ('Lucida', 11), fg = 'black')
    button.bind('<Button-1>', new_user)
    welcome = Label(registration, text='Please fill the neccessary information!', bg='floral white', font=('Lucida', 12, 'bold'), fg='bisque4')
    welcome.pack(side = 'top')
    label_name.pack()
    entry_name.pack()
    label_address.pack()
    entry_address.pack()
    label_login.pack()
    entry_login.pack()
    label_password.pack()
    entry_password.pack()
    button.pack()
    label_login.place(x=30, y=30)
    entry_login.place(x=150, y=30)
    label_password.place(x=30, y=60)
    entry_password.place(x=150, y=60)
    label_name.place(x = 30, y = 90)
    entry_name.place(x = 150, y = 90)
    label_address.place(x = 30, y = 120)
    entry_address.place(x = 150, y = 120)
    button.place(x = 120, y = 150)

def check_new_user(name, address, login, password):
    if name =='' or address=='' or login=='' or password =='':
        mistake = Toplevel(root)
        mistake.title('Error')
        mistake.geometry('200x40')
        mistake.configure(bg='floral white')
        print = Label(mistake, text='Please fill the information', bg='floral white', font=('Lucida',12, 'bold'), fg='bisque4')
        print.pack(fill=BOTH)
        return 0
    else: return 1

def new_user(event):
    global costumers
    name = entry_name.get()
    address = entry_address.get()
    login = entry_login.get()
    password = entry_password.get()

    if check_new_user(name, address, login, password):
        mycursor.execute("insert into costumers values('%s', '%s')" % (str(name), str(address)))

        costumers = []
        result = mycursor.execute('select costumer_id from costumers')
        for x in result:
            x = str(x)
            x = x.replace('(', '')
            x = x.replace(', )', '')
            costumers.append(int(x))

        id = max(costumers)

        # print(id)

        mycursor.execute("insert into custs_login values('%s','%s','%s')" % (int(id), str(login), str(password)))

        mistake = Toplevel(root)
        mistake.title('Messege')
        mistake.geometry('300x40')
        mistake.configure(bg='floral white')
        print = Label(mistake, text='Registered successfully with id: "%s"' % (str(id)), bg='floral white', font=('Lucida', 12, 'bold'), fg='bisque4')
        print.pack(fill=BOTH)

def user(event):
    global entry_login_user, entry_password_user
    user = Toplevel(root)
    user.title('User autorization')
    user.geometry('300x120')
    user.configure(bg='RosyBrown1')
    label_login = Label(user, text = 'login', bg = 'RosyBrown1', font = ('Lucida', 10), fg = 'purple')
    label_password = Label(user, text = 'password', bg = 'RosyBrown1', font = ('Lucida', 10), fg = 'purple')
    entry_login_user = Entry(user, bg = 'mistyrose')
    entry_password_user = Entry(user, bg = 'mistyrose')
    button = Button(user, text = 'Enter', bg = 'mistyrose', font = ('Lucida', 10), fg = 'purple', width = 8)
    button.bind('<Button-1>', enter)
    label_login.pack()
    entry_login_user.pack()
    label_password.pack()
    entry_password_user.pack()
    button.pack()
    label_login.place(x = 30, y = 10)
    entry_login_user.place(x = 150, y = 10)
    label_password.place(x = 30, y = 50)
    entry_password_user.place(x = 150, y = 50)
    button.place(x = 120, y = 90)

def enter(event):
    login = entry_login_user.get()
    password = entry_password_user.get()
    data = mycursor.execute('select name, surname from users')
    if check_old_user(login,password):
        all_data = Toplevel(root)
        all_data.title('User autorised')
        all_data.geometry('300x120')
        all_data.configure(bg='RosyBrown1')
        print = Label(all_data, text = 'Autorised successfully', bg = 'RosyBrown1', font = ('Lucida', 10), fg = 'purple')
        print['text'] += '\n'
        for i in data:
            print['text'] += str(i)
            print['text'] += '\n'
        print.pack(fill = BOTH)

def customer(event):
    global entry_login_cust, entry_password_cust
    cust = Toplevel(root)
    cust.title('Customer autorization')
    cust.geometry('300x130')
    cust.configure(bg='floral white')
    label_login = Label(cust, text='Login', bg='floral white', font=('Lucida', 10, 'bold'), fg='bisque4')
    label_password = Label(cust, text='Password', bg='floral white', font=('Lucida', 10, 'bold'), fg='bisque4')
    entry_login_cust = Entry(cust, bg='bisque4', fg='floral white')
    entry_password_cust = Entry(cust, bg='bisque4', fg='floral white')
    button_enter = Button(cust, text='Enter', bg='bisque4', font=('Lucida'), fg='black', width=8)
    button_enter.bind('<Button-1>', enter_cust)
    label_login.pack()
    entry_login_cust.pack()
    label_password.pack()
    entry_password_cust.pack()
    button_enter.pack()
    label_login.place(x=30, y=10)
    entry_login_cust.place(x=150, y=10)
    label_password.place(x=30, y=50)
    entry_password_cust.place(x=150, y=50)
    button_enter.place(x=120, y=90)

def enter_cust(event):
    login = entry_login_cust.get()
    password = entry_password_cust.get()
    select = tuple(mycursor.execute('''
            select cl.cust_id,c.costumer_name from custs_login cl
            join costumers c on
            c.costumer_id=cl.cust_id
            where login=? and PASSWORD=?
        ''', login, password))
    if len(select) != 0:
        customer_buy(select)

def customer_buy(select):
    (cust_id, cust_name) = select[0]
    stock_shop = Toplevel()
    stock_shop.title('Available products')
    stock_shop.geometry('800x800')
    stock_shop.configure(bg='floral white')
    label_cust_name = Label(stock_shop, text=f'Hi, {cust_name}!', bg='floral white', font=('Lucida', 12, 'bold'),
                            fg='bisque4')
    label_cust_name.pack(side = 'top')
    prod_select = tuple(mycursor.execute('''
                        select stock_id,sell_price,stock_name from in_stock
                    '''))
    if len(prod_select) != 0:
        pos = 80
        orders = []

        class Product:
            window = None
            products = []
            total = 0
            l_total = None

            def __init__(self, window, stock_id, sell_price, stock_name, x, y):
                Product.window = window
                Product.l_total=Label(window, text=f'Total: {Product.total}', bg='floral white', font=('Lucida', 11, 'bold'),
                      fg='bisque4')
                self.q = 0
                self.ordered = False
                self.window = window
                self.x = x
                self.y = y
                self.stock_id = stock_id
                self.sell_price = sell_price
                self.stock_name = stock_name
                self.remove = Button(self.window, text='Remove', bg='bisque4', font=('Lucida'), fg='black', width=8)
                self.remove.bind('<Button-1>', self.decrease)
                self.remove.pack()
                self.remove.place(x=self.x - 150, y=self.y)
                self.l_name = Label(self.window, text=f'{self.stock_name}: {self.sell_price}', bg='floral white',
                                    font=('Lucida', 11, 'bold'),
                                    fg='bisque4')
                self.l_name.pack()
                self.l_name.place(x=self.x, y=self.y)
                self.add = Button(self.window, text='Add', bg='bisque4', font=('Lucida'), fg='black', width=8)
                self.add.bind('<Button-1>', self.increase)
                self.add.pack()
                self.add.place(x=self.x + 150, y=self.y)
                self.l_q = Label(self.window, text=f'{self.q}', bg='floral white',
                                 font=('Lucida', 11, 'bold'),
                                 fg='bisque4')
                self.l_q.pack()
                self.l_q.place(x=self.x+ 300, y=self.y)
                Product.products.append(self)

            def increase(self, event):
                self.q += 1
                self.l_q['text'] = str(self.q)
                if self.q > 0:
                    self.ordered = True
                    Product.total += self.sell_price
                else:
                    self.ordered = False
                Product.l_total['text'] = 'Total: '+str(Product.total)
                # print(Product.total)

            def decrease(self, event):
                self.q -= 1
                if self.q>=0:
                    self.ordered=True
                    if self.q==0:
                        self.ordered=False
                    Product.total+=-self.sell_price
                else:
                    self.q=0
                    self.ordered=False
                self.l_q['text'] = str(self.q)
                Product.l_total['text'] = 'Total: '+str(Product.total)
                # print(Product.total)

        for (stock_id, sell_price, stock_name) in prod_select:
            p = Product(stock_shop, stock_id, sell_price, stock_name, 150, pos)
            pos += 100
        Product.l_total.pack()
        Product.l_total.place(x=600, y=400)
        # print(stock_shop)

        def order(event):
            if Product.total!=0:
                mycursor.execute('''
                exec online_order @costumer_id = ?
                ''', cust_id)
                mycursor.commit()
                for p in Product.products:
                    if p.ordered:
                        mycursor.execute('''
                        insert into orders values((select max(order_id) from detail_order),?,?)
                        ''', p.stock_id, p.q)
                        mycursor.commit()

                thanks = Toplevel()
                thanks.title('Thank you')
                thanks.geometry('300x300')
                thanks.configure(bg='floral white')
                label_th = Label(stock_shop, text=f'Thank you, your order was written!', bg='floral white',
                                        font=('Lucida', 12, 'bold'),
                                        fg='bisque4')
                label_th.pack()
                label_th.place(x=0, y=5)
                stock_shop.destroy()
            else:
                please = Toplevel()
                please.title('Attention')
                please.geometry('300x300')
                please.configure(bg='floral white')
                label_pl = Label(please, text=f'Please, order something!', bg='floral white',
                                 font=('Lucida', 12, 'bold'),
                                 fg='bisque4')
                label_pl.pack()
                label_pl.place(x=0, y=5)


        button_order = Button(stock_shop, text='Order', bg='bisque4', font=('Lucida'), fg='black', width=8)
        button_order.bind('<Button-1>', order)
        button_order.pack()
        button_order.place(x=600, y=500)

'''admin'''

def admin(event):
    global entry_login_admin, entry_password_admin
    admin = Toplevel(root)
    admin.title('Admin autorization')
    admin.geometry('300x130')
    admin.configure(bg='floral white')
    label_login = Label(admin, text = 'Login', bg = 'floral white', font = ('Lucida', 10, 'bold'), fg = 'bisque4')
    label_password = Label(admin, text = 'Password', bg = 'floral white', font = ('Lucida', 10, 'bold'), fg = 'bisque4')
    entry_login_admin = Entry(admin, bg = 'bisque4', fg = 'floral white')
    entry_password_admin = Entry(admin, bg = 'bisque4', fg = 'floral white')
    button_enter = Button(admin, text = 'Enter', bg = 'bisque4', font = ('Lucida'), fg = 'black', width = 8)
    button_enter.bind('<Button-1>', enter_admin)
    label_login.pack()
    entry_login_admin.pack()
    label_password.pack()
    entry_password_admin.pack()
    button_enter.pack()
    label_login.place(x=30, y=10)
    entry_login_admin.place(x=150, y=10)
    label_password.place(x=30, y=50)
    entry_password_admin.place(x=150, y=50)
    button_enter.place(x=120, y=90)

def check_admin(login,password):
    if login == '' or password == '':
        mistake = Toplevel(root)
        mistake.title('Error')
        mistake.geometry('200x40')
        mistake.configure(bg='floral white')
        print = Label(mistake, text = 'Please fill the information', bg = 'floral white', font=('Lucida', 12, 'bold'), fg='bisque4')
        print.pack(fill = BOTH)
        return 0
    elif login in admin_login.keys() and password == admin_login[login]:
        return 1
    else:
        mistake = Toplevel(root)
        mistake.title('Error')
        mistake.geometry('200x40')
        mistake.configure(bg='floral white')
        print = Label(mistake, text='Wrong login or password', bg='floral white', font=('Lucida', 12, 'bold'), fg='bisque4')
        print.pack(fill=BOTH)
        return 0

def enter_admin(event):
    login = entry_login_admin.get()
    password = entry_password_admin.get()
    if check_admin(login, password):
        admins = Toplevel(root)
        admins.title('Users control')
        admins.geometry('300x250')
        admins.configure(bg='floral white')
        print = Label(admins, text = 'Choose the command', bg = 'floral white', font = ('Lucida', 12, 'bold'), fg = 'bisque4')
        button_discounts = Button(admins, text = 'Check discounts', bg = 'bisque4', font = ('Lucida',11), fg = 'black', width = 20)
        #button_discounts.bind('<Button-1>', discounts)
        button_cards = Button(admins, text='Check bonus cards', bg = 'bisque4', font = ('Lucida',11), fg = 'black', width = 20)
        #button_cards.bind('<Button-1>', bonus_cards)
        button_profit = Button(admins, text = 'Check month profit', bg = 'bisque4', font = ('Lucida',11), fg = 'black', width = 20)
        #button_profit.bind('<Button-1>', profit)
        button_costumer = Button(admins, text='Costumer controle', bg='bisque4', font=('Lucida', 11), fg='black', width=20)
        button_costumer.bind('<Button-1>', costumers_controle)
        button_purchase = Button(admins, text='Make purchase', bg='bisque4', font=('Lucida', 11), fg='black', width=20)
        #button_purchase.bind('<Button-1>', purchase)
        button_stock = Button(admins, text='Check stock', bg='bisque4', font=('Lucida', 11), fg='black', width=20)
        #button_stock.bind('<Button-1>', stock)
        print.pack(side = 'top')
        button_discounts.pack()
        button_cards.pack()
        button_profit.pack()
        button_costumer.pack()
        button_purchase.pack()
        button_stock.pack()
        button_discounts.place(x = 55, y = 30)
        button_cards.place(x = 55, y = 62)
        button_profit.place(x = 55, y = 94)
        button_costumer.place(x=55, y=126)
        button_purchase.place(x = 55, y = 158)
        button_stock.place(x = 55, y = 190)

def costumers_controle(event):
    costumers = Toplevel(root)
    costumers.title('Costumers control')
    costumers.geometry('300x90')
    costumers.configure(bg='floral white')
    print = Label(costumers, text = 'What to do with costumer?', bg = 'floral white', font = ('Lucida', 12, 'bold'), fg = 'bisque4')
    button_insert = Button(costumers, text = 'insert', bg = 'bisque4', font = ('Lucida', 11), fg = 'black', width = 8)
    button_insert.bind('<Button-1>', register)
    button_delete = Button(costumers, text='delete', bg = 'bisque4', font = ('Lucida', 11), fg = 'black', width = 8)
    button_delete.bind('<Button-1>', delete_command)
    button_update = Button(costumers, text = 'update', bg = 'bisque4', font = ('Lucida', 11), fg = 'black', width = 8)
    button_update.bind('<Button-1>', update_command)
    print.pack(side = 'top')
    button_update.pack()
    button_insert.pack()
    button_delete.pack()
    button_update.place(x = 30, y = 30)
    button_insert.place(x = 115, y = 30)
    button_delete.place(x = 200, y = 30)

def delete_command(event):
    global entry_delete
    delete = Toplevel(root)
    delete.title('Delete')
    delete.geometry('300x90')
    delete.configure(bg='floral white')
    label_login = Label(delete, text = 'Costumer ID', bg = 'floral white', font = ('Lucida', 11, 'bold'), fg = 'bisque4')
    entry_delete = Entry(delete, bg = 'bisque4', fg = 'floral white')
    button_delete = Button(delete, text = 'Delete', bg = 'bisque4', font = ('Lucida', 11), fg = 'black', width = 8)
    button_delete.bind('<Button-1>', delete_user)
    label_login.pack()
    entry_delete.pack()
    button_delete.pack()
    label_login.place(x=30, y=10)
    entry_delete.place(x=150, y=10)
    button_delete.place(x = 120, y = 40)

def delete_user(event):
    global costumers
    ID = str(entry_delete.get())

    costumers = []
    result = mycursor.execute('select costumer_id from costumers')
    for x in result:
        x = str(x)
        x = x.replace('(', '')
        x = x.replace(', )', '')
        costumers.append(x)

    if ID in costumers:
        mycursor.execute("delete from custs_login where cust_id = '%s'" % (ID))
        mycursor.execute("delete from costumers where costumer_id = '%s'" % (ID))
        mistake = Toplevel(root)
        mistake.title('Messenge')
        mistake.geometry('300x40')
        mistake.configure(bg='floral white')
        print = Label(mistake, text='Costumer deleted successfully!', bg='floral white', font=('Lucida', 12 ,'bold'), fg='bisque4')
        print.pack(fill=BOTH)
    else:
        mistake = Toplevel(root)
        mistake.title('Error')
        mistake.geometry('300x40')
        mistake.configure(bg='RosyBrown1')
        print = Label(mistake, text='No costumer with such login!', bg='floral white', font=('Lucida', 12, 'bold'), fg='bisque4')
        print.pack(fill=BOTH)

def update_command(event):
    global id, name, address, login, password
    update = Toplevel(root)
    update.title('Update costumer')
    update.geometry('300x250')
    update.configure(bg='floral white')
    label_id = Label(update, text = 'ID number', bg = 'floral white', font = ('Lucida', 10, 'bold'), fg = 'bisque4')
    label_login = Label(update, text = 'New Login', bg = 'floral white', font = ('Lucida', 10, 'bold'), fg = 'bisque4')
    label_password = Label(update, text = 'New Password', bg = 'floral white', font = ('Lucida', 10, 'bold'), fg = 'bisque4')
    label_name = Label(update, text = 'New Name', bg = 'floral white', font = ('Lucida', 10, 'bold'), fg = 'bisque4')
    label_address = Label(update, text = 'New Address', bg = 'floral white', font = ('Lucida', 10, 'bold'), fg = 'bisque4')
    id = Entry(update, bg = 'bisque4', fg = 'floral white')
    login = Entry(update, bg = 'bisque4', fg = 'floral white')
    password = Entry(update, bg = 'bisque4', fg = 'floral white')
    name = Entry(update, bg = 'bisque4', fg = 'floral white')
    address = Entry(update, bg = 'bisque4', fg = 'floral white')
    button_update = Button(update, text = 'update', bg = 'bisque4', font = ('Lucida', 11), fg = 'black', width = 8)
    button_update.bind('<Button-1>', update_user)
    label_id.pack()
    id.pack()
    label_login.pack()
    login.pack()
    label_password.pack()
    password.pack()
    label_name.pack()
    name.pack()
    label_address.pack()
    address.pack()
    label_id.place(x=30, y=30)
    id.place(x=150, y=30)
    label_login.place(x=30, y=60)
    login.place(x=150, y=60)
    label_password.place(x=30, y=90)
    password.place(x=150, y=90)
    label_name.place(x=30, y=120)
    name.place(x=150, y=120)
    label_address.place(x=30, y=150)
    address.place(x=150, y=150)
    button_update.place(x=120, y=180)

def update_user(event):
    global costumers
    id_old = str(id.get())
    name_new = str(name.get())
    address_new = str(address.get())
    login_new = str(login.get())
    password_new = str(password.get())

    costumers = []
    result = mycursor.execute('select costumer_id from costumers')
    for x in result:
        x = str(x)
        x = x.replace('(', '')
        x = x.replace(', )', '')
        costumers.append(x)

    if id_old in costumers:
        if name_new != '':
            mycursor.execute("update costumers set costumer_name = '%s' where costumer_id = '%s'" % (name_new, id_old))
        if address_new != '':
            mycursor.execute("update costumers set costumer_address = '%s' where costumer_id = '%s'" % (address_new, id_old))
        if login_new != '':
            mycursor.execute("update custs_login set login = '%s' where cust_id = '%s'" % (login_new, id_old))
        if password_new != '':
            mycursor.execute("update custs_login set PASSWORD = '%s' where cust_id = '%s'" % (password_new, id_old))
        mistake = Toplevel(root)
        mistake.title('Messenge')
        mistake.geometry('300x40')
        mistake.configure(bg='floral white')
        print = Label(mistake, text='Costumer updated successfully!', bg='floral white', font=('Lucida', 12, 'bold'), fg='bisque4')
        print.pack(fill=BOTH)
    else:
        mistake = Toplevel(root)
        mistake.title('Error')
        mistake.geometry('200x40')
        mistake.configure(bg='floral white')
        print = Label(mistake, text='No user with such id!', bg='floral white', font=('Lucida', 12, 'bold'), fg='bisque4')
        print.pack(fill=BOTH)


root = Tk()
root.title('Welcome!')
root.geometry('300x120')
root.configure(bg = 'floral white')

welcome = Label(root, text='Welcome to our internet-shop!', bg='floral white', font=('Lucida', 12, 'bold'), fg='bisque4')
who = Label(root, text='Are you an admin or costumer?', bg='floral white', font=('Lucida'), fg='bisque4')
button_costumer = Button(root, text='Costumer', bg = 'bisque4', font = ('Lucida', 10), fg = 'black', width = 8)
button_admin = Button(root, text='Admin',bg = 'bisque4', font = ('Lucida', 10), fg = 'black', width = 8)

button_costumer.bind('<Button-1>', customer)
button_admin.bind('<Button-1>', admin)

welcome.pack(side = 'top')
who.pack(side = 'top')
button_costumer.pack()
button_admin.pack()
button_costumer.place(x = 120, y = 50)
button_admin.place(x = 120, y = 82)

root.mainloop()
