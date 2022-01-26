from joblib import dump, load
import os
import shutil
from application_logging.logger import AppLogger


class FileOperation:
    """
    This class is used to save a model, load a model, and find the correct model to load.
    """

    def __init__(self):
        self.model_directory = "Models/"

    def save_model(self, model, filename):
        logger = AppLogger("Training_Logs/Model_Training_Logs.txt")
        logger.log("Entered the save_model method of FileOperation class")
        try:
            path = os.path.join(self.model_directory, filename)
            if os.path.isdir(path):
                logger.log(f"Directory exists for {filename} model already")
                # If there is an existing model in the same location, delete it.
                shutil.rmtree(path)
                logger.log(f"Deleted the existing directory for {filename} model.")
                # And create a new folder for the model
                os.makedirs(path)
                logger.log(f"Created a new directory for {filename} model.")
            else:
                os.makedirs(path)

            # Creating a the model in a folder same as the filename
            logger.log(f"Saving the {filename} model at {path} directory as {filename}.joblib")
            dump(value=model, filename=path + '/' + filename + '.joblib')
            logger.log(f"Successfully saving the {filename} model in the {path} directory.")
            logger.log("Exited the save_model method of FileOperation class")

        except Exception as e:
            logger.log(f"Error occurred while saving the {model} model as {filename}")
            logger.log("Exited the save_model method of FileOperation class")
            raise e

    def load_model(self, filename):
        logger = AppLogger("Prediction_Logs/Model_Prediction_Logs.txt")
        logger.log("Entered the load_model method of FileOperation class")
        try:
            path = os.path.join(self.model_directory, filename)
            logger.log(f"Loading the {filename}.joblib from {path}")
            model = load(filename=path+'/'+filename+'.joblib')
            logger.log("Successfully loaded the {filename}.joblib")
            logger.log("Exiting the load_model method of FileOperation class")
            return model
        except Exception as e:
            logger.log(f"Error occurred while loading the {filename} model")
            logger.log("Exited the load_model method of FileOperation class")
            raise e

    def find_correct_model_file(self, cluster_number):
        logger = AppLogger("Prediction_Logs/Model_Prediction_Logs.txt")
        logger.log('Entered the find_correct_model_file method of the FileOperation class')
        try:
            logger.log(f"Started finding the correct model file for the cluster number: {cluster_number}")
            folders = os.listdir(self.model_directory)
            for folder in folders:
                if str(folder[-1]) == str(cluster_number):
                    correct_folder = folder
            # Since our folder name and file name are same
            correct_model = correct_folder
            logger.log(f"Found the correct model for the cluster number: {cluster_number}")
            return correct_model

        except Exception as e:
            logger.log(f"Error occurred while finding the correct_model for the cluster number: {cluster_number}")
            logger.log("Exited the find_correct_model_file method of FileOperation class")
            raise e
