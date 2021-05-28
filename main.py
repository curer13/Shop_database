from tkinter import *
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
            costumers.append(x)

        id = max(costumers)

        mycursor.execute("insert into custs_login values('%s','%s','%s')" % (int(id), str(login), str(password)))

        mistake = Toplevel(root)
        mistake.title('Messege')
        mistake.geometry('300x40')
        mistake.configure(bg='floral white')
        print = Label(mistake, text='Registered successfully with id: "%s"' % (str(id)), bg='floral white', font=('Lucida', 12, 'bold'), fg='bisque4')
        print.pack(fill=BOTH)

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
    def customer_order(event):
        (cust_id, cust_name) = select[0]
        stock_shop = Toplevel()
        stock_shop.title('Available products')
        stock_shop.geometry('800x800')
        stock_shop.configure(bg='floral white')
        label_cust_name = Label(stock_shop, text=f'Hi, {cust_name}!', bg='floral white', font=('Lucida', 12, 'bold'),
                                fg='bisque4')
        label_cust_name.pack(side='top')
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
                    Product.l_total = Label(window, text=f'Total: {Product.total}', bg='floral white',
                                            font=('Lucida', 11, 'bold'),
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
                    self.l_q.place(x=self.x + 300, y=self.y)
                    Product.products.append(self)

                def increase(self, event):
                    self.q += 1
                    self.l_q['text'] = str(self.q)
                    if self.q > 0:
                        self.ordered = True
                        Product.total += self.sell_price
                    else:
                        self.ordered = False
                    Product.l_total['text'] = 'Total: ' + str(Product.total)
                    # print(Product.total)

                def decrease(self, event):
                    self.q -= 1
                    if self.q >= 0:
                        self.ordered = True
                        if self.q == 0:
                            self.ordered = False
                        Product.total += -self.sell_price
                    else:
                        self.q = 0
                        self.ordered = False
                    self.l_q['text'] = str(self.q)
                    Product.l_total['text'] = 'Total: ' + str(Product.total)
                    # print(Product.total)

            for (stock_id, sell_price, stock_name) in prod_select:
                p = Product(stock_shop, stock_id, sell_price, stock_name, 150, pos)
                pos += 100
            Product.l_total.pack()
            Product.l_total.place(x=600, y=400)

            # print(stock_shop)

            def order(event):
                if Product.total != 0:
                    mycursor.execute('''
                    exec online_order @costumer_id = ?
                    ''', cust_id)
                    mycursor.commit()
                    for p in Product.products:
                        if p.ordered:
                            s_ord=mycursor.execute('''
                            set nocount on
                            insert into orders values((select max(order_id) from detail_order),?,?)
                            ''', p.stock_id, p.q)

                            tx=list(s_ord)[0][0]

                    thanks = Toplevel()
                    thanks.title('Thank you')
                    thanks.geometry('300x300')
                    thanks.configure(bg='floral white')
                    label_th = Label(thanks, text='Thank you, your order was written!\n'+tx, bg='floral white',
                                     font=('Lucida', 12, 'bold'),
                                     fg='bisque4')
                    label_th.pack()
                    label_th.place(x=5, y=150)
                    stock_shop.destroy()
                else:
                    please = Toplevel()
                    please.title('Attention')
                    please.geometry('300x300')
                    please.configure(bg='floral white')
                    label_pl = Label(please, text='Please, order something!', bg='floral white',
                                     font=('Lucida', 12, 'bold'),
                                     fg='bisque4')
                    label_pl.pack()
                    label_pl.place(x=0, y=5)

            button_order = Button(stock_shop, text='Order', bg='bisque4', font=('Lucida'), fg='black', width=8)
            button_order.bind('<Button-1>', order)
            button_order.pack()
            button_order.place(x=600, y=500)

    def bask(event=None):
        (cust_id, cust_name) = select[0]
        s_dorder=list(mycursor.execute('''
        select order_id,date_ordered,total_price,paid from detail_order
        where costumer_id=? and paid='F'
        ''', cust_id))
        basket = Toplevel(root)
        basket.title('Basket')
        basket.geometry('800x900')

        class Order:
            def __init__(self,window,order_id,date_ordered,total_price,x,y):
                self.x=x
                self.y=y
                self.total_price=total_price
                self.window=window
                self.date_ordered=date_ordered
                self.order_id=order_id
                self.l_warn = Label(self.window, text='', bg='floral white',
                                   font=('Lucida', 12, 'bold'),
                                   fg='bisque4')
                self.l_order = Label(self.window, text=f'{self.order_id}    {self.date_ordered}    {self.total_price}', bg='floral white',
                                     font=('Lucida', 12, 'bold'),
                                     fg='bisque4')
                self.b_paybb=Button(self.window, text='Pay by bonuses', bg='bisque4', font=('Lucida'), fg='black', width=8)
                self.b_pay=Button(self.window, text='Pay', bg='bisque4', font=('Lucida'), fg='black', width=8)
                self.b_pay.bind('<Button-1>', self.pay)
                self.b_paybb.bind('<Button-1>',self.paybb)
                self.b_pay.pack()
                self.b_cancel=Button(self.window, text='Cancel', bg='bisque4', font=('Lucida'), fg='black', width=8)
                self.b_cancel.bind('<Button-1>', self.cancel)
                self.b_cancel.pack()
                self.b_paybb.pack()
                self.l_order.place(x=self.x,y=self.y)
                self.b_cancel.place(x=self.x+540,y=self.y)
                self.b_pay.place(x=self.x+300,y=self.y)
                self.b_paybb.place(x=self.x+420,y=self.y)

            def cancel(self,event):
                mycursor.execute('''
                exec cancel_order @order_id=?     
                ''',self.order_id)

                res=list(mycursor.execute('''
                if not EXISTS(select order_id from detail_order where order_id=?)
                BEGIN
                    select concat('The order ',?,' was canceled')
                end
                else
                    select ''
                ''',self.order_id,self.order_id))[0][0]

                if res=='':
                    self.l_warn['text']='Нельзя отменить заказ'
                    self.l_warn.pack()
                    self.l_warn.place(x=self.x + 660, y=self.y)
                else:
                    self.l_warn['text']=res
                    self.l_warn.pack()
                    self.l_warn.place(x=self.x + 660, y=self.y)
                    self.window.destroy()
                    bask()


            def pay(self,event):
                mycursor.execute('''
                update detail_order
                set paid='T'
                where order_id=?
                ''',self.order_id)

                mycursor.execute('''
                exec proc_deliver @order_id=?
                ''',self.order_id)

                th = Toplevel(root)
                th.title('Thank you!')
                th.geometry('200x200')
                l_th=Label(th, text=f'You order {self.order_id} was paid!',
                      bg='floral white',
                      font=('Lucida', 12, 'bold'),
                      fg='bisque4')
                l_th.pack()
                l_th.place(x=25, y=100)
                # window=self.window
                self.window.destroy()
                bask()


            def paybb(self,event):
                mycursor.execute('''
                exec pay_by_bonuses @order_id = ?
                ''',self.order_id)

                mycursor.execute('''
                exec proc_deliver @order_id=?
                ''', self.order_id)

                res=tuple(mycursor.execute('''
                select paid from detail_order
                where order_id=?
                ''',self.order_id))[0][0]

                att = Toplevel(root)
                att.title('Attention!')
                att.geometry('200x200')
                l_att = Label(att, text='',
                             bg='floral white',
                             font=('Lucida', 12, 'bold'),
                             fg='bisque4')
                if res=='T':
                    l_att['text']=f'Thank you, your order {self.order_id} was paid by bonuses'
                    self.window.destroy()
                    bask()
                else:
                    l_att['text']=f'Недостаточно бонусов для оплаты'
                l_att.pack()
                l_att.place(x=25, y=100)

        y = 10
        for order_id,date_ordered,total_price,paid in s_dorder:
            o=Order(basket,order_id,date_ordered,total_price,5,y)
            y+=40

        if not s_dorder:
            l_em = Label(basket, text=f'У вас нет заказов',
                         bg='floral white',
                         font=('Lucida', 12, 'bold'),
                         fg='bisque4')
            l_em.pack()
            l_em.place(x=25, y=100)

    def bonus(event):
        (cust_id, cust_name) = select[0]
        w_bon = Toplevel(root)
        w_bon.title('Bonuses')
        w_bon.geometry('300x300')
        mycursor.execute('''
        exec check_bonus
        ''')
        s_bon=list(mycursor.execute('''
        select bonuses,open_date,last_bonus, DATEDIFF(day, last_bonus, getdate()) from bonus_cards
        where costumer_id=?
        ''',cust_id))

        info=''
        if s_bon:
            (bonuses, open_date, last_bonus, expire)=s_bon[0]
            exp = ''
            if expire >= 3:
                exp = '\nВаши бонусы будут обнулены в связи того что их больше 10,000 и с последней покупки прошло 3 дня'
            info=f'{bonuses}   {open_date}    {last_bonus}{exp}'

            def present(event):
                w_pres = Toplevel(root)
                w_pres.title('Presents')
                w_pres.geometry('800x800')
                s_pres = mycursor.execute('''
                select present_id, present_name,present_price from presents
                ''')
                l_bon = Label(w_pres, text=str(bonuses),
                              bg='floral white',
                              font=('Lucida', 12, 'bold'),
                              fg='bisque4')

                class Present:
                    def __init__(self, window, id, name, price, x, y):
                        self.id = id
                        self.name = name
                        self.price = price
                        self.window = window
                        self.x = x
                        self.y = y
                        self.b_ch = Button(self.window, text='Обменять', bg='bisque4', font=('Lucida'), fg='black',
                                           width=8)
                        self.l_pr = Label(self.window, text=self.name + '   ' + str(self.price),
                                          bg='floral white',
                                          font=('Lucida', 12, 'bold'),
                                          fg='bisque4')
                        self.l_er = Label(self.window, text='',
                                          bg='floral white',
                                          font=('Lucida', 12, 'bold'),
                                          fg='bisque4')
                        self.b_ch.bind('<Button-1>', self.chan)
                        self.b_ch.pack()
                        self.l_er.pack()
                        self.l_pr.pack()
                        self.b_ch.place(x=self.x + 100, y=self.y)
                        self.l_pr.place(x=self.x, y=self.y)
                        self.l_er.place(x=self.x + 200, y=self.y)

                    def chan(self, event):
                        '''if bonuses < self.price:
                            self.l_er['text'] = 'Недостаточно бонусов'
                        else:'''
                        # print(cust_id,self.id)
                        s_ch = tuple(mycursor.execute('''
                        SET NOCOUNT ON
                        exec presents_trade @costumer_id = ?, @present_id = ?
                        ''', cust_id, self.id))[0][0]

                        if s_ch == 'Недостаточно бонусов!':
                            self.l_er['text'] = 'Недостаточно бонусов'
                        else:
                            w_succ = Toplevel(root)
                            w_succ.title('Attention!')
                            w_succ.geometry('200x200')
                            l_succ = Label(w_succ, text='Бонусы успешно были обменены на подарок',
                                           bg='floral white',
                                           font=('Lucida', 12, 'bold'),
                                           fg='bisque4')
                            l_succ.pack()
                            l_succ.place(x=0, y=100)
                            w_pres.destroy()
                            w_bon.destroy()
                            # present(None)
                            bonus(None)

                y = 40
                for present_id, present_name, present_price in s_pres:
                    pr = Present(w_pres, present_id, present_name, present_price, 5, y)
                    y += 40

                l_bon.pack()
                l_bon.place(x=400, y=0)

            button_change = Button(w_bon, text='Обменять на подарки', bg='bisque4', font=('Lucida'), fg='black',
                                   width=8)
            button_change.bind('<Button-1>', present)
            button_change.pack()
        else:
            info='У вас нет бонусов!'


        l_bon = Label(w_bon, text=info,
                     bg='floral white',
                     font=('Lucida', 12, 'bold'),
                     fg='bisque4')
        l_bon.pack()
        l_bon.place(x=25, y=100)

    def my_pres(event):
        (cust_id, cust_name) = select[0]
        w_mpr = Toplevel(root)
        w_mpr.title('Presents')
        w_mpr.geometry('150x800')
        pr_l = list(mycursor.execute('''
        select p.present_name from presents_bonus pb
        join presents p
        on pb.present_id=p.present_id
        where costumer_id=?
        ''',cust_id))
        print(pr_l)
        if pr_l:
            pr_name='\n'.join([pr[0] for pr in pr_l])
        else:
            pr_name='У вас нет подарков'
        l_mpr = Label(w_mpr, text=pr_name,
                      bg='floral white',
                      font=('Lucida', 12, 'bold'),
                      fg='bisque4')
        l_mpr.pack()
        l_mpr.place(x=0, y=100)

    if len(select) != 0:

        pay_or_order = Toplevel(root)
        pay_or_order.title('Customer autorization')
        pay_or_order.geometry('300x130')
        pay_or_order.configure(bg='floral white')
        button_pay = Button(pay_or_order, text='Basket', bg='bisque4', font=('Lucida'), fg='black', width=8)
        button_pay.bind('<Button-1>', bask)
        button_bon = Button(pay_or_order, text='Bonuses', bg='bisque4', font=('Lucida'), fg='black', width=8)
        button_bon.bind('<Button-1>', bonus)
        button_order = Button(pay_or_order, text='Order', bg='bisque4', font=('Lucida'), fg='black', width=8)
        button_order.bind('<Button-1>', customer_order)
        button_pres = Button(pay_or_order, text='My presents', bg='bisque4', font=('Lucida'), fg='black', width=8)
        button_pres.bind('<Button-1>', my_pres)

        button_pay.pack()
        button_pres.pack()
        button_bon.pack()
        button_order.pack()
        button_pay.place(x=0, y=65)
        button_pres.place(x=100, y=25)
        button_bon.place(x=100, y=65)
        button_order.place(x=200, y=65)

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

def bonus_cards(event):
    s_bon = list(mycursor.execute('''
            select * from bonus_cards
            '''))
    w_bon = Toplevel(root)
    w_bon.title('Bonuses')
    w_bon.geometry('800x800')
    w_bon.configure(bg='floral white')
    if s_bon:
        tx='\n'.join(str(cust_id)+'     '+str(bonuses)+'    '+str(op_date)+'    '+str(last_date) for cust_id,bonuses,op_date,last_date in s_bon)
    else:
        tx='No bonuses'
    label_bon = Label(w_bon, text = tx, bg = 'floral white', font = ('Lucida', 10, 'bold'), fg = 'bisque4')
    label_bon.pack()
    label_bon.place(x=5,y=5)

def profit(event):
    (mycursor.execute('''
    declare @m nvarchar(25)=datename(month,getdate())
    exec month_profit @mes=@m
    '''))
    w_prof = Toplevel(root)
    w_prof.title('Users control')
    w_prof.geometry('500x500')
    w_prof.configure(bg='floral white')
    label_accs = Label(w_prof, text='', bg='floral white', font=('Lucida', 10, 'bold'), fg='bisque4')
    e_mes = Entry(w_prof, bg = 'bisque4', fg = 'floral white')
    e_mes.pack()
    e_mes.place(x=200, y=5)
    def calcProf(event):
        mes=e_mes.get()
        print(mes)
        s_showp=list(mycursor.execute('''
        select * from dbo.profit_fun(?)
        ''',mes))
        if s_showp:
            tx=s_showp[0][0]
            print(tx)
            label_message = Label(w_prof, text='', bg='floral white', font=('Lucida', 10, 'bold'), fg='bisque4')
            label_message['text']=str(tx)
            label_message.pack()
            label_message.place(x=200, y=50)

    button_prof = Button(w_prof, text='Show profit', bg='bisque4', font=('Lucida', 11), fg='black', width=20)
    button_prof.bind('<Button-1>', calcProf)
    button_prof.pack()
    button_prof.place(x=200,y=200)


    s_acc=list(mycursor.execute('''
    select acc_name,wealth,last_upd from accounts
    '''))
    tx_acc='\n'.join([str(acc_name)+'   '+str(wealth)+'     '+str(last_upd) for acc_name,wealth,last_upd in s_acc])
    label_accs['text']=tx_acc
    label_accs.pack()
    label_accs.place(x=200, y=100)



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
        button_discounts.bind('<Button-1>', discount)
        button_cards = Button(admins, text='Check bonus cards', bg = 'bisque4', font = ('Lucida',11), fg = 'black', width = 20)
        button_cards.bind('<Button-1>', bonus_cards)
        button_profit = Button(admins, text = 'Check month profit', bg = 'bisque4', font = ('Lucida',11), fg = 'black', width = 20)
        button_profit.bind('<Button-1>', profit)
        button_costumer = Button(admins, text='Costumer controle', bg='bisque4', font=('Lucida', 11), fg='black', width=20)
        button_costumer.bind('<Button-1>', costumers_controle)
        button_purchase = Button(admins, text='Make purchase', bg='bisque4', font=('Lucida', 11), fg='black', width=20)
        button_purchase.bind('<Button-1>', purchase)
        button_stock = Button(admins, text='Check stock', bg='bisque4', font=('Lucida', 11), fg='black', width=20)
        button_stock.bind('<Button-1>', stock)
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

def discount(event):
    global discounts
    discount = Toplevel(root)
    discount.title('Discount')
    discount.geometry('300x300')
    discount.configure(bg='floral white')
    label = Label(discount, text = 'Discounts', bg = 'floral white', font = ('Lucida', 12, 'bold'), fg = 'bisque4')
    discounts = Label(discount, text = 'Product    discount(%) \n', bg = 'floral white', font = ('Lucida', 11), fg = 'bisque4')
    new_discounts = Button(discount, bg = 'bisque4', text = 'Set new discounts', font = ('Lucida', 11), fg = 'black', width = 15)
    result = mycursor.execute('select stock_id, discount from discounts')
    for x,y in result:
        if x < 10:
            discounts['text'] += f' {x}         '
        else:
            discounts['text'] += f' {x}        '
        discounts['text'] += f'{y}   \n'
    new_discounts.bind('<Button-1>', new_discount)
    label.pack(side='top')
    new_discounts.pack(side='top')
    discounts.pack()

def new_discount(event):
    mycursor.execute('exec set_discount')
    discounts['text'] = 'Product    discount(%) \n'
    result = mycursor.execute('select stock_id, discount from discounts')
    for x, y in result:
        if x < 10:
            discounts['text'] += f' {x}         '
        else:
            discounts['text'] += f' {x}        '
        discounts['text'] += f'{y}   \n'

def stock(event):
    needs=list(mycursor.execute('''
    exec stock_to_buy
    '''))
    if needs:
        n = '\n'.join([str(need[0]) for need in needs])
    in_s=mycursor.execute('''
    select stock_id, stock_q from in_stock
    ''')
    goods = Toplevel(root)
    goods.title('Stock')
    goods.geometry('500x600')
    goods.configure(bg='floral white')
    s="\n".join([str(prod[0]) + "   " + str(prod[1]) for prod in in_s])
    l_ins = Label(goods, text=s, bg='floral white', font=('Lucida', 12, 'bold'), fg='bisque4')
    l_ins.pack()
    l_ins.place(x=100,y=5)
    l_need = Label(goods, text=n, bg='floral white', font=('Lucida', 12, 'bold'), fg='bisque4')
    l_need.pack()
    l_need.place(x=200, y=5)

def purchase(event):
    purch = Toplevel(root)
    purch.title('Purchase stock')
    purch.geometry('500x500')
    purch.configure(bg='floral white')
    # label_buyer = Label(purch, text='Buyer id', bg='floral white', font=('Lucida', 10, 'bold'), fg='bisque4')
    label_stock = Label(purch, text='Stock id', bg='floral white', font=('Lucida', 10, 'bold'), fg='bisque4')
    label_q = Label(purch, text='Quantity', bg='floral white', font=('Lucida', 10, 'bold'), fg='bisque4')
    entry_buyer = Entry(purch, bg='bisque4', fg='floral white')
    entry_stock = Entry(purch, bg='bisque4', fg='floral white')
    entry_q = Entry(purch, bg='bisque4', fg='floral white')
    button_enter = Button(purch, text='Enter', bg='bisque4', font=('Lucida'), fg='black', width=8)

    label_del = Label(purch, text='', bg='floral white', font=('Lucida', 10, 'bold'), fg='bisque4')
    def buy_stock(event):
        buyer_id = tuple(mycursor.execute('''
            select buyer_id from buyer_stock
            where stock_id=?
            ''', entry_stock.get()))[0][0]
        # print(buyer_id)
        deleted=tuple(mycursor.execute('''
            SET NOCOUNT ON
            insert into purchase_date values(?,?,?,GETDATE())
        ''',buyer_id,entry_stock.get(),entry_q.get()))[0][0]
        label_del['text']+='\n'+deleted

    button_enter.bind('<Button-1>', buy_stock)
    label_q.pack()
    entry_q.pack()
    label_del.pack()
    # label_buyer.pack()
    # entry_buyer.pack()
    label_stock.pack()
    entry_stock.pack()
    button_enter.pack()
    # label_buyer.place(x=30, y=10)
    # entry_buyer.place(x=150, y=10)
    label_stock.place(x=30, y=50)
    entry_stock.place(x=150, y=50)
    label_q.place(x=30,y=90)
    entry_q.place(x=150,y=90)
    button_enter.place(x=120, y=140)
    label_del.place(x=120,y=190)

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
            mycursor.execute("update custs_login set login = '%s' where costumer_id = '%s'" % (login_new, id_old))
        if password_new != '':
            mycursor.execute("update custs_login set PASSWORD = '%s' where costumer_id = '%s'" % (password_new, id_old))
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
