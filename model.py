
from lightgbm import LGBMClassifier
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
from sklearn import model_selection
from sklearn.metrics import accuracy_score
from sklearn.calibration import LabelEncoder
from sklearn.decomposition import PCA
from sklearn.ensemble import ExtraTreesClassifier, RandomForestClassifier
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.neighbors import KNeighborsClassifier, NearestCentroid, RadiusNeighborsClassifier
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
import optuna
from optuna.samplers import TPESampler, CmaEsSampler
from optuna import Trial, visualization

def objective(trial):

    
    rf_params = {
        'n_estimators': trial.suggest_int("n_estimators1", 100, 500, log=True),
        'criterion': trial.suggest_categorical("criterion1", ['log_loss', 'entropy', 'gini']),
        'max_features':  trial.suggest_int("max_features1", 1, 8, log=True),
        'max_depth': trial.suggest_int("max_depth1", 5, 30, log=True),
        'min_samples_split': trial.suggest_int("min_samples_split1", 2, 100, log=True),
        'min_samples_leaf': trial.suggest_int("min_samples_leaf1", 1, 10, log=True)
    }

    xgb_params = {
        'lambda': trial.suggest_loguniform('lambda2', 1e-3, 10.0),
        'alpha': trial.suggest_loguniform('alpha2', 1e-3, 10.0),
        'colsample_bytree': trial.suggest_categorical('colsample_bytree2', [0.3,0.4,0.5,0.6,0.7,0.8,0.9, 1.0]),
        'subsample': trial.suggest_categorical('subsample2', [0.4,0.5,0.6,0.7,0.8,1.0]),
        'learning_rate': trial.suggest_categorical('learning_rate2', [0.008,0.01,0.012,0.014,0.016,0.018, 0.02]),
        'n_estimators': 10000,
        'max_depth': trial.suggest_categorical('max_depth2', [5,7,9,11,13,15,17]),
        'random_state': trial.suggest_categorical('random_state2', [2020]),
        'min_child_weight': trial.suggest_int('min_child_weight2', 1, 300),
    }

    et_params = {
    'n_estimators': trial.suggest_int('n_estimators3', 50, 120),
    'max_depth': trial.suggest_int('max_depth3', 10, 16),
    'max_leaf_nodes': trial.suggest_int('max_leaf_nodes3', 15, 25),
    'criterion': trial.suggest_categorical('criterion3', ['gini', 'entropy'])
}

    lgbm_params = { 
        "objective": "multiclass",
        "verbosity": -1,
        "boosting_type": "gbdt",
        "lambda_l1": trial.suggest_float("lambda_l1", 1e-8, 10.0, log=True),
        "lambda_l2": trial.suggest_float("lambda_l2", 1e-8, 10.0, log=True),
        "num_leaves": trial.suggest_int("num_leaves", 2, 256),
        "feature_fraction": trial.suggest_float("feature_fraction", 0.4, 1.0),
        "bagging_fraction": trial.suggest_float("bagging_fraction", 0.4, 1.0),
        "bagging_freq": trial.suggest_int("bagging_freq", 1, 7),
        "min_child_samples": trial.suggest_int("min_child_samples", 5, 100),
        }

    nc_params = {
        'shrink_threshold': trial.suggest_uniform('shrink_threshold', 0, 1)
    }

    classifiers = ["NearestCentroid", "XGBClassifier", "RandomForestClassifier", "ExtraTreesClassifier", "LGBMClassifier"]

    clfs = {"NearestCentroid": NearestCentroid(**nc_params), 
            "LGBMClassifier": LGBMClassifier(**lgbm_params), 
            "XGBClassifier": XGBClassifier(**xgb_params), 
            "ExtraTreesClassifier": ExtraTreesClassifier(**et_params), 
            "RandomForestClassifier": RandomForestClassifier(**rf_params)}
    classifier_name = trial.suggest_categorical("classifier", classifiers)
    classifier_obj = clfs[classifier_name]
    score = model_selection.cross_val_score(classifier_obj, X_train, y_train, n_jobs=-1, cv=3)
    accuracy = score.mean()
    return accuracy

def pca_analysis(X_encoded):
    # Create the PCA instance and fit and transform the data with pca
    pca = PCA()

    # Fit the PCA model to your data
    pca.fit(X_encoded)

    # Get the explained variance ratio for each component
    explained_variance_ratio = pca.explained_variance_ratio_

    # Calculate the cumulative explained variance ratio
    cumulative_explained_variance = np.cumsum(explained_variance_ratio)

    # Plot the cumulative explained variance ratio
    plt.plot(range(1, len(cumulative_explained_variance) + 1), cumulative_explained_variance, marker='o')
    plt.xlabel('Number of Components')
    plt.ylabel('Cumulative Explained Variance Ratio')
    plt.show()

    plt.plot(range(1, len(explained_variance_ratio) + 1), explained_variance_ratio, marker='o')
    plt.xlabel('Number of Components')
    plt.ylabel('Explained Variance Ratio')
    plt.show()

    # Set the threshold for the desired variance to retain
    desired_variance = 0.95

    # Find the number of components that achieve the desired variance
    n_components = np.argmax(cumulative_explained_variance >= desired_variance) + 1
    print("Number of components to retain", desired_variance * 100, "% variance:", n_components)

methods = ['glinert', 'blau']


for method in methods:
    df = pd.read_excel(f'merged_{method}.xlsx')
    df.replace({None: pd.NA}, inplace=True)
    df.drop(columns=['target word_0'], inplace=True)
    df.dropna(subset=[method.capitalize()], inplace=True)
    df = df[df[method.capitalize()] != '-']
    df.fillna('', inplace=True)

    X = df.iloc[:, :-1]
    print(f"X size = {X.size}")  
    y = df.iloc[:, -1]
    print(f"y size = {y.size}")

    encoder = OneHotEncoder(sparse=False , handle_unknown='ignore')
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    X_train = encoder.fit_transform(X_train)
    X_test = encoder.fit_transform(X_test)

    label_encoder = LabelEncoder()
    y_train = label_encoder.fit_transform(y_train)
    y_test = label_encoder.fit_transform(y_test)

    # clf = LazyClassifier(verbose=0,ignore_warnings=True, custom_metric=None)
    # models,predictions = clf.fit(X_train, X_test, y_train, y_test)
    # print(models)
    study = optuna.create_study(direction="maximize", sampler=TPESampler())
    study.optimize(objective, n_trials=1000)
    file_path = f"optuna_{method}.txt"
    try:
        with open(file_path, 'w') as file:
            file.write(f'best_trial: {study.best_trial}\nbest_params: {study.best_params}\nbest_value: {study.best_value}')
        print("Data has been written to the file.")
    except IOError as e:
        print(f"An error occurred while writing to the file: {e}")



# best models for glinert
# NearestCentroid                    0.57               0.43    None      0.57        0.04
# LGBMClassifier                     0.59               0.28    None      0.54        0.91
# XGBClassifier                      0.59               0.28    None      0.54        1.21
# ExtraTreesClassifier               0.58               0.28    None      0.53        0.30
# RandomForestClassifier 


# best models for blau
# NearestCentroid                    0.56               0.37    None      0.56        0.04
# XGBClassifier                      0.64               0.30    None      0.59        0.94
# LGBMClassifier                     0.63               0.29    None      0.59        0.68
# RandomForestClassifier             0.62               0.29    None      0.57        0.30
# ExtraTreesClassifier               0.60               0.28    None      0.55        0.28
