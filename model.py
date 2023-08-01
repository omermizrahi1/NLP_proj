import threading
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
from sklearn.calibration import _CalibratedClassifier, CalibratedClassifierCV, LabelEncoder, LinearSVC
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


glinert = pd.read_excel('merged_glinert.xlsx')
glinert.replace({None: pd.NA}, inplace=True)
glinert.drop(columns=['target word_0'], inplace=True)
# Drop rows where 'glinert' column contains NaN or '-'
glinert.dropna(subset=['Glinert'], inplace=True)
glinert = glinert[glinert['Glinert'] != '-']
# glinert.to_excel('sanity_check.xlsx', index=False)
glinert.fillna('', inplace=True)


X = glinert.iloc[:, :-1]
X.to_excel('X.xlsx', index=False)
print(f"X size = {X.size}")  # Select all columns except the last one as features
y = glinert.iloc[:, -1]   # Select only the last column as labels
print(f"y size = {y.size}")
# Now, you can proceed with the train-test split as before:


encoder = OneHotEncoder(sparse=False)
X_encoded = encoder.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(X_encoded, y, test_size=0.2, random_state=42)


label_encoder = LabelEncoder()
# Fit and transform the encoder on your features
y_train_encoded = label_encoder.fit_transform(y_train)
y_test_encoded = label_encoder.fit_transform(y_test)


rf = RandomForestClassifier(n_estimators=100, random_state=42)
rf.fit(X_train, y_train_encoded)
accuracy = rf.score(X_test, y_test_encoded)
print(accuracy)


def train_model(model, X, y, results, lock):
    name, clf = model
    clf.fit(X, y)
    score = clf.score(X_test, y_test_encoded)
    with lock:
        results[name] = score

models = [
    ('LogisticRegression', LogisticRegression(max_iter=15000)), 
    ('XGBoost', XGBClassifier()),
    ('KNN', KNeighborsClassifier()),
    ('RandomForest', RandomForestClassifier()),
    ('NaiveBayes', GaussianNB()),
    ('GradientBoosting', GradientBoostingClassifier()),
    ('AdaBoost', AdaBoostClassifier()),
    ('Dummy', DummyClassifier()),
    ('SVC', SVC()),
    ('MLPClassifier', MLPClassifier()),
    ('DecisionTreeClassifier', DecisionTreeClassifier()),
    ('BaggingClassifier', BaggingClassifier()),
    ('ExtraTreesClassifier', ExtraTreesClassifier()),
    ('LinearDiscriminantAnalysis', LinearDiscriminantAnalysis()),
    ('QuadraticDiscriminantAnalysis', QuadraticDiscriminantAnalysis()),
    ('LinearSVC', LinearSVC()),
    ('SGDClassifier', SGDClassifier()),
    ('GaussianProcessClassifier', GaussianProcessClassifier()),
    ('CalibratedClassifierCV', CalibratedClassifierCV()),
    ('Perceptron', Perceptron()),
    ('PassiveAggressiveClassifier', PassiveAggressiveClassifier()),
    ('VotingClassifier', VotingClassifier(estimators=[('lr', LogisticRegression(max_iter=15000)), ('rf', RandomForestClassifier()), ('gnb', GaussianNB())], voting='hard')),
    ('LabelPropagation', LabelPropagation()),
    ('LabelSpreading', LabelSpreading()),
    ('NearestCentroid', NearestCentroid()),
    ('HistGradientBoostingClassifier', HistGradientBoostingClassifier()),
    ('CatBoostClassifier', CatBoostClassifier()),
    ('StackingClassifier', StackingClassifier(estimators=[('lr', LogisticRegression(max_iter=15000)), ('rf', RandomForestClassifier()), ('gnb', GaussianNB())], final_estimator=LogisticRegression(max_iter=15000)))
]

results = {}
lock = threading.Lock()

threads = []
for model in models:
    t = threading.Thread(target=train_model, args=(model, X_train, y_train_encoded, results, lock))
    t.start()
    threads.append(t)

for t in threads:
    t.join()

names = [model[0] for model in models]

#some plotting configurations
x = np.array(range(len(models)))
plt.figure(figsize=(13,5))
plt.title('Classification Algorithms Accuracy')
plt.xlabel('Algorithm')
plt.ylabel('Prediction accuracy')
plt.scatter(x, [results[name] for name in names], marker='o', color='red')   
plt.xticks(x, names, fontsize = 1)
plt.show()

print({k: v for k, v in sorted(results.items(), key=lambda item: item[1], reverse=True)})