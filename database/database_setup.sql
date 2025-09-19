-- =====================================================
-- MoMo SMS Data Processing System - Database Setup
-- Week 2: Database Design and Implementation
-- =====================================================

-- Create database (optional if managed externally)
CREATE DATABASE IF NOT EXISTS momo_sms;
USE momo_sms;

-- =====================================================
-- DDL STATEMENTS - TABLE CREATION
-- =====================================================

-- Users table - Customer information
CREATE TABLE Users (
    user_id INT AUTO_INCREMENT PRIMARY KEY COMMENT 'Unique user identifier',
    phone_number VARCHAR(15) UNIQUE NOT NULL COMMENT 'User phone number (international format)',
    full_name VARCHAR(100) COMMENT 'User full name',
    account_status ENUM('active', 'suspended', 'inactive') DEFAULT 'active' COMMENT 'Account status',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT 'Account creation timestamp'
) ENGINE=InnoDB COMMENT='User accounts and customer information';

-- Transaction Categories table - Transaction type classification
CREATE TABLE Transaction_Categories (
    category_id INT AUTO_INCREMENT PRIMARY KEY COMMENT 'Unique category identifier',
    category_name VARCHAR(50) NOT NULL UNIQUE COMMENT 'Category name (e.g., Transfer, Payment)',
    description TEXT COMMENT 'Detailed category description',
    rule_pattern VARCHAR(200) COMMENT 'Regex pattern for automatic categorization'
) ENGINE=InnoDB COMMENT='Transaction type categories and classification rules';

-- Raw Messages table - Original SMS data
CREATE TABLE Raw_Messages (
    message_id INT AUTO_INCREMENT PRIMARY KEY COMMENT 'Unique message identifier',
    raw_content TEXT NOT NULL COMMENT 'Original SMS message content',
    parsed_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT 'Message parsing timestamp',
    processing_status ENUM('pending', 'processed', 'failed', 'ignored') DEFAULT 'pending' COMMENT 'Processing status'
) ENGINE=InnoDB COMMENT='Raw SMS messages for audit and reprocessing';

-- Transactions table - Main transaction records
CREATE TABLE Transactions (
    transaction_id INT AUTO_INCREMENT PRIMARY KEY COMMENT 'Unique transaction identifier',
    sender_id INT COMMENT 'Sender user ID (can be NULL for external senders)',
    receiver_id INT COMMENT 'Receiver user ID (can be NULL for external receivers)',
    category_id INT NOT NULL COMMENT 'Transaction category ID',
    message_id INT UNIQUE COMMENT 'Associated raw message ID',
    amount DECIMAL(15,2) NOT NULL CHECK (amount >= 0) COMMENT 'Transaction amount (non-negative)',
    currency VARCHAR(3) DEFAULT 'RWF' COMMENT 'Currency code (ISO 4217)',
    timestamp DATETIME NOT NULL COMMENT 'Transaction timestamp',
    transaction_type ENUM('send', 'receive', 'pay', 'withdraw', 'deposit', 'transfer') NOT NULL COMMENT 'Transaction type',
    status ENUM('completed', 'pending', 'failed', 'cancelled') DEFAULT 'pending' COMMENT 'Transaction status',
    reference_number VARCHAR(50) UNIQUE COMMENT 'Transaction reference number',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT 'Record creation timestamp',
    
    -- Foreign key constraints
    FOREIGN KEY (sender_id) REFERENCES Users(user_id) ON DELETE SET NULL ON UPDATE CASCADE,
    FOREIGN KEY (receiver_id) REFERENCES Users(user_id) ON DELETE SET NULL ON UPDATE CASCADE,
    FOREIGN KEY (category_id) REFERENCES Transaction_Categories(category_id) ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (message_id) REFERENCES Raw_Messages(message_id) ON DELETE SET NULL ON UPDATE CASCADE,
    
    -- Additional constraints
    CONSTRAINT chk_sender_receiver CHECK (sender_id != receiver_id OR sender_id IS NULL OR receiver_id IS NULL),
    CONSTRAINT chk_currency CHECK (currency IN ('RWF', 'USD', 'EUR', 'UGX', 'TZS', 'KES'))
) ENGINE=InnoDB COMMENT='Main transaction records with financial data';

-- System Logs table - ETL processing logs
CREATE TABLE System_Logs (
    log_id INT AUTO_INCREMENT PRIMARY KEY COMMENT 'Unique log identifier',
    level ENUM('DEBUG', 'INFO', 'WARN', 'ERROR', 'CRITICAL') NOT NULL COMMENT 'Log level',
    message TEXT NOT NULL COMMENT 'Log message content',
    context_json JSON COMMENT 'Additional context data in JSON format',
    transaction_id INT NULL COMMENT 'Associated transaction ID (if applicable)',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT 'Log creation timestamp',
    
    -- Foreign key constraint
    FOREIGN KEY (transaction_id) REFERENCES Transactions(transaction_id) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB COMMENT='System logs for ETL processing and debugging';

-- =====================================================
-- INDEXES FOR PERFORMANCE OPTIMIZATION
-- =====================================================

-- Users table indexes
CREATE INDEX idx_users_phone ON Users(phone_number);
CREATE INDEX idx_users_status ON Users(account_status);
CREATE INDEX idx_users_created ON Users(created_at);

-- Transactions table indexes
CREATE INDEX idx_transactions_timestamp ON Transactions(timestamp);
CREATE INDEX idx_transactions_sender ON Transactions(sender_id);
CREATE INDEX idx_transactions_receiver ON Transactions(receiver_id);
CREATE INDEX idx_transactions_category ON Transactions(category_id);
CREATE INDEX idx_transactions_type ON Transactions(transaction_type);
CREATE INDEX idx_transactions_status ON Transactions(status);
CREATE INDEX idx_transactions_amount ON Transactions(amount);
CREATE INDEX idx_transactions_reference ON Transactions(reference_number);
CREATE INDEX idx_transactions_created ON Transactions(created_at);

-- Composite indexes for common queries
CREATE INDEX idx_transactions_user_timestamp ON Transactions(sender_id, timestamp);
CREATE INDEX idx_transactions_user_status ON Transactions(sender_id, status);
CREATE INDEX idx_transactions_category_timestamp ON Transactions(category_id, timestamp);

-- Transaction_Categories table indexes
CREATE INDEX idx_categories_name ON Transaction_Categories(category_name);
CREATE INDEX idx_categories_pattern ON Transaction_Categories(rule_pattern);

-- Raw_Messages table indexes
CREATE INDEX idx_messages_status ON Raw_Messages(processing_status);
CREATE INDEX idx_messages_parsed ON Raw_Messages(parsed_at);

-- System_Logs table indexes
CREATE INDEX idx_logs_level ON System_Logs(level);
CREATE INDEX idx_logs_created ON System_Logs(created_at);
CREATE INDEX idx_logs_transaction ON System_Logs(transaction_id);
CREATE INDEX idx_logs_level_created ON System_Logs(level, created_at);

-- =====================================================
-- SAMPLE DATA INSERTION (DML)
-- =====================================================

-- Insert sample users
INSERT INTO Users (phone_number, full_name, account_status) VALUES
('+250788123456', 'Manzi Arnold', 'active'),
('+250788234567', 'Kevin Nizeyimana', 'active'),
('+250788345678', 'Christian Tuyishime', 'active'),
('+250788456789', 'Katsia Teta', 'suspended'),
('+250788567890', 'Karigirwa Ange', 'active');

-- Insert transaction categories
INSERT INTO Transaction_Categories (category_name, description, rule_pattern) VALUES
('Transfer', 'Person-to-person money transfer', '.*transfer.*|.*sent.*|.*received.*'),
('Payment', 'Payment for goods or services', '.*payment.*|.*paid.*|.*purchase.*'),
('Withdrawal', 'Cash withdrawal from agent or ATM', '.*withdraw.*|.*cash.*|.*agent.*'),
('Deposit', 'Cash deposit to account', '.*deposit.*|.*top.*up.*'),
('Airtime', 'Mobile airtime purchase', '.*airtime.*|.*credit.*|.*top.*up.*'),
('Bill Payment', 'Utility or bill payment', '.*bill.*|.*electricity.*|.*water.*');

-- Insert sample raw messages
INSERT INTO Raw_Messages (raw_content, processing_status) VALUES
('Wakiriye 5000 RWF uva +250788123456. Umubare mushya: 15000 RWF', 'processed'),
('Kwishyura 2500 RWF ku Shop ABC byagenze neza. Ref: TXN001', 'processed'),
('Gusohoka 10000 RWF ku agent byagenze neza. Ref: TXN002', 'processed'),
('Kohereza 3000 RWF kuri +250788234567 byagenze neza. Ref: TXN003', 'processed'),
('Gura airtime 1000 RWF byagenze neza. Ref: TXN004', 'processed');

-- Insert sample transactions
INSERT INTO Transactions (sender_id, receiver_id, category_id, message_id, amount, currency, timestamp, transaction_type, status, reference_number) VALUES
(1, 2, 1, 1, 5000.00, 'RWF', '2024-01-15 10:30:00', 'receive', 'completed', 'TXN001'),
(2, NULL, 2, 2, 2500.00, 'RWF', '2024-01-15 11:15:00', 'pay', 'completed', 'TXN002'),
(3, NULL, 3, 3, 10000.00, 'RWF', '2024-01-15 14:20:00', 'withdraw', 'completed', 'TXN003'),
(4, 5, 1, 4, 3000.00, 'RWF', '2024-01-15 16:45:00', 'send', 'completed', 'TXN004'),
(5, NULL, 5, 5, 1000.00, 'RWF', '2024-01-15 18:30:00', 'pay', 'completed', 'TXN005');

-- Insert sample system logs
INSERT INTO System_Logs (level, message, context_json, transaction_id) VALUES
('INFO', 'SMS yasohotse neza', '{"message_id": 1, "parser_version": "1.0"}', 1),
('INFO', 'Transaction yashyizwe mu Transfer', '{"category_id": 1, "confidence": 0.95}', 1),
('INFO', 'Umubare wa Manzi Arnold wavuguruwe', '{"user_id": 2, "new_balance": 15000}', 1),
('WARN', 'Transaction categorization nke', '{"category_id": 2, "confidence": 0.65}', 2),
('INFO', 'Kwishyura ku Shop ABC byagenze neza', '{"merchant": "Shop ABC", "amount": 2500}', 2);

-- =====================================================
-- BASIC CRUD OPERATIONS TESTING
-- =====================================================

-- Test 1: SELECT operations
SELECT '=== TEST 1: Basic SELECT Operations ===' as test_name;

-- Get all active users
SELECT user_id, phone_number, full_name, account_status 
FROM Users 
WHERE account_status = 'active' 
ORDER BY created_at DESC;

-- Get transactions for a specific user
SELECT t.transaction_id, t.amount, t.currency, t.transaction_type, t.status, t.timestamp,
       u_sender.full_name as sender_name, u_receiver.full_name as receiver_name,
       tc.category_name
FROM Transactions t
LEFT JOIN Users u_sender ON t.sender_id = u_sender.user_id
LEFT JOIN Users u_receiver ON t.receiver_id = u_receiver.user_id
JOIN Transaction_Categories tc ON t.category_id = tc.category_id
WHERE t.sender_id = 1 OR t.receiver_id = 1
ORDER BY t.timestamp DESC;

-- Get transaction summary by category
SELECT tc.category_name, COUNT(*) as transaction_count, 
       SUM(t.amount) as total_amount, AVG(t.amount) as avg_amount
FROM Transactions t
JOIN Transaction_Categories tc ON t.category_id = tc.category_id
WHERE t.status = 'completed'
GROUP BY tc.category_id, tc.category_name
ORDER BY total_amount DESC;

-- Test 2: UPDATE operations
SELECT '=== TEST 2: UPDATE Operations ===' as test_name;

-- Update transaction status
UPDATE Transactions 
SET status = 'completed' 
WHERE transaction_id = 1;

-- Update user account status
UPDATE Users 
SET account_status = 'suspended' 
WHERE user_id = 4;

-- Test 3: INSERT operations
SELECT '=== TEST 3: INSERT Operations ===' as test_name;

-- Insert new user
INSERT INTO Users (phone_number, full_name, account_status) 
VALUES ('+250788999999', 'Test User', 'active');

-- Insert new transaction
INSERT INTO Transactions (sender_id, receiver_id, category_id, amount, currency, timestamp, transaction_type, status, reference_number)
VALUES (9, 1, 1, 2000.00, 'RWF', NOW(), 'send', 'pending', 'TXN009');

-- Test 4: DELETE operations (with proper constraints)
SELECT '=== TEST 4: DELETE Operations ===' as test_name;

-- Delete a system log (safe - no foreign key constraints)
DELETE FROM System_Logs WHERE log_id = 8;

-- Test 5: Complex queries
SELECT '=== TEST 5: Complex Analytical Queries ===' as test_name;

-- Daily transaction volume
SELECT DATE(timestamp) as transaction_date,
       COUNT(*) as transaction_count,
       SUM(amount) as total_volume,
       AVG(amount) as avg_transaction_amount
FROM Transactions
WHERE status = 'completed'
GROUP BY DATE(timestamp)
ORDER BY transaction_date DESC;

-- User transaction activity
SELECT u.full_name, u.phone_number,
       COUNT(t.transaction_id) as total_transactions,
       SUM(CASE WHEN t.sender_id = u.user_id THEN t.amount ELSE 0 END) as total_sent,
       SUM(CASE WHEN t.receiver_id = u.user_id THEN t.amount ELSE 0 END) as total_received
FROM Users u
LEFT JOIN Transactions t ON (u.user_id = t.sender_id OR u.user_id = t.receiver_id)
WHERE t.status = 'completed' OR t.status IS NULL
GROUP BY u.user_id, u.full_name, u.phone_number
ORDER BY total_transactions DESC;

-- =====================================================
-- DATABASE VERIFICATION
-- =====================================================

SELECT '=== DATABASE SETUP COMPLETED SUCCESSFULLY ===' as status;
SELECT 'Tables created:' as info, COUNT(*) as count FROM information_schema.tables WHERE table_schema = 'momo_sms';
SELECT 'Users inserted:' as info, COUNT(*) as count FROM Users;
SELECT 'Transactions inserted:' as info, COUNT(*) as count FROM Transactions;
SELECT 'Categories inserted:' as info, COUNT(*) as count FROM Transaction_Categories;
SELECT 'Raw messages inserted:' as info, COUNT(*) as count FROM Raw_Messages;
SELECT 'System logs inserted:' as info, COUNT(*) as count FROM System_Logs;