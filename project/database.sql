
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
    event_date DATE NOT NULL,
    event_time TIME NOT NULL,
    pax INT NOT NULL,
    notes TEXT NOT NULL,
    FOREIGN KEY (cart_id) REFERENCES cart(id),
    FOREIGN KEY (photographer_id) REFERENCES photographers(id),
    FOREIGN KEY (package_id) REFERENCES packages(id)
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

-- Default credentials for admin 1: admin@test.com / Admin123
INSERT INTO users (email, password_hash, first_name, last_name, role, profile_image, phone, created_at)
SELECT
    'admin@test.com',
    'pbkdf2:sha256:1000000$iQFxqpTjE4LOThXO$11e9350f5bc12fa5069822c022bcfe4ad8d107d1b66c5d26eb6de0bbb646299a',
    'Super',
    'Admin',
    'Admin',
    NULL,
    '0400000000',
    NOW()
WHERE NOT EXISTS (
    SELECT 1 FROM users WHERE email = 'admin@test.com'
);

-- Default credentials for admin 2: admin2@test.com / Admin567
INSERT INTO users (email, password_hash, first_name, last_name, role, profile_image, phone, created_at)
SELECT
    'admin2@test.com',
    'pbkdf2:sha256:1000000$0BA1FEUDzOjFFo59$16bbb282da5d22db373e426da4686584c23bea0e6fd69650c4cad04a29f0fdbe',
    'Super',
    'Admin',
    'Admin',
    NULL,
    '0400000009',
    NOW()
WHERE NOT EXISTS (
    SELECT 1 FROM users WHERE email = 'admin2@test.com'
);

-- Default credentials for customer_1: customer@test.com / customer123
INSERT INTO users (email, password_hash, first_name, last_name, role, profile_image, phone, created_at)
SELECT
    'customer@test.com',
    'pbkdf2:sha256:1000000$Fl12fLtid5y51OXw$c56a78171284dc7c11cf976a684dd276c1a201c606c1555c0e02ef47e2ef22e1',
    'Katie',
    'Holmes',
    'Customer',
    NULL,
    '0400 000 001',
    NOW()
WHERE NOT EXISTS (
    SELECT 1 FROM users WHERE email = 'customer@test.com'
);

-- Create customer profile for demo customer_1
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

-- Default credentials for customer_2: customer2@test.com / Roger123
INSERT INTO users (email, password_hash, first_name, last_name, role, profile_image, phone, created_at)
SELECT
    'customer2@test.com',
    'pbkdf2:sha256:1000000$AEHrqGbttpqtbN0Y$dc6c7a42c88d8042b71af42c4dd44a0ab76de026bc186ec2f3929ad4e727a900',
    'Roger',
    'Chavez',
    'Customer',
    NULL,
    '0400 000 006',
    NOW()
WHERE NOT EXISTS (
    SELECT 1 FROM users WHERE email = 'customer2@test.com'
);

-- Create customer profile for demo customer_2
INSERT INTO customers (user_id, address, city, postcode, billing_address)
SELECT
    u.id,
    '234 Brisbane, Australia',
    'Brisbane',
    '4001',
    '234 Brisbane, Australia'
FROM users u
WHERE u.email = 'customer2@test.com'
AND NOT EXISTS (
    SELECT 1 FROM customers WHERE user_id = u.id
);

-- Insert demo photographer user
-- Default credentials for photographer_1: photo@test.com / photo123
INSERT INTO users (email, password_hash, first_name, last_name, role, profile_image, phone)
SELECT
    'photo@test.com',
    'pbkdf2:sha256:1000000$YoUDg7LC9YTd0xEq$9ba94263116947ce2e9c27d0a298b403be1d389aa492892df960365d08eca5d1',
    'Steve',
    'Philips',
    'Photographer',
    'profile_5_20251023_122340.jpg',
    '0400 000 002'
WHERE NOT EXISTS (
    SELECT 1 FROM users WHERE email = 'photo@test.com'
);

-- Default credentials for photographer_2: photo2@test.com / Bryan123
INSERT INTO users (email, password_hash, first_name, last_name, role, profile_image, phone)
SELECT
    'photo2@test.com',
    'pbkdf2:sha256:1000000$HgrBr181DITCLmPP$a88ceb911e669d2cd91924a78828248b737f5bc6487f42fe99372ac8ade9cd60',
    'Bryan',
    'Bays',
    'Photographer',
    'profile_6_20251022_093104.jpg',
    '0400 000 011'
WHERE NOT EXISTS (
    SELECT 1 FROM users WHERE email = 'photo2@test.com'
);

-- Insert sample service categories
INSERT INTO category (category_name, description) VALUES
    ('Wedding', 'Complete wedding photography services'),
    ('Portrait', 'Individual and family portrait sessions'),
    ('Events','Turning your event into unforgettable memories'),
    ('Pet Photography', 'Pet photography services'),
    ('Party', 'Commercial party and events photography'),
    ('Maternity', 'Maternity shooting services'),
    ('Newborn','Capturing precious moments'),
    ('Branding','Branding creatives'),
    ('Sports', 'Capturing moments in athletic events'),
    ('Cosplay','Bringing your character to life')
ON DUPLICATE KEY UPDATE category_name=category_name;

-- Create photographer profile for demo photographer_1
INSERT INTO photographers (user_id, category_id, bio, location, social_link, availability, featured)
SELECT
    u.id,
    1,
    'Professional photographer specialising in weddings, portraits, events, business branding, and cosplay photography. Over 10 years of experience capturing precious moments.',
    'Brisbane, Australia',
    'https://instagram.com/demophotographer',
    NOW(),
    TRUE
FROM users u
WHERE u.email = 'photo@test.com'
AND NOT EXISTS (
    SELECT 1 FROM photographers WHERE user_id = u.id
);

-- Create photographer profile for demo photographer_2
INSERT INTO photographers (user_id, category_id, bio, location, social_link, availability, featured)
SELECT
    u.id,
    2,
    'Professional photographer specialising in maternity, newborn, party, pet, and events photography. 7 years of turning moments into breathtaking memories.',
    'Gold Coast, Australia',
    'https://instagram.com/demophotographer2',
    NOW(),
    TRUE
FROM users u
WHERE u.email = 'photo2@test.com'
AND NOT EXISTS (
    SELECT 1 FROM photographers WHERE user_id = u.id
);

-- Insert sample packages
INSERT INTO packages (package_name, photographer_id, category_id, price, inclusions) VALUES
    ('Basic', 1, 1, 250.00, '1-hour photo session, 10 edited digital images'),
    ('Standard', 1, 1, 350.00, '2-hour photo session, 25 edited digital images'),
    ('Premium', 1, 1, 600.00, '3-hour session, 40 edited images, and prints'),
    ('Basic', 1, 2, 250.00, '1-hour photo session, 10 edited digital images'),
    ('Standard', 1, 2, 350.00, '2-hour photo session, 25 edited digital images'),
    ('Premium', 1, 2, 600.00, '3-hour session, 40 edited images, and prints'),
    ('Basic', 1, 3, 250.00, '1-hour photo session, 10 edited digital images'),
    ('Standard', 1, 3, 350.00, '2-hour photo session, 25 edited digital images'),
    ('Premium', 1, 3, 600.00, '3-hour session, 40 edited images, and prints'),
    ('Basic', 1, 8, 250.00, '1-hour photo session, 10 edited digital images'),
    ('Standard', 1, 8, 350.00, '2-hour photo session, 25 edited digital images'),
    ('Premium', 1, 8, 600.00, '3-hour session, 40 edited images, and prints'),
    ('Basic', 1, 10, 250.00, '1-hour photo session, 10 edited digital images'),
    ('Standard', 1, 10, 350.00, '2-hour photo session, 25 edited digital images'),
    ('Premium', 1, 10, 600.00, '3-hour session, 40 edited images, and prints'),
    ('Basic', 2, 3, 200.00, '1-hour photo session, 10 BW and 10 colored edited digital images'),
    ('Standard', 2, 3, 350.00, '2-hour photo session, 10 BW and 30 colored edited digital images'),
    ('Premium', 2, 3, 550.00, '3-hour session, 50 edited images, and prints'),
    ('Basic', 2, 4, 200.00, '1-hour photo session, 10 BW and 10 colored edited digital images'),
    ('Standard', 2, 4, 350.00, '2-hour photo session, 10 BW and 30 colored edited digital images'),
    ('Premium', 2, 4, 550.00, '3-hour session, 50 edited images, and prints'),
    ('Basic', 2, 5, 200.00, '1-hour photo session, 10 BW and 10 colored edited digital images'),
    ('Standard', 2, 5, 350.00, '2-hour photo session, 10 BW and 30 colored edited digital images'),
    ('Premium', 2, 5, 550.00, '3-hour session, 50 edited images, and prints'),
    ('Basic', 2, 6, 200.00, '1-hour photo session, 10 BW and 10 colored edited digital images'),
    ('Standard', 2, 6, 350.00, '2-hour photo session, 10 BW and 30 colored edited digital images'),
    ('Premium', 2, 6, 550.00, '3-hour session, 50 edited images, and prints'),
    ('Basic', 2, 7, 200.00, '1-hour photo session, 10 BW and 10 colored edited digital images'),
    ('Standard', 2, 7, 350.00, '2-hour photo session, 10 BW and 30 colored edited digital images'),
    ('Premium', 2, 7, 550.00, '3-hour session, 50 edited images, and prints')
ON DUPLICATE KEY UPDATE package_name=package_name;

INSERT INTO portfolio_items (photographer_id, title, caption, image_path) VALUES
    (1,"Outdoor wedding","Beach wedding shot","1_20251021_195046_wedding2.jpg"),
    (1,"Flowers and rings","Close up photos for flowers and rings","1_20251021_195134_wedding5.jpg"),
    (1,"Couple photo","Outdoor couple shot","1_20251021_195331_wedding1.jpg"),
    (1,"Portrait sample 1","Portrait Sample 1","portrait1.jpg"),
    (1,"Portrait sample 2","Portrait Sample 2","portrait2.jpg"),
    (1,"Portrait sample 3","Portrait Sample 3","portrait3.jpg"),
    (1,"Event sample 1","Event sample 1","event1.jpg"),
    (1,"Event sample 2","Event sample 2","event2.jpg"),
    (1,"Event sample 3","Event sample 3","event3.jpg"),
    (1,"Cosplay sample 1","Cosplay sample 1","cosplay1.jpg"),
    (1,"Cosplay sample 2","Cosplay sample 2","cosplay2.jpg"),
    (2,"BW Maternity","Black & White maternity shot","2_20251021_214659_maternity1.jpg"),
    (2,"Baby feet","Mum with baby","2_20251021_221533_maternity2.jpg"),
    (2,"Autumn shoot",NULL,"2_20251021_221550_maternity3.jpg"),
    (2,"Party sample 1","Party sample 1","party1.jpg"),
    (2,"Party sample 2","Party sample 2","party2.jpg"),
    (2,"Party sample 3","Party sample 3","party3.jpg"),
    (2,"Pet sample 1","Pet sample 1","pet1.jpg"),
    (2,"Pet sample 2","Pet sample 2","pet2.jpg"),
    (2,"Pet sample 3","Pet sample 3","pet3.jpg")
ON DUPLICATE KEY UPDATE photographer_id=photographer_id;

-- Insert sample cart
INSERT INTO cart (customer_id, subtotal, status) VALUES
    (1, 200, 'Completed'),
    (1, 900, 'Completed'),
    (2, 800, 'Completed')
ON DUPLICATE KEY UPDATE id=id;

-- Insert sample cart_item
INSERT INTO cart_item (cart_id, photographer_id, package_id, price, event_date, event_time, pax, notes) VALUES
    (1, 1, 19, 200, '2025-11-21','15:00', 2, 'Sample photoshoot notes'),
    (2, 1, 5, 350, '2025-11-10', '09:00', 20, 'Sample photoshoot notes'),
    (2, 2, 21, 550, '2025-12-21','10:00', 10, 'Sample photoshoot notes'),
    (3, 1, 13, 250, '2025-12-01','11:00', 5, 'Sample photoshoot notes'),
    (3, 2, 22, 200, '2025-12-19','12:00', 4, 'Sample photoshoot notes'),
    (3, 2, 29, 350, '2025-12-30','13:00', 3, 'Sample photoshoot notes')
ON DUPLICATE KEY UPDATE id=id;

-- Insert sample bookings
INSERT INTO bookings (cart_id, customer_id, payment_date, total_amount, status) VALUES
    (1, 1, CURRENT_TIMESTAMP, 200, 'Completed'),
    (2, 1, CURRENT_TIMESTAMP, 900, 'Completed'),
    (3, 2, CURRENT_TIMESTAMP, 800, 'Completed')
ON DUPLICATE KEY UPDATE id=id;
