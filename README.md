# MoMo SMS Data Processor

## Team Members
- Kevin Nizeyimana
- Arnaud Manzi Ineza
- Tuyishime Christian
- Katsia Teta
- Karigirwa Ange

## Project Description
Enterprise-level full-stack application for processing Mobile Money (MoMo) SMS data in XML format. The system does not function fully due to the empty files that does not contain data.

## System Architecture
[https://drive.google.com/file/d/1Xa7DOjepNgDx9xvPfTrK3o_vju3nNNQe/view?usp=sharing]

## Features
- XML data parsing and processing

## Scrum Board
[https://github.com/users/christiantuyishime01/projects/3/views/1]


## Week 2: Database Design and Implementation

- ERD diagram: see `docs/erd_diagram.md` and commit your PNG/PDF in `docs/`.
- SQL setup script: `database/database_setup.sql` (author schema per ERD; include sample data and indexes).
- JSON examples: `examples/json_schemas.json` (team-authored serialization examples).
- AI Usage Log: `AI_USAGE.md`.

### Design Explanation: Making Sense of the Money Moves

Imagine our database is like a well-organized office that tracks every mobile money transaction. We've created different filing cabinets (tables) for different types of information so that everything has its place and is easy to find.

First, we have the **Users cabinet**. This is our address book. It holds the essential info for every customer—their unique phone number, name, and account status. The user_id is like giving each person their own employee ID number; it's a simple, unique way to identify them across our entire system.

Next is the main **Transactions cabinet**, the heart of our operation. Every time money is sent or received, we file a record here. But instead of writing out the sender's and receiver's full details every single time, we simply write down their user_id (like referencing their employee ID). This creates a smart, efficient link back to the Users cabinet. We do the same thing for the category_id and message_id, which point to their own specialized cabinets. This prevents duplicate information and keeps everything consistent. The reference_number acts as a unique tracking number for each transaction, much like a receipt number.

The **Transaction_Categories cabinet** is our rulebook. It helps us understand the type of each transaction, like "cash deposit," "bill payment," or "money transfer." Each category can have its own rule pattern, which is like a set of instructions for our system on how to handle that specific kind of transaction.

The **Raw_Messages cabinet** is our "Inbox." It stores the original, unedited text messages (SMS) that come in from the telecom network before our system translates them. Once a message is processed, we update its status and timestamp it.

Finally, the **System_Logs cabinet** is our security guard and secretary. It keeps a detailed diary of everything that happens in our system—successes, errors, and warnings. This is crucial for troubleshooting problems and maintaining a clear audit trail.

### Week 2 Deliverables Status:
- ✅ **ERD Design**: Complete with visual diagram and documentation
- ✅ **SQL Implementation**: Complete MySQL database with constraints and sample data
- ✅ **JSON Modeling**: Complete serialization examples and mapping documentation
- ✅ **Team Collaboration**: Repository updated with all deliverables

### Next Steps:
- [ ] Save ERD diagram as PNG/PDF in `docs/` folder
- [ ] Create Database Design Document (PDF) with screenshots
- [ ] Update Scrum board with completed tasks
- [ ] Run sample queries and capture screenshots for documentation
