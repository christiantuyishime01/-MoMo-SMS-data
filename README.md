
MoMo SMS Data Processor
An enterprise-level full-stack application designed to process and manage Mobile Money (MoMo) transaction data received via SMS in XML format. This system parses, stores, and structures transactional data for reporting, analytics, and user management.

Team Members
Kevin Nizeyimana

Arnaud Manzi Ineza

Tuyishime Christian

Katsia Teta

Karigirwa Ange

Project Overview
Many mobile money transactions in Rwanda are confirmed via SMS. These messages contain structured XML data that must be parsed, validated, and stored for further processing. This system serves as a backbone for capturing, categorizing, and logging these transactions in a reliable and scalable database.

 System Architecture
For a detailed overview of the system design, refer to the Architecture Diagram.

 Key Features
XML-based SMS parsing and validation

Transaction categorization and user management

Robust logging and error handling

RESTful JSON API for front-end integration

Scalable relational database design

  
 
Database Design & Implementation 
Completed Tasks:
ERD Design: Designed a detailed Entity-Relationship Diagram identifying core entities like Users, Transactions, Categories, and Logs.

SQL Scripts: Full MySQL implementation with constraints, indexes, and sample data.

JSON Serialization: Sample JSON structures demonstrating API response format.

Team Collaboration: All deliverables committed and organized via GitHub.

Design Philosophy:
We structured the database like a well-organized office:

Users is our address book 

Transactions is the main ledger 

Transaction_Categories is the rulebook 

Raw_Messages is the inbox 

System_Logs is the security log 

Using foreign keys (like user_id or category_id), we link these tables efficiently—avoiding duplication and ensuring data integrity.

How to Set Up the Database

Clone the repository

Navigate to the database/ folder

Run the SQL script in your MySQL environment:


mysql -u your_username -p < database_setup.sql

Verify sample data is inserted correctly

Use the sample queries (included) to test CRUD operations
