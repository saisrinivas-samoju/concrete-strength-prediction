from Training_Raw_data_validation.raw_validation import RawDataValidation
from application_logging.logger import AppLogger
from Database_Operations.dtype_validation import DatabaseOperation
from DataTransform_Training.Data_Transformation import DataTransform

class TrainValidation:
    """
    This class is used for validating all the training batch files for generating a final input file for training the models.
    """
    def __init__(self, path):
        self.raw_data_validation = RawDataValidation(path)
        self.data_transform = DataTransform()
        self.db_operation = DatabaseOperation()

    def train_validation(self):
        logger = AppLogger("Training_Logs/Training_Main_Log.txt")
        try:
            ################### Starting Raw Data Validation ########################
            logger.log('Validation of training batch files has started!')

            # Extracting the values from the schema file for training
            len_date_stamp, len_time_stamp, column_names, no_of_columns = self.raw_data_validation.schema_validation()

            # Validating the filename
            self.raw_data_validation.validate_filename(len_date_stamp, len_time_stamp)

            # Validating the no. of columns in each csv file
            self.raw_data_validation.validate_col_len(no_of_columns)

            # Validating if there are any columns with all null values
            self.raw_data_validation.validate_null_columns()

            logger.log("Raw Data Validation has been completed!")

            ################# Inserting the qualified files in a database #################

            logger.log("Data Transformation has started")

            self.data_transform.replace_null_with_NULL()

            logger.log("Data Transformation is completed! File(s) are ready to be inserted in the database")

            logger.log("Creating database for training data on the basis of given schema")

            self.db_operation.create_table("Training", column_names)

            logger.log("Table Created Successfully!")

            logger.log("Data insertion in the database has started!")

            self.db_operation.insert_data_into_db("Training")

            logger.log("Data has been inserted into the database successfully!")

            logger.log("Creating a master csv file for training...")

            self.db_operation.db_to_csv("Training")

            logger.log("Created the csv file for training!")

            logger.log("Deleting the existing Good data folder...")

            self.raw_data_validation.del_existing_good_data_training_folder()

            logger.log("Deleted the existing Good Data Folder")

            logger.log("Moving the Bad Data Folder to Archive...")

            self.raw_data_validation.move_bad_files_to_archive()

            logger.log("Moved the existing Bad Data folder to Archive!")

            logger.log("#### Validation for training files has been completed successfully! ####")

        except Exception as e:
            logger.log("Error Occurred during training validation process")
            logger.log("Exited train_validation method from TrainValidation class")
            raise e
