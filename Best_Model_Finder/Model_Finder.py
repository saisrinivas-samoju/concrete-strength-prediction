from sklearn.model_selection import GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression, ElasticNet, ElasticNetCV
from sklearn.svm import SVR
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
from sklearn.metrics import r2_score
from application_logging.logger import AppLogger

class ModelFinder:
    """
    This class is used to find the best performing model for each cluster of the training data.
    """

    def __init__(self, X_train, y_train, X_test, y_test):
        self.logger = AppLogger("Training_Logs/Model_Training_Logs.txt")
        self.X_train = X_train
        self.y_train = y_train
        self.X_test = X_test
        self.y_test = y_test

    def lr_model(self):

        logger = self.logger
        X_train = self.X_train
        y_train = self.y_train
        logger.log("Entered lr_model method in ModelFinder class")
        try:
            # Scaling the data

            scaler = StandardScaler()
            scaled_X_train = scaler.fit_transform(X_train)

            # Creating the base model

            base_lr = LinearRegression()

            # Creating the parameters grid

            param_grid = {'fit_intercept': [True, False], 'normalize': [True, False], 'copy_X': [True, False]}

            # Grid Model Creation

            grid = GridSearchCV(estimator=base_lr, param_grid=param_grid, verbose=3, cv=5)

            # Training the grid model with the scaled data

            grid.fit(scaled_X_train, y_train)

            # Capturing the best parameters

            fit_intercept = grid.best_params_['fit_intercept']

            normalize = grid.best_params_['normalize']

            copy_X = grid.best_params_['copy_X']

            # Logging the best parameters found

            logger.log(
                f"Best parameters for Linear Regression model: fit_intercept={fit_intercept}; normalize={normalize}; copy_X={copy_X}")

            # Creating a scaler object for the pipeline creation

            scaler = StandardScaler()

            # Creating a linear regression model with the best parameters

            lr = LinearRegression(fit_intercept=fit_intercept, normalize=normalize, copy_X=copy_X)

            # Pipe line Creation

            operations = [('scaler', scaler), ('lr', lr)]
            pipe_lr = Pipeline(steps=operations)

            # Training the pipeline with the unscaled data

            pipe_lr.fit(X_train, y_train)

            # Logging the completion of the process

            logger.log("Exited lr_model method in ModelFinder class")

            # Returning the best linear regression model

            return pipe_lr

        except Exception as e:
            logger.log("Error occurred while creating Linear Regression Model")
            logger.log("Exited lr_model method in ModelFinder class")
            raise e

    def elastic_net_model(self):

        logger = self.logger
        X_train = self.X_train
        y_train = self.y_train
        logger.log("Entered elastic_net_model method in ModelFinder class")

        try:
            # Scaling the data

            scaler = StandardScaler()
            scaled_X_train = scaler.fit_transform(X_train)

            # ElasticNetCV Model creation for finding the best parameters

            elastic_cv_model = ElasticNetCV(l1_ratio=[.1, .5, .7, .9, .95, .99, 1],
                                            eps=0.001,
                                            n_alphas=100,
                                            max_iter=1000000,
                                            tol=0.0001,
                                            cv=5,
                                            n_jobs=-1, verbose=3)

            # Training the CV model with the scaled training data

            elastic_cv_model.fit(scaled_X_train, y_train)

            # Logging the best parameters found

            logger.log(
                f"Best parameters for elastic net model: l1_ratio={elastic_cv_model.l1_ratio_}; alpha={elastic_cv_model.alpha_}")

            # Creating a scaler object for the pipeline creation

            scaler = StandardScaler()

            # Creating the an elasticNet model with the best parameters

            elastic_model = ElasticNet(alpha=elastic_cv_model.alpha_, l1_ratio=elastic_cv_model.l1_ratio_,
                                       max_iter=1000000, tol=0.0001)

            # Creating a pipeline for returning the best model of elasticnet

            pipe_en = Pipeline(steps=[('scaler', scaler), ('elastic_model', elastic_model)])

            # Training the pipeline which consists of elastic model and standard scaler.

            pipe_en.fit(X_train, y_train)

            # With best parameters, create the pipeline again and return it

            logger.log("Exited elastic_net_model method in ModelFinder class")

            return pipe_en

        except Exception as e:
            logger.log("Error occurred while creating ElasticNet Model")
            logger.log("Exited elastic_net_model method in ModelFinder class")
            raise e

    def svr_model(self):

        logger = self.logger
        X_train = self.X_train
        y_train = self.y_train
        logger.log("Entered svr_model method in ModelFinder class")

        try:
            # Scaling the data

            scaler = StandardScaler()
            scaled_X_train = scaler.fit_transform(X_train)

            # Creating the base model

            base_svr = SVR()

            # Creating the parameters grid

            param_grid = {"C": [0.01, 0.1, 1], 'kernel': ['linear', 'poly', 'rbf'], 'degree': [2, 3, 4]}

            # Grid Model Creation

            grid = GridSearchCV(estimator=base_svr, param_grid=param_grid, verbose=3, cv=5)

            # Training the grid model with the scaled data

            grid.fit(scaled_X_train, y_train)

            # Capturing the best parameters

            C = grid.best_params_['C']
            kernel = grid.best_params_['kernel']
            degree = grid.best_params_['degree']

            # Logging the best parameters found

            logger.log(f"Best parameters for SVR model: C={C}; kernel={kernel}; degree={degree}")

            # Creating a scaler object for the pipeline creation

            scaler = StandardScaler()

            # Creating a Support Vector regression model with the best parameters

            svr = SVR(C=C, kernel=kernel, degree=degree)

            # Pipe line Creation

            pipe_svr = Pipeline(steps=[('scaler', scaler), ('svr', svr)])

            # Training the pipeline with the unscaled data

            pipe_svr.fit(X_train, y_train)

            # Logging the completion of the process

            logger.log("Exited svr_model method in ModelFinder class")

            # Returning the best Support Vector regression model

            return pipe_svr

        except Exception as e:
            logger.log("Error occurred while creating Support Vector Regression Model")
            logger.log("Exited svr_model method in ModelFinder class")
            raise e

    def dt_model(self):

        logger = self.logger
        X_train = self.X_train
        y_train = self.y_train
        logger.log("Entered dt_model method in ModelFinder class")

        try:
            # Create a base model for decision tree

            base_dt = DecisionTreeRegressor()

            # Create a param_grid for grid search cv

            param_grid = {"criterion": ["mse", "friedman_mse", "mae"], "max_depth": [1, 2, 3, 4, 5, 6, 7, None]}

            # Create GridSearchCV model

            grid = GridSearchCV(estimator=base_dt, param_grid=param_grid, verbose=3, cv=5)

            # Train the grid model with X_train and y_train

            grid.fit(X_train, y_train)

            # Find the best paramaters from the grid model

            criterion = grid.best_params_['criterion']
            max_depth = grid.best_params_['max_depth']

            # Logging the best parameters found

            logger.log(f"Best parameters for Decision Tree model: criterion={criterion}; max_depth={max_depth}")

            # Create a new decision tree model with the best parameters

            dt = DecisionTreeRegressor(criterion=criterion, max_depth=max_depth)

            # Train the decision tree model with the best parameters using X_train and y_train

            dt.fit(X_train, y_train)

            # Logging the completion of the process

            logger.log("Exited dt_model method in ModelFinder class")

            # Return the decision tree models

            return dt

        except Exception as e:
            logger.log("Error occurred while creating Decision Tree Regression Model")
            logger.log("Exited dt_model method in ModelFinder class")
            raise e

    def rf_model(self):

        logger = self.logger
        X_train = self.X_train
        y_train = self.y_train

        logger.log("Entered rf_model method in ModelFinder class")
        try:
            # Create a base model for Random Forest Regressor

            base_rf = RandomForestRegressor()

            # Create a param_grid for grid search cv

            param_grid = {"n_estimators": [50, 100, 150, 200],
                          "max_depth": [1, 2, 3, 4, 5, 6, 7, None],
                          "criterion": ["mae", "mse"]}

            # Create GridSearchCV model

            grid = GridSearchCV(estimator=base_rf, param_grid=param_grid, verbose=3, cv=5)

            # Train the grid model with X_train and y_train

            grid.fit(X_train, y_train)

            # Find the best paramaters from the grid model

            n_estimators = grid.best_params_['n_estimators']
            max_depth = grid.best_params_['max_depth']
            criterion = grid.best_params_['criterion']

            # Logging the best parameters found

            logger.log(
                f"Best parameters for Random Forest model: n_estimators={n_estimators}; criterion={criterion}; max_depth={max_depth}")

            # Create a new random forest model with the best parameters

            rf = RandomForestRegressor(n_estimators=n_estimators, max_depth=max_depth, criterion=criterion)

            # Train the decision tree model with the best parameters using X_train and y_train

            rf.fit(X_train, y_train)

            # Logging the completion of the process

            logger.log("Exited rf_model method in ModelFinder class")

            # Return the decision tree models

            return rf

        except Exception as e:
            logger.log("Error occurred while creating Random Forest Regression Model")
            logger.log("Exited rf_model method in ModelFinder class")
            raise e

    def xgb_model(self):

        logger = self.logger
        X_train = self.X_train
        y_train = self.y_train

        logger.log("Entered xgb_model method in ModelFinder class")
        try:
            # Create a base model for XGBoost Regressor

            base_xgb = XGBRegressor()

            # Create a param_grid for grid search cv

            param_grid = {"n_estimators": [100, 200, 500, 1000], 'learning_rate': [0.1, 0.01, 0.001]}

            # Create GridSearchCV model

            grid = GridSearchCV(estimator=base_xgb, param_grid=param_grid, verbose=3, cv=5)

            # Train the grid model with X_train and y_train

            grid.fit(X_train, y_train)

            # Find the best paramaters from the grid model

            n_estimators = grid.best_params_['n_estimators']
            learning_rate = grid.best_params_['learning_rate']

            # Logging the best parameters found

            logger.log(f"Best parameters for XGBoost model: n_estimators={n_estimators}; learning_rate={learning_rate}")

            # Create a new XGBoost model with the best parameters

            xgb = XGBRegressor(n_estimators=n_estimators, learning_rate=learning_rate, tree_method='auto',
                               predictor='auto')

            # Train the XGBoost model with the best parameters using X_train and y_train

            xgb.fit(X_train, y_train, verbose=3)

            # Logging the completion of the process

            logger.log("Exited xgb_model method in ModelFinder class")

            # Return the decision tree models

            return xgb

        except Exception as e:
            logger.log("Error occurred while creating XGBoost Regression Model")
            logger.log("Exited xgb_model method in ModelFinder class")
            raise e

    def get_best_model(self):

        logger = self.logger
        X_test = self.X_test
        y_test = self.y_test

        logger.log("Entered get_best_model method in ModelFinder class")
        try:
            # Linear Regression
            lr_model = self.lr_model()
            lr_preds = lr_model.predict(X_test)
            lr_score = r2_score(y_test, lr_preds)

            # Elastic Net Model
            elastic_net_model = self.elastic_net_model()
            elastic_net_preds = elastic_net_model.predict(X_test)
            elastic_net_score = r2_score(y_test, elastic_net_preds)

            # Support Vector Regressor
            svr_model = self.svr_model()
            svr_preds = svr_model.predict(X_test)
            svr_score = r2_score(y_test, svr_preds)

            # Decision Tree
            dt_model = self.dt_model()
            dt_preds = dt_model.predict(X_test)
            dt_score = r2_score(y_test, dt_preds)

            # Random Forest
            rf_model = self.rf_model()
            rf_preds = rf_model.predict(X_test)
            rf_score = r2_score(y_test, rf_preds)

            # XGBoost
            xgb_model = self.xgb_model()
            xgb_preds = xgb_model.predict(X_test)
            xgb_score = r2_score(y_test, xgb_preds)

            # Finding the best model with the best score
            scores = [lr_score, elastic_net_score, svr_score, dt_score, rf_score, xgb_score]
            model_idx = scores.index(max(scores))

            if model_idx == 0:
                return lr_model, "LinearRegression"
            elif model_idx == 1:
                return elastic_net_model, "ElasticNet"
            elif model_idx == 2:
                return svr_model, "SupportVectorRegressor"
            elif model_idx == 3:
                return dt_model, "DecisionTree"
            elif model_idx == 4:
                return rf_model, "RandomForest"
            else:
                return xgb_model, "XGBoost"

        except Exception as e:
            logger.log("Error occurred while finding the best model")
            logger.log("Exited get_best_model method in ModelFinder class")
            raise e
