'''
This is the interface to an SQLite Database
'''

import sqlite3
import csv

class RegDbSqlite:
    def __init__(self, dbName='Candidates.db'):
        super().__init__()
        self.dbName = dbName
        self.csvFile = self.dbName.replace('.db', '.csv')
        self.conn = sqlite3.connect(self.dbName)
        self.cursor = self.conn.cursor()

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Candidates (
                idbarangay TEXT PRIMARY KEY,
                name TEXT,
                barangay TEXT,
                age TEXT,
                gender TEXT)''')
        self.conn.commit()
        self.conn.close()

    def connect_cursor(self):
        self.conn = sqlite3.connect(self.dbName)
        self.cursor = self.conn.cursor()        

    def commit_close(self):
        self.conn.commit()
        self.conn.close()        

    def create_table(self):
        self.connect_cursor()
        self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS Candidates (
                    idbarangay TEXT PRIMARY KEY,
                    name TEXT,
                    barangay TEXT,
                    age TEXT,
                    gender TEXT)''')
        self.commit_close()

    def fetch_candidates(self):
        self.connect_cursor()
        self.cursor.execute('SELECT * FROM Candidates')
        candidates = self.cursor.fetchall()
        self.conn.close()
        return candidates

    def insert_candidate(self, idbarangay, name, barangay, age, gender):
        self.connect_cursor()
        self.cursor.execute('INSERT INTO Candidates (idbarangay, name, barangay, age, gender) VALUES (?, ?, ?, ?, ?)',
                    (idbarangay, name, barangay, age, gender))
        self.commit_close()

    def delete_candidate(self, idbarangay):
        self.connect_cursor()
        self.cursor.execute('DELETE FROM Candidates WHERE id = ?', (idbarangay,))
        self.commit_close()

    def update_candidate(self, new_name, new_barangay, new_age, new_gender, idbarangay):
        self.connect_cursor()
        self.cursor.execute('UPDATE Candidates SET name = ?, barangay = ?, age = ?, gender = ? WHERE idbarangay = ?',
                    (new_name, new_barangay, new_age, new_gender, idbarangay))
        self.commit_close()

    def id_exists(self, idbarangay):
        self.connect_cursor()
        self.cursor.execute('SELECT COUNT(*) FROM Candidates WHERE idbarangay = ?', (idbarangay,))
        result =self.cursor.fetchone()
        self.conn.close()
        return result[0] > 0

    def export_csv(self):
        with open(self.csvFile, "w") as filehandle:
            dbEntries = self.fetch_candidates()
            for entry in dbEntries:
                print(entry)
                filehandle.write(f"{entry[0]},{entry[1]},{entry[2]},{entry[3]},{entry[4]}\n")

    def import_csv(self, csv_filename):
        try:
            if not csv_filename.lower().endswith('.csv'):
                csv_filename += '.csv'

            with open(csv_filename, 'r') as csvFile:
                reader = csv.reader(csvFile)
                next(reader)  # Skip header row
                for row in reader:
                    idbarangay, name, barangay, age, gender = row
                    # Add logic to handle the data, e.g., insert into your database
                    self.insert_candidate(idbarangay, name, barangay, age, gender)
            print('Data imported successfully')
            return True
        except FileNotFoundError:
            print(f'Error importing data: File not found - {csv_filename}')
            return False
        except Exception as e:
            print(f'Error importing data: {e}')
            return False

def test_RegDb():
    iRegDb = RegDbSqlite(dbName='RegDbSql.db')

    for entry in range(30):
        iRegDb.insert_candidate(entry, f'Name{entry} Surname{entry}', f'Barangay {entry}', '17', 'Male')
        assert iRegDb.id_exists(entry)

    all_entries = iRegDb.fetch_candidates()
    assert len(all_entries) == 30

    for entry in range(10, 20):
        iRegDb.update_candidate(f'Name{entry} Surname{entry}', f'Barangay {entry}', '18', 'Female', entry)
        assert iRegDb.id_exists(entry)

    all_entries = iRegDb.fetch_candidates()
    assert len(all_entries) == 30

    for entry in range(10):
        iRegDb.delete_candidate(entry)
        assert not iRegDb.id_exists(entry) 

    all_entries = iRegDb.fetch_candidates()
    assert len(all_entries) == 20