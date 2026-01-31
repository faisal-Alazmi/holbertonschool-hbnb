-- HBnB Initial Data
-- This script inserts the administrator user and initial amenities

-- Insert Administrator User
-- Password: admin1234 (hashed with bcrypt)
INSERT INTO users (id, first_name, last_name, email, password, is_admin, created_at, updated_at)
VALUES (
    '36c9050e-ddd3-4c3b-9731-9f487208bbc1',
    'Admin',
    'HBnB',
    'admin@hbnb.io',
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYqGj1Gj9Da',
    TRUE,
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP
);

-- Insert Initial Amenities
INSERT INTO amenities (id, name, created_at, updated_at)
VALUES
    ('557d60c7-88ee-411b-9384-4f8d0742f398', 'WiFi', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
    ('53b0e16f-1bd0-4572-b3f9-f3957537ed5f', 'Swimming Pool', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
    ('f842930b-630a-4741-8bda-8e346e49bb7a', 'Air Conditioning', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);
