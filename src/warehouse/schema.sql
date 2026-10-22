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
    FOREIGN KEY (delivery_id) REFERENCES deliveries(delivery_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id),
    UNIQUE (delivery_id, product_id)
);
INSERT OR IGNORE INTO categories (category_id, name) VALUES
    (1, 'Канцелярия'),
    (2, 'Электроника');

INSERT OR IGNORE INTO suppliers (supplier_id, name, phone) VALUES
    (1, 'ООО «Снабжение»', '+7-900-111-22-33'),
    (2, 'ООО «ТехноПоставка»', '+7-900-444-55-66');

INSERT OR IGNORE INTO products (product_id, name, unit, category_id) VALUES
    (1, 'Бумага A4', 'пачка', 1),
    (2, 'Ручка шариковая', 'шт.', 1),
    (3, 'Клавиатура', 'шт.', 2),
    (4, 'Мышь компьютерная', 'шт.', 2);

INSERT OR IGNORE INTO deliveries
    (delivery_id, supplier_id, delivery_date) VALUES
    (1, 1, '2026-10-20'),
    (2, 2, '2026-10-21');

INSERT OR IGNORE INTO delivery_items
    (item_id, delivery_id, product_id, quantity, unit_price) VALUES
    (1, 1, 1, 20, 350.00),
    (2, 1, 2, 50, 25.00),
    (3, 2, 3, 5, 1800.00),
    (4, 2, 4, 10, 750.00);