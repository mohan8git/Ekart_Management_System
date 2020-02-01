# E-kart 
A python project for interacting with a database(SQL) using tkinter

# Overview
It is a simple TkInter project written in python 3 to create a interface for the MySQL database. It allows insertion and deletion to the various tables present in the database.

# Packages Installed
  * PyMySQL==0.9.2
  
# Database structure
The project contains the following tables -

 * admin : This table contains the login credentials
 * customer : This table contains information about the customers
 * products : This table contains all the necessary information regarding the product
 * supplier : This table contains all the necessary inforamtion regarding the supplier of hte products
 * orders : This table contains all the information of the orders which the customers have made

# Admin table structure
|Field|Type|Null|Key|Default|Extra|
|-----|----|----|---|-------|-----|
|id|int(11)|NO|PRI|NULL|AUTO_INCREMENT|
|username|varchar(20)|NO|UNI|NULL||
|password|varchar(20)|YES||NULL||

# Customer table structure
|Field|Type|Null|Key|Default|Extra|
|-----|----|----|---|-------|-----|
|customer_id|int|NO|PRI|NULL|AUTO_INCREMENT|
|customer_name|varchar(50)|YES||NULL||
|delivery_address|varchar(70)|YES||NULL||
|phone|int(11)|YES||NULL||
|email|varchar(70)|YES||NULL||

# Supplier table struture
|Field|Type|Null|Key|Default|Extra|
|-----|----|----|---|-------|-----|
|supplier_id|int|NO|PRI|NULL|AUTO_INCREMENT|
|company_name|varchar(50)|YES||NULL||
|contact_name|varchar(50)|YES||NULL||
|address|varchar(70)|YES||NULL||
|phone|int(11)|YES||NULL||

# Products table structure
|Field|Type|Null|Key|Default|Extra|
|-----|----|----|---|-------|-----|
|product_id|int|NO|PRI|NULL|AUTO_INCREMENT|
|product_name|varchar(50)|YES||NULL||
|supplier_id|int|NO|FORGN|NULL||
|MRP|float(6,2)|YES||NULL||

# Orders table structure
|Field|Type|Null|Key|Default|Extra|
|-----|----|----|---|-------|-----|
|order_id|int|NO|PRI|NULL|AUTO_INCREMENT|
|customer_id|int|NO|FORGN|NULL||
|product_id|int|NO|FORGN|NULL||
|Total|float(6,2)|YES||NULL||
|Shipment_date|date|YES||NULL||
