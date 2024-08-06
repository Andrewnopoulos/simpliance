-- Create the users table
CREATE TABLE IF NOT EXISTS users (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL
);

-- Create the auth_keys table
CREATE TABLE IF NOT EXISTS auth_keys (
    role_id TEXT NOT NULL,
    external_id TEXT NOT NULL,
    user_id TEXT NOT NULL,
    PRIMARY KEY (role_id, external_id, user_id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Create the reports table
CREATE TABLE IF NOT EXISTS reports (
    id TEXT PRIMARY KEY,
    process_state TEXT NOT NULL,
    datetime_started TEXT NOT NULL,
    datetime_completed TEXT NOT NULL,
    user_id TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Create indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_auth_keys_user_id ON auth_keys(user_id);
CREATE INDEX IF NOT EXISTS idx_reports_user_id ON reports(user_id);