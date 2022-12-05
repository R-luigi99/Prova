import pandas as pd
from sklearn.tree import DecisionTreeClassifier
tables = pd.read_csv("table.csv", sep=",")
car = tables.shape[1] - 1
numpy_array = tables.values
x_train = numpy_array[:, : car]
y_train = numpy_array[:, car]

modello=DecisionTreeClassifier(class_weight='balanced', max_depth=10)


modello.fit(x_train,y_train)
from joblib import dump
dump(modello, 'prova.sav') #caricamento
