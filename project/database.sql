
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
    event_location VARCHAR(200) NOT NULL,
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

-- Default credentials for photographer_3: events@test.com / Events123
INSERT INTO users (email, password_hash, first_name, last_name, role, profile_image, phone)
SELECT
    'events@test.com',
    'scrypt:32768:8:1$xEOzURTQhrn3ogk4$8dba241ad13ee8f011ed39db83381f8fda06341c923fce2076ac92e562b7b757316b8d08dc572aa2909df941c27e68ad4d380f471d059a255f844d9e55fa00b8',
    'Emma',
    'Thompson',
    'Photographer',
    'profile_events.jpg',
    '0400 000 003'
WHERE NOT EXISTS (
    SELECT 1 FROM users WHERE email = 'events@test.com'
);

-- Default credentials for photographer_4: pet@test.com / Pet123
INSERT INTO users (email, password_hash, first_name, last_name, role, profile_image, phone)
SELECT
    'pet@test.com',
    'scrypt:32768:8:1$oPlgWfHWnTEI6Fyz$8f70768d16a8d619d79c9360e74923f64fbad69f05a22878fd87926757afe59f8e2562268597d945f21b5ee71360f66c365fb1fcc171b8269aeec42af503abaf',
    'Alex',
    'Johnson',
    'Photographer',
    'profile_pet.jpg',
    '0400 000 004'
WHERE NOT EXISTS (
    SELECT 1 FROM users WHERE email = 'pet@test.com'
);

-- Default credentials for photographer_5: party@test.com / Party123
INSERT INTO users (email, password_hash, first_name, last_name, role, profile_image, phone)
SELECT
    'party@test.com',
    'scrypt:32768:8:1$XxrzllPIBdN67tD1$04723b050e8a353e47e2125d06411f2503f2d8d7d43053a04beac358bddccd5ad2a0befb8b1d661716c3d71901d7f8390ccb84755930454499742019afc05569',
    'Sarah',
    'Wilson',
    'Photographer',
    'profile_party.jpg',
    '0400 000 005'
WHERE NOT EXISTS (
    SELECT 1 FROM users WHERE email = 'party@test.com'
);

-- Default credentials for photographer_6: maternity@test.com / Maternity123
INSERT INTO users (email, password_hash, first_name, last_name, role, profile_image, phone)
SELECT
    'maternity@test.com',
    'scrypt:32768:8:1$9s4xcTbFmcTRvH5O$92291ca8ca86908b6c856aff60cd03b200ac38866d2a9bfb7b0381b666e85d97fceddb64b117e10294a12f1444feda413d56e5c3d87cc4b5eeca8a77048fee65',
    'Lisa',
    'Anderson',
    'Photographer',
    'profile_maternity.jpg',
    '0400 000 007'
WHERE NOT EXISTS (
    SELECT 1 FROM users WHERE email = 'maternity@test.com'
);

-- Default credentials for photographer_7: newborn@test.com / Newborn123
INSERT INTO users (email, password_hash, first_name, last_name, role, profile_image, phone)
SELECT
    'newborn@test.com',
    'scrypt:32768:8:1$vlfNevIrL7imuZUg$71c6f8c201b40a81f9b1ffa57fb289e5fc495d0534054ef94a9bdfe5874683712a81cecf52e0f36cde56c5ec659fca6097721cd829f10e5ac69437c0b81a722f',
    'Michael',
    'Brown',
    'Photographer',
    'profile_newborn.jpg',
    '0400 000 008'
WHERE NOT EXISTS (
    SELECT 1 FROM users WHERE email = 'newborn@test.com'
);

-- Default credentials for photographer_8: branding@test.com / Branding123
INSERT INTO users (email, password_hash, first_name, last_name, role, profile_image, phone)
SELECT
    'branding@test.com',
    'scrypt:32768:8:1$e2XNT1uUn02gMkrs$c7d7a80f38c549b6bb6a007255cb417f1320ea2ade7ac881bb2a83b5a4c8ec665a7246048c9798f695dbf9f604278c53e4c24e1b06f6e611216546cf88abf84c',
    'David',
    'Miller',
    'Photographer',
    'profile_branding.jpg',
    '0400 000 009'
WHERE NOT EXISTS (
    SELECT 1 FROM users WHERE email = 'branding@test.com'
);

-- Default credentials for photographer_9: sports@test.com / Sports123
INSERT INTO users (email, password_hash, first_name, last_name, role, profile_image, phone)
SELECT
    'sports@test.com',
    'scrypt:32768:8:1$GsgQWgsYgORQSf7j$c050f611115be7fc000629efa27a75c02b4f15fc5e3b8f8c67bc77af3a35759fb96bd7605faa63cb85e7d291cf5d968de058270f0e838c1367201fe10a726bda',
    'James',
    'Taylor',
    'Photographer',
    'profile_sports.jpg',
    '0400 000 010'
WHERE NOT EXISTS (
    SELECT 1 FROM users WHERE email = 'sports@test.com'
);

-- Default credentials for photographer_10: cosplay@test.com / Cosplay123
INSERT INTO users (email, password_hash, first_name, last_name, role, profile_image, phone)
SELECT
    'cosplay@test.com',
    'scrypt:32768:8:1$W2QmcLcD6e5O8e1Y$41bb33f46840dba1cc6b8c689b28fbc0f3fd20627ceda46cadfb90c72a70e6239485ca461b21ab61d4becbc6093aa52647cf354c41cac076868a024365339de6',
    'Rachel',
    'Davis',
    'Photographer',
    'profile_cosplay.jpg',
    '0400 000 012'
WHERE NOT EXISTS (
    SELECT 1 FROM users WHERE email = 'cosplay@test.com'
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

-- Create photographer profile for Events specialist
INSERT INTO photographers (user_id, category_id, bio, location, social_link, availability, featured)
SELECT
    u.id,
    3,
    'Event photography specialist with 8 years experience capturing corporate events, conferences, and celebrations. Expert in low-light and dynamic environments.',
    'Sydney, Australia',
    'https://instagram.com/eventsphotographer',
    NOW(),
    TRUE
FROM users u
WHERE u.email = 'events@test.com'
AND NOT EXISTS (
    SELECT 1 FROM photographers WHERE user_id = u.id
);

-- Create photographer profile for Pet specialist
INSERT INTO photographers (user_id, category_id, bio, location, social_link, availability, featured)
SELECT
    u.id,
    4,
    'Pet photography specialist with 6 years experience capturing the unique personalities of dogs, cats, and exotic pets. Patient and animal-loving professional.',
    'Melbourne, Australia',
    'https://instagram.com/petphotographer',
    NOW(),
    TRUE
FROM users u
WHERE u.email = 'pet@test.com'
AND NOT EXISTS (
    SELECT 1 FROM photographers WHERE user_id = u.id
);

-- Create photographer profile for Party specialist
INSERT INTO photographers (user_id, category_id, bio, location, social_link, availability, featured)
SELECT
    u.id,
    5,
    'Party and celebration photographer with 5 years experience capturing birthdays, anniversaries, and special occasions. Expert in candid and posed shots.',
    'Perth, Australia',
    'https://instagram.com/partyphotographer',
    NOW(),
    TRUE
FROM users u
WHERE u.email = 'party@test.com'
AND NOT EXISTS (
    SELECT 1 FROM photographers WHERE user_id = u.id
);

-- Create photographer profile for Maternity specialist
INSERT INTO photographers (user_id, category_id, bio, location, social_link, availability, featured)
SELECT
    u.id,
    6,
    'Maternity photography specialist with 9 years experience capturing the beauty of pregnancy. Specializes in elegant and artistic maternity portraits.',
    'Adelaide, Australia',
    'https://instagram.com/maternityphotographer',
    NOW(),
    TRUE
FROM users u
WHERE u.email = 'maternity@test.com'
AND NOT EXISTS (
    SELECT 1 FROM photographers WHERE user_id = u.id
);

-- Create photographer profile for Newborn specialist
INSERT INTO photographers (user_id, category_id, bio, location, social_link, availability, featured)
SELECT
    u.id,
    7,
    'Newborn photography specialist with 7 years experience safely photographing babies. Certified in newborn safety and specialized equipment.',
    'Canberra, Australia',
    'https://instagram.com/newbornphotographer',
    NOW(),
    TRUE
FROM users u
WHERE u.email = 'newborn@test.com'
AND NOT EXISTS (
    SELECT 1 FROM photographers WHERE user_id = u.id
);

-- Create photographer profile for Branding specialist
INSERT INTO photographers (user_id, category_id, bio, location, social_link, availability, featured)
SELECT
    u.id,
    8,
    'Commercial branding photographer with 10 years experience in corporate headshots, product photography, and business branding. Studio and location shoots.',
    'Brisbane, Australia',
    'https://instagram.com/brandingphotographer',
    NOW(),
    TRUE
FROM users u
WHERE u.email = 'branding@test.com'
AND NOT EXISTS (
    SELECT 1 FROM photographers WHERE user_id = u.id
);

-- Create photographer profile for Sports specialist
INSERT INTO photographers (user_id, category_id, bio, location, social_link, availability, featured)
SELECT
    u.id,
    9,
    'Sports and action photographer with 8 years experience capturing athletic events, competitions, and training sessions. Expert in fast-paced photography.',
    'Gold Coast, Australia',
    'https://instagram.com/sportsphotographer',
    NOW(),
    TRUE
FROM users u
WHERE u.email = 'sports@test.com'
AND NOT EXISTS (
    SELECT 1 FROM photographers WHERE user_id = u.id
);

-- Create photographer profile for Cosplay specialist
INSERT INTO photographers (user_id, category_id, bio, location, social_link, availability, featured)
SELECT
    u.id,
    10,
    'Cosplay and character photography specialist with 6 years experience. Expert in costume photography, character portraits, and convention shoots.',
    'Sydney, Australia',
    'https://instagram.com/cosplayphotographer',
    NOW(),
    TRUE
FROM users u
WHERE u.email = 'cosplay@test.com'
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
    ('Premium', 2, 7, 550.00, '3-hour session, 50 edited images, and prints'),
    ('Basic', 3, 3, 300.00, '2-hour event coverage, 20 edited digital images'),
    ('Standard', 3, 3, 500.00, '4-hour event coverage, 50 edited digital images'),
    ('Premium', 3, 3, 800.00, '6-hour event coverage, 100 edited images, and prints'),
    ('Basic', 4, 4, 180.00, '1-hour pet session, 15 edited digital images'),
    ('Standard', 4, 4, 280.00, '1.5-hour pet session, 25 edited digital images'),
    ('Premium', 4, 4, 400.00, '2-hour pet session, 40 edited images, and prints'),
    ('Basic', 5, 5, 200.00, '2-hour party coverage, 20 edited digital images'),
    ('Standard', 5, 5, 350.00, '3-hour party coverage, 40 edited digital images'),
    ('Premium', 5, 5, 500.00, '4-hour party coverage, 60 edited images, and prints'),
    ('Basic', 6, 6, 250.00, '1-hour maternity session, 15 edited digital images'),
    ('Standard', 6, 6, 400.00, '1.5-hour maternity session, 30 edited digital images'),
    ('Premium', 6, 6, 600.00, '2-hour maternity session, 50 edited images, and prints'),
    ('Basic', 7, 7, 300.00, '1-hour newborn session, 15 edited digital images'),
    ('Standard', 7, 7, 450.00, '2-hour newborn session, 30 edited digital images'),
    ('Premium', 7, 7, 650.00, '3-hour newborn session, 50 edited images, and prints'),
    ('Basic', 8, 8, 400.00, '1-hour branding session, 10 edited digital images'),
    ('Standard', 8, 8, 600.00, '2-hour branding session, 20 edited digital images'),
    ('Premium', 8, 8, 900.00, '3-hour branding session, 35 edited images, and prints'),
    ('Basic', 9, 9, 250.00, '1-hour sports session, 20 edited digital images'),
    ('Standard', 9, 9, 400.00, '2-hour sports session, 40 edited digital images'),
    ('Premium', 9, 9, 600.00, '3-hour sports session, 60 edited images, and prints'),
    ('Basic', 10, 10, 200.00, '1-hour cosplay session, 15 edited digital images'),
    ('Standard', 10, 10, 350.00, '1.5-hour cosplay session, 30 edited digital images'),
    ('Premium', 10, 10, 500.00, '2-hour cosplay session, 50 edited images, and prints')
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
    (2,"Pet sample 3","Pet sample 3","pet3.jpg"),
    (3,"Corporate Conference","Professional corporate event photography","events_corporate1.jpg"),
    (3,"Wedding Reception","Elegant wedding reception coverage","events_wedding1.jpg"),
    (3,"Product Launch","Dynamic product launch event","events_product1.jpg"),
    (3,"Charity Gala","Sophisticated charity event","events_charity1.jpg"),
    (3,"Conference Speaker","Professional speaker photography","events_speaker1.jpg"),
    (4,"Golden Retriever","Happy dog portrait in natural light","pet_dog1.jpg"),
    (4,"Cat Portrait","Elegant cat photography","pet_cat1.jpg"),
    (4,"Dog Action","Dynamic dog action shot","pet_action1.jpg"),
    (4,"Pet Family","Pet with family portrait","pet_family1.jpg"),
    (4,"Exotic Pet","Unique exotic pet photography","pet_exotic1.jpg"),
    (5,"Birthday Celebration","Fun birthday party moments","party_birthday1.jpg"),
    (5,"Anniversary Party","Romantic anniversary celebration","party_anniversary1.jpg"),
    (5,"Kids Party","Joyful children's party","party_kids1.jpg"),
    (5,"Cocktail Party","Elegant cocktail event","party_cocktail1.jpg"),
    (5,"Surprise Party","Exciting surprise celebration","party_surprise1.jpg"),
    (6,"Elegant Maternity","Beautiful maternity portrait","maternity_elegant1.jpg"),
    (6,"Outdoor Maternity","Natural outdoor maternity shoot","maternity_outdoor1.jpg"),
    (6,"Studio Maternity","Professional studio maternity","maternity_studio1.jpg"),
    (6,"Couple Maternity","Expecting parents together","maternity_couple1.jpg"),
    (6,"Artistic Maternity","Creative maternity photography","maternity_artistic1.jpg"),
    (7,"Sleeping Newborn","Peaceful newborn portrait","newborn_sleeping1.jpg"),
    (7,"Family Newborn","Newborn with family","newborn_family1.jpg"),
    (7,"Newborn Props","Creative newborn prop shots","newborn_props1.jpg"),
    (7,"Tiny Details","Newborn detail photography","newborn_details1.jpg"),
    (7,"Newborn Lifestyle","Natural newborn lifestyle","newborn_lifestyle1.jpg"),
    (8,"Corporate Headshot","Professional business portrait","branding_headshot1.jpg"),
    (8,"Product Photography","Clean product shots","branding_product1.jpg"),
    (8,"Team Photo","Corporate team photography","branding_team1.jpg"),
    (8,"Office Environment","Professional workspace","branding_office1.jpg"),
    (8,"Executive Portrait","Senior executive photography","branding_executive1.jpg"),
    (9,"Football Action","Dynamic sports action shot","sports_football1.jpg"),
    (9,"Swimming Competition","Underwater sports photography","sports_swimming1.jpg"),
    (9,"Basketball Game","Fast-paced basketball action","sports_basketball1.jpg"),
    (9,"Track and Field","Athletic competition moments","sports_track1.jpg"),
    (9,"Team Victory","Celebration moments","sports_victory1.jpg"),
    (10,"Fantasy Character","Epic fantasy cosplay","cosplay_fantasy1.jpg"),
    (10,"Anime Character","Anime character recreation","cosplay_anime1.jpg"),
    (10,"Superhero Costume","Superhero cosplay photography","cosplay_superhero1.jpg"),
    (10,"Medieval Character","Medieval fantasy cosplay","cosplay_medieval1.jpg"),
    (10,"Sci-Fi Character","Science fiction cosplay","cosplay_scifi1.jpg")
ON DUPLICATE KEY UPDATE photographer_id=photographer_id;

-- Insert sample cart
INSERT INTO cart (customer_id, subtotal, status) VALUES
    (1, 200, 'Completed'),
    (1, 900, 'Completed'),
    (2, 800, 'Completed')
ON DUPLICATE KEY UPDATE id=id;

-- Insert sample cart_item
INSERT INTO cart_item (cart_id, photographer_id, package_id, price, event_date, event_time, pax, notes, event_location) VALUES
    (1, 1, 19, 200, '2025-11-21','15:00', 2, 'Sample photoshoot notes', 'Brisbane'),
    (2, 1, 5, 350, '2025-11-10', '09:00', 20, 'Sample photoshoot notes', 'Gold Coast'),
    (2, 2, 21, 550, '2025-12-21','10:00', 10, 'Sample photoshoot notes', 'Sunshine Coast'),
    (3, 1, 13, 250, '2025-12-01','11:00', 5, 'Sample photoshoot notes', 'Brisbane'),
    (3, 2, 22, 200, '2025-12-19','12:00', 4, 'Sample photoshoot notes', 'Gold Coast'),
    (3, 2, 29, 350, '2025-12-30','13:00', 3, 'Sample photoshoot notes', 'Sunshine Coast')
ON DUPLICATE KEY UPDATE id=id;

-- Insert sample bookings
INSERT INTO bookings (cart_id, customer_id, payment_date, total_amount, status) VALUES
    (1, 1, CURRENT_TIMESTAMP, 200, 'Completed'),
    (2, 1, CURRENT_TIMESTAMP, 900, 'Completed'),
    (3, 2, CURRENT_TIMESTAMP, 800, 'Completed')
ON DUPLICATE KEY UPDATE id=id;
