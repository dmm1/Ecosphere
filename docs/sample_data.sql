-- Alter the crm_customer table to add the industry field
ALTER TABLE crm_customer ADD COLUMN industry VARCHAR(255) NULL;

-- Insert sample customers with industries
INSERT INTO crm_customer (name, email, phone, created_at, updated_at, user_id, industry) VALUES
('John Doe', 'john.doe@example.com', '555-1234', NOW(), NOW(), (SELECT id FROM auth_user WHERE username = 'john_doe_1'), 'Technology');

INSERT INTO crm_customer (name, email, phone, created_at, updated_at, user_id, industry) VALUES
('Jane Smith', 'jane.smith@example.com', '555-5678', NOW(), NOW(), (SELECT id FROM auth_user WHERE username = 'jane_smith_1'), 'Manufacturing');

INSERT INTO crm_customer (name, email, phone, created_at, updated_at, user_id, industry) VALUES
('Michael Johnson', 'michael.johnson@example.com', '555-9012', NOW(), NOW(), (SELECT id FROM auth_user WHERE username = 'michael_johnson_1'), 'Retail');

INSERT INTO crm_customer (name, email, phone, created_at, updated_at, user_id, industry) VALUES
('Emily Brown', 'emily.brown@example.com', '555-3456', NOW(), NOW(), (SELECT id FROM auth_user WHERE username = 'emily_brown_1'), 'Healthcare');

INSERT INTO crm_customer (name, email, phone, created_at, updated_at, user_id, industry) VALUES
('David Lee', 'david.lee@example.com', '555-7890', NOW(), NOW(), (SELECT id FROM auth_user WHERE username = 'david_lee_1'), 'Finance');

INSERT INTO crm_customer (name, email, phone, created_at, updated_at, user_id, industry) VALUES
('Sarah Davis', 'sarah.davis@example.com', '555-2345', NOW(), NOW(), (SELECT id FROM auth_user WHERE username = 'sarah_davis_1'), 'Education');

INSERT INTO crm_customer (name, email, phone, created_at, updated_at, user_id, industry) VALUES
('Robert Wilson', 'robert.wilson@example.com', '555-6789', NOW(), NOW(), (SELECT id FROM auth_user WHERE username = 'robert_wilson_1'), 'Construction');

INSERT INTO crm_customer (name, email, phone, created_at, updated_at, user_id, industry) VALUES
('Olivia Martinez', 'olivia.martinez@example.com', '555-0123', NOW(), NOW(), (SELECT id FROM auth_user WHERE username = 'olivia_martinez_1'), 'Transportation');

INSERT INTO crm_customer (name, email, phone, created_at, updated_at, user_id, industry) VALUES
('William Hernandez', 'william.hernandez@example.com', '555-4567', NOW(), NOW(), (SELECT id FROM auth_user WHERE username = 'william_hernandez_1'), 'Agriculture');

INSERT INTO crm_customer (name, email, phone, created_at, updated_at, user_id, industry) VALUES
('Sophia Gutierrez', 'sophia.gutierrez@example.com', '555-8901', NOW(), NOW(), (SELECT id FROM auth_user WHERE username = 'sophia_gutierrez_1'), 'Energy');
