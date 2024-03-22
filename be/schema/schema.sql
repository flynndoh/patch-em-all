
-- Create Flight table
CREATE TABLE IF NOT EXISTS "flight" (
  id  INTEGER PRIMARY KEY,
  name  VARCHAR(255) NOT NULL,
  timestamp datetime
);

-- Create User table
CREATE TABLE IF NOT EXISTS "user" (
    id INTEGER PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Create Patch table
CREATE TABLE IF NOT EXISTS "patch" (
    user_id INTEGER,
    flight_id INTEGER,
    patch_number INTEGER,
    PRIMARY KEY (user_id, flight_id),
    FOREIGN KEY (user_id) REFERENCES "user" (id),
    FOREIGN KEY (flight_id) REFERENCES flight (id)
);