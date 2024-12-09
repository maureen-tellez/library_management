CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(50) NOT NULL,
    role VARCHAR(20) NOT NULL CHECK(role IN ('admin', 'user'))
);
-- Insertar un usuario admin
INSERT INTO users (username, password, role) 
VALUES ('admin', '123456', 'admin');

-- Insertar un usuario regular
INSERT INTO users (username, password, role) 
VALUES ('user', '9876', 'user');
