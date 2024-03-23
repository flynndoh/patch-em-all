
-- Create Flight table
DROP TABLE "flight";
CREATE TABLE IF NOT EXISTS "flight" (
  id  INTEGER PRIMARY KEY,
  name  VARCHAR(255) NOT NULL,
  timestamp datetime NOT NULL
);

-- Create User table
DROP TABLE "user";
CREATE TABLE IF NOT EXISTS "user" (
    id VARCHAR(36) PRIMARY KEY,
    hashed_password VARCHAR(255) NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    is_superuser BOOLEAN NOT NULL DEFAULT FALSE,
    is_verified BOOLEAN NOT NULL DEFAULT FALSE,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Create Patch table
DROP TABLE "patch";
CREATE TABLE IF NOT EXISTS "patch" (
    id VARCHAR(36) PRIMARY KEY,
    user_id VARCHAR(36) NOT NULL,
    flight_id INTEGER NOT NULL,
    patch_number INTEGER,
    FOREIGN KEY (user_id) REFERENCES "user" (id),
    FOREIGN KEY (flight_id) REFERENCES flight (id)
);

-- Create Access Token table
DROP TABLE "accesstoken";
CREATE TABLE IF NOT EXISTS "accesstoken" (
    token VARCHAR(36) PRIMARY KEY,
    user_id VARCHAR(36) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES "user" (id)
);