import sqlite3

DB_PATH = 'customers.db'

conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

# Step 1: Rename old table
c.execute('ALTER TABLE customers RENAME TO customers_old')

# Step 2: Create new table with id
c.execute('''
    CREATE TABLE customers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        corporate_number TEXT UNIQUE,
        company_name TEXT NOT NULL,
        contact_person TEXT,
        email TEXT,
        phone TEXT,
        address TEXT,
        last_contact_date TEXT,
        notes TEXT
    )
''')

# Step 3: Copy data from old to new (id will be auto-generated)
c.execute('''
    INSERT INTO customers (corporate_number, company_name, contact_person, email, phone, address, last_contact_date, notes)
    SELECT corporate_number, company_name, contact_person, email, phone, address, last_contact_date, notes FROM customers_old
''')

# Step 4: Drop old table
c.execute('DROP TABLE customers_old')

conn.commit()
conn.close()

print('Migration complete! The customers table now has an auto-incrementing id.')
