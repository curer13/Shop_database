from tkinter import *
stock_shop = Toplevel()
stock_shop.title('Available products')
stock_shop.geometry('600x600')
stock_shop.configure(bg='floral white')

def f():
    label_total.config(var.get())

var=IntVar()
q = Scale(stock_shop, from_=1, to=100, orient=HORIZONTAL,variable=var,command=f)
q.set(18)
label_total = Label(stock_shop, text=f'{q.get()}', bg='floral white', font=('Lucida', 20, 'bold'), fg='bisque4')
q.pack(anchor=CENTER)
label_total.pack()
label_total.place(x=450, y=20)
stock_shop.mainloop()