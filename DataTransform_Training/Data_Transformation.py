from os import listdir
import pandas as pd
from application_logging.logger import AppLogger


class DataTransform:
    """
    This class is used for converting the training data such that it can be entered into the database without any errors.
    """
    def __init__(self):
        self.good_data_path = "Training_Raw_files_validated/Good_Raw"

    def replace_null_with_NULL(self):
        logger = AppLogger("Training_Logs/data_transform_logs.txt")
        try:
            files = [f for f in listdir(self.good_data_path)]
            for file in files:
                df = pd.read_csv(self.good_data_path + "/" + file)
                if df.isna().sum().sum() > 0:
                    df.fillna('NULL', inplace=True)
                    df.to_csv(self.good_data_path + "/" + file, index=None, header=True)
                    logger.log(f"All the null values are replaced with 'NULL' in the file: {file}")
                else:
                    logger.log(f"No null values are present in the file: {file}")
        except Exception as e:
            logger.log(f"Null values replacement has been failed due to: {e}")
