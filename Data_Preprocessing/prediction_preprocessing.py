import numpy as np
import pandas as pd
from sklearn.impute import KNNImputer
from application_logging.logger import AppLogger
from Data_Preprocessing.preprocessing import Preprocessor
from Data_Loader.Training_Data_Loading import data_loader_training


class PredictionPreprocessor:
    """
    This class is used for preprocessing the validated prediction data.
    """

    def __init__(self):
        self.logger = AppLogger("Prediction_Logs/Model_Prediction_Logs.txt")

    def remove_columns(self, df, columns):
        self.logger.log("Entered remove_columns method in PredictionPreprocessor Class")
        try:
            if columns is not None:
                df = df.drop(columns=columns)
                self.logger.log(f"Remove the column(s): {columns} successfully")
                return df
            else:
                self.logger.log("No columns to remove")
            self.logger.log("Exited the remove_columns method from PredictionPreprocessor class")
        except Exception as e:
            self.logger.log(f"Error occurred while removing {columns} column(s) from the dataset.")
            self.logger.log("Exited the remove_columns method from the PredictionPreprocessor class")
            raise e

    def is_null_present(self, df):
        self.logger.log("Entered is_null_present in PredictionPreprocessor Class")
        try:
            if df.isnull().sum().sum():
                self.logger.log("Null values present inside the InputFile.csv")
                self.logger.log("Creating a DataFrame containing all the missing values in the prediction data...")
                pd.DataFrame(df.isnull().sum()[df.isnull().sum() > 0], columns=['no. of missing values']).to_csv(
                    'Preprocessing_Data/pred_null_columns.csv', index=False, header=True)
                self.logger.log("DataFrame has been created for all the missing values!")
            else:
                self.logger.log("No null values are present in the prediction dataset.")

            self.logger.log("Exited the is_null_present method from the PredictionPreprocessor class")
        except Exception as e:
            self.logger.log("Error occurred while checking the null values in the dataset.")
            self.logger.log("Exited the is_null_present method from the PredictionPreprocessor class")
            raise e
        return df.isnull().sum().sum() != 0

    def impute_missing_values(self, df):
        self.logger.log("Entered impute_missing_values in PredictionPreprocessor Class")
        try:
            imputer = KNNImputer(n_neighbors=5, weights='distance', missing_values=np.nan)
            full_data = imputer.fit_transform(df)
            full_df = pd.DataFrame(data=full_data, columns=df.columns)
            self.logger.log("Missing value imputation is successful!")
            return full_df
        except Exception as e:
            self.logger.log("Error occurred while imputing the null values in the dataset.")
            self.logger.log("Exited the impute_missing_values method from the PredictionPreprocessor class")
            raise e

    def match_columns(self, df):
        self.logger.log("Entered match_columns in PredictionProcessor Class")
        try:
            train_df = data_loader_training()
            train_preprocessor = Preprocessor()
            zero_std_cols = train_preprocessor.get_columns_with_zero_std(train_df)
            if zero_std_cols is not None:
                df = self.remove_columns(df, zero_std_cols)
                self.logger.log(
                    "Removed {zero_std_cols} successfully to match the features with the training features.")
            else:
                self.logger.log("No column to remove to match the column in training and prediction datasets.")
            self.logger.log("Exited the match_columns method from the PredictionPreprocessor class")
            return df
        except Exception as e:
            self.logger.log("Error occurred while matching the column with the columns used for training")
            self.logger.log("Exited the match_columns method from the PredictionPreprocessor class")
            raise e
