import pandas as pd
from application_logging.logger import AppLogger


def data_loader_prediction():
    """
    This function is used to load the validated prediction data.
    """
    file_location = 'Prediction_FileFromDB/InputFile.csv'
    logger = AppLogger("Prediction_Logs/Prediction_Main_Log.txt")

    try:
        df = pd.read_csv(file_location)
        logger.log("Data Loaded Successfully!")
        return df
    except Exception as e:
        logger.log(f"Error occurred while loading the data from InputFile.csv: {str(e)}")
        logger.log("Data loading unsuccessful!")
