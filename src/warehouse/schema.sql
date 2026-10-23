PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS categories (
    category_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS suppliers (
    supplier_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    phone TEXT
);

CREATE TABLE IF NOT EXISTS products (
    product_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    unit TEXT NOT NULL,
    category_id INTEGER NOT NULL,
    FOREIGN KEY (category_id) REFERENCES categories(category_id)
);

CREATE TABLE IF NOT EXISTS deliveries (
    delivery_id INTEGER PRIMARY KEY AUTOINCREMENT,
    supplier_id INTEGER NOT NULL,
    delivery_date TEXT NOT NULL,
    FOREIGN KEY (supplier_id) REFERENCES suppliers(supplier_id)
);

CREATE TABLE IF NOT EXISTS delivery_items (
    item_id INTEGER PRIMARY KEY AUTOINCREMENT,
    delivery_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    unit_price REAL NOT NULL CHECK (unit_price >= 0),
    expiration_date TEXT NOT NULL,
    FOREIGN KEY (delivery_id) REFERENCES deliveries(delivery_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id),
    UNIQUE (delivery_id, product_id)
);
CREATE TABLE IF NOT EXISTS writeoffs (
    writeoff_id INTEGER PRIMARY KEY AUTOINCREMENT,
    writeoff_date TEXT NOT NULL,
    reason TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS writeoff_items (
    writeoff_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
    writeoff_id INTEGER NOT NULL,
    item_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    FOREIGN KEY (writeoff_id) REFERENCES writeoffs(writeoff_id),
    FOREIGN KEY (item_id) REFERENCES delivery_items(item_id),
    UNIQUE (writeoff_id, item_id)
);
INSERT OR IGNORE INTO categories (category_id, name) VALUES
    (1, 'Молочные продукты'),
    (2, 'Крупы и бакалея');

INSERT OR IGNORE INTO suppliers (supplier_id, name, phone) VALUES
    (1, 'ООО «Ферма»', '+7-900-111-22-33'),
    (2, 'ООО «Крупторг»', '+7-900-444-55-66');

INSERT OR IGNORE INTO products (product_id, name, unit, category_id) VALUES
    (1, 'Молоко', 'л', 1),
    (2, 'Кефир', 'л', 1),
    (3, 'Рис', 'кг', 2),
    (4, 'Гречка', 'кг', 2);

INSERT OR IGNORE INTO deliveries
    (delivery_id, supplier_id, delivery_date) VALUES
    (1, 1, '2026-10-20'),
    (2, 2, '2026-10-21');

INSERT OR IGNORE INTO delivery_items
    (item_id, delivery_id, product_id, quantity, unit_price, expiration_date) VALUES
    (1, 1, 1, 20, 90.00, '2026-11-05'),
    (2, 1, 2, 15, 85.00, '2026-11-03'),
    (3, 2, 3, 30, 110.00, '2027-10-20'),
    (4, 2, 4, 25, 95.00, '2027-08-15');
    INSERT OR IGNORE INTO writeoffs
    (writeoff_id, writeoff_date, reason)
VALUES
    (1, '2026-10-23', 'Тестовое списание');

INSERT OR IGNORE INTO writeoff_items
    (writeoff_item_id, writeoff_id, item_id, quantity)
VALUES
    (1, 1, 1, 2);