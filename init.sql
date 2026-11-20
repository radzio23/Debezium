CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    price NUMERIC(10,2) NOT NULL
);
ALTER TABLE products REPLICA IDENTITY FULL;
INSERT INTO products(name, price) VALUES ('Mysz bezprzewodowa', 99.90);
INSERT INTO products(name, price) VALUES ('Klawiatura', 199.99);
INSERT INTO products(name, price) VALUES ('Słuchawki', 149.99);
