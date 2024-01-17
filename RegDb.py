from RegDbEntry import RegDbEntry
import csv

class RegDb:
    " - simple database to store RegDbEntry objects "
        

    def __init__(self, init=False, dbName='RegDb.csv'):
        """
        - initialize database variables here
        - mandatory :
            - any type can be used to store database entries for RegDbEntry objects
            - e.g. list of class, list of dictionary, list of tuples, dictionary of tuples etc.
        """
               
        self.dbName = dbName
        self.entries = []  

        print('TODO: __init__')

    def fetch_candidates(self):
        """
        - returns a list of tuples containing Registration Form entry fields

        """

        print('TODO: fetch_candidates')

        tupleList = []
        tupleList += [(entry.idbarangay, entry.name, entry.barangay, entry.age, entry.gender) for entry in self.entries]

        return tupleList

    def insert_candidate(self, idbarangay, name, barangay, age, gender):
        """
        - inserts an entry in the database
        - no return value
        """

        newEntry = RegDbEntry(idbarangay=idbarangay, name=name, barangay=barangay, age=age, gender=gender)
        self.entries.append(newEntry)
        print('TODO: insert_candidate')

    def delete_candidate(self, idbarangay):
        """
        - deletes the corresponding entry in the database as specified by 'idbarangay'
        - no return value
        """

        for entry in self.entries:
            if entry.idbarangay == idbarangay:
                self.entries.remove(entry)
                break
        print('TODO: delete_candidate')

    def update_candidate(self, new_name, new_barangay, new_age, new_gender, idbarangay):
        """
        - updates the corresponding entry in the database as specified by 'id'
        - no return value
        """

        for entry in self.entries:
            if entry.idbarangay == idbarangay:
                entry.name = new_name
                entry.barangay = new_barangay
                entry.age = new_age
                entry.gender = new_gender
                break
        print('TODO: update_candidate')

    def export_csv(self):
        """
        - exports database entries as a CSV file
        - CSV : Comma Separated Values
        - no return value      
        """
        
        with open(self.dbName, 'w') as file:
            for entry in self.entries:
                file.write(f"{entry.idbarangay},{entry.name},{entry.barangay},{entry.age},{entry.gender}\n")
        print('TODO: export_csv')

    def import_csv(self, csv_filename):
        try:
            self.entries = []
            if not csv_filename.lower().endswith('.csv'):
                csv_filename += '.csv'

            with open(csv_filename, 'r') as csvFile:
                reader = csv.reader(csvFile)
                for row in reader:
                    idbarangay, name, barangay, age, gender = row
                    self.insert_candidate(idbarangay, name, barangay, age, gender)
            print('Data imported successfully')
            return True
        except FileNotFoundError:
            print(f'Error importing data: File not found - {csv_filename}')
            return False
        except Exception as e:
            print(f'Error importing data: {e}')
            return False


    def id_exists(self, idbarangay):
        """
        - returns True if an entry exists for the specified 'id'
        - else returns False
        """

        return any(entry.idbarangay == idbarangay for entry in self.entries)
