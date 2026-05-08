CREATE SCHEMA IF NOT EXISTS inventario;

CREATE TABLE inventario.users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(80) NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    role VARCHAR(30) NOT NULL DEFAULT 'operator',
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE inventario.products (
    product_id SERIAL PRIMARY KEY,
    sku VARCHAR(80) NOT NULL UNIQUE,
    product_name VARCHAR(150) NOT NULL,
    description TEXT,
    category VARCHAR(80),
    unit VARCHAR(30) NOT NULL DEFAULT 'pieza',
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE inventario.inventory_stock (
    stock_id SERIAL PRIMARY KEY,
    product_id INT NOT NULL UNIQUE,
    quantity_on_hand INT NOT NULL DEFAULT 0 CHECK (quantity_on_hand >= 0),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),

    CONSTRAINT fk_stock_product
        FOREIGN KEY (product_id)
        REFERENCES inventario.products(product_id)
);

CREATE TABLE inventario.inventory_movements (
    movement_id SERIAL PRIMARY KEY,
    product_id INT NOT NULL,
    movement_type VARCHAR(10) NOT NULL CHECK (movement_type IN ('IN', 'OUT')),
    quantity INT NOT NULL CHECK (quantity > 0),
    reference_text VARCHAR(150),
    notes TEXT,
    created_by INT,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),

    CONSTRAINT fk_movement_product
        FOREIGN KEY (product_id)
        REFERENCES inventario.products(product_id),

    CONSTRAINT fk_movement_user
        FOREIGN KEY (created_by)
        REFERENCES inventario.users(user_id)
);