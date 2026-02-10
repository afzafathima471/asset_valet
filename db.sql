-- Asset Management System Database Dump
-- Target: PostgreSQL
-- Purpose: HR/Admin Managed Asset Tracking

-- -----------------------------------------------------
-- 1. Departments Table
-- -----------------------------------------------------
CREATE TABLE departments (
    id SERIAL PRIMARY KEY,
    department_name VARCHAR(100) NOT NULL,
    cost_center_code VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO departments (department_name, cost_center_code) VALUES 
('Engineering', 'CC-101'),
('Human Resources', 'CC-202'),
('Marketing', 'CC-303'),
('Operations', 'CC-404');

-- -----------------------------------------------------
-- 2. Employees Table (Managed by Admin/HR)
-- -----------------------------------------------------
CREATE TABLE employees (
    id SERIAL PRIMARY KEY,
    employee_code VARCHAR(20) UNIQUE NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(150),
    department_id INTEGER, -- logical reference to departments.id
    job_title VARCHAR(100),
    status VARCHAR(20) DEFAULT 'active', -- active, terminated, on_leave
    joining_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO employees (employee_code, first_name, last_name, email, department_id, job_title, joining_date) VALUES 
('EMP001', 'John', 'Doe', 'john.doe@company.com', 1, 'Senior Developer', '2022-01-15'),
('EMP002', 'Jane', 'Smith', 'jane.smith@company.com', 2, 'HR Specialist', '2021-06-01'),
('EMP003', 'Alice', 'Johnson', 'alice.j@company.com', 3, 'Campaign Manager', '2023-03-10');

-- -----------------------------------------------------
-- 3. Admin Users Table (System Access)
-- -----------------------------------------------------
CREATE TABLE admin_users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    full_name VARCHAR(100),
    role VARCHAR(20) NOT NULL, -- super_admin, hr_admin, it_admin
    last_login TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO admin_users (username, password_hash, full_name, role) VALUES 
('admin_master', '$2b$12$LQvPHiZ2N/pGZ9.eM.W8e.fHl', 'System Administrator', 'super_admin'),
('hr_sarah', '$2b$12$R9h/pGZ9.eM.W8e.fHlLQvPHiZ2N', 'Sarah Jenkins', 'hr_admin'),
('it_mike', '$2b$12$W8e.fHlLQvPHiZ2NR9h/pGZ9.eM.', 'Mike Ross', 'it_admin');

-- -----------------------------------------------------
-- 4. Assets Table
-- -----------------------------------------------------
CREATE TABLE assets (
    id SERIAL PRIMARY KEY,
    asset_tag VARCHAR(50) UNIQUE NOT NULL, -- Unique barcode/RFID tag
    name VARCHAR(255) NOT NULL,
    category VARCHAR(50), -- Laptop, Furniture, Vehicle, Mobile
    serial_number VARCHAR(100),
    model_number VARCHAR(100),
    manufacturer VARCHAR(100),
    purchase_date DATE,
    purchase_cost DECIMAL(12, 2),
    status VARCHAR(30) DEFAULT 'available', -- available, assigned, maintenance, retired, lost
    current_condition VARCHAR(50) DEFAULT 'new', -- new, good, fair, poor, damaged
    location VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO assets (asset_tag, name, category, serial_number, manufacturer, purchase_cost, status) VALUES 
('AST-LAP-001', 'MacBook Pro 16"', 'Laptop', 'SN12345678', 'Apple', 2500.00, 'assigned'),
('AST-LAP-002', 'Dell XPS 15', 'Laptop', 'SN87654321', 'Dell', 1800.00, 'available'),
('AST-MON-001', 'LG UltraWide 34"', 'Monitor', 'MON-9900', 'LG', 600.00, 'assigned'),
('AST-CHR-050', 'Ergonomic Office Chair', 'Furniture', 'FURN-050', 'Herman Miller', 1200.00, 'available');

-- -----------------------------------------------------
-- 5. Asset Assignments Table (Tracking)
-- -----------------------------------------------------
CREATE TABLE asset_assignments (
    id SERIAL PRIMARY KEY,
    asset_id INTEGER NOT NULL, -- logical reference to assets.id
    employee_id INTEGER NOT NULL, -- logical reference to employees.id
    assigned_by_admin_id INTEGER NOT NULL, -- logical reference to admin_users.id
    assignment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expected_return_date DATE,
    actual_return_date TIMESTAMP,
    initial_condition VARCHAR(50),
    return_condition VARCHAR(50),
    notes TEXT
);

INSERT INTO asset_assignments (asset_id, employee_id, assigned_by_admin_id, initial_condition) VALUES 
(1, 1, 3, 'new'),
(3, 1, 3, 'good');

-- -----------------------------------------------------
-- 6. Condition Reports Table
-- -----------------------------------------------------
CREATE TABLE condition_reports (
    id SERIAL PRIMARY KEY,
    asset_id INTEGER NOT NULL, -- logical reference to assets.id
    reported_by_admin_id INTEGER NOT NULL, -- logical reference to admin_users.id
    report_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    condition_status VARCHAR(50) NOT NULL,
    description TEXT,
    action_taken VARCHAR(100), -- none, repair_requested, decommissioned
    photo_url TEXT
);

INSERT INTO condition_reports (asset_id, reported_by_admin_id, condition_status, description) VALUES 
(1, 3, 'good', 'Routine check-up during software update.'),
(2, 3, 'fair', 'Minor scratches on the bottom casing.');

-- -----------------------------------------------------
-- 7. Audit Logs Table (Admin Actions Tracking)
-- -----------------------------------------------------
CREATE TABLE audit_logs (
    id SERIAL PRIMARY KEY,
    admin_id INTEGER NOT NULL, -- logical reference to admin_users.id
    action_type VARCHAR(50) NOT NULL, -- CREATE, UPDATE, DELETE, ASSIGN, RETURN
    target_table VARCHAR(50) NOT NULL,
    target_id INTEGER, -- logical reference to row in target_table
    action_details TEXT,
    ip_address VARCHAR(45),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO audit_logs (admin_id, action_type, target_table, target_id, action_details) VALUES 
(1, 'CREATE', 'employees', 1, 'Added new employee: John Doe'),
(3, 'ASSIGN', 'assets', 1, 'Assigned MacBook Pro to John Doe'),
(2, 'UPDATE', 'assets', 2, 'Updated condition status for Dell XPS');

-- -----------------------------------------------------
-- Indexes for Performance
-- -----------------------------------------------------
CREATE INDEX idx_asset_tag ON assets(asset_tag);
CREATE INDEX idx_employee_code ON employees(employee_code);
CREATE INDEX idx_assignment_asset ON asset_assignments(asset_id);
CREATE INDEX idx_assignment_employee ON asset_assignments(employee_id);