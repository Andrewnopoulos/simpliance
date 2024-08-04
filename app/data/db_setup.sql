-- Create the users table
CREATE TABLE IF NOT EXISTS users (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    reports TEXT  -- This will store a comma-separated list of report IDs
);

-- Create the auth_keys table
CREATE TABLE IF NOT EXISTS auth_keys (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT NOT NULL,
    role_id TEXT NOT NULL,
    external_id TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Create the reports table
CREATE TABLE IF NOT EXISTS reports (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    process_state TEXT NOT NULL,
    datetime_started TEXT NOT NULL,
    datetime_completed TEXT,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Create indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_auth_keys_user_id ON auth_keys(user_id);
CREATE INDEX IF NOT EXISTS idx_reports_user_id ON reports(user_id);