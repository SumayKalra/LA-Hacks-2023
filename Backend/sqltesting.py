import pyodbc 

def read(conn):
    print("Read")
    cursor = conn.cursor()
    cursor.execute("select * from Departments")
    for row in cursor:
        print(f'row = {row}')
    print()

conn = pyodbc.connect(
"Driver=SQL SERVER NATIVE CLIENT 16.0};"
"Server=DESKTOP-2H3M36F;"
"Database=AllClasses;"
"Trusted_Connection=yes"
)

read(conn)
