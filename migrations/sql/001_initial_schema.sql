
CREATE TABLE IF NOT EXISTS roles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS service_categories (
    id INT AUTO_INCREMENT PRIMARY KEY,
    category_name VARCHAR(100) NOT NULL,
    description TEXT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(120) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    profile_image VARCHAR(200),
    role_id INT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX ix_users_email (email),
    FOREIGN KEY (role_id) REFERENCES roles(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


CREATE TABLE IF NOT EXISTS customers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    phone VARCHAR(20),
    address VARCHAR(200),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS photographers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    bio TEXT,
    phone VARCHAR(20),
    location VARCHAR(100),
    social_link VARCHAR(200),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


CREATE TABLE IF NOT EXISTS bookings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT NOT NULL,
    booking_number VARCHAR(50) NOT NULL UNIQUE,
    service_fee FLOAT NOT NULL,
    processing_fee FLOAT NOT NULL,
    total_price FLOAT NOT NULL,
    status VARCHAR(20) DEFAULT 'pending',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES customers(id)
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


CREATE TABLE IF NOT EXISTS services (
    id INT AUTO_INCREMENT PRIMARY KEY,
    photographer_id INT NOT NULL,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    service_category_id INT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (photographer_id) REFERENCES photographers(id),
    FOREIGN KEY (service_category_id) REFERENCES service_categories(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


CREATE TABLE IF NOT EXISTS payments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    booking_id INT NOT NULL,
    total_price FLOAT NOT NULL,
    card_last4 VARCHAR(4),
    cardholder_name VARCHAR(100),
    card_expiry DATETIME,
    status VARCHAR(20) DEFAULT 'pending',
    payment_date DATETIME,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (booking_id) REFERENCES bookings(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


CREATE TABLE IF NOT EXISTS service_packages (
    id INT AUTO_INCREMENT PRIMARY KEY,
    service_id INT NOT NULL,
    package_name VARCHAR(100) NOT NULL,
    price FLOAT NOT NULL,
    details TEXT,
    location VARCHAR(200),
    duration INT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (service_id) REFERENCES services(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


CREATE TABLE IF NOT EXISTS booking_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    booking_id INT NOT NULL,
    service_package_id INT NOT NULL,
    photographer_id INT NOT NULL,
    service_price FLOAT NOT NULL,
    event_start DATE NOT NULL,
    event_location VARCHAR(200),
    event_notes TEXT,
    event_pax INT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (booking_id) REFERENCES bookings(id),
    FOREIGN KEY (photographer_id) REFERENCES photographers(id),
    FOREIGN KEY (service_package_id) REFERENCES service_packages(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


INSERT INTO roles (name) VALUES
    ('customer'),
    ('photographer'),
    ('admin')
ON DUPLICATE KEY UPDATE name=name;


-- Default credentials: admin@test.com / Admin123
INSERT INTO users (email, password_hash, first_name, last_name, role_id, created_at)
SELECT
    'admin@test.com',
    'scrypt:32768:8:1$vdVMI7dDENnBLjjC$135eaa86bef9cff49f048a3f83af83f173dde2ac5f8ba46ebd77d07cf51da93e26b1e991aa8eb82af13664d32ddfd4a1f0416a353675564bf5cc412d269f3791',
    'Super',
    'Admin',
    (SELECT id FROM roles WHERE name = 'admin' LIMIT 1),
    NOW()
WHERE NOT EXISTS (
    SELECT 1 FROM users WHERE email = 'admin@test.com'
);


-- Default credentials: customer@test.com / customer123
INSERT INTO users (email, password_hash, first_name, last_name, role_id, created_at)
SELECT
    'customer@test.com',
    'scrypt:32768:8:1$GRBu4CIvnxydSres$08f327db51930911c8b3dbd3a660fa37bb2e1eb5fa6379398769a1134859df281aa36932636eacaaf833a2b93f488a0071d5683b75bd9d3529f9008d0879f87f',
    'Demo',
    'Customer',
    (SELECT id FROM roles WHERE name = 'customer' LIMIT 1),
    NOW()
WHERE NOT EXISTS (
    SELECT 1 FROM users WHERE email = 'customer@test.com'
);

-- Create customer profile for demo customer
INSERT INTO customers (user_id, phone, address, created_at)
SELECT
    u.id,
    '614232323',
    '123 Brisbane, Australia',
    NOW()
FROM users u
WHERE u.email = 'customer@test.com'
AND NOT EXISTS (
    SELECT 1 FROM customers WHERE user_id = u.id
);

-- Insert demo photographer user
-- Default credentials: photo@test.com / photo123
INSERT INTO users (email, password_hash, first_name, last_name, role_id, created_at)
SELECT
    'photo@test.com',
    'scrypt:32768:8:1$kcbZEKcIvveiBhDu$d423d2fd1be147a474a3f6eea71626328121576994123986afe1bb4e48059b2df6d902e2c932d2d507aa437ee025394329d0568ac3c55fbe62fc943e29fe24be',
    'Demo',
    'Photographer',
    (SELECT id FROM roles WHERE name = 'photographer' LIMIT 1),
    NOW()
WHERE NOT EXISTS (
    SELECT 1 FROM users WHERE email = 'photo@test.com'
);

-- Create photographer profile for demo photographer
INSERT INTO photographers (user_id, bio, phone, location, social_link, created_at)
SELECT
    u.id,
    'Professional photographer specializing in weddings, portraits, and events. Over 10 years of experience capturing precious moments.',
    '+614253434',
    'Brisbane, Australia',
    'https://instagram.com/demophotographer',
    NOW()
FROM users u
WHERE u.email = 'photo@test.com'
AND NOT EXISTS (
    SELECT 1 FROM photographers WHERE user_id = u.id
);

-- Insert sample service categories
INSERT INTO service_categories (category_name, description) VALUES
    ('Wedding Photography', 'Complete wedding photography services'),
    ('Portrait Photography', 'Individual and family portrait sessions'),
    ('Event Photography', 'Corporate and private event coverage'),
    ('Product Photography', 'Commercial product photography')
ON DUPLICATE KEY UPDATE category_name=category_name;
