import sqlite3

# Connect to the database (creates a file-based database if it doesn't exist)
conn = sqlite3.connect("projects.db")
cursor = conn.cursor()

# Create the `projects` table with AUTOINCREMENT for the `id` column
cursor.execute("""
CREATE TABLE IF NOT EXISTS projects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    corporate_number TEXT,
    project_name TEXT NOT NULL,
    status TEXT,
    start_date TEXT,
    end_date TEXT,
    budget INTEGER,
    sales_person TEXT,
    description TEXT,
    management_url TEXT
)
""")

# Function to add a new project
def add_project(corporate_number, project_name, status, start_date, end_date, budget, sales_person, description, management_url):
    cursor.execute("""
    INSERT INTO projects (corporate_number, project_name, status, start_date, end_date, budget, sales_person, description, management_url)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (corporate_number, project_name, status, start_date, end_date, budget, sales_person, description, management_url))
    conn.commit()
    print("New project added.")

# Add sample data
add_project('12345678', 'Project A', 'In Progress', '2025-04-16', '2025-12-31', 100000, 'John Doe', 'Sample project description', 'http://example.com')

# Fetch all data to confirm ID assignment
cursor.execute("SELECT * FROM projects")
rows = cursor.fetchall()
for row in rows:
    print(row)

conn.close()
