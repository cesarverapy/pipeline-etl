-- Drop child table first to avoid foreign key issues
DROP TABLE IF EXISTS products_data;
DROP TABLE IF EXISTS outlets;

-- Create the outlets table (normalized)
CREATE TABLE outlets (
    outlet_id VARCHAR PRIMARY KEY,
    establishment_year INT,
    outlet_size VARCHAR(20),
    location_type VARCHAR(20),
    outlet_type VARCHAR(30)
);

-- Create the products_data table with foreign key reference
CREATE TABLE products_data (
    product_id VARCHAR,
    weight FLOAT,
    fat_content VARCHAR(20),
    product_visibility FLOAT,
    product_type VARCHAR(50),
    mrp FLOAT,
    outlet_id VARCHAR,
    PRIMARY KEY (product_id, outlet_id),
    FOREIGN KEY (outlet_id) REFERENCES outlets(outlet_id)
);
