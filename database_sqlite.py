import sqlite3

# Step 1: Connect to SQLite database (or create one if it doesn't exist)
conn = sqlite3.connect("rbac_group6.db")

# Step 2: Create a cursor object to execute SQL commands
cursor = conn.cursor()

# Step 3: Drop existing tables if they exist
cursor.execute("DROP TABLE IF EXISTS Log;")
cursor.execute("DROP TABLE IF EXISTS Permission;")
cursor.execute("DROP TABLE IF EXISTS SpecialAccess;")
cursor.execute("DROP TABLE IF EXISTS Access;")
cursor.execute("DROP TABLE IF EXISTS Employee;")
cursor.execute("DROP TABLE IF EXISTS Role;")

# Step 4: Create tables with AUTOINCREMENT primary keys
cursor.execute("""
CREATE TABLE Role (
    RoleID INTEGER PRIMARY KEY AUTOINCREMENT,
    RoleName VARCHAR(32) NOT NULL,
    Description VARCHAR(128),
    CreatedOn TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UpdatedOn TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
""")

cursor.execute("""
CREATE TABLE Employee (
    EmployeeID INTEGER PRIMARY KEY AUTOINCREMENT,
    FirstName VARCHAR(32) NOT NULL,
    LastName VARCHAR(32) NOT NULL,
    Email VARCHAR(32) NOT NULL UNIQUE, 
    Password VARCHAR(64) NOT NULL,
    Phone VARCHAR(12) NOT NULL UNIQUE,
    Department VARCHAR(32),
    RoleID INTEGER NOT NULL,
    HireDate DATE NOT NULL,
    ManagerID INTEGER NOT NULL,
    IsActive BOOLEAN DEFAULT TRUE,
    CreatedOn TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CreatedBy INTEGER,
    UpdatedOn TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UpdatedBy INTEGER,
    FOREIGN KEY (RoleID) REFERENCES Role(RoleID),
    FOREIGN KEY (ManagerID) REFERENCES Employee(EmployeeID)
);
""")

cursor.execute("""
CREATE TABLE Permission (
    PermissionID INTEGER PRIMARY KEY AUTOINCREMENT,
    RoleID INTEGER,
    TableName VARCHAR(32),
    ReadPermission BOOLEAN DEFAULT FALSE,
    WritePermission BOOLEAN DEFAULT FALSE,
    UpdatePermission BOOLEAN DEFAULT FALSE,
    DeletePermission BOOLEAN DEFAULT FALSE,
    CreatedOn TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UpdatedOn TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (RoleID) REFERENCES Role(RoleID)
);
""")

cursor.execute("""
CREATE TABLE Access (
    AccessID INTEGER PRIMARY KEY AUTOINCREMENT,
    RoleID INTEGER,
    Application VARCHAR(64),
    CreatedOn TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UpdatedOn TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (RoleID) REFERENCES Role(RoleID)
);
""")

cursor.execute("""
CREATE TABLE SpecialAccess (
    SpecialAccessID INTEGER PRIMARY KEY AUTOINCREMENT,
    EmployeeID INTEGER,
    SpecialAccessApplication VARCHAR(64),
    Approval BOOLEAN DEFAULT FALSE,
    IsActive BOOLEAN DEFAULT FALSE,
    CreatedOn TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CreatedBy INTEGER,
    UpdatedOn TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UpdatedBy INTEGER,
    FOREIGN KEY (EmployeeID) REFERENCES Employee(EmployeeID)
);
""")

cursor.execute("""
CREATE TABLE Log (
    LogID INTEGER PRIMARY KEY AUTOINCREMENT,
    EmployeeID INTEGER,
    Action VARCHAR(128),
    Timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (EmployeeID) REFERENCES Employee(EmployeeID)
);
""")

# Step 5: Insert sample data (with RoleID, EmployeeID, etc. automatically handled)
cursor.execute("""
INSERT INTO Role (RoleName, Description, CreatedOn, UpdatedOn)
VALUES
('Admin', 'Administrator with full access', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('Manager', 'Manager with moderate access', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('Employee', 'Employee with limited access', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);
""")

cursor.execute("""
INSERT INTO Employee (FirstName, LastName, Email, Password, Phone, Department, RoleID, HireDate, ManagerID, IsActive, CreatedOn, CreatedBy, UpdatedOn, UpdatedBy)
VALUES
('Rajesh', 'Sharma', 'rajesh.sharma@example.com', 'password123', '9876543210', 'Admin', 1, '2020-03-15', 1, TRUE, CURRENT_TIMESTAMP, 1, CURRENT_TIMESTAMP, 1),
('Amit', 'Verma', 'amit.verma@example.com', 'password123', '9876543211', 'Manager', 2, '2018-07-20', 1, TRUE, CURRENT_TIMESTAMP, 1, CURRENT_TIMESTAMP, 1),
('Suresh', 'Gupta', 'suresh.gupta@example.com', 'password123', '9876543212', 'Manager', 2, '2021-01-05', 1, TRUE, CURRENT_TIMESTAMP, 1, CURRENT_TIMESTAMP, 1),
('Priya', 'Nair', 'priya.nair@example.com', 'password123', '9876543213', 'Employee', 3, '2019-02-12', 2, TRUE, CURRENT_TIMESTAMP, 1, CURRENT_TIMESTAMP, 1),
('Sneha', 'Singh', 'sneha.singh@example.com', 'password123', '9876543214', 'Employee', 3, '2021-05-15', 2, TRUE, CURRENT_TIMESTAMP, 1, CURRENT_TIMESTAMP, 1),
('Anjali', 'Patel', 'anjali.patel@example.com', 'password123', '9876543215', 'Employee', 3, '2017-11-30', 2, TRUE, CURRENT_TIMESTAMP, 1, CURRENT_TIMESTAMP, 1),
('Manoj', 'Kulkarni', 'manoj.kulkarni@example.com', 'password123', '9876543216', 'Employee', 3, '2022-03-10', 3, TRUE, CURRENT_TIMESTAMP, 1, CURRENT_TIMESTAMP, 1),
('Sunita', 'Joshi', 'sunita.joshi@example.com', 'password123', '9876543217', 'Employee', 3, '2020-09-25', 3, TRUE, CURRENT_TIMESTAMP, 1, CURRENT_TIMESTAMP, 1),
('Rakesh', 'Mishra', 'rakesh.mishra@example.com', 'password123', '9876543218', 'Employee', 3, '2018-12-15', 3, TRUE, CURRENT_TIMESTAMP, 1, CURRENT_TIMESTAMP, 1),
('Neha', 'Mehta', 'neha.mehta@example.com', 'password123', '9876543219', 'Employee', 3, '2019-06-18', 3, TRUE, CURRENT_TIMESTAMP, 1, CURRENT_TIMESTAMP, 1);
""")

cursor.execute("""
INSERT INTO Permission (RoleID, TableName, ReadPermission, WritePermission, UpdatePermission, DeletePermission, CreatedOn, UpdatedOn)
VALUES
(1, 'Employee', TRUE, TRUE, TRUE, FALSE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(1, 'Role', TRUE, TRUE, TRUE, TRUE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(1, 'Permission', TRUE, TRUE, TRUE, TRUE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(1, 'Access', TRUE, FALSE, FALSE, FALSE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(2, 'Permission', TRUE, FALSE, FALSE, FALSE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(2, 'Employee', TRUE, FALSE, FALSE, FALSE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(2, 'Access', TRUE, FALSE, FALSE, FALSE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(2, 'Role', TRUE, FALSE, FALSE, FALSE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(3, 'Employee', TRUE, FALSE, FALSE, FALSE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(3, 'Access', TRUE, FALSE, FALSE, FALSE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);
""")

cursor.execute("""
INSERT INTO Access (RoleID, Application, CreatedOn, UpdatedOn)
VALUES
(1, 'Create Employee', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(1, 'Edit Employee', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(1, 'Log Data', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(1, 'Special Access Data', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(1, 'Date Application', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(1, 'Clock Application', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(2, 'Log Data', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(2, 'Special Access Data', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(2, 'Date Application', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(2, 'Clock Application', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(2, 'Special Access Granting', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(3, 'ESpecial Access Request', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(3, 'Log Data', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(3, 'Special Access Data', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(3, 'Date Application', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(3, 'Clock Application', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
""")

cursor.execute("""
INSERT INTO SpecialAccess (EmployeeID, SpecialAccessApplication, Approval, IsActive, CreatedOn, CreatedBy, UpdatedOn, UpdatedBy)
VALUES
(4, 'Date Application', TRUE, TRUE, CURRENT_TIMESTAMP, 1, CURRENT_TIMESTAMP, 1)
""")

cursor.execute("""
INSERT INTO Log (EmployeeID, Action, Timestamp)
VALUES
(4, 'Logged into the portal', CURRENT_TIMESTAMP),
(4, 'Submitted Special Access', CURRENT_TIMESTAMP),
(2, 'Logged into the portal', CURRENT_TIMESTAMP),
(2, 'Granted Special Access', CURRENT_TIMESTAMP)
""")

# Step 6: Commit the changes to the database
conn.commit()

# Step 7: Perform a query to verify the data inserted
cursor.execute("SELECT * FROM Role")
roles = cursor.fetchall()
print("Roles:")
for role in roles:
    print(role)

cursor.execute("SELECT * FROM Employee")
employees = cursor.fetchall()
print("\nEmployees:")
for employee in employees:
    print(employee)

# Step 8: Close the connection to the database
conn.close()
