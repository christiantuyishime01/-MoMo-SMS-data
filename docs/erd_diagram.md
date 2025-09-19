# ERD: MoMo SMS Data System (Week 2)

## Visual ERD Diagram
The ERD diagram has been created and shows the complete database design with all entities, relationships, and foreign key constraints.

- Diagram file: `docs/erd_diagram.png` (saved in repository)
- Source: dbdiagram.io
- Status: ✅ Complete

## Text-Based ERD Structure

```
┌─────────────────────────────────────┐
│              USERS                  │
├─────────────────────────────────────┤
│ user_id (PK) - INT AUTO_INCREMENT   │
│ phone_number - VARCHAR(15) UNIQUE   │
│ full_name - VARCHAR(100)            │
│ account_status - ENUM('active',     │
│                      'suspended')   │
│ created_at - DATETIME               │
└─────────────────────────────────────┘
                    │
                    │ 1:M
                    │
┌─────────────────────────────────────┐
│           TRANSACTIONS              │
├─────────────────────────────────────┤
│ transaction_id (PK) - INT AUTO_INC  │
│ amount - DECIMAL(15,2)              │
│ currency - VARCHAR(3) DEFAULT 'RWF' │
│ timestamp - DATETIME                 │
│ transaction_type - ENUM('send',     │
│                        'receive',  │
│                        'pay',       │
│                        'withdraw')  │
│ status - ENUM('completed',          │
│              'pending',             │
│              'failed')              │
│ sender_phone - VARCHAR(15)          │
│ receiver_phone - VARCHAR(15)        │
│ reference_number - VARCHAR(50)      │
│ category_id (FK) - INT               │
│ raw_message_id (FK) - INT           │
│ created_at - DATETIME               │
└─────────────────────────────────────┘
                    │
                    │ M:1
                    │
┌─────────────────────────────────────┐
│      TRANSACTION_CATEGORIES         │
├─────────────────────────────────────┤
│ category_id (PK) - INT AUTO_INC     │
│ category_name - VARCHAR(50) UNIQUE  │
│ description - TEXT                  │
│ rule_pattern - VARCHAR(200)         │
│ created_at - DATETIME               │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│           RAW_MESSAGES              │
├─────────────────────────────────────┤
│ message_id (PK) - INT AUTO_INC      │
│ raw_content - TEXT                  │
│ parsed_at - DATETIME                │
│ processing_status - ENUM('pending', │
│                         'processed',│
│                         'failed')   │
│ created_at - DATETIME               │
└─────────────────────────────────────┘
                    │
                    │ 1:1
                    │
┌─────────────────────────────────────┐
│           SYSTEM_LOGS              │
├─────────────────────────────────────┤
│ log_id (PK) - INT AUTO_INC          │
│ level - ENUM('INFO', 'WARN',        │
│             'ERROR', 'DEBUG')       │
│ message - TEXT                      │
│ context_json - JSON                 │
│ transaction_id (FK) - INT NULL      │
│ created_at - DATETIME               │
└─────────────────────────────────────┘
```

## Key Relationships

1. **Users → Transactions (1:M)**: One user can have many transactions as sender/receiver
2. **Transactions → Categories (M:1)**: Many transactions belong to one category
3. **Transactions → Raw_Messages (1:1)**: Each transaction links to one raw SMS message
4. **Transactions → System_Logs (1:M)**: One transaction can generate multiple log entries

## Design Rationale (200–300 words)

This ERD design prioritizes data integrity and query performance for MoMo SMS transaction analysis. The core `TRANSACTIONS` table centralizes all financial data with proper normalization, separating user information into a dedicated `USERS` table to avoid redundancy and enable user-based analytics.

The `TRANSACTION_CATEGORIES` table supports flexible transaction classification through rule-based patterns, allowing the system to automatically categorize transactions based on SMS content analysis. The `RAW_MESSAGES` table preserves original SMS data for audit trails and reprocessing capabilities.

Foreign key constraints ensure referential integrity, while strategic indexes on frequently queried columns (timestamp, phone numbers, status) optimize performance. The `SYSTEM_LOGS` table with JSON context enables comprehensive debugging and monitoring of the ETL pipeline.

This design supports both operational queries (transaction lookups, user history) and analytical queries (aggregate reports, trend analysis) while maintaining data consistency and supporting future scalability requirements.

## Design Explanation: Making Sense of the Money Moves

Imagine our database is like a well-organized office that tracks every mobile money transaction. We've created different filing cabinets (tables) for different types of information so that everything has its place and is easy to find.

First, we have the **Users cabinet**. This is our address book. It holds the essential info for every customer—their unique phone number, name, and account status. The user_id is like giving each person their own employee ID number; it's a simple, unique way to identify them across our entire system.

Next is the main **Transactions cabinet**, the heart of our operation. Every time money is sent or received, we file a record here. But instead of writing out the sender's and receiver's full details every single time, we simply write down their user_id (like referencing their employee ID). This creates a smart, efficient link back to the Users cabinet. We do the same thing for the category_id and message_id, which point to their own specialized cabinets. This prevents duplicate information and keeps everything consistent. The reference_number acts as a unique tracking number for each transaction, much like a receipt number.

The **Transaction_Categories cabinet** is our rulebook. It helps us understand the type of each transaction, like "cash deposit," "bill payment," or "money transfer." Each category can have its own rule pattern, which is like a set of instructions for our system on how to handle that specific kind of transaction.

The **Raw_Messages cabinet** is our "Inbox." It stores the original, unedited text messages (SMS) that come in from the telecom network before our system translates them. Once a message is processed, we update its status and timestamp it.

Finally, the **System_Logs cabinet** is our security guard and secretary. It keeps a detailed diary of everything that happens in our system—successes, errors, and warnings. This is crucial for troubleshooting problems and maintaining a clear audit trail.

## Change Log

- v0.1 scaffold added (placeholders only)
- v0.2 added text-based ERD structure with entities and relationships

