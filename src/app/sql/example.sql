-- Example SQL File
-- This demonstrates various SQL operations that can be executed using mysql client

-- ============================================
-- DATABASE SETUP
-- ============================================

-- Create database if not exists (usually handled by docker-compose)
-- CREATE DATABASE IF NOT EXISTS my_db;
-- USE my_db;

-- ============================================
-- TABLE CREATION
-- ============================================

-- Create a users table
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    full_name VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    INDEX idx_username (username),
    INDEX idx_email (email)
);

-- Create a posts table
CREATE TABLE IF NOT EXISTS posts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    title VARCHAR(200) NOT NULL,
    content TEXT,
    published_at TIMESTAMP NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_published_at (published_at)
);

-- Create a comments table
CREATE TABLE IF NOT EXISTS comments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    post_id INT NOT NULL,
    user_id INT NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (post_id) REFERENCES posts(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_post_id (post_id),
    INDEX idx_user_id (user_id)
);

-- ============================================
-- INSERT SAMPLE DATA
-- ============================================

-- Insert sample users
INSERT INTO users (username, email, full_name) VALUES
    ('john_doe', 'john@example.com', 'John Doe'),
    ('jane_smith', 'jane@example.com', 'Jane Smith'),
    ('bob_wilson', 'bob@example.com', 'Bob Wilson'),
    ('alice_brown', 'alice@example.com', 'Alice Brown')
ON DUPLICATE KEY UPDATE updated_at = CURRENT_TIMESTAMP;

-- Insert sample posts
INSERT INTO posts (user_id, title, content, published_at) VALUES
    (1, 'Getting Started with MySQL', 'MySQL is a powerful relational database...', NOW()),
    (1, 'Advanced SQL Queries', 'Learn about joins, subqueries, and more...', NOW()),
    (2, 'Python and Databases', 'How to connect Python with MySQL...', NOW()),
    (3, 'Docker Compose Tutorial', 'Setting up multi-container applications...', NOW()),
    (4, 'Best Practices for Database Design', 'Normalization and optimization tips...', NOW())
ON DUPLICATE KEY UPDATE updated_at = CURRENT_TIMESTAMP;

-- Insert sample comments
INSERT INTO comments (post_id, user_id, content) VALUES
    (1, 2, 'Great introduction! Very helpful for beginners.'),
    (1, 3, 'Thanks for sharing this.'),
    (2, 4, 'The section on subqueries was particularly useful.'),
    (3, 1, 'Nice work! I would add more examples on ORM usage.'),
    (3, 4, 'Very comprehensive guide.'),
    (4, 2, 'Docker makes deployment so much easier!'),
    (5, 1, 'Excellent tips on normalization.')
ON DUPLICATE KEY UPDATE created_at = CURRENT_TIMESTAMP;

-- ============================================
-- QUERY EXAMPLES
-- ============================================

-- Select all users
SELECT * FROM users;

-- Select active users only
SELECT username, email, full_name 
FROM users 
WHERE is_active = TRUE
ORDER BY created_at DESC;

-- Get posts with user information (JOIN)
SELECT 
    p.id,
    p.title,
    p.content,
    u.username,
    u.full_name,
    p.published_at,
    p.created_at
FROM posts p
INNER JOIN users u ON p.user_id = u.id
ORDER BY p.published_at DESC;

-- Get posts with comment count
SELECT 
    p.id,
    p.title,
    u.username AS author,
    COUNT(c.id) AS comment_count,
    p.published_at
FROM posts p
INNER JOIN users u ON p.user_id = u.id
LEFT JOIN comments c ON p.id = c.post_id
GROUP BY p.id, p.title, u.username, p.published_at
ORDER BY comment_count DESC;

-- Get all comments for a specific post with user info
SELECT 
    c.id,
    c.content,
    u.username,
    u.full_name,
    c.created_at
FROM comments c
INNER JOIN users u ON c.user_id = u.id
WHERE c.post_id = 1
ORDER BY c.created_at ASC;

-- Get user activity summary
SELECT 
    u.username,
    u.full_name,
    COUNT(DISTINCT p.id) AS post_count,
    COUNT(DISTINCT c.id) AS comment_count,
    MAX(p.created_at) AS last_post_date,
    MAX(c.created_at) AS last_comment_date
FROM users u
LEFT JOIN posts p ON u.id = p.user_id
LEFT JOIN comments c ON u.id = c.user_id
GROUP BY u.id, u.username, u.full_name
ORDER BY post_count DESC, comment_count DESC;

-- Search posts by title keyword
SELECT 
    p.title,
    u.username AS author,
    p.published_at
FROM posts p
INNER JOIN users u ON p.user_id = u.id
WHERE p.title LIKE '%SQL%'
ORDER BY p.published_at DESC;

-- ============================================
-- UPDATE EXAMPLES
-- ============================================

-- Update user information
-- UPDATE users 
-- SET full_name = 'John Michael Doe'
-- WHERE username = 'john_doe';

-- Mark a user as inactive
-- UPDATE users 
-- SET is_active = FALSE
-- WHERE username = 'bob_wilson';

-- ============================================
-- DELETE EXAMPLES (commented out for safety)
-- ============================================

-- Delete a specific comment
-- DELETE FROM comments WHERE id = 1;

-- Delete all comments for a specific post
-- DELETE FROM comments WHERE post_id = 1;

-- Delete a user (will cascade to their posts and comments)
-- DELETE FROM users WHERE username = 'bob_wilson';

-- ============================================
-- UTILITY QUERIES
-- ============================================

-- Show table structure
DESCRIBE users;
DESCRIBE posts;
DESCRIBE comments;

-- Show all tables in database
SHOW TABLES;

-- Get table row counts
SELECT 
    'users' AS table_name, 
    COUNT(*) AS row_count 
FROM users
UNION ALL
SELECT 
    'posts' AS table_name, 
    COUNT(*) AS row_count 
FROM posts
UNION ALL
SELECT 
    'comments' AS table_name, 
    COUNT(*) AS row_count 
FROM comments;

-- ============================================
-- CLEANUP (commented out for safety)
-- ============================================

-- Drop tables (in correct order due to foreign keys)
-- DROP TABLE IF EXISTS comments;
-- DROP TABLE IF EXISTS posts;
-- DROP TABLE IF EXISTS users;
