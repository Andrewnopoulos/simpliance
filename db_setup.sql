-- Create the users table
CREATE TABLE IF NOT EXISTS users (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL
);

-- Create the auth_keys table
CREATE TABLE IF NOT EXISTS auth_keys (
    id TEXT PRIMARY KEY,
    role_id TEXT NOT NULL,
    external_id TEXT NOT NULL,
    user_id TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id),
    UNIQUE (role_id, external_id, user_id)
);

-- Create the reports table with a reference to auth_keys only
CREATE TABLE IF NOT EXISTS reports (
    id TEXT PRIMARY KEY,
    process_state TEXT NOT NULL,
    datetime_started TEXT NOT NULL,
    datetime_completed TEXT NOT NULL,
    user_id TEXT NOT NULL,
    auth_key_id TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (auth_key_id) REFERENCES auth_keys(id),
    UNIQUE (auth_key_id)  -- This ensures one-to-one relationship
);

-- Create indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_auth_keys_user_id ON auth_keys(user_id);
CREATE INDEX IF NOT EXISTS idx_reports_user_id ON reports(user_id);
CREATE INDEX IF NOT EXISTS idx_reports_auth_key_id ON reports(auth_key_id);