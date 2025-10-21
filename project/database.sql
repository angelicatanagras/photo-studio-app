
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(120) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    role ENUM('Customer', 'Photographer', 'Admin') NOT NULL,
    profile_image VARCHAR(200),
    phone VARCHAR(20),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX ix_users_email (email)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS customers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    address VARCHAR(200),
    city VARCHAR(50),
    postcode VARCHAR(10) NOT NULL,
    billing_address VARCHAR(200),
    FOREIGN KEY (user_id) REFERENCES users(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS category (
    id INT AUTO_INCREMENT PRIMARY KEY,
    category_name VARCHAR(25),
    description VARCHAR(100)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS photographers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    category_id INT NOT NULL,
    bio TEXT,
    location VARCHAR(100) NOT NULL,
    social_link VARCHAR(200) NOT NULL,
    availability DATETIME NOT NULL,
    featured BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (category_id) REFERENCES category(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS packages (
    id INT AUTO_INCREMENT PRIMARY KEY,
    package_name ENUM('Basic', 'Standard', 'Premium') NOT NULL,
    photographer_id INT NOT NULL,
    category_id INT NOT NULL,
    price FLOAT NOT NULL,
    inclusions TEXT NOT NULL,
    FOREIGN KEY (photographer_id) REFERENCES photographers(id),
    FOREIGN KEY (category_id) REFERENCES category(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS portfolio_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    photographer_id INT NOT NULL,
    title VARCHAR(100) NOT NULL,
    caption TEXT,
    image_path VARCHAR(200) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (photographer_id) REFERENCES photographers(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS cart (
    id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT NOT NULL,
    subtotal FLOAT NOT NULL,
    status ENUM('Pending', 'Completed') NOT NULL DEFAULT 'Pending',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES customers(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS cart_item (
    id INT AUTO_INCREMENT PRIMARY KEY,
    cart_id INT NOT NULL,
    photographer_id INT NOT NULL,
    package_id INT NOT NULL,
    price FLOAT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (cart_id) REFERENCES cart(id),
    FOREIGN KEY (package_id) REFERENCES packages(id),
    FOREIGN KEY (photographer_id) REFERENCES photographers(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS bookings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    cart_id INT NOT NULL,
    customer_id INT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    payment_date DATETIME,
    total_amount FLOAT NOT NULL,
    status ENUM('Pending', 'Completed') NOT NULL DEFAULT 'Pending',
    FOREIGN KEY (cart_id) REFERENCES cart(id),
    FOREIGN KEY (customer_id) REFERENCES customers(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Default credentials: admin@test.com / Admin123
INSERT INTO users (email, password_hash, first_name, last_name, role, profile_image, phone, created_at)
SELECT
    'admin@test.com',
    'scrypt:32768:8:1$vdVMI7dDENnBLjjC$135eaa86bef9cff49f048a3f83af83f173dde2ac5f8ba46ebd77d07cf51da93e26b1e991aa8eb82af13664d32ddfd4a1f0416a353675564bf5cc412d269f3791',
    'Super',
    'Admin',
    'Admin',
    NULL,
    '0400000000',
    NOW()
WHERE NOT EXISTS (
    SELECT 1 FROM users WHERE email = 'admin@test.com'
);

-- Default credentials: customer@test.com / customer123
INSERT INTO users (email, password_hash, first_name, last_name, role, profile_image, phone, created_at)
SELECT
    'customer@test.com',
    'scrypt:32768:8:1$GRBu4CIvnxydSres$08f327db51930911c8b3dbd3a660fa37bb2e1eb5fa6379398769a1134859df281aa36932636eacaaf833a2b93f488a0071d5683b75bd9d3529f9008d0879f87f',
    'Demo',
    'Customer',
    'Customer',
    NULL,
    '0400 000 001',
    NOW()
WHERE NOT EXISTS (
    SELECT 1 FROM users WHERE email = 'customer@test.com'
);

-- Create customer profile for demo customer
INSERT INTO customers (user_id, address, city, postcode, billing_address)
SELECT
    u.id,
    '123 Brisbane, Australia',
    'Brisbane',
    '4000',
    '123 Brisbane, Australia'
FROM users u
WHERE u.email = 'customer@test.com'
AND NOT EXISTS (
    SELECT 1 FROM customers WHERE user_id = u.id
);

-- Insert demo photographer user
-- Default credentials: photo@test.com / photo123
INSERT INTO users (email, password_hash, first_name, last_name, role, profile_image, phone)
SELECT
    'photo@test.com',
    'scrypt:32768:8:1$kcbZEKcIvveiBhDu$d423d2fd1be147a474a3f6eea71626328121576994123986afe1bb4e48059b2df6d902e2c932d2d507aa437ee025394329d0568ac3c55fbe62fc943e29fe24be',
    'Demo',
    'Photographer',
    'Photographer',
    NULL,
    '0400 000 002'
WHERE NOT EXISTS (
    SELECT 1 FROM users WHERE email = 'photo@test.com'
);

-- Insert sample service categories
INSERT INTO category (category_name, description) VALUES
    ('Wedding Photography', 'Complete wedding photography services'),
    ('Portrait Photography', 'Individual and family portrait sessions'),
    ('Pet Photography', 'Pet photography services'),
    ('Party Photography', 'Commercial party and events photography'),
    ('Maternity Photography', 'Maternity shooting services')
ON DUPLICATE KEY UPDATE category_name=category_name;

-- Create photographer profile for demo photographer
INSERT INTO photographers (user_id, category_id, bio, location, social_link, availability, featured)
SELECT
    u.id,
    c.id,
    'Professional photographer specializing in weddings, portraits, and events. Over 10 years of experience capturing precious moments.',
    'Brisbane, Australia',
    'https://instagram.com/demophotographer',
    NOW(),
    TRUE
FROM users u
JOIN category c ON c.category_name = 'Wedding Photography'
WHERE u.email = 'photo@test.com'
AND NOT EXISTS (
    SELECT 1 FROM photographers WHERE user_id = u.id
);

-- Insert sample packages
INSERT INTO packages (package_name, photographer_id, category_id, price, inclusions) VALUES
    ('Basic', 1, 1, 250.00, '1-hour photo session, 10 edited digital images'),
    ('Standard', 1, 1, 350.00, '2-hour photo session, 25 edited digital images'),
    ('Premium', 1, 1, 600.00, '3-hour session, 40 edited images, and prints')
ON DUPLICATE KEY UPDATE package_name=package_name;

