import pandas as pd
from sklearn.calibration import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split
from lazypredict.Supervised import LazyClassifier
import os


def test_train(method, comb = False):
    excel_folder = 'excel'
    if comb:
        df = pd.read_excel(os.path.join(excel_folder,f'merged_comb_{method}.xlsx'))
    else:
        df = pd.read_excel(os.path.join(excel_folder,f'merged_{method}.xlsx'))
    df.replace({None: pd.NA}, inplace=True)
    df.drop(columns=['target word_0'], inplace=True)
    df.dropna(subset=[method.capitalize()], inplace=True)
    df = df[df[method.capitalize()] != '-']
    df.fillna('', inplace=True)

    X = df.iloc[:, :-1]
    y = df.iloc[:, -1]

    encoder = OneHotEncoder(sparse=False , handle_unknown='ignore')
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    encoder.fit(X_train)
    X_train = encoder.transform(X_train)
    X_test = encoder.transform(X_test)

    label_encoder = LabelEncoder()
    y_train = label_encoder.fit_transform(y_train)
    y_test = label_encoder.fit_transform(y_test)
    return X_train, X_test, y_train, y_test



def lazypredict():
    methods = [('glinert',False), ('blau',False), ('glinert',True), ('blau',True)]
    for method, comb in methods:
        X_train, X_test, y_train, y_test = test_train(method, comb)
        clf = LazyClassifier(verbose=0,ignore_warnings=True, custom_metric=None)
        models, predictions = clf.fit(X_train, X_test, y_train, y_test)
        
        file_path = f"lazypredict_results.txt"
        try:
            with open(file_path, 'a+') as file:
                file.write(f"### models for {method} {'with' if comb == True else 'without'} attribute combination ###\n\n")
                file.write(f"{models.sort_values(by='Accuracy', ascending=False)}\n\n")
            print("Data has been appended to the file.")
        except IOError as e:
            print(f"An error occurred while writing to the file: {e}")




if __name__ == "__main__":
    lazypredict()





