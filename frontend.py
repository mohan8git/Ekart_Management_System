from tkinter import *
from tkinter import font as tkFont
from backend import login_check, relate_all,insert_supplier,supplier_names,remove_supplier,insert_product, \
    remove_product, product_names,customer_names,insert_customer,remove_customer,insert_orders,\
    remove_orders, order_customer_names

class E_Kart(Tk):
    # Main class for the system

    def __init__(self, *args, **kwargs):
        # Function for intializing all the views

        Tk.__init__(self, *args, **kwargs)
        self.title_font = tkFont.Font(
            family='Helvetica', size=18, weight="bold", slant="italic")

        # Stacking of multiple frames on top of each other
        # the one visible will be raised on top
        container = Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # All the classes whose view is to be shown
        self.classes = (login_view, main_view,GUI_Supplier_Edit,GUI_Supplier_Input,GUI_Supplier_Remove,GUI_Product_Edit,
                        GUI_Product_Input,GUI_Product_Remove,GUI_Customer_Edit,GUI_Customer_Input,GUI_Customer_Remove,
                        GUI_Orders_Edit,GUI_Orders_Input,GUI_Orders_Remove)
        self.frames = {}
        for F in self.classes:
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("login_view")  # First frame to be shown

    def show_frame(self, page_name):
        # Function to raise the requested frame to the top
        frame = self.frames[page_name]
        frame.tkraise()


class login_view(Frame):
    # Login view class of the app

    def __init__(self, parent, controller):
        # Function for initializing the components of the view
        Frame.__init__(self, parent)
        self.controller = controller

        self.current_row = 0  # Set the current row count of the view

        # Username Field
        self.username_label = Label(self, text='Username: ')
        self.username_label.grid(row=self.current_row, column=0)
        self.username_text = StringVar()
        self.username_entry = Entry(
            self, textvariable=self.username_text, width=60)
        self.username_entry.grid(row=self.current_row, column=1, sticky='we')
        self.current_row += 1

        # Password field
        self.password_label = Label(self, text='Password: ')
        self.password_label.grid(row=self.current_row, column=0)
        self.password_text = StringVar()
        self.password_entry = Entry(
            self, textvariable=self.password_text, show='*', width=60)
        self.password_entry.grid(row=self.current_row, column=1, sticky='we')
        self.current_row += 1

        # Query status
        self.querystatus = Label(self, text='')
        self.querystatus.grid(row=self.current_row, column=0, columnspan=2)
        self.current_row += 1

        # Button for login action
        self.button = Button(
            self, text="Login", command= self.login)
        self.button.grid(row=self.current_row, column=0)
        self.current_row += 1

    def login(self):
        response = login_check(self.username_text.get(), self.password_text.get())
        if response:
            self.controller.show_frame('main_view')
        else:
           self.querystatus.configure(text='Incorrect Login Details')


class main_view(Frame):
    # Issues view of the app

    def __init__(self, parent, controller):
        # Function to initialize the components of the view
        Frame.__init__(self, parent)
        self.controller = controller
        self.initUI(parent, controller)

    def initUI(self, parent, controller):
        # Function to initialize the various frames

        # Frame one declaration
        self.frame_one = Frame(self, parent, bg='#FAEBD7')
        # self.frame_one.config(bg='#FAEBD7') #ANtique WHite 4
        self.frame_one.grid(row=0, column=0)

        # Frame two declaration
        self.frame_two = Frame(self, parent, bg='#fff0f5')
        # self.frame_two.config(bg='#fff0f5') #Lavender Blush 4
        self.frame_two.grid(row=1, column=0)

        # Canvas decalaration
        self.canvas = Canvas(self.frame_two)

        # List frame declaration
        self.list_frame = Frame(self.canvas)

        # Scrollbar declaration
        self.scrolllib = Scrollbar(
            parent, orient='vertical', command=self.canvas.yview)
        self.scrolllib.grid(row=0, column=1, sticky='nsew')
        self.canvas['yscrollcommand'] = self.scrolllib.set

        # Canvas window creation
        self.canvas.create_window((0, 0), window=self.list_frame, anchor='nw')

        # Binding of the scrolling function to the frame
        self.list_frame.bind('<Configure>', self.Auxscrollfunction)

        self.canvas.pack(side='left')

        # Frame three declaration
        self.frame_three = Frame(parent)
        # self.frame_three.config(bg='#8b8989') #snow 4
        self.frame_three.grid(row=0, column=0)


        self.populate()

        # Button declarations
        self.button_customer = Button(self.frame_one, text="Edit Customer",
                             command=lambda: controller.show_frame("GUI_Customer_Edit"))
        self.button_supplier = Button(
            self.frame_one, text="Edit Suppliers", command=lambda: controller.show_frame("GUI_Supplier_Edit"))
        self.button_product = Button(
            self.frame_one, text="Edit Products", command=lambda: controller.show_frame("GUI_Product_Edit"))
        self.button_order = Button(
            self.frame_one, text="Edit Orders", command=lambda: controller.show_frame("GUI_Orders_Edit"))
        self.button_refresh = Button(
            self.frame_one, text='Refesh', command=self.populate)

        # Button positioning
        self.button_customer.grid(row=0, column=0, sticky='w')
        self.button_supplier.grid(row=0, column=1)
        self.button_product.grid(row=0, column=2)
        self.button_order.grid(row=0, column=3)
        self.button_refresh.grid(row=0, column=4)

    def populate(self):
        # Function to populate the list view
        for widget in self.list_frame.winfo_children():
            widget.destroy()

        # Column labels
        self.customer_name = Label(
            self.list_frame, text='Customer Name', font='Helvetica 10 bold', width=10, wraplength=90)
        self.customer_name.grid(row=0, column=0)
        self.customer_phone = Label(self.list_frame, text='Customer Phone',
                                font='Helvetica 10 bold', width=10, wraplength=70)
        self.customer_phone.grid(row=0, column=1)
        self.order_total = Label(
            self.list_frame, text='Total', font='Helvetica 10 bold', width=10, wraplength=75)
        self.order_total.grid(row=0, column=2)
        self.product_name = Label(
            self.list_frame, text='Product Name', font='Helvetica 10 bold', width=15, wraplength=70)
        self.product_name.grid(row=0, column=3)
        self.order_date = Label(
            self.list_frame, text='Shipment Date', font='Helvetica 10 bold', width=10, wraplength=70)
        self.order_date.grid(row=0, column=4)
        self.supplier_name = Label(
            self.list_frame, text='Company Name', font='Helvetica 10 bold', width=20, wraplength=70)
        self.supplier_name.grid(row=0, column=5)

        data = relate_all()

        for index, dat in enumerate(data):
            Label(self.list_frame, text=dat[0]).grid(row=index + 1, column=0)
            Label(self.list_frame, text=dat[1]).grid(row=index + 1, column=1)
            Label(self.list_frame, text=dat[2]).grid(row=index + 1, column=2)
            Label(self.list_frame, text=dat[3]).grid(row=index + 1, column=3)
            Label(self.list_frame, text=dat[4]).grid(row=index + 1, column=4)
            Label(self.list_frame, text=dat[5]).grid(row=index + 1, column=5)

    def Auxscrollfunction(self, event):
        # Function for the scrolling of the canvas
        self.canvas.configure(scrollregion=self.canvas.bbox(
            'all'), width=650, height=300)

class GUI_Supplier_Edit(Frame):
    # Supplier editing options view of the app

    def __init__(self, parent, controller):
        # Function to initialize the components of the view
        Frame.__init__(self, parent)
        self.controller = controller

        self.current_row = 0  # Set the current row count of the view

        # Buttons declaration
        self.button_input = Button(
            self, text='Add supplier', command=lambda: controller.show_frame('GUI_Supplier_Input'))
        self.button_delete = Button(
            self, text='Remove supplier', command=lambda: controller.show_frame('GUI_Supplier_Remove'))
        self.button_back = Button(
            self, text='Back', command=lambda: controller.show_frame('main_view'))

        # Buttons positioning
        self.button_input.pack()
        self.button_delete.pack()
        self.button_back.pack(side='left')

class GUI_Supplier_Input(Frame):
    # Supplier input view for the app

    def __init__(self, parent, controller):
        # Function for initializing the components of the app
        Frame.__init__(self, parent)
        self.controller = controller

        self.current_row = 0  # Set the current row count of the view

        # Supplier0 Name field
        self.supplier_label = Label(self, text="Supplier Name: ")
        self.supplier_label.grid(row=self.current_row, column=0)
        self.supplier_text = StringVar()
        self.supplier_entry = Entry(self, textvariable=self.supplier_text)
        self.supplier_entry.grid(row=self.current_row, column=1)
        self.current_row += 1
        self.supplier_label = Label(self, text="Company Name:")
        self.supplier_label.grid(row=self.current_row, column=0)
        self.supplier_text2 = StringVar()
        self.supplier_entry = Entry(self, textvariable=self.supplier_text2)
        self.supplier_entry.grid(row=self.current_row,column=1)
        self.current_row += 1
        self.supplier_label = Label(self, text="Address: ")
        self.supplier_label.grid(row=self.current_row, column=0)
        self.supplier_text3 = StringVar()
        self.supplier_entry = Entry(self, textvariable=self.supplier_text3)
        self.supplier_entry.grid(row=self.current_row,column=1)
        self.current_row += 1
        self.supplier_label = Label(self, text="Phone: ")
        self.supplier_label.grid(row=self.current_row, column=0)
        self.supplier_text4 = StringVar()
        self.supplier_entry= Entry(self, textvariable=self.supplier_text4)
        self.supplier_entry.grid(row=self.current_row, column=1)
        self.current_row +=1


        # Query status
        self.querystatus = Label(self, text='')
        self.querystatus.grid(row=self.current_row, column=0, columnspan=2)
        self.current_row += 1

        # Button declaration
        self.button = Button(self, text='Back',
                        command=lambda: controller.show_frame("GUI_Supplier_Edit"))
        self.button_save = Button(self, text='Insert supplier', command=self.send_query)

        # Button positioning
        self.button_save.grid(row=self.current_row, column=0)
        self.button.grid(row=self.current_row, column=1)
        self.current_row += 1

    def send_query(self):
        # Function to pass on the details for insertion of the supplier
        supplier_name = self.supplier_text.get()
        company_name = self.supplier_text2.get()
        address=self.supplier_text3.get()
        phone=self.supplier_text4.get()
        response = insert_supplier(supplier_name,company_name,address,phone)
        self.querystatus.configure(text=response)

class GUI_Supplier_Remove(Frame):

    # Supplier removal view of the app

    def __init__(self, parent, controller):
        # Function for initializing the components of the app
        Frame.__init__(self, parent)
        self.controller = controller

        self.current_row = 0  # Set the current row count of the view

        # Supplier selection menu
        self.supplier_label = Label(self, text="Supplier: ")
        self.supplier_label.grid(row=self.current_row, column=0)
        self.supplier_text = StringVar(self)
        self.supplier_text.set('Choose a supplier')
        self.supplier_options = OptionMenu(
            self, self.supplier_text, *self.get_options())
        self.supplier_options.grid(row=self.current_row, column=1)
        self.supplier_refresh = Button(
            self, text='Refresh', command=self.update_supplier_option)  # Button for resfreshing the option menu
        self.supplier_refresh.grid(row=self.current_row, column=2)
        self.current_row += 1

        # Query status
        self.querystatus = Label(self, text='')
        self.querystatus.grid(row=self.current_row, column=0, columnspan=2)
        self.current_row += 1

        # Button declaration
        self.button_back = Button(self, text='Back',
                             command=lambda: controller.show_frame("GUI_Supplier_Edit"))
        self.button_remove = Button(self, text='Remove Supplier',
                               command=self.send_query)

        # Button positioning
        self.button_back.grid(row=self.current_row, column=0)
        self.button_remove.grid(row=self.current_row, column=1)
        self.current_row += 1

    def get_options(self):
        # Function to get the names of the existing supplier
        return supplier_names()


    def update_supplier_option(self):
        # Function to update the option menu
        menu = self.supplier_options['menu']
        menu.delete(0, 'end')
        for value in supplier_names():
            menu.add_command(
                 label=value, command=lambda v=value: self.supplier_text.set(v))

    def send_query(self):
        # Function to pass on the values for removal of the teams
        supplier_name = self.supplier_text.get()
        response = remove_supplier(supplier_name)
        self.querystatus.configure(text=response)

class GUI_Product_Edit(Frame):
    # Product editing options view of the app

    def __init__(self, parent, controller):
        # Function to initialize the components of the view
        Frame.__init__(self, parent)
        self.controller = controller

        self.current_row = 0  # Set the current row count of the view

        # Buttons declaration
        self.button_input = Button(
            self, text='Add product', command=lambda: controller.show_frame('GUI_Product_Input'))
        self.button_delete = Button(
            self, text='Remove product', command=lambda: controller.show_frame('GUI_Product_Remove'))
        self.button_back = Button(
            self, text='Back', command=lambda: controller.show_frame('main_view'))

        # Buttons positioning
        self.button_input.pack()
        self.button_delete.pack()
        self.button_back.pack(side='left')

class GUI_Product_Input(Frame):
    # product insertion view for the app

    def __init__(self, parent, controller):
        # Function for initializing the components of the app
        Frame.__init__(self, parent)
        self.controller = controller

        self.current_row = 0  # Set the current row count of the view

        # Product0 Name field
        self.product_label = Label(self, text="Product Name: ")
        self.product_label.grid(row=self.current_row, column=0)
        self.product_text = StringVar()
        self.product_entry = Entry(self, textvariable=self.product_text)
        self.product_entry.grid(row=self.current_row, column=1)
        self.current_row += 1
        self.product_label = Label(self, text="MRP: ")
        self.product_label.grid(row=self.current_row, column=0)
        self.product_text1 = StringVar()
        self.product_entry = Entry(self, textvariable=self.product_text1)
        self.product_entry.grid(row=self.current_row,column=1)
        self.current_row +=1
        self.product_label = Label(self, text="Supplier Name: ")
        self.product_label.grid(row=self.current_row, column=0)
        self.product_text2 = StringVar(self)
        self.product_text2.set('Choose the supplier name')
        self.product_options = OptionMenu(
            self, self.product_text2, *self.get_options())
        self.product_options.grid(row=self.current_row, column=1)
        self.product_refresh = Button(
            self, text='Refresh', command=self.update_product_option)  # Button for resfreshing the option menu
        self.product_refresh.grid(row=self.current_row, column=2)
        self.current_row += 1


        # Query status
        self.querystatus = Label(self, text='')
        self.querystatus.grid(row=self.current_row, column=0, columnspan=2)
        self.current_row += 1

        # Button declaration
        self.button = Button(self, text='Back',
                        command=lambda: controller.show_frame("GUI_Product_Edit"))
        self.button_save = Button(self, text='Insert product', command=self.send_query)

        # Button positioning
        self.button_save.grid(row=self.current_row, column=0)
        self.button.grid(row=self.current_row, column=1)
        self.current_row += 1

    def get_options(self):
        # Function to get the names of the existing suppliers
        return supplier_names()


    def update_product_option(self):
        # Function to update the option menu
        menu = self.product_options['menu']
        menu.delete(0, 'end')
        for value in supplier_names():
            menu.add_command(
                 label=value, command=lambda v=value: self.product_text2.set(v))

    def send_query(self):
        # Function to pass on the details for insertion of the product
        product_name = self.product_text.get()
        product_mrp = self.product_text1.get()
        product_supplierName = self.product_text2.get()
        response = insert_product(product_name,product_mrp,product_supplierName)
        self.querystatus.configure(text=response)

class GUI_Product_Remove(Frame):

    # Supplier removal view of the app

    def __init__(self, parent, controller):
        # Function for initializing the components of the app
        Frame.__init__(self, parent)
        self.controller = controller

        self.current_row = 0  # Set the current row count of the view

        # Product selection menu
        self.product_label = Label(self, text="Products: ")
        self.product_label.grid(row=self.current_row, column=0)
        self.product_text = StringVar(self)
        self.product_text.set('Choose a product')
        self.product_options = OptionMenu(
            self, self.product_text, *self.get_options())
        self.product_options.grid(row=self.current_row, column=1)
        self.supplier_refresh = Button(
            self, text='Refresh', command=self.update_product_option)  # Button for resfreshing the option menu
        self.supplier_refresh.grid(row=self.current_row, column=2)
        self.current_row += 1

        # Query status
        self.querystatus = Label(self, text='')
        self.querystatus.grid(row=self.current_row, column=0, columnspan=2)
        self.current_row += 1

        # Button declaration
        self.button_back = Button(self, text='Back',
                             command=lambda: controller.show_frame("GUI_Product_Edit"))
        self.button_remove = Button(self, text='Remove Product',
                               command=self.send_query)

        # Button positioning
        self.button_back.grid(row=self.current_row, column=0)
        self.button_remove.grid(row=self.current_row, column=1)
        self.current_row += 1

    def get_options(self):
        # Function to get the names of the existing products
        return product_names()


    def update_product_option(self):
        # Function to update the option menu
        menu = self.product_options['menu']
        menu.delete(0, 'end')
        for value in product_names():
            menu.add_command(
                label=value, command=lambda v=value: self.product_text.set(v))

    def send_query(self):
        # Function to pass on the values for removal of the products
        product_name = self.product_text.get()
        response = remove_product(product_name)
        self.querystatus.configure(text=response)

class GUI_Customer_Edit(Frame):
    # Customer editing options view of the app

    def __init__(self, parent, controller):
        # Function to initialize the components of the view
        Frame.__init__(self, parent)
        self.controller = controller

        self.current_row = 0  # Set the current row count of the view

        # Buttons declaration
        self.button_input = Button(
            self, text='Add customer', command=lambda: controller.show_frame('GUI_Customer_Input'))
        self.button_delete = Button(
            self, text='Remove customer', command=lambda: controller.show_frame('GUI_Customer_Remove'))
        self.button_back = Button(
            self, text='Back', command=lambda: controller.show_frame('main_view'))

        # Buttons positioning
        self.button_input.pack()
        self.button_delete.pack()
        self.button_back.pack(side='left')

class GUI_Customer_Input(Frame):
    # Customer input view for the app

    def __init__(self, parent, controller):
        # Function for initializing the components of the app
        Frame.__init__(self, parent)
        self.controller = controller

        self.current_row = 0  # Set the current row count of the view

        # Customer Name field
        self.customer_label = Label(self, text="Customer Name: ")
        self.customer_label.grid(row=self.current_row, column=0)
        self.customer_text = StringVar()
        self.customer_entry = Entry(self, textvariable=self.customer_text)
        self.customer_entry.grid(row=self.current_row, column=1)
        self.current_row += 1
        self.customer_label = Label(self, text="Phone Number: ")
        self.customer_label.grid(row=self.current_row, column=0)
        self.customer_text1 = StringVar()
        self.customer_entry = Entry(self, textvariable=self.customer_text1)
        self.customer_entry.grid(row=self.current_row,column=1)
        self.current_row +=1
        self.customer_label = Label(self, text="Delivery Address: ")
        self.customer_label.grid(row=self.current_row, column=0)
        self.customer_text2 = StringVar()
        self.customer_entry = Entry(self, textvariable=self.customer_text2)
        self.customer_entry.grid(row=self.current_row, column=1)
        self.current_row += 1
        self.customer_label = Label(self, text="Email ID: ")
        self.customer_label.grid(row=self.current_row, column=0)
        self.customer_text3 = StringVar()
        self.customer_entry = Entry(self, textvariable=self.customer_text3)
        self.customer_entry.grid(row=self.current_row, column=1)
        self.current_row += 1


        # Query status
        self.querystatus = Label(self, text='')
        self.querystatus.grid(row=self.current_row, column=0, columnspan=2)
        self.current_row += 1

        # Button declaration
        self.button = Button(self, text='Back',
                        command=lambda: controller.show_frame("GUI_Customer_Edit"))
        self.button_save = Button(self, text='Insert customer', command=self.send_query)

        # Button positioning
        self.button_save.grid(row=self.current_row, column=0)
        self.button.grid(row=self.current_row, column=1)
        self.current_row += 1

    def send_query(self):
        # Function to pass on the details for insertion of the customer
        customer_name = self.customer_text.get()
        customer_phone = self.customer_text1.get()
        customer_address = self.customer_text2.get()
        customer_email = self.customer_text3.get()
        response = insert_customer(customer_name,customer_phone,customer_address,customer_email)
        self.querystatus.configure(text=response)

class GUI_Customer_Remove(Frame):

    # Customer removal view of the app

    def __init__(self, parent, controller):
        # Function for initializing the components of the app
        Frame.__init__(self, parent)
        self.controller = controller

        self.current_row = 0  # Set the current row count of the view

        # Customer selection menu
        self.customer_label = Label(self, text="Customer: ")
        self.customer_label.grid(row=self.current_row, column=0)
        self.customer_text = StringVar(self)
        self.customer_text.set('Choose a customer')
        self.customer_options = OptionMenu(
            self, self.customer_text, *self.get_options())
        self.customer_options.grid(row=self.current_row, column=1)
        self.customer_refresh = Button(
            self, text='Refresh', command=self.update_customer_option)  # Button for resfreshing the option menu
        self.customer_refresh.grid(row=self.current_row, column=2)
        self.current_row += 1

        # Query status
        self.querystatus = Label(self, text='')
        self.querystatus.grid(row=self.current_row, column=0, columnspan=2)
        self.current_row += 1

        # Button declaration
        self.button_back = Button(self, text='Back',
                             command=lambda: controller.show_frame("GUI_Customer_Edit"))
        self.button_remove = Button(self, text='Remove Customer',
                               command=self.send_query)

        # Button positioning
        self.button_back.grid(row=self.current_row, column=0)
        self.button_remove.grid(row=self.current_row, column=1)
        self.current_row += 1

    def get_options(self):
        # Function to get the names of the existing customers
        return customer_names()


    def update_customer_option(self):
        # Function to update the option menu
        menu = self.customer_options['menu']
        menu.delete(0, 'end')
        for value in customer_names():
            menu.add_command(
                label=value, command=lambda v=value: self.customer_text.set(v))

    def send_query(self):
        # Function to pass on the values for removal of the customer
        customer_name = self.customer_text.get()
        response = remove_customer(customer_name)
        self.querystatus.configure(text=response)

class GUI_Orders_Edit(Frame):
    # Orders editing options view of the app

    def __init__(self, parent, controller):
        # Function to initialize the components of the view
        Frame.__init__(self, parent)
        self.controller = controller

        self.current_row = 0  # Set the current row count of the view

        # Buttons declaration
        self.button_input = Button(
            self, text='Add order', command=lambda: controller.show_frame('GUI_Orders_Input'))
        self.button_delete = Button(
            self, text='Remove order', command=lambda: controller.show_frame('GUI_Orders_Remove'))
        self.button_back = Button(
            self, text='Back', command=lambda: controller.show_frame('main_view'))

        # Buttons positioning
        self.button_input.pack()
        self.button_delete.pack()
        self.button_back.pack(side='left')

class GUI_Orders_Input(Frame):
    # Order input view for the app

    def __init__(self, parent, controller):
        # Function for initializing the components of the app
        Frame.__init__(self, parent)
        self.controller = controller

        self.current_row = 0  # Set the current row count of the view

        # Order Name field
        self.orders_label = Label(self, text="Customer Name: ")
        self.orders_label.grid(row=self.current_row, column=0)
        self.orders_text = StringVar(self)
        self.orders_text.set('Choose the customer name')
        self.orders_options = OptionMenu(
            self, self.orders_text, *self.get_options())
        self.orders_options.grid(row=self.current_row, column=1)
        self.current_row += 1
        self.orders_label = Label(self, text="Product Name: ")
        self.orders_label.grid(row=self.current_row, column=0)
        self.orders_text1 = StringVar(self)
        self.orders_text1.set('Choose the product name')
        self.orders_options = OptionMenu(
            self, self.orders_text1, *self.get_products())
        self.orders_options.grid(row=self.current_row, column=1)
        self.current_row +=1
        self.orders_label = Label(self, text="Shipment Date (YYYY-MM-DD): ")
        self.orders_label.grid(row=self.current_row, column=0)
        self.orders_text2 = StringVar()
        self.orders_entry = Entry(self, textvariable=self.orders_text2)
        self.orders_entry.grid(row=self.current_row, column=1)
        self.current_row += 1


        # Query status
        self.querystatus = Label(self, text='')
        self.querystatus.grid(row=self.current_row, column=0, columnspan=2)
        self.current_row += 1

        # Button declaration
        self.button = Button(self, text='Back',
                        command=lambda: controller.show_frame("GUI_Orders_Edit"))
        self.button_save = Button(self, text='Insert order', command=self.send_query)

        # Button positioning
        self.button_save.grid(row=self.current_row, column=0)
        self.button.grid(row=self.current_row, column=1)
        self.current_row += 1

    def get_products(self):
        # Function to get the names of the products
        return product_names()

    def get_options(self):
        # Function to get the names of the existing suppliers
        return customer_names()

    def send_query(self):
        # Function to pass on the details for insertion of the team
        orders_customername = self.orders_text.get()
        orders_productname = self.orders_text1.get()
        orders_date = self.orders_text2.get()
        response = insert_orders(orders_customername,orders_productname,orders_date)
        self.querystatus.configure(text=response)

class GUI_Orders_Remove(Frame):

    # Orders removal view of the app

    def __init__(self, parent, controller):
        # Function for initializing the components of the app
        Frame.__init__(self, parent)
        self.controller = controller

        self.current_row = 0  # Set the current row count of the view

        # Order selection menu
        self.orders_label = Label(self, text="Orders: ")
        self.orders_label.grid(row=self.current_row, column=0)
        self.orders_text = StringVar(self)
        self.orders_text.set('Choose the customer')
        self.orders_options = OptionMenu(
            self, self.orders_text, *self.get_options())
        self.orders_options.grid(row=self.current_row, column=1)
        self.supplier_refresh = Button(
            self, text='Refresh', command=self.update_orders_option)  # Button for resfreshing the option menu
        self.supplier_refresh.grid(row=self.current_row, column=2)
        self.current_row += 1

        # Query status
        self.querystatus = Label(self, text='')
        self.querystatus.grid(row=self.current_row, column=0, columnspan=2)
        self.current_row += 1

        # Button declaration
        self.button_back = Button(self, text='Back',
                             command=lambda: controller.show_frame("GUI_Orders_Edit"))
        self.button_remove = Button(self, text='Remove Orders',
                               command=self.send_query)

        # Button positioning
        self.button_back.grid(row=self.current_row, column=0)
        self.button_remove.grid(row=self.current_row, column=1)
        self.current_row += 1

    def get_options(self):
        # Function to get the names of the existing teams
        return order_customer_names()


    def update_orders_option(self):
        # Function to update the option menu
        menu = self.orders_options['menu']
        menu.delete(0, 'end')
        for value in order_customer_names():
            menu.add_command(
                label=value, command=lambda v=value: self.orders_text.set(v))

    def send_query(self):
        # Function to pass on the values for removal of the teams
        orders_name = self.orders_text.get()
        response = remove_orders(orders_name)
        self.querystatus.configure(text=response)


window = E_Kart()
window.title("E-Kart")


window.mainloop()
