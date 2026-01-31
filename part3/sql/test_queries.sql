-- HBnB Test Queries
-- This script contains test queries to verify CRUD operations

-- ============================================
-- SELECT Operations (READ)
-- ============================================

-- Test 1: Verify admin user exists
SELECT 'Test 1: Verify admin user' AS test_name;
SELECT id, first_name, last_name, email, is_admin
FROM users
WHERE email = 'admin@hbnb.io';

-- Test 2: Verify amenities were inserted
SELECT 'Test 2: List all amenities' AS test_name;
SELECT id, name FROM amenities ORDER BY name;

-- Test 3: Count users
SELECT 'Test 3: Count users' AS test_name;
SELECT COUNT(*) as total_users FROM users;

-- ============================================
-- INSERT Operations (CREATE)
-- ============================================

-- Test 4: Insert a regular user
SELECT 'Test 4: Insert regular user' AS test_name;
INSERT INTO users (id, first_name, last_name, email, password, is_admin)
VALUES (
    'a1b2c3d4-e5f6-7890-abcd-ef1234567890',
    'John',
    'Doe',
    'john.doe@example.com',
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYqGj1Gj9Da',
    FALSE
);

-- Test 5: Insert a place
SELECT 'Test 5: Insert a place' AS test_name;
INSERT INTO places (id, title, description, price, latitude, longitude, owner_id)
VALUES (
    'b2c3d4e5-f6a7-8901-bcde-f12345678901',
    'Cozy Apartment',
    'A beautiful apartment in the city center',
    120.50,
    40.7128,
    -74.0060,
    '36c9050e-ddd3-4c3b-9731-9f487208bbc1'
);

-- Test 6: Link amenities to the place
SELECT 'Test 6: Link amenities to place' AS test_name;
INSERT INTO place_amenity (place_id, amenity_id)
VALUES
    ('b2c3d4e5-f6a7-8901-bcde-f12345678901', '557d60c7-88ee-411b-9384-4f8d0742f398'),
    ('b2c3d4e5-f6a7-8901-bcde-f12345678901', 'f842930b-630a-4741-8bda-8e346e49bb7a');

-- Test 7: Insert a review
SELECT 'Test 7: Insert a review' AS test_name;
INSERT INTO reviews (id, text, rating, user_id, place_id)
VALUES (
    'c3d4e5f6-a7b8-9012-cdef-123456789012',
    'Great place! Very comfortable and clean.',
    5,
    'a1b2c3d4-e5f6-7890-abcd-ef1234567890',
    'b2c3d4e5-f6a7-8901-bcde-f12345678901'
);

-- ============================================
-- Complex SELECT Queries (JOIN Operations)
-- ============================================

-- Test 8: Get all places with their owners
SELECT 'Test 8: Places with owners' AS test_name;
SELECT
    p.id AS place_id,
    p.title,
    p.price,
    u.first_name,
    u.last_name,
    u.email AS owner_email
FROM places p
INNER JOIN users u ON p.owner_id = u.id;

-- Test 9: Get all reviews for a place with user info
SELECT 'Test 9: Reviews for a place' AS test_name;
SELECT
    r.id AS review_id,
    r.text,
    r.rating,
    u.first_name,
    u.last_name,
    p.title AS place_title
FROM reviews r
INNER JOIN users u ON r.user_id = u.id
INNER JOIN places p ON r.place_id = p.id
WHERE p.id = 'b2c3d4e5-f6a7-8901-bcde-f12345678901';

-- Test 10: Get all amenities for a place
SELECT 'Test 10: Amenities for a place' AS test_name;
SELECT
    p.title AS place_title,
    a.name AS amenity_name
FROM places p
INNER JOIN place_amenity pa ON p.id = pa.place_id
INNER JOIN amenities a ON pa.amenity_id = a.id
WHERE p.id = 'b2c3d4e5-f6a7-8901-bcde-f12345678901';

-- Test 11: Get all places owned by a user
SELECT 'Test 11: Places owned by admin' AS test_name;
SELECT
    u.first_name,
    u.last_name,
    COUNT(p.id) AS total_places,
    AVG(p.price) AS average_price
FROM users u
LEFT JOIN places p ON u.id = p.owner_id
WHERE u.email = 'admin@hbnb.io'
GROUP BY u.id, u.first_name, u.last_name;

-- ============================================
-- UPDATE Operations
-- ============================================

-- Test 12: Update user information
SELECT 'Test 12: Update user information' AS test_name;
UPDATE users
SET first_name = 'Jane', last_name = 'Smith'
WHERE email = 'john.doe@example.com';

-- Verify update
SELECT id, first_name, last_name, email FROM users WHERE email = 'john.doe@example.com';

-- Test 13: Update place price
SELECT 'Test 13: Update place price' AS test_name;
UPDATE places
SET price = 150.00
WHERE id = 'b2c3d4e5-f6a7-8901-bcde-f12345678901';

-- Verify update
SELECT id, title, price FROM places WHERE id = 'b2c3d4e5-f6a7-8901-bcde-f12345678901';

-- ============================================
-- DELETE Operations
-- ============================================

-- Test 14: Delete a review
SELECT 'Test 14: Delete a review' AS test_name;
DELETE FROM reviews WHERE id = 'c3d4e5f6-a7b8-9012-cdef-123456789012';

-- Verify deletion
SELECT COUNT(*) AS remaining_reviews FROM reviews;

-- Test 15: Test cascade delete (delete place, should delete place_amenity links)
SELECT 'Test 15: Cascade delete test' AS test_name;
DELETE FROM places WHERE id = 'b2c3d4e5-f6a7-8901-bcde-f12345678901';

-- Verify cascade deletion
SELECT COUNT(*) AS remaining_place_amenities FROM place_amenity;

-- ============================================
-- Constraint Tests
-- ============================================

-- Test 16: Try to insert duplicate email (should fail)
SELECT 'Test 16: Duplicate email constraint' AS test_name;
-- This should fail due to UNIQUE constraint on email
-- INSERT INTO users (id, first_name, last_name, email, password)
-- VALUES ('test-uuid', 'Test', 'User', 'admin@hbnb.io', 'password');

-- Test 17: Try to insert review with rating > 5 (should fail)
SELECT 'Test 17: Rating constraint check' AS test_name;
-- This should fail due to CHECK constraint on rating
-- INSERT INTO reviews (id, text, rating, user_id, place_id)
-- VALUES ('test-uuid', 'Bad rating', 6, 'a1b2c3d4-e5f6-7890-abcd-ef1234567890', 'b2c3d4e5-f6a7-8901-bcde-f12345678901');

-- Test 18: Try to insert duplicate review from same user on same place (should fail)
SELECT 'Test 18: Unique review constraint' AS test_name;
-- This should fail due to UNIQUE constraint on (user_id, place_id)
-- INSERT INTO reviews (id, text, rating, user_id, place_id)
-- VALUES ('test-uuid-1', 'First review', 4, 'a1b2c3d4-e5f6-7890-abcd-ef1234567890', 'b2c3d4e5-f6a7-8901-bcde-f12345678901');
-- INSERT INTO reviews (id, text, rating, user_id, place_id)
-- VALUES ('test-uuid-2', 'Second review', 5, 'a1b2c3d4-e5f6-7890-abcd-ef1234567890', 'b2c3d4e5-f6a7-8901-bcde-f12345678901');

-- ============================================
-- Cleanup (Optional)
-- ============================================

-- Test 19: Cleanup test data
SELECT 'Test 19: Cleanup test data' AS test_name;
DELETE FROM users WHERE email = 'john.doe@example.com';

-- Final verification
SELECT 'Final verification: Remaining data' AS test_name;
SELECT
    (SELECT COUNT(*) FROM users) AS total_users,
    (SELECT COUNT(*) FROM places) AS total_places,
    (SELECT COUNT(*) FROM reviews) AS total_reviews,
    (SELECT COUNT(*) FROM amenities) AS total_amenities;
