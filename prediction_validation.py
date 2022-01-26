from Prediction_Raw_data_validation.prediction_raw_validation import PredictionRawDataValidation
from application_logging.logger import AppLogger
from Database_Operations.prediction_dtype_validation import PredictionDatabaseOperation
from DataTransform_Prediction.Prediction_Data_Transformation import PredictionDataTransform


class PredictionValidation:
    """
    This class is used for validating the all the batch files provided for prediction to generate a final input file for prediction.
    """
    def __init__(self, path):
        self.raw_data_validation = PredictionRawDataValidation(path)
        self.data_transform = PredictionDataTransform()
        self.db_operation = PredictionDatabaseOperation()

    def prediction_validation(self):
        logger = AppLogger("Prediction_Logs/Prediction_Main_Log.txt")
        try:
            ################### Starting Raw Data Validation ########################
            logger.log('Validation of prediction batch files has started!')

            # Extracting the values from the schema file for prediction
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

            logger.log("Creating database for prediction data on the basis of given schema")

            self.db_operation.create_table("Prediction", column_names)

            logger.log("Table Created Successfully!")

            logger.log("Data insertion in the database has started!")

            self.db_operation.insert_data_into_db("Prediction")

            logger.log("Data has been inserted into the database successfully!")

            logger.log("Creating a master csv file for prediction...")

            self.db_operation.db_to_csv("Prediction")

            logger.log("Created the csv file for prediction!")

            logger.log("Deleting the existing Good data folder...")

            self.raw_data_validation.del_existing_good_data_prediction_folder()

            logger.log("Deleted the existing Good Data Folder")

            logger.log("Moving the Bad Data Folder to Archive...")

            self.raw_data_validation.move_bad_files_to_archive()

            logger.log("Moved the existing Bad Data folder to Archive!")

            logger.log("Deleted the existing Prediction Database")

            #### Deleting the existing database for prediction ####
            self.db_operation.delete_existing_db("Prediction")

            logger.log("#### Validation for prediction files has been completed successfully! ####")

        except Exception as e:
            logger.log("Error Occurred during prediction validation process")
            logger.log("Exited prediction_validation method from PredictionValidation class")
            raise e
