import pymysql


def login_check(username, password):
    # Function to check the login details
    try:
        con = pymysql.connect(user='root',
                              db='database',
                              password='',
                              charset='utf8mb4',
                              cursorclass=pymysql.cursors.DictCursor)
        cur = con.cursor()
        cur.execute('SELECT username, password from adminx')
        data = cur.fetchall()
        users = {}
        for dic in data:
            users[dic['username']] = dic['password']
        if users[username] == password:
            return True
        else:
            return False
    except Exception as e:
        return False

def relate_all():
    # Fucntion to provide the bsae view of the app
    try:
        con = pymysql.connect(user='root',
                              db='localhost',
                              password='',
                              charset='utf8mb4')
        cur = con.cursor()
        cur.execute("SELECT customer_name, customer.phone, Total, product_name, Shipment_date, company_name " 
                    "FROM customer, orders, products, supplier WHERE customer.customer_id = orders.customer_id AND "
                    "orders.product_id = products.product_id AND products.supplier_id = supplier.supplier_id;")  # SQL
        # query to join the tables to get the necessary details
        data = cur.fetchall()
        con.close()
        return data
    except Exception as e:
        raise Exception(str(e))

def insert_supplier(supplier_name,company_name,address,phone):
    # Function to insert the specified supplier
    try:
        con = pymysql.connect(user='root',
                              db='localhost',
                              password='',
                              charset='utf8mb4',
                              cursorclass=pymysql.cursors.DictCursor)
        cur = con.cursor()
        cur.execute("INSERT INTO supplier(contact_name,company_name,address,phone) values(%s,%s,%s,%s)",
                    (supplier_name,company_name,address,phone))  # SQL query to insert supplier
        con.commit()
        con.close()
        return "Successfully added \'" + supplier_name + "\'" + company_name +"\'"
    except Exception as e:
        return str(e)

def supplier_names():
    # Function to get the supplier names
    try:
        con = pymysql.connect(user='root',
                              db='localhost',
                              password= '',
                              charset='utf8mb4',
                              cursorclass=pymysql.cursors.DictCursor)
        cur = con.cursor()
        cur.execute("SELECT company_name FROM supplier")
        data = cur.fetchall()
        names = []
        if data:
            for dic in data:
                names.append(dic['company_name'])
        else:
            names = ['Placeholder']
        con.commit()
        con.close()
        return names
    except Exception as e:
        raise Exception(str(e))

def remove_supplier(supplier_name):
    # Function to remove the specified supplier
    try:
        con = pymysql.connect(user='root',
                              db='localhost',
                              password='',
                              charset='utf8mb4',
                              cursorclass=pymysql.cursors.DictCursor)
        cur = con.cursor()
        cur.execute("DELETE from supplier where company_name=\"" +
                    supplier_name + "\"")  # SQL query to remove the product
        con.commit()
        con.close()
        return "Successfully removed \'" + supplier_name + "\'"
    except Exception as e:
        return str(e)

def insert_product(product_name,product_mrp,product_supplierName):
    # Function to insert the specified product
    try:
        con = pymysql.connect(user='root',
                              db='localhost',
                              password='',
                              charset='utf8mb4',
                              cursorclass=pymysql.cursors.DictCursor)

        supid = con.cursor()
        supid.execute("Select supplier_id,company_name from supplier")
        data = supid.fetchall()
        prod = {}
        for dic in data:
            prod[dic['company_name']] =  dic['supplier_id']

        supid.execute("INSERT INTO products(product_name, supplier_id, MRP) VALUES(%s,%s, %s)",
            (product_name, prod[product_supplierName], product_mrp))
        con.commit()
        con.close()
        return "Successfully added \'" + product_name + "\'" + product_mrp +"\'"
    except Exception as e:
        return str(e)


def product_names():
    # Function to get the product names
    try:
        con = pymysql.connect(user='root',
                              db='localhost',
                              password= '',
                              charset='utf8mb4',
                              cursorclass=pymysql.cursors.DictCursor)

        cur = con.cursor()
        cur.execute("SELECT product_name FROM products")
        data = cur.fetchall()
        names = []
        if data:
            for dic in data:
                names.append(dic['product_name'])
        else:
            names = ['Placeholder']
        con.commit()
        con.close()
        return names
    except Exception as e:
        raise Exception(str(e))

def remove_product(product_name):
    # Function to remove the specified product
    try:
        con = pymysql.connect(user='root',
                              db='localhost',
                              password='',
                              charset='utf8mb4',
                              cursorclass=pymysql.cursors.DictCursor)
        cur = con.cursor()
        cur.execute("DELETE from products where product_name=\"" +
                    product_name + "\"")  # SQL query to remove the product
        con.commit()
        con.close()
        return "Successfully removed \'" + product_name + "\'"
    except Exception as e:
        return str(e)

def customer_names():
    # Function to get the customer names
    try:
        con = pymysql.connect(user='root',
                              db='localhost',
                              password= '',
                              charset='utf8mb4',
                              cursorclass=pymysql.cursors.DictCursor)
        cur = con.cursor()
        cur.execute("SELECT customer_name FROM customer")
        data = cur.fetchall()
        names = []
        if data:
            for dic in data:
                names.append(dic['customer_name'])
        else:
            names = ['Placeholder']
        con.commit()
        con.close()
        return names
    except Exception as e:
        raise Exception(str(e))

def order_customer_names():
    # Function to get the names of the customers who gave the order
    try:
        con = pymysql.connect(user='root',
                              db='localhost',
                              password='',
                              charset='utf8mb4',
                              cursorclass=pymysql.cursors.DictCursor)
        cur = con.cursor()
        cur.execute("SELECT customer_name FROM customer,orders WHERE orders.customer_id = customer.customer_id")
        data = cur.fetchall()
        names = []
        if data:
            for dic in data:
                names.append(dic['customer_name'])
        else:
            names = ['Placeholder']
        con.commit()
        con.close()
        return names
    except Exception as e:
        raise Exception(str(e))


def insert_customer(customer_name,customer_phone,customer_address,customer_email):
    # Function to insert the specified customer
    try:
        con = pymysql.connect(user='root',
                              db='localhost',
                              password='',
                              charset='utf8mb4',
                              cursorclass=pymysql.cursors.DictCursor)
        cur = con.cursor()
        cur.execute("INSERT INTO customer(customer_name,phone,delivery_address,email) values(%s,%s,%s,%s)",
                    (customer_name,customer_phone,customer_address,customer_email))  # SQL query to insert customer
        con.commit()
        con.close()
        return "Successfully added \'" + customer_name + "\'"
    except Exception as e:
        return str(e)

def remove_customer(customer_name):
    # Function to remove the specified customer
    try:
        con = pymysql.connect(user='root',
                              db='localhost',
                              password='',
                              charset='utf8mb4',
                              cursorclass=pymysql.cursors.DictCursor)
        cur = con.cursor()
        cur.execute("DELETE from customer where customer_name=\"" +
                    customer_name + "\"")  # SQL query to remove the customer
        con.commit()
        con.close()
        return "Successfully removed \'" + customer_name + "\'"
    except Exception as e:
        return str(e)

def orders_names():
    # Function to get the orders names
    try:
        con = pymysql.connect(user='root',
                              db='localhost',
                              password= '',
                              charset='utf8mb4',
                              cursorclass=pymysql.cursors.DictCursor)
        cur = con.cursor()
        cur.execute("SELECT order_id FROM orders")
        data = cur.fetchall()
        names = []
        if data:
            for dic in data:
                names.append(dic['order_id'])
        else:
            names = ['Placeholder']
        con.commit()
        con.close()
        return names
    except Exception as e:
        raise Exception(str(e))

def insert_orders(orders_customername,orders_productname,orders_date):
    # Function to insert the specified order
    try:
        con = pymysql.connect(user='root',
                              db='localhost',
                              password='',
                              charset='utf8mb4',
                              cursorclass=pymysql.cursors.DictCursor)

        cur = con.cursor()
        cur.execute("SELECT customer_id,customer_name FROM customer")
        cndata = cur.fetchall()
        cn = {}
        for dic in cndata:
            cn[dic['customer_name']] = dic['customer_id']
        cur.execute("SELECT product_id,product_name FROM products")
        prdata = cur.fetchall()
        pr = {}
        for dic in prdata:
            pr[dic['product_name']] = dic['product_id']
        cur.execute("SELECT product_name,MRP FROM products")
        totdata = cur.fetchall()
        tot = {}
        for dic in totdata:
            tot[dic['product_name']] = dic['MRP']

        cur.execute("INSERT INTO orders(customer_id,product_id,Shipment_date,Total) VALUES (%s,%s,%s,%s)",
                    (cn[orders_customername],pr[orders_productname],orders_date,tot[orders_productname]))
        con.commit()
        con.close()
        return "Successfully added \'" + orders_customername + "\'" + orders_productname +"\'"
    except Exception as e:
        return str(e)

def remove_orders(orders_name):
    # Function to remove the specified order
    try:
        con = pymysql.connect(user='root',
                              db='localhost',
                              password='',
                              charset='utf8mb4',
                              cursorclass=pymysql.cursors.DictCursor)
        cur = con.cursor()
        cur.execute("SELECT customer_name,customer_id FROM customer")
        data = cur.fetchall()
        custo = {}
        for dic in data:
            custo[dic['customer_name']] = dic['customer_id']
        cur.execute("DELETE from orders where customer_id = %s",custo[orders_name])  # SQL query to remove the order
        con.commit()
        con.close()
        return "Successfully removed \'" + orders_name + "\'"
    except Exception as e:
        return str(e)