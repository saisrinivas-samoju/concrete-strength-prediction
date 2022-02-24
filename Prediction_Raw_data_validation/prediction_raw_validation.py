from datetime import datetime
from os import listdir
import os
import json
import shutil
import pandas as pd
from application_logging.logger import AppLogger


class PredictionRawDataValidation:
    """
    This class is used for validating the all the prediction batch files.
    """

    def __init__(self, path):
        self.batch_directory = path
        self.schema_path = 'schema_prediction.json'

    def schema_validation(self):

        logger = AppLogger("Prediction_Logs/schema_validation_logs.txt")

        try:
            with open(self.schema_path, 'r') as f:
                dic = json.load(f)
                f.close()
            pattern = dic['SampleFileName']
            len_date_stamp = dic['LengthOfDateStampInFile']
            len_time_stamp = dic['LengthOfTimeStampInFile']
            column_names = dic['ColName']
            no_of_columns = dic['NumberofColumns']
            message = f"LengthOfDateStampInFile::{len_date_stamp}\tLengthOfTimeStampInFile::{len_time_stamp}\tNumberofColumns::{no_of_columns}\n"
            logger.log(message)

        except ValueError:
            logger.log("ValueError:Value not found inside schema_prediction.json")
            raise ValueError

        except KeyError:
            logger.log("KeyError:Key value error incorrect key passed")
            raise KeyError
            
        except Exception as e:
            logger.log(str(e))
            raise e

        return len_date_stamp, len_time_stamp, column_names, no_of_columns

    def create_dir_for_good_bad_data(self):

        logger = AppLogger("Prediction_Logs/general_logs.txt")

        try:
            path = os.path.join('Prediction_Raw_files_validated/', "Good_Raw/")

            if not os.path.isdir(path):
                os.makedirs(path)
                logger.log("Created Good Raw Directory!")
            #             else:
            #                 logger.log("Good Raw Directory is already present!")

            path = os.path.join('Prediction_Raw_files_validated/', "Bad_Raw/")
            if not os.path.isdir(path):
                os.makedirs(path)
                logger.log("Created Bad Raw Directory!")
        #             else:
        #                 logger.log("Bad Raw Directory is already present!")

        except OSError as e:
            logger.log(f"Error while creating Directory: {e}")
            raise OSError
        except Exception as e:
            logger.log(str(e))
            raise e

    def del_existing_good_data_prediction_folder(self):

        path = 'Prediction_Raw_files_validated/'
        logger = AppLogger("Prediction_Logs/general_logs.txt")

        try:
            if os.path.isdir(path + 'Good_Raw/'):
                shutil.rmtree(path + 'Good_Raw/')
                logger.log("Good Raw directory has been deleted successfully!")

        except OSError as e:
            logger.log(f"Error while Deleting Good Raw directory: {e}")
            raise OSError

        except Exception as e:
            logger.log(str(e))
            raise e

    def del_existing_bad_data_prediction_folder(self):

        path = 'Prediction_Raw_files_validated/'
        logger = AppLogger("Prediction_Logs/general_logs.txt")

        try:
            if os.path.isdir(path + 'Bad_Raw/'):
                shutil.rmtree(path + 'Bad_Raw/')
                logger.log("Bad Raw directory has been deleted successfully!")
        except OSError as e:
            logger.log(f"Error while Deleting Bad Raw directory: {e}")
            raise OSError

        except Exception as e:
            logger.log(str(e))
            raise e

    def move_bad_files_to_archive(self):

        now = datetime.now()
        date = now.date()
        time = now.strftime("%H%M%S")
        source = 'Prediction_Raw_files_validated/Bad_Raw/'
        logger = AppLogger("Prediction_Logs/general_logs.txt")

        try:
            if os.path.isdir(source):
                path = "PredictionArchiveBadData"
                if not os.path.isdir(path):
                    os.makedirs(path)
                dest = 'PredictionArchiveBadData/BadData_' + str(date) + "_" + str(time)
                if not os.path.isdir(dest):
                    os.makedirs(dest)
                files = os.listdir(source)
                for f in files:
                    if f not in os.listdir(dest):
                        shutil.move(source + f, dest)
                logger.log("Bad data files moved to archive")
                path = 'Prediction_Raw_files_validated/'
                if os.path.isdir(path + 'Bad_Raw/'):
                    shutil.rmtree(path + 'Bad_Raw/')
                logger.log("Bad Raw Data Folder Deleted successfully!")

        except Exception as e:
            logger.log(f"Error while moving bad files to archive: {e}")
            raise e

    def validate_filename(self, len_date_stamp, len_time_stamp):

        self.del_existing_bad_data_prediction_folder()
        self.del_existing_good_data_prediction_folder()

        files = [f for f in listdir(self.batch_directory)]

        logger = AppLogger("Prediction_Logs/filename_validation_logs.txt")

        try:
            self.create_dir_for_good_bad_data()
            for filename in files:
                text = filename
                if "concrete_strength_" in text:
                    text = text.replace("concrete_strength_", '')
                    if '.csv' in text:
                        text = text.replace(".csv", '')
                        if '_' in text:
                            text = text.split('_')
                            if text[0].isdigit() and text[0].isdigit():
                                if len(text[0]) == len_date_stamp and len(
                                        text[1]) == len_time_stamp:  # len_date_stamp and len_time_stamp
                                    shutil.copy("Prediction_Batch_Files/" + filename,
                                                "Prediction_Raw_files_validated/Good_Raw")
                                    logger.log(f"Valid File name! File moved to GoodRaw Folder : {filename}")
                                else:
                                    shutil.copy("Prediction_Batch_Files/" + filename,
                                                "Prediction_Raw_files_validated/Bad_Raw")
                                    logger.log(f"Invalid File Name!! File moved to Bad Raw Folder : {filename}")
                            else:
                                shutil.copy("Prediction_Batch_Files/" + filename,
                                            "Prediction_Raw_files_validated/Bad_Raw")
                                logger.log(f"Invalid File Name!! File moved to Bad Raw Folder : {filename}")
                        else:
                            shutil.copy("Prediction_Batch_Files/" + filename, "Prediction_Raw_files_validated/Bad_Raw")
                            logger.log(f"Invalid File Name!! File moved to Bad Raw Folder : {filename}")
                    else:
                        shutil.copy("Prediction_Batch_Files/" + filename, "Prediction_Raw_files_validated/Bad_Raw")
                        logger.log(f"Invalid File Name!! File moved to Bad Raw Folder : {filename}")

        except Exception as e:
            logger.log(f"Error occured while validating Filename {e}")
            raise e

    def validate_col_len(self, no_of_columns):

        logger = AppLogger("Prediction_Logs/column_validation_logs.txt")

        try:
            for file in listdir('Prediction_Raw_files_validated/Good_Raw/'):
                df = pd.read_csv("Prediction_Raw_files_validated/Good_Raw/" + file)
                if df.shape[1] != no_of_columns:
                    shutil.move(f"Prediction_Raw_files_validated/Good_Raw/{file}",
                                "Prediction_Raw_files_validated/Bad_Raw")
                    logger.log(f"Invalid Column Length for the file! File moved to Bad Raw Folder : {file}")
            logger.log("Column Length Validation Completed!")

        except OSError:
            logger.log(f"Error Occured while moving the file : {OSError}")
            raise OSError

        except Exception as e:
            logger.log(f"Error Occured: {e}")
            raise e

    def validate_null_columns(self):

        logger = AppLogger("Prediction_Logs/null_columns.txt")

        try:
            for file in listdir('Prediction_Raw_files_validated/Good_Raw/'):
                df = pd.read_csv(f"Prediction_Raw_files_validated/Good_Raw/{file}")
                count = 0
                for columns in df:
                    if df[columns].count() == 0:
                        count += 1
                        shutil.move("Prediction_Raw_files_validated/Good_Raw/" + file,
                                    "Prediction_Raw_files_validated/Bad_Raw")
                        logger.log(f"Invalid Column Length for the file!! File moved to Bad Raw Folder : {file}")
                        break

        except OSError:
            logger.log(f"Error Occured while moving the file : {OSError}")
            raise OSError

        except Exception as e:
            logger.log(f"Error Occured:: {e}")
            raise e
