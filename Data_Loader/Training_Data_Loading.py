import pandas as pd
from application_logging.logger import AppLogger


def data_loader_training():
    """
    This function is used load the validated training data.
    """
    file_location = 'Training_FileFromDB/InputFile.csv'
    logger = AppLogger("Training_Logs/Training_Main_Log.txt")

    try:
        df = pd.read_csv(file_location)
        logger.log("Data Loaded Successfully!")
        df = df.drop_duplicates(keep='first')
        logger.log("Dropped duplicate values from the dataframe!")
        df.to_csv(file_location, index = False)
        return df
    except Exception as e:
        logger.log(f"Error occurred while loading the data from InputFile.csv: {str(e)}")
        logger.log("Data loading unsuccessful!")
