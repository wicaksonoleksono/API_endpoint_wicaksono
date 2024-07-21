-- Create the BANK database
CREATE DATABASE BANK;

-- Switch to the BANK database
USE BANK;

-- Create the Users table
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Create the Accounts table
CREATE TABLE accounts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    account_type VARCHAR(255),
    account_number VARCHAR(255) UNIQUE NOT NULL,
    balance DECIMAL(10, 2) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES Users(id)
);

-- Create the Transactions table
CREATE TABLE transactions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    from_account_id INT,
    to_account_id INT,
    amount DECIMAL(10, 2) NOT NULL,
    type VARCHAR(255),
    description VARCHAR(255),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (from_account_id) REFERENCES Accounts(id),
    FOREIGN KEY (to_account_id) REFERENCES Accounts(id)
);


-- Insert sample data into Users table
INSERT INTO users (username, email, password_hash)
VALUES ('john_doe', 'john@example.com', 'hashed_password_1');

INSERT INTO users (username, email, password_hash)
VALUES ('jane_smith', 'jane@example.com', 'hashed_password_2');


-- Insert sample data into Accounts table
INSERT INTO accounts (user_id, account_type, account_number, balance)
VALUES (1, 'checking', 'CHK1234567890', 1500.00);

INSERT INTO accounts (user_id, account_type, account_number, balance)
VALUES (1, 'savings', 'SAV1234567890', 3000.00);

INSERT INTO accounts (user_id, account_type, account_number, balance)
VALUES (2, 'checking', 'CHK0987654321', 2500.00);

-- Insert sample data into Transactions table
INSERT INTO transactions (from_account_id, to_account_id, amount, type, description)
VALUES (1, 2, 500.00, 'transfer', 'Transfer to Jane Smith');

INSERT INTO transactions (from_account_id, to_account_id, amount, type, description)
VALUES (2, NULL, 200.00, 'deposit', 'Deposit to savings account');

INSERT INTO transactions (from_account_id, to_account_id, amount, type, description)
VALUES (NULL, 1, 100.00, 'withdrawal', 'Withdrawal from checking account');

select * from users
