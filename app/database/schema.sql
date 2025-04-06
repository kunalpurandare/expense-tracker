-- Drop tables if they exist (for fresh setup)
DROP TABLE IF EXISTS transactions;
DROP TABLE IF EXISTS users;

-- Users table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    hashed_password TEXT NOT NULL,
    role TEXT NOT NULL DEFAULT 'user'
);

-- Transactions table
CREATE TABLE transactions (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    amount NUMERIC(10, 2) NOT NULL,
    type TEXT NOT NULL CHECK (type IN ('income', 'expense')),
    category TEXT NOT NULL,
    date DATE NOT NULL,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE
);

-- Insert dummy transactions (user_id references users)
INSERT INTO transactions (title, amount, type, category, date, user_id)
VALUES
  ('Salary', 5000.00, 'income', 'salary', '2025-04-01', 1),
  ('Groceries', 150.00, 'expense', 'food', '2025-04-02', 1),
  ('Electricity Bill', 80.00, 'expense', 'utilities', '2025-04-03', 1),
  ('Freelance Work', 1200.00, 'income', 'freelance', '2025-04-04', 2),
  ('Gym Membership', 50.00, 'expense', 'fitness', '2025-04-05', 2),
  ('Internet Bill', 60.00, 'expense', 'utilities', '2025-04-06', 2),
  ('Book Sale', 100.00, 'income', 'other', '2025-04-07', 1),
  ('Dining Out', 90.00, 'expense', 'entertainment', '2025-04-08', 1);

