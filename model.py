import threading
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
from sklearn.calibration import _CalibratedClassifier, CalibratedClassifierCV, LabelEncoder, LinearSVC
from sklearn.decomposition import PCA
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis, QuadraticDiscriminantAnalysis
from sklearn.dummy import DummyClassifier
from sklearn.ensemble import AdaBoostClassifier, BaggingClassifier, ExtraTreesClassifier, GradientBoostingClassifier, HistGradientBoostingClassifier, RandomForestClassifier, StackingClassifier, VotingClassifier
from sklearn.gaussian_process import GaussianProcessClassifier
from sklearn.linear_model import LogisticRegression, PassiveAggressiveClassifier, Perceptron, SGDClassifier
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier, NearestCentroid, RadiusNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder
from sklearn.semi_supervised import LabelPropagation, LabelSpreading
from sklearn.svm import SVC, NuSVC
from sklearn.tree import DecisionTreeClassifier
from xgboost import XGBClassifier
from catboost import CatBoostClassifier
from lazypredict.Supervised import LazyClassifier
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
import optuna
from optuna.samplers import TPESampler, CmaEsSampler



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
    X.to_excel('X.xlsx', index=False)
    print(f"X size = {X.size}")  
    y = df.iloc[:, -1]   
    print(f"y size = {y.size}")

    encoder = OneHotEncoder(sparse=False)
    X_encoded = encoder.fit_transform(X)
    X_train, X_test, y_train, y_test = train_test_split(X_encoded, y, test_size=0.2, random_state=42)

    label_encoder = LabelEncoder()
    y_train_encoded = label_encoder.fit_transform(y_train)
    y_test_encoded = label_encoder.fit_transform(y_test)

    clf = LazyClassifier(verbose=0,ignore_warnings=True, custom_metric=None)
    models,predictions = clf.fit(X_train, X_test, y_train_encoded, y_test_encoded)
    print(models)



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


g_classifiers = ["NearestCentroid", "LGBMClassifier", "XGBClassifier, ExtraTreesClassifier, ExtraTreesClassifier"]
b_classifiers = ["NearestCentroid", "XGBClassifier", "LGBMClassifier", "RandomForestClassifier", "ExtraTreesClassifier"]

def objective(trial):
    

    classifier_name = trial.suggest_categorical("classifier", g_classifiers)
    if classifier_name == "SVC":
        svc_c = trial.suggest_float("svc_c", 1e-10, 1e10, log=True)
        classifier_obj = sklearn.svm.SVC(C=svc_c, gamma="auto")
    elif classifier_name == "RandomForest":
        rf_max_depth = trial.suggest_int("rf_max_depth", 2, 32, log=True)
        classifier_obj = sklearn.ensemble.RandomForestClassifier(
            max_depth=rf_max_depth, n_estimators=10)
    elif classifier_name == "Logistic":
        logistic_penalty = trial.suggest_categorical("logistic_penalty", ["l1", "l2", "elasticnet", None])
        classifier_obj = sklearn.linear_model.LogisticRegression(penalty=logistic_penalty)
    else:
        exit('error: unknown classifier')
    score = sklearn.model_selection.cross_val_score(classifier_obj, x, y, n_jobs=-1, cv=3)
    accuracy = score.mean()
    return accuracy

