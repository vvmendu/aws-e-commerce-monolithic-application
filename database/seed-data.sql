USE ecommerce_db;

-- CATEGORIES
INSERT INTO categories (id, name, slug, description) VALUES
(1, 'Electronics', 'electronics', 'Gadgets, devices, and tech accessories'),
(2, 'Household Items', 'household', 'Appliances, furniture, and home décor'),
(3, 'Books', 'books', 'Fiction, non-fiction, textbooks, and more'),
(4, 'Clothing & Fashion','clothing', 'Apparel for men, women, and kids'),
(5, 'Sports & Outdoors', 'sports', 'Fitness, camping, and outdoor gear'),
(6, 'Best Sellers', 'bestsellers', 'Top-selling cross-category products'),
(7, 'Gift Cards', 'giftcards', 'Digital gift cards for every occasion');

-- ADMIN USER (password: Admin@12345)
INSERT INTO users (email, password_hash, first_name, last_name, role) VALUES
('admin@shopnow.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/lewdBPj6hsxq5Sqq', 'Admin', 'User', 'admin');

-- Sample customer accounts (password: Test@12345)
INSERT INTO users (email, password_hash, first_name, last_name, role) VALUES
('alice@example.com', '$2b$12$KIXHc1yqBWVHxkd0LHAkCOiZ8UvxNRKrhO9/lewdBPj6hsxq5Test', 'Alice', 'Johnson', 'customer'),
('bob@example.com', '$2b$12$KIXHc1yqBWVHxkd0LHAkCOiZ8UvxNRKrhO9/lewdBPj6hsxq5Test', 'Bob', 'Smith', 'customer'),
('carol@example.com', '$2b$12$KIXHc1yqBWVHxkd0LHAkCOiZ8UvxNRKrhO9/lewdBPj6hsxq5Test', 'Carol', 'Williams', 'customer');

-- ELECTRONICS
INSERT INTO products (category_id, name, slug, description, price, sale_price, sku, stock_qty, rating_avg, rating_count, brand, is_featured, is_bestseller) VALUES
(1, 'Apple MacBook Pro 14-inch M3', 'apple-macbook-pro-14-m3', 'The MacBook Pro 14-inch features the powerful M3 chip with an 8-core CPU and 10-core GPU. Stunning Liquid Retina XDR display, up to 18 hours battery life, and 16GB unified memory.', 1999.99, 1849.99, 'ELEC-001', 45, 4.80, 312, 'Apple', 1, 1),
(1, 'Samsung Galaxy S24 Ultra', 'samsung-galaxy-s24-ultra', 'Experience the pinnacle of Android innovation with the Galaxy S24 Ultra. Features a 200MP main camera, built-in S Pen, 6.8-inch Dynamic AMOLED display with 120Hz refresh rate.', 1299.99, 1199.99, 'ELEC-002', 78, 4.70, 489, 'Samsung', 1, 1),
(1, 'Sony WH-1000XM5 Headphones', 'sony-wh1000xm5', 'Industry-leading noise canceling headphones with 30-hour battery life and multipoint connection. Features eight microphones and two processors for precise noise isolation.', 349.99, 279.99, 'ELEC-003', 120, 4.85, 678, 'Sony', 0, 1),
(1, 'iPad Pro 12.9-inch M2', 'ipad-pro-12-9-m2', 'The iPad Pro features the Apple M2 chip, bringing desktop-class performance to the ultimate iPad experience. The stunning 12.9-inch Liquid Retina XDR display, advanced cameras.', 1099.99, NULL, 'ELEC-004', 60, 4.75, 203, 'Apple', 1, 0),
(1, 'Canon EOS R6 Mark II Camera', 'canon-eos-r6-mark-ii', 'The EOS R6 Mark II offers 40fps continuous shooting, 6K RAW video output, and Dual Pixel CMOS AF II with subject recognition. Weather-sealed magnesium alloy body.', 2499.99, 2299.99, 'ELEC-006', 22, 4.90, 87, 'Canon', 1, 0);

-- HOUSEHOLD ITEMS
INSERT INTO products (category_id, name, slug, description, price, sale_price, sku, stock_qty, rating_avg, rating_count, brand, is_featured, is_bestseller) VALUES
(2, 'Instant Pot Duo Plus 9-in-1', 'instant-pot-duo-plus-9in1', 'The Instant Pot Duo Plus is a 9-in-1 electric pressure cooker that speeds up cooking by 2-6x. Functions include pressure cooker, slow cooker, rice cooker, steamer, sauté, yogurt maker, sterilizer, and food warmer.', 99.95, 79.95, 'HOME-001', 150, 4.80, 3421, 'Instant Pot', 1, 1),
(2, 'Dyson V15 Detect Vacuum', 'dyson-v15-detect', 'The most powerful cordless vacuum Dyson has ever made with laser dust detection. HEPA filtration captures 99.97% of particles. Up to 60 minutes runtime with LCD screen.', 749.99, 649.99, 'HOME-002', 65, 4.75, 892, 'Dyson', 1, 1),
(2, 'KitchenAid Artisan Stand Mixer', 'kitchenaid-artisan-stand-mixer', 'The iconic KitchenAid Artisan Stand Mixer with 5-quart stainless steel bowl and 10-speed settings. Includes flat beater, dough hook, and wire whip attachments.', 449.99, 399.99, 'HOME-003', 80, 4.90, 2134, 'KitchenAid', 1, 1);

-- BOOKS
INSERT INTO products (category_id, name, slug, description, price, sale_price, sku, stock_qty, rating_avg, rating_count, brand, is_featured, is_bestseller) VALUES
(3, 'Atomic Habits by James Clear', 'atomic-habits-james-clear', 'The #1 New York Times bestseller about tiny changes that yield remarkable results. Over 10 million copies sold worldwide.', 16.99, 13.99, 'BOOK-001', 500, 4.90, 45678, 'Penguin', 1, 1),
(3, 'Sapiens: A Brief History of Humankind', 'sapiens-brief-history-harari', 'Yuval Noah Harari explores the history and impact of Homo sapiens from the Stone Age to the twenty-first century.', 17.99, 14.99, 'BOOK-003', 400, 4.75, 23456, 'Harper', 1, 1),
(3, 'AWS Certified Solutions Architect Study Guide', 'aws-certified-solutions-architect-guide', 'The ultimate study guide for the AWS Certified Solutions Architect Associate exam. Covers all domains including design resilient architectures.', 59.99, 49.99, 'BOOK-008', 200, 4.65, 3456, 'Sybex', 1, 0);

-- CLOTHING
INSERT INTO products (category_id, name, slug, description, price, sale_price, sku, stock_qty, rating_avg, rating_count, brand, is_featured, is_bestseller) VALUES
(4, "Levi's 501 Original Jeans Men's", 'levis-501-original-mens', "The iconic 501 Original Jeans that started it all. Made from 100% cotton denim with button fly and straight leg fit.", 69.99, 54.99, 'CLTH-001', 200, 4.70, 8901, "Levi's", 1, 1),
(4, 'Nike Air Max 270 Sneakers', 'nike-air-max-270', "The Nike Air Max 270 features Nike's biggest heel Air unit yet. The sleek upper is made from engineered mesh for breathability.", 150.00, 119.99, 'CLTH-002', 180, 4.75, 12345, 'Nike', 1, 1),
(4, 'Patagonia Better Sweater Fleece Jacket', 'patagonia-better-sweater-fleece', 'Made from 100% recycled polyester fleece. Features a zip-up front, self-fabric collar, and regular fit. Fair Trade Certified sewn.', 149.00, 119.00, 'CLTH-003', 90, 4.85, 3456, 'Patagonia', 0, 1);

-- SPORTS & OUTDOORS
INSERT INTO products (category_id, name, slug, description, price, sale_price, sku, stock_qty, rating_avg, rating_count, brand, is_featured, is_bestseller) VALUES
(5, 'Bowflex SelectTech 552 Adjustable Dumbbells', 'bowflex-selecttech-552', 'Replace 15 sets of weights with one pair. Adjusts from 5 to 52.5 pounds in 2.5-pound increments.', 429.00, 379.00, 'SPRT-003', 55, 4.80, 5678, 'Bowflex', 1, 1),
(5, 'Hydro Flask 32 oz Wide Mouth Water Bottle', 'hydroflask-32oz-wide-mouth', 'TempShield double-wall vacuum insulation keeps drinks cold up to 24 hours and hot up to 12 hours. BPA-free 18/8 stainless steel.', 44.95, 39.95, 'SPRT-005', 300, 4.85, 8901, 'Hydro Flask', 0, 1),
(5, 'Yeti Tundra 45 Cooler', 'yeti-tundra-45-cooler', 'Puncture-resistant rotomolded construction keeps ice longer. PermaFrost insulation and ColdLock gasket. Holds 28 cans.', 325.00, 299.00, 'SPRT-006', 40, 4.75, 3456, 'Yeti', 0, 1);

-- BEST SELLERS
INSERT INTO products (category_id, name, slug, description, price, sale_price, sku, stock_qty, rating_avg, rating_count, brand, is_featured, is_bestseller) VALUES
(6, '[BS] Apple AirPods Pro 2nd Generation', 'bs-airpods-pro-2nd-gen', 'The best-in-class ANC earbuds with Adaptive Audio. USB-C MagSafe charging case. 30 total hours with case.', 249.99, 219.99, 'BSEL-001', 250, 4.85, 23456, 'Apple', 1, 1),
(6, '[BS] Instant Pot Duo 7-in-1 6-Quart', 'bs-instant-pot-duo-7in1', "America's #1 selling multi-cooker. 10 safety features. Capacity feeds 4-6 people.", 99.99, 79.99, 'BSEL-002', 300, 4.80, 45678, 'Instant Pot', 1, 1);

-- GIFT CARDS
INSERT INTO products (category_id, name, slug, description, price, sku, stock_qty, rating_avg, rating_count, brand, is_featured, is_bestseller) VALUES
(7, 'ShopNow $25 Gift Card', 'shopnow-gift-card-25', 'Digital gift card delivered instantly by email. Valid for any purchase. No fees, no expiration.', 25.00, 'GIFT-025', 9999, 5.00, 1234, 'ShopNow', 0, 0),
(7, 'ShopNow $50 Gift Card', 'shopnow-gift-card-50', 'Digital gift card delivered instantly by email. The most popular denomination.', 50.00, 'GIFT-050', 9999, 5.00, 1567, 'ShopNow', 1, 1),
(7, 'ShopNow $100 Gift Card', 'shopnow-gift-card-100', 'Digital gift card delivered instantly by email. Give the gift of choice.', 100.00, 'GIFT-100', 9999, 5.00, 2345, 'ShopNow', 1, 1);

-- PRODUCT IMAGES
INSERT INTO product_images (product_id, image_url, alt_text, is_primary, sort_order) VALUES
(1, 'https://ecommerce-images.s3.amazonaws.com/macbook-pro-m3-1.jpg', 'MacBook Pro 14-inch M3 front view', 1, 1),
(1, 'https://ecommerce-images.s3.amazonaws.com/macbook-pro-m3-2.jpg', 'MacBook Pro 14-inch M3 side view', 0, 2),
(2, 'https://ecommerce-images.s3.amazonaws.com/galaxy-s24-ultra-1.jpg', 'Samsung Galaxy S24 Ultra', 1, 1);
