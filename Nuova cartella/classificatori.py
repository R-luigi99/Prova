import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.svm import SVC
from sklearn import metrics
from sklearn.metrics import plot_confusion_matrix
from sklearn.model_selection import cross_val_score
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import train_test_split

import warnings

warnings.filterwarnings('ignore')

tables = pd.read_csv("table.csv", sep=",")



def classificationFunction(df):
    car = df.shape[1] - 1
    numpy_array = df.values
    x = numpy_array[:, : car]
    y = numpy_array[:, car]
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=42)

    names = ["RandomForrest", "ExtraTrees", "DecisionTree"]

    classifiers = [
        RandomForestClassifier(class_weight='balanced', random_state=1, n_estimators=100, max_features=1),
        ExtraTreesClassifier(class_weight='balanced', random_state=1),
        DecisionTreeClassifier(class_weight='balanced', max_depth=10)]

    result = pd.DataFrame(
        columns=["Classifier", "Accuracy", "Precision", "Recall", "FScore",
                 "K-Cross Validation best result Accuracy",
                 "K-Cross Validation best result Precision", "K-Cross Validation best result Recall",
                 "K-Cross Validation best result FScore"])

    for name, classifier in zip(names, classifiers):
        classifier.fit(x_train, y_train)
        y_pred = classifier.predict(x_test)
        pr, rc, fs, sup = metrics.precision_recall_fscore_support(y_test, y_pred, average='macro')
        report = classification_report(y_pred, y_test)
        disp = plot_confusion_matrix(classifier, x_test, y_test, cmap=plt.cm.BuPu, normalize=None)
        disp.ax_.set_title("Confusion matrix for " + name)
        print()
        print(name, "\n")
        print(report)
        print(name, "Confusion Matrix: \n", disp.confusion_matrix)
        print()
        print('Accuracy score: ', round(accuracy_score(y_test, y_pred), 3), ' Precision', round(pr, 3), ' Recall',
              round(rc, 3), ' FScore', round(fs, 3))
        cvA = cross_val_score(classifier, x_test, y_test, cv=10, scoring='accuracy')
        cvP = cross_val_score(classifier, x_test, y_test, cv=10, scoring='precision_macro')
        cvR = cross_val_score(classifier, x_test, y_test, cv=10, scoring='recall_macro')
        cvF = cross_val_score(classifier, x_test, y_test, cv=10, scoring='f1_macro')
        print("\n", name, "K cross validation: ")
        print("Score Accuracy: ", cvA)
        print("Mean Accuracy: ", round(np.mean(cvA), 3))
        print("Score Precision: ", cvP)
        print("Mean Precision: ", round(np.mean(cvP), 3))
        print("Score Recall: ", cvR)
        print("Mean Recall: ", round(np.mean(cvR), 3))
        print("Score FScore: ", cvF)
        print("Mean FScore: ", round(np.mean(cvF), 3))
        print("\n\n")
        result = result.append({"Classifier": name, "Accuracy": round(metrics.accuracy_score(y_test, y_pred), 4),
                                "Precision": round(pr, 3), "Recall": round(rc, 3), "FScore": round(fs, 3),
                                "K-Cross Validation best result Accuracy": round(max(cvA), 3),
                                "K-Cross Validation best result Precision": round(max(cvP), 3),
                                "K-Cross Validation best result Recall": round(max(cvR), 3),
                                "K-Cross Validation best result FScore": round(max(cvF), 3)
                                }, ignore_index=True)

    print(result)
    return result


classificationFunction(tables)


# Cross-validate
def display_accuracy_scores(pipeline, x, y):
    scores = cross_val_score(pipeline, x, y, cv=10, scoring='accuracy')
    print('Scores\t:', scores)
    print('Mean\t:', scores.mean())
    print('SD\t:', scores.std())