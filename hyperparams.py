from lightgbm import LGBMClassifier
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
from sklearn import model_selection
from sklearn.metrics import accuracy_score, f1_score
from sklearn.calibration import LabelEncoder
from sklearn.decomposition import PCA
from sklearn.ensemble import ExtraTreesClassifier, RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier, NearestCentroid
from sklearn.preprocessing import OneHotEncoder
from sklearn.svm import SVC
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
import optuna
from optuna.samplers import TPESampler, CmaEsSampler
from lazypredict.Supervised import LazyClassifier
import numpy as np
from model import test_train
import logging
from concurrent.futures import ThreadPoolExecutor


N_TRIALS = 500

def xgb_objective(trial):
    xgb_params = {
        "n_estimators": 1000,
        "verbosity": 0,
        "learning_rate": trial.suggest_float("learning_rate", 1e-3, 0.1, log=True),
        "max_depth": trial.suggest_int("max_depth", 1, 10),
        "subsample": trial.suggest_float("subsample", 0.05, 1.0),
        "colsample_bytree": trial.suggest_float("colsample_bytree", 0.05, 1.0),
        "min_child_weight": trial.suggest_int("min_child_weight", 1, 20),
    }
    clf = XGBClassifier(**xgb_params)
    score = model_selection.cross_val_score(clf, X_train, y_train, n_jobs=-1, cv=20)
    accuracy = score.mean()
    return accuracy



def et_objective(trial):
    et_params = {
        'n_estimators': trial.suggest_int("n_estimators", 8, 2048),
        'max_depth': trial.suggest_int("max_depth", 4, 2048),
        'min_samples_split': trial.suggest_int("min_samples_split", 2, 16),
        'min_samples_leaf': trial.suggest_int("min_samples_leaf", 1, 8),
        'criterion': trial.suggest_categorical("criterion", ['gini', 'entropy'])
    }

    
    clf = ExtraTreesClassifier(**et_params)
    score = model_selection.cross_val_score(clf, X_train, y_train, n_jobs=-1, cv=20)
    accuracy = score.mean()
    return accuracy


def rf_objective(trial):
    rf_params = {
        'n_estimators': trial.suggest_int("n_estimators", 100, 500, log=True),
        'criterion': trial.suggest_categorical("criterion", ['log_loss', 'entropy', 'gini']),
        'max_features':  trial.suggest_int("max_features", 50, 1050, log=True),
        'min_samples_split': trial.suggest_int("min_samples_split", 2, 100, log=True),
        'min_samples_leaf': trial.suggest_int("min_samples_leaf", 1, 10, log=True)
    }

    clf = RandomForestClassifier(**rf_params)
    score = model_selection.cross_val_score(clf, X_train, y_train, n_jobs=-1, cv=20)
    accuracy = score.mean()
    return accuracy


if __name__ == "__main__":
    methods = [
    ('glinert', False, rf_objective),
    ('blau', False, xgb_objective),
    ('glinert', True, et_objective),
    ('blau', True, et_objective)
]
    for method, comb, objective in methods:
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)  
        log_file_name = f"optuna_{method}_{'with' if comb == True else 'without'}_combinations.log"
        logger.addHandler(logging.FileHandler(f'logs\\{log_file_name}', mode="a"))

        optuna.logging.enable_propagation()
        optuna.logging.disable_default_handler()
        
        X_train, X_test, y_train, y_test = test_train(method, comb)
        study = optuna.create_study(direction="maximize", sampler=TPESampler())
        logger.info("Start optimization.")
        study.optimize(objective, n_trials=N_TRIALS)

        with open(log_file_name) as f:
            assert f.readline().startswith("A new study created")
            assert f.readline() == "Start optimization.\n"
        for handler in logger.handlers:
            handler.close()
            logger.removeHandler(handler)







