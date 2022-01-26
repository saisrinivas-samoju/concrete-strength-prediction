import pandas as pd
from Data_Preprocessing.prediction_preprocessing import PredictionPreprocessor
from application_logging.logger import AppLogger
from File_Operations.file_methods import FileOperation
from Data_Loader.Prediction_Data_Loading import data_loader_prediction
from Prediction_Raw_data_validation.prediction_raw_validation import PredictionRawDataValidation


class PredictResults:
    """
    This class is used for predicting the results of the final input file generated after all the validation steps are done.
    """

    def __init__(self, path):
        self.path = path
        self.logger = AppLogger("Prediction_Logs/Model_Prediction_Logs.txt")

    def predict_many(self):

        try:
            self.logger.log("Predicting the output of the given batch files has started!")

            # Load the validated data into a dataframe df
            df = data_loader_prediction()

            self.logger.log("Data loaded successfully for prediction")

            # Check if there are any null values and impute them if they exist

            preprocessor = PredictionPreprocessor()

            if preprocessor.is_null_present(df):
                self.logger.log("Null values present in the prediction data")

                # Imputing the null values

                df = preprocessor.impute_missing_values(df)

                self.logger.log("Null values imputed successfully.")

            # Check if there is/are any column(s) removed from the training data and remove them in the prediction data as well

            df = preprocessor.match_columns(df)

            self.logger.log("Columns matched in prediction data with the training data")

            # Cluster the dataframe

            file_operation = FileOperation()

            kmeans = file_operation.load_model("KMeans")

            # kmeans._n_threads = 1

            self.logger.log("Clustering model loaded successfully")

            # Creating a dataframe for combine all the data

            full_df = pd.DataFrame(columns=df.columns)

            df['clusters'] = kmeans.predict(df)

            # Create for loop for the each cluster find the best model and predict the results

            full_df['Predictions'] = []

            for i in df['clusters'].unique():
                cluster_df = df[df['clusters'] == i]
                cluster_df = cluster_df.drop(columns="clusters")
                filename = file_operation.find_correct_model_file(i)
                model = file_operation.load_model(filename)
                cluster_df['Predictions'] = model.predict(cluster_df.values)

                # Combine all the clusters

                full_df = pd.concat([full_df, cluster_df])

            # sort the data with predictions based on the index values

            full_df = full_df.sort_index()

            self.logger.log("Dataframe with the predictions has been created successfully.")

            # Save the dataframe with results and input data, except cluster data

            full_df.to_csv("Prediction_Results/Predictions.csv", index=False, header=True)

            self.logger.log("Dataframe with Predictions has been saved at: 'Prediction_Results/Predictions.csv'")

            self.logger.log("Exited predict_many method in PredictResults Class")

            return full_df

        except Exception as e:
            self.logger.log("Predicting results failed")
            self.logger.log("Error occurred while predicting the results from the given batch files")
            self.logger.log("Exited predict_many method in PredictResults Class")
            raise e

    def predict_one(self, lst):

        try:
            self.logger.log("Predicting the output of the given input has started!")

            # Get the input as list (Assuming no values in the list are Null or empty)

            validation_data = PredictionRawDataValidation(self.path)

            cols = validation_data.schema_validation()[2].keys()

            df = pd.DataFrame({list(cols)[i]: [lst[i]] for i in range(len(lst))})

            # Check if the no. of columns are matching or not

            preprocessor = PredictionPreprocessor()

            df = preprocessor.match_columns(df)

            # If matching, find the cluster no. for the lst

            file_operation = FileOperation()

            kmeans = file_operation.load_model("KMeans")

            # kmeans._n_threads = 1

            cluster = kmeans.predict(df)

            # Find the model based on the cluster no.

            filename = file_operation.find_correct_model_file(cluster[0])

            model = file_operation.load_model(filename)

            # predict the output and return it.

            result = model.predict(df.values)

            self.logger.log(f"Result predicted successfully: result = {result}")
            self.logger.log("Exited predict_one method in PredictResults Class")

            print(result[0])
            return result[0]

        except Exception as e:
            self.logger.log("Result prediction failed")
            self.logger.log("Error occurred while predicting the result of the given input")
            self.logger.log("Exited predict_one method in PredictResults Class")
            raise e
