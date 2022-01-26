import shutil
import sqlite3
from os import listdir
import os
import csv
from application_logging.logger import AppLogger

class DatabaseOperation:
    """
    This class is used for validating the datatypes of the columns in our training data files.
    """
    def __init__(self):
        self.path = 'Training_Database/'
        self.bad_data_path = "Training_Raw_files_validated/Bad_Raw"
        self.good_data_path = "Training_Raw_files_validated/Good_Raw"
        self.logger = AppLogger("Training_Logs/database_logs.txt")

    def database_connection(self, db_name):
        try:
            con = sqlite3.connect(self.path+db_name+'.db')
            self.logger.log(f"Opened {db_name} database successfully")
        except ConnectionError:
            self.logger.log(f"Error while connecting to {db_name} database")
            raise ConnectionError
        return con

    def create_table(self, db_name, column_names):
        try:
            conn = self.database_connection(db_name)
            cur = conn.cursor()
            cur.execute("SELECT count(name)  FROM sqlite_master WHERE type = 'table' AND name = 'Good_Raw_Data'")
            if cur.fetchone()[0] == 1:
                conn.close()
                self.logger.log("Table already exists!")
                self.logger.log(f"Closed {db_name} database successfully")
            else:
                for key in column_names.keys():
                    dtype = column_names[key]
                    try:
                        conn.execute(f'ALTER TABLE Good_Raw_Data ADD COLUMN "{key}" {dtype}')
                    except:
                        conn.execute(f'CREATE TABLE  Good_Raw_Data ({key} {dtype})')
                conn.close()
                self.logger.log("Tables Created successfully!")
                self.logger.log(f"Closed {db_name} database successfully")

        except Exception as e:
            self.logger.log(f"Error while creating table: {e}")
            conn.close()
            self.logger.log(f"Closed {db_name} database successfully")
            raise e

    def insert_data_into_db(self, db_name):

        conn = self.database_connection(db_name)

        good_data_path = self.good_data_path
        bad_data_path = self.bad_data_path

        files = [f for f in listdir(good_data_path)]

        for file in files:
            try:
                with open(good_data_path + '/' + file, "r") as f:
                    next(f)
                    reader = csv.reader(f, delimiter="\n")
                    for line in enumerate(reader):
                        for list_ in (line[1]):
                            try:
                                conn.execute('INSERT INTO Good_Raw_Data values ({values})'.format(values=(list_)))
                                self.logger.log(f"'{file}' file loaded successfully.")
                                conn.commit()
                            except Exception as e:
                                raise e

            except Exception as e:
                conn.rollback()
                self.logger.log(f"Error while creating table: {e}")
                shutil.move(good_data_path + '/' + file, bad_data_path)
                self.logger.log(f"'{file}' File Moved Successfully to Bad_Raw Folder.")
                conn.close()

        conn.close()

    def db_to_csv(self, db_name):

        dest = "Training_FileFromDB/"
        filename = 'InputFile.csv'

        try:
            if not os.path.isdir(dest):
                os.makedirs(dest)

            conn = self.database_connection(db_name)
            command = "SELECT *  FROM Good_Raw_Data"
            cur = conn.cursor()

            cur.execute(command)

            results = cur.fetchall()

            cols = [i[0] for i in cur.description]

            csv_file = csv.writer(open(dest + filename, 'w', newline=''), delimiter=',',
                                  lineterminator='\r\n', quoting=csv.QUOTE_ALL, escapechar='\\')

            csv_file.writerow(cols)
            csv_file.writerows(results)

            self.logger.log("File Exported Successfully!")

        except Exception as e:
            self.logger.log(f"Failed to Export the InputFile.csv due to {e}")
            raise e
