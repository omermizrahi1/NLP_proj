
import pandas as pd
from sklearn.calibration import LabelEncoder
from sklearn.ensemble import ExtraTreesClassifier, RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
from sklearn.preprocessing import OneHotEncoder
from xgboost import XGBClassifier
from model import test_train





glinert_with_combinations_params = {
    'n_estimators': 1213, 
    'max_depth': 1446, 
    'min_samples_split': 11, 
    'min_samples_leaf': 2, 
    'criterion': 'entropy'
}

glinert_without_combinations_params = {
    'n_estimators': 492,
    'criterion': 'entropy',
    'max_features': 98,
    'min_samples_split': 12,
    'min_samples_leaf': 4
}

blau_with_combinations_params = {
    'n_estimators': 1976,
    'max_depth': 1754,
    'min_samples_split': 6,
    'min_samples_leaf': 7,
    'criterion': 'gini'
}

blau_without_combinations_params =  {
    'learning_rate': 0.07065406111162569,
    'max_depth': 9,
    'subsample': 0.5330322464317575,
    'colsample_bytree': 0.736391557003238,
    'min_child_weight': 19
}




def test_optimization():
    methods = {
        ('glinert', True): (ExtraTreesClassifier , glinert_with_combinations_params),
        ('glinert', False): (RandomForestClassifier, glinert_without_combinations_params),
        ('blau', True): (ExtraTreesClassifier, blau_with_combinations_params),
        ('blau', False): (XGBClassifier, blau_without_combinations_params)
    }

    for method in methods:
        result = {'optimized':[], 'not_optimized':[]}
        for i in range(100):
            X_train, X_test, y_train, y_test = test_train(method[0], method[1])
            opt_model = methods[method][0](**methods[method][1])
            opt_model.fit(X_train, y_train)
            y_pred_opt = opt_model.predict(X_test)
            result['optimized'].append(accuracy_score(y_test, y_pred_opt))
            not_opt_model = methods[method][0]()
            not_opt_model.fit(X_train, y_train)
            y_pred = not_opt_model.predict(X_test)
            result['not_optimized'].append(accuracy_score(y_test, y_pred))

        optmized_mean = sum(result['optimized'])/len(result['optimized'])
        not_optimized_mean = sum(result['not_optimized'])/len(result['not_optimized'])

        print(f'results: {result}')
        print (f'optimized mean: {optmized_mean}')
        print (f'not optimized mean: {not_optimized_mean}')

        if optmized_mean > not_optimized_mean:
            print(f'{method[0]} with combinations={method[1]} is better with optimization')
            print(classification_report(y_test, y_pred_opt))
            
        else:
            print(f'{method[0]} with combinations={method[1]} is better without optimization')
            print(classification_report(y_test, y_pred))


def encoded_dataset(method, comb=True):
    if comb:
        df = pd.read_excel(f'merged_comb_{method}.xlsx')
    else:
        df = pd.read_excel(f'merged_{method}.xlsx')
    df.replace({None: pd.NA}, inplace=True)
    df.drop(columns=['target word_0'], inplace=True)
    df.dropna(subset=[method.capitalize()], inplace=True)
    df = df[df[method.capitalize()] != '-']
    df.fillna('', inplace=True)

    X = df.iloc[:, :-1]
    y = df.iloc[:, -1]

    encoder = OneHotEncoder(sparse=False , handle_unknown='ignore')
    encoder.fit(X)
    X = encoder.transform(X)

    label_encoder = LabelEncoder()
    y = label_encoder.fit_transform(y)

    return X, y



if __name__ == '__main__':
    test_optimization()

    glinert_final_model = ExtraTreesClassifier(**glinert_with_combinations_params)
    blau_final_model = ExtraTreesClassifier(**blau_with_combinations_params)
    X, y = encoded_dataset('glinert')
    glinert_final_model.fit(X, y)
    X, y = encoded_dataset('blau')
    blau_final_model.fit(X, y)