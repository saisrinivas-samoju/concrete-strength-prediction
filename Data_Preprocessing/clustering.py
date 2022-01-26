import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from kneed import KneeLocator
from File_Operations.file_methods import FileOperation
from application_logging.logger import AppLogger


def clustering(X):
    """
    Takes the feature set and returns the feature set with cluster column and saves the clustering model for further use
    """
    logger = AppLogger("Training_Logs/Model_Training_Logs.txt")
    logger.log("Entered clustering function")

    wcss = []
    try:
        for i in range(1, 11):
            kmeans = KMeans(n_clusters=i, init='k-means++')
            kmeans.fit(X)
            wcss.append(kmeans.inertia_)

        # Saving the elbow plot
        plt.plot(range(1, 11), wcss)
        plt.title('The Elbow Method')
        plt.xlabel('Number of clusters')
        plt.ylabel('WCSS')
        plt.savefig('Preprocessing_Data/K-Means_Elbow.PNG')

        # optimum k value
        k = KneeLocator(range(1, 11), wcss, curve='convex', direction='decreasing')

        logger.log(f"Found the optimum cluster value; k={k.knee}")

        # Creating clusters column

        kmeans = KMeans(n_clusters=k.knee, init='k-means++')

        logger.log("Adding 'clusters' column to the feature set")

        X["clusters"] = kmeans.fit_predict(X)

        logger.log("Successfully added 'clusters' column to the feature set")

        # Saving the clustering model

        logger.log("Saving the clustering model for future use")

        file_operation = FileOperation()
        file_operation.save_model(model=kmeans, filename="KMeans")

        return X

    except Exception as e:
        logger.log("Error in creating clusters")
        raise e
