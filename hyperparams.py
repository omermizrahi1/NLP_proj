from sklearn import model_selection
from sklearn.ensemble import ExtraTreesClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.neighbors import NearestCentroid
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
import optuna
from optuna.samplers import TPESampler
from model import test_train
import logging


N_TRIALS = 400

def xgb_objective(trial):
    xgb_params = {
        "n_estimators": trial.suggest_int("n_estimators", 75, 300),
        "verbosity": 0,
        "learning_rate": trial.suggest_float("learning_rate", 0.05, 0.35, log=True),
        "max_depth": trial.suggest_int("max_depth", 2, 10),
        "subsample": trial.suggest_float("subsample", 0.1, 1.0),
        "colsample_bytree": trial.suggest_float("colsample_bytree", 0.1, 1.0),
        "min_child_weight": trial.suggest_int("min_child_weight", 1, 10),
    }
    clf = XGBClassifier(**xgb_params)
    score = model_selection.cross_val_score(clf, X_train, y_train, n_jobs=10, cv=5)
    accuracy = score.mean()
    return accuracy



def lr_objective(trial):
    lr_params = {
        "C": trial.suggest_float("C", 1e-6, 1.0, log=True),
        "fit_intercept": trial.suggest_categorical("fit_intercept", [True, False]),
        "solver": trial.suggest_categorical("solver", ['newton-cg', 'lbfgs', 'liblinear', 'sag', 'saga']),
        "max_iter": trial.suggest_int("max_iter", 100, 1000),
    }
    if lr_params["solver"] in ['liblinear', 'saga']:
        lr_params["penalty"] = trial.suggest_categorical("penalty", ['l1', 'l2'])
    else:
        lr_params["penalty"] = 'l2'
    
    clf = LogisticRegression(**lr_params, random_state=0)
    score = model_selection.cross_val_score(clf, X_train, y_train, n_jobs=10, cv=20)
    accuracy = score.mean()
    return accuracy


def nc_objective(trial):
    nc_params = {
        "shrink_threshold": trial.suggest_float("shrink_threshold", 0, 0.3),
    }

    clf = NearestCentroid(**nc_params)
    score = model_selection.cross_val_score(clf, X_train, y_train, n_jobs=10, cv=5)
    accuracy = score.mean()
    return accuracy


if __name__ == "__main__":
    methods = [
    # ('glinert', False, lr_objective),
    # ('blau', False, xgb_objective),
    # ('glinert', True, nc_objective),
    ('blau', True, xgb_objective)
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