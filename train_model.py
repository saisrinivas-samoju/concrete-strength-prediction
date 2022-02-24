import pandas as pd
from sklearn.model_selection import train_test_split
from Data_Loader.Training_Data_Loading import data_loader_training
from Data_Preprocessing.preprocessing import Preprocessor
from File_Operations.file_methods import FileOperation
from Data_Preprocessing.clustering import clustering
from application_logging.logger import AppLogger
from Best_Model_Finder.Model_Finder import ModelFinder


class TrainModel:
    """
    This class is used for training different models based on the cluster numbers.
    """

    def __init__(self):
        self.logger = AppLogger("Training_Logs/Model_Training_Logs.txt")

    def model_training(self):
        self.logger.log("Training Started...")
        try:
            # Loading the data
            df = data_loader_training()

            # Data Preprocessing
            preprocessor = Preprocessor()

            # If there are any null values in the dataframe
            if preprocessor.is_null_present(df):
                # Imputing the null values
                df = preprocessor.impute_missing_values(df)

            # Separating feature set and label series
            X, y = preprocessor.separate_label_feature(df, 'Concrete_compressive_strength')

            # Removing if there are any columns with zero standard deviation
            zero_std_cols = preprocessor.get_columns_with_zero_std(X)

            X = preprocessor.remove_columns(X, zero_std_cols)

            # Clustering the feature data

            X = clustering(X)

            df = pd.concat([X, y], axis=1)

            list_of_clusters = X['clusters'].unique()

            for i in list_of_clusters:
                cluster_df = df[df['clusters'] == i]

                cluster_df = cluster_df.drop(columns="clusters")

                cluster_X, cluster_y = preprocessor.separate_label_feature(cluster_df, 'Concrete_compressive_strength')

                # As we apply cross validation using GridSearchCV, this test size will be a hold you test set.
                X_train, X_test, y_train, y_test = train_test_split(cluster_X, cluster_y, test_size=0.25, random_state=42)

                ##################### Best model finder class/function is left #####################

                model_finder = ModelFinder(X_train=X_train, y_train=y_train, X_test=X_test, y_test=y_test)

                model, filename = model_finder.get_best_model()

                # Saving the best model

                file_operation = FileOperation()
                file_operation.save_model(model, filename + str(i))

            self.logger.log("Successfully completed the model training")

        except Exception as e:
            self.logger.log("Model training Failed")
            self.logger.log("Error occurred while training the models")
            self.logger.log("Exited model_training method in TrainModel Class")
            raise e
