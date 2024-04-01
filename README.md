# Online-Automotive-Dealership-System
Introduction

 	Having a platform where cars, trucks, and other vehicles may be sold online is essential in today's intensely competitive automotive dealer market. An automotive dealers management system was created to manage the store and sell automobiles online. An automobile store's staff can use this application to manage customers' orders and make it easier for customers to place their own. By categories, the vehicles in the shop are arranged. Each car is assigned a category, name, cost, and description.  The staff can log in and manage the category details, product details, customer details, and order details along with the information about order date and time, bill amount,  payment status, and delivery status. The following customer information will be maintained: Cust-Id, Name,  Delivery Address, Phone number, and Email. The customer must register and log in to access the product page with the automobiles listed. The main point of developing this system is to help Dealers to manage their business and help customers with online ordering.
Features

●	Login – This module is used for admin login.
●	Logout Functionality
●	Dashboard – Admin dashboard related to all Car, Car details.
●	Car Management Module
○	Adding New Car Details
○	Edit the Exiting Car Details
○	View all the details of the Car
○	Listing of all Car
●	Order Management Module
○	Adding New Order Details
○	Edit the Exiting Order Details
○	View all the details of the Order
●	Test Drive Management Module
○	Adding New test drive Details
○	Edit the Exiting test drive Details
○	View all the details of the test drives
Technologies

●	HTML: The page layout has been designed in HTML
●	CSS: CSS has been used for all the designing part
●	JavaScript: All the validation task and animations has been developed by JavaScript
●	Python: All the business logic has been implemented in Python
●	NoSQL: NoSQL database has been used as a database for the project
●	Django: Project has been developed over the Django Framework

Purpose of the Database

The purpose of the database in this automotive dealer management system is to store and manage essential data related to vehicles, customers, orders, and test drives. It serves as the backbone of the system, facilitating data retrieval, storage, and manipulation. The database is needed to:
●	Store vehicle details: This includes information such as category, name, cost, and description of each vehicle, which is crucial for listing and managing the inventory of the automotive dealer.
●	Store customer information: It should maintain customer data, including Cust-Id, Name, Delivery Address, Phone number, and Email, enabling the system to associate customers with their orders and contact them for updates or promotions.
●	Store order details: The database should record order information, including order date and time, bill amount, payment status, and delivery status. This allows for order tracking and financial management.
●	Store test drive details: It should also keep track of test drive information, such as the date, time, and details of the test drive. This is important for managing and scheduling test drives for potential customers.
Users and Information Needs
Dealer: They need access to all modules of the system for managing the inventory, orders, and test drives. They require the ability to add, edit, and view car details, order details, and test drive details. They also need access to the admin dashboard for an overview of the system's performance.

Customers: They need access to the product page with a list of automobiles for sale. They must register and log in to place orders. Customers also want to view their order history and, if applicable, schedule test drives.
Problem:

1.	Efficiently manage and organize vehicle inventory.
2.	Streamline the ordering process for customers.
3.	Enable administrators to track and manage orders, including payment and delivery status.
4.	Facilitate scheduling and tracking of test drives.
5.	Provide a user-friendly interface for both customers and administrators.
Input Data Available to the Database
●	Vehicle details: Category, name, cost, description.
●	Customer information: Cust-Id, Name, Delivery Address, Phone number, Email.
●	Order details: Order date and time, bill amount, payment status, delivery status.
●	Test drive details: Date, time, and related information for test drive scheduling.
AWS Deployment :

1.	Amazon EC2 (Elastic Compute Cloud):
a.	EC2 instances will host our Django application. 
2.	Amazon RDS (Relational Database Service):
a.	RDS is used to host our database. 
3.	Amazon VPC (Virtual Private Cloud):
a.	Set up a Virtual Private Cloud to isolate our resources and provide network-level security.
4.	Amazon Route 53:
a.	Use Route 53 for domain registration and DNS management. It can route incoming traffic to your EC2 instances.
5.	AWS Identity and Access Management (IAM):
a.	Create IAM roles and policies to control access and permissions for AWS resources.
6.	Elastic IP  address
a.	Amazon EC2 instance will have a public IP address 
