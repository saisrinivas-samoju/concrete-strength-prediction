# Concrete Compressive Strength prediction

---

## Link

<a href="https://concrete-strength--prediction.herokuapp.com/">Heroku App Link</a>

#### Problem Statement:

  The goal is to build a programme to predict the compressive strength of concrete mixture without having to wait for it to set and test, with the information previously gathered by using regression methods in Machine Learning.

#### Architecture

<a href="https://ibb.co/d57fbC3"><img src="https://i.ibb.co/W2sHD8d/Flow-Chart.png" alt="Flow-Chart" border="0"></a>

#### Data Description

  * As per the Data Sharing agreement, we will receive data files in a shared location by the client, in the pre-decided formats. The format of files agreed is comma-separated values(.csv) files, with 9 columns representing the components of concrete mixer, it’s age, and the compressive strength of concrete as the label.
  * As per the data sharing agreement, we will also get two schema files from the client, which contains all the relevant information about the training and prediction datafiles.

<a href="https://ibb.co/bWK8Z75"><img src="https://i.ibb.co/QbK1RXv/Concrete-Data-Description.png" alt="Concrete-Data-Description" border="0"></a>


#### Data Validation and Transformation

  Once we gather all the data from the client. We will start the data validation process as the data sharing agreement and the requirements of machine learning process as a part of our training process.
  1. Filename validation: First we will start with the file name validation, as per the schema file given for the training datasets. We will manually enter the name tag present in the files name from the schema file, and validate it. After validating the pattern in the name, we will check for the length of date and time in the file name. If all the values are as per the schema file, we will move such files to Good_Data_Folder. Else, we will move such files to Bad_Data_Folder.
  2. No. of Columns: We will validate the no. of columns present in each file in the Good_Data_Folder, if the no. of columns present in a file matches the no. of columns present in the schema file for training, that file will be retained in the same folder. Else, that file will be moved to Bad_Data_Folder.
  3. Name of Columns: The names of the columns present in each file in the Good_Data_Folder is validated and should be as per the schema file. Else, those files will be moved to the Bad_Data_Folder.
  4. Datatype of Columns: The datatypes of the columns present in each file in the Good_Data_Folder is validated and should be as per the schema file. Else, those files will be moved to the Bad_Data_Folder.
  5. Null values in columns: If any of the columns in a file have all the values as Null or missing, we discard such a file and move it to Bad_Data_Folder. And, we will replace the other null values with a string code “Null”.

#### Data Insertion into Database

  * Database Creation: Create a SQLite database, if it is not already present in the given directory. If it is present, open the database by connecting to that database.
  * Table Creation in the Database: Create a table in the database with name “Good_Data” for inserting the files in the Good_Data_Folder based on given column names and datatypes in the schema file, if it is not already present in the database. If that table is already present in the database, no need to create a new table.
  * Insertion of files in the table: All the files in the Good_Data_Folder are inserted in this table. If any files are raising errors while inserting the data to the table due to the invalid datatypes, those files will be moved to the Bad_Data_Folder.

#### Export the data to a csv file

  * The data from the database will be exported to the csv file, and is used for model training in the later stages.
  * All the files in the Bad_Data_Folder will be moved to Archives, as we want to show the rejected files to the client.
  * All the files in the Good_Data_Folder will be deleted as we have already captured this data in our database.

#### Data Pre-processing

  We then read the exported csv file, and impute all the values with Null String code using KNN Imputer. We will also perform necessary feature engineering techniques as part of our pre-processing step, like dropping all the columns with zero standard deviation etc.

#### Data Clustering

  We are using an semi-supervised machine learning process. So, once our data is clean, we cluster the data into different clusters (using KMeans Clustering Algorithm) which we later use for training different models on each cluster, this will increase the overall accuracy of the project. So, first we divide the data based on implicit patterns in the data. Then, we give a number to each cluster, and add new column which consists of cluster name.

#### Model Training

  By using six machine learning algorithms, “Linear Regression”, “Elastic Net”, “Support-Vector Regressor”, “Decision-Tree Regressor”, “Random-Forest Regressor”, and “XGBoost Regressor”, we will train each cluster by Grid Searching few hyperparameters that are already defined using Cross-validation. We decide the best model for each cluster based on their R2 square score. Once we find the best models for each cluster, we will save them in the models folder with their clusters numbers in their names and folder names.

#### Deployment

  * After training the model in the local system, and testing it. We will create a CICD pipeline using circleci and dockerhub for our model deployment.
  * We will deploy trained model in Heroku platform.
  * This model can be used for training and prediction after deployment directly in the webpage.

#### Prediction

  * There are two types of predictions can be done in the project:
    * Predicting a single sample result
    * Prediction of Batch files
  * Using the Predict Batch Files page, you can predict compressive strength for all the samples in all the validate csv files provided. This is can be helpful, if you want to check the compressive strength of multiple samples at a time for evaluating later.
  * Using Predict page, you can quickly predict the compressive strength of concrete just by entering input values. This can handy during the concrete mixing period.
  Prediction

#### Predicting a single sample result

  * Calculating the compressive strength of concrete mixing before even mixing it, will save a lot of time. So, before  mixing the concrete, by entering the densities of the mixer and after how many no. of days we want to measure the strength of concrete, we can directly find the compressive strength. Using this insight, further actions can be done in the project planning process.
  * For predicting the concrete compressive strength, inputs for all the 8 features is required. If a particular feature is not present in a particular mixer, you can give value 0 for it.
  * Once, you enter all the data and click predict, this data will get a cluster number by the already trained Kmeans clustering model.
  * Based on this cluster number, the best machine learning model will be assigned for prediction, and the output is generated by this machine learning taking all the using input values, if they are valid.

#### Prediction of Batch Files

  * If the compressive strength is not as per the requirements, multiple combination of mixers can be given as csv files to Predict Batch Files page for checking the combination i.e. best suited for that particular construction project.
  * Before predicting the output of the data present in the data files, we have to perform some similar actions we did in the training process. These steps are required to insert our data  for prediction. We will also have a schema file for prediction, with a little difference when compared to the schema file for training i.e. no output column present in the prediction schema file and in the batch files given for the prediction. We will perform the following steps:
    * File name validation
    * File type validation
    * No. of columns validation
    * Name of columns validation
    * Datatypes of the columns validation
    * Null values validation and transformation
  * The validated data will inserted into a database, and after completing the insertion process for all the files. The files present in the  Good_Data_Folder will be deleted and Bad_Data_Folder will be moved to archive.
  * The data from the database will be exported into a csv file and similar pre-processing steps will be performed on the data loaded from this csv file.
  * After the pre-processing steps, the data will be divided into the clusters by using the already trained Kmeans clustering model.
  * And, the best model created for each cluster will be used for prediction and all the data will be compiled together as per their original index order and the filename order.
  * Finally, the prediction results will be exported as “Predictions.csv” file in “Prediction Results” folder.

### Screenshots

#### Homepage

<a href="https://ibb.co/Jd8cFXY"><img src="https://i.ibb.co/26RFYXz/Homepage.png" alt="Homepage" border="0"></a>

#### Train page

<a href="https://ibb.co/t8rHvsC"><img src="https://i.ibb.co/yWjNZys/Train-01.png" alt="Train-01" border="0"></a>

#### Training Successful

<a href="https://ibb.co/MccGHsT"><img src="https://i.ibb.co/bss2VPh/Train-02.png" alt="Train-02" border="0"></a>

#### Predict page

<a href="https://ibb.co/mDk0N4T"><img src="https://i.ibb.co/YRmX0hQ/Predict-01.png" alt="Predict-01" border="0"></a>

#### Prediction Successful

<a href="https://ibb.co/X4dNVRp"><img src="https://i.ibb.co/Jdb0CJ2/Predict-02.png" alt="Predict-02" border="0"></a>

#### Predict Batch Files page

<a href="https://ibb.co/M8zpcrJ"><img src="https://i.ibb.co/TKQR46N/Predict-Batch-Files-01.png" alt="Predict-Batch-Files-01" border="0"></a>

#### Batch Files Prediction Successful

<a href="https://ibb.co/k9XFTZY"><img src="https://i.ibb.co/KLWHgnC/Predict-Batch-Files-02.png" alt="Predict-Batch-Files-02" border="0"></a>

----

## Create a file "Dockerfile" with below content

```
FROM python:3.7
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
ENTRYPOINT [ "python" ]
CMD [ "app.py" ]
```

## Create a "Procfile" with following content
```
web: gunicorn app:app
```

## create a file ".circleci\config.yml" with following content
```
version: 2.1
orbs:
  heroku: circleci/heroku@1.0.1
jobs:
  build-and-test:
    executor: heroku/default
    docker:
      - image: circleci/python:3.6.2-stretch-browsers
        auth:
          username: mydockerhub-user
          password: $DOCKERHUB_PASSWORD  # context / project UI env-var reference
    steps:
      - checkout
      - restore_cache:
          key: deps1-{{ .Branch }}-{{ checksum "requirements.txt" }}
      - run:
          name: Install Python deps in a venv
          command: |
            echo 'export TAG=0.1.${CIRCLE_BUILD_NUM}' >> $BASH_ENV
            echo 'export IMAGE_NAME=python-circleci-docker' >> $BASH_ENV
            python3 -m venv venv
            . venv/bin/activate
            pip install --upgrade pip
            pip install -r requirements.txt
      - save_cache:
          key: deps1-{{ .Branch }}-{{ checksum "requirements.txt" }}
          paths:
            - "venv"
      - run:
          command: |
            . venv/bin/activate
            python -m pytest -v tests/test_script.py
      - store_artifacts:
          path: test-reports/
          destination: tr1
      - store_test_results:
          path: test-reports/
      - setup_remote_docker:
          version: 19.03.13
      - run:
          name: Build and push Docker image
          command: |
            docker build -t $DOCKERHUB_USER/$IMAGE_NAME:$TAG .
            docker login -u $DOCKERHUB_USER -p $DOCKER_HUB_PASSWORD_USER docker.io
            docker push $DOCKERHUB_USER/$IMAGE_NAME:$TAG
  deploy:
    executor: heroku/default
    steps:
      - checkout
      - run:
          name: Storing previous commit
          command: |
            git rev-parse HEAD > ./commit.txt
      - heroku/install
      - setup_remote_docker:
          version: 18.06.0-ce
      - run:
          name: Pushing to heroku registry
          command: |
            heroku container:login
            #heroku ps:scale web=1 -a $HEROKU_APP_NAME
            heroku container:push web -a $HEROKU_APP_NAME
            heroku container:release web -a $HEROKU_APP_NAME

workflows:
  build-test-deploy:
    jobs:
      - build-and-test
      - deploy:
          requires:
            - build-and-test
          filters:
            branches:
              only:
                - main
```
## to create requirements.txt

```buildoutcfg
pip freeze>requirements.txt
```

## initialize git repo

```
git init
git add README.md
git commit -m "first commit"
git branch -M main
git remote add origin
git push -u origin main
```

## create a account at circle ci

<a href="https://circleci.com/login/">Circle CI</a>

## setup your project

<a href="https://app.circleci.com/pipelines/github/saisrinivas-samoju/concrete-strength-prediction"> Setup project </a>

## Select project setting in CircleCI and below environment variable

>DOCKERHUB_USER
>DOCKER_HUB_PASSWORD_USER
>HEROKU_API_KEY
>HEROKU_APP_NAME
>HEROKU_EMAIL_ADDRESS

>DOCKER_IMAGE_NAME=<concretestrengthprediction>

## to update the modification

```
git add .
git commit -m "proper message"
git push
```


## #docker login -u $DOCKERHUB_USER -p $DOCKER_HUB_PASSWORD_USER docker.io
