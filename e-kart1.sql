create database ekart;
use ekart;

create table adminx ( id int not null primary key,
					 username varchar(20) not null unique,
                     password varchar(20));
insert into adminx 
values
(01,'mohit','zzz'),
(02,'anmol','xxx'),
(03,'charan','yyy');
alter table adminx modify column id int auto_increment;
insert into adminx (username,password) values('anuj','aaa');

create table supplier ( supplier_id int not null primary key auto_increment,
						company_name varchar(30),
                        contact_name varchar(30),
                        address varchar(50),
                        phone int(10));
                        
insert into supplier (company_name,contact_name,address,phone)
values
('Globe Telcome','Divij','West Enclave New-Delhi', 1234567800),
('China Homes','Ajay','Modi Nagar New-Delhi', 465123780),
('Plc Technology','Prakhar','Potheri Chennai', 741258960),
('Acp Technology','Aniket','Bank-colony Uttar Pradesh',965478201);


create table products ( product_id int not null primary key auto_increment,
						product_name varchar(20),
                        supplier_id int,
                        MRP float(6,2),
                        foreign key (supplier_id) references supplier(supplier_id));
                        
insert into products (product_name,supplier_id,MRP)
values
('Vista',1,2000),
('Chalk Talk',2,500),
('fire floss',2,700),
('ecake',3,1000),
('deal light',4,800),
('magiCoil',3,600),
('page gear',4,450),
('gluid',1,200),
('feather lace',2,100);


create table customer ( customer_id int not null primary key auto_increment,
						name varchar(20),
                        delivery_address varchar(30),
                        phone int(10),
                        email varchar(30));
                        
insert into customer (name,delivery_address,phone,email)
values
('Sheena','Karol Bagh New Delhi',987658912,'sheena011@gmail.com'),
('Amit','Pitampura New Delhi',65482179,'amit067@gmail.com'),
('Robin','Egmore Chennai',36521478,'robin77@gmail.com'),
('Chirag','Darshan Vihar Uttar Pradesh',41852063,'chirag44@gmail.com'),
('Athira','Shivaji Puram Kerala',12597460,'athira66@gmail.com');

create table orders ( order_id int not null primary key auto_increment,
					  customer_id int,
                      product_id int,
                      Total int,
                      Shipment_date date,
                      foreign key (customer_id) references customer (customer_id),
                      foreign key (product_id) references products (product_id));
update orders
	set Total = (
		Select MRP
        from products
        where orders.product_id = products.product_id);
        
insert into orders (customer_id,product_id,Shipment_date)
values
(1,4,'2008-02-11'),
(2,7,'2008-04-18'),
(3,6,'2008-09-22'),
(4,2,'2007-01-31'),
(2,1,'2007-10-25'),
(5,3,'2007-06-22');

Create trigger after_insert_total
after insert on orders
for each row
update orders
set orders.Total = products.MRP
where orders.product_id = products.product_id;

Create trigger after_insert_id
after insert on orders
for each row
update orders
set orders.supplier_id = products.supplier_id
where orders.product_id = products.product_id;

insert into orders (customer_id,product_id,Shipment_date)
values
(1,12,'2016-02-22');






