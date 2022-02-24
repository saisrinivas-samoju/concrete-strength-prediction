import numpy as np
import pandas as pd
from sklearn.impute import KNNImputer
from application_logging.logger import AppLogger


class Preprocessor:
    """
    This class is used for preprocessing the validated training data.
    """

    def __init__(self):
        self.logger = AppLogger("Training_Logs/Model_Training_Logs.txt")

    def remove_columns(self, df, columns):
        self.logger.log("Entered remove_columns method in Proprocessor Class")
        try:
            if columns is not None:
                df = df.drop(columns=columns)
                self.logger.log(f"Remove the column(s): {columns} successfully")
                return df
            else:
                self.logger.log("No columns to remove")
            self.logger.log("Exited the remove_columns method from Preprocessor class")
            
        except Exception as e:
            self.logger.log(f"Error occurred while removing {columns} column(s) from the dataset.")
            self.logger.log("Exited the remove_columns method from the Preprocessing class")
            raise e

    def separate_label_feature(self, df, label_column_name):
        self.logger.log("Entered separate_label_feature method in Preprocessor class")
        try:
            X = df.drop(columns=label_column_name)
            y = df[label_column_name]
            self.logger.log("Separated Features and label successfully.")
            self.logger.log("Exited the separate_label_feature method in Preprocessor class.")
            return X, y
        except Exception as e:
            self.logger.log(f"Error occurred while separating features and label in the dataset.")
            self.logger.log("Exited the separate_label_feature method from the Preprocessing class")
            raise e

    def is_null_present(self, df):
        self.logger.log("Entered is_null_present in Preprocessor Class")
        try:
            if df.isnull().sum().sum():
                self.logger.log("Null values present inside the InputFile.csv")
                self.logger.log("Creating a DataFrame containing all the missing values in the training data...")
                pd.DataFrame(df.isnull().sum()[df.isnull().sum() > 0], columns=['no. of missing values']).to_csv('Preprocessing_Data/null_columns.csv', index=False, header=True)
                self.logger.log("DataFrame has been created for all the missing values!")
            else:
                self.logger.log("No null values are present in the training dataset.")

            self.logger.log("Exited the is_null_present method from the Preprocessing class")
        except Exception as e:
            self.logger.log("Error occurred while checking the null values in the dataset.")
            self.logger.log("Exited the is_null_present method from the Preprocessing class")
            raise e
        return df.isnull().sum().sum() != 0

    def impute_missing_values(self, df):
        self.logger.log("Entered impute_missing_values in Preprocessor Class")
        try:
            imputer = KNNImputer(n_neighbors=5, weights='distance', missing_values=np.nan)
            full_data = imputer.fit_transform(df)
            full_df = pd.DataFrame(data=full_data, columns=df.columns)
            self.logger.log("Missing value imputation is successful!")
            return full_df
        except Exception as e:
            self.logger.log("Error occurred while imputing the null values in the dataset.")
            self.logger.log("Exited the impute_missing_values method from the Preprocessing class")
            raise e

    def get_columns_with_zero_std(self, df):
        self.logger.log("Entered get_columns_with_zero_std in Preprocessor Class")
        self.logger.log("Searching for all the columns with a zero standard deviation...")
        try:
            constant_columns = list(df.describe().transpose()['std'][df.describe().transpose()['std'] == 0].index)
            if len(constant_columns) > 0:
                self.logger.log("Found the columns with zero standard deviation")
            else:
                self.logger.log("No columns with zero standard deviation")
            self.logger.log("Exited the get_columns_with_zero_std method in the Preprocessing class")
            return constant_columns
        except Exception as e:
            self.logger.log("Error occurred while finding columns with zero std in the dataset.")
            self.logger.log("Exited the get_columns_with_zero_std method from the Preprocessing class")
            raise e
