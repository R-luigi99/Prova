import pandas as pd
from sklearn.tree import DecisionTreeClassifier
import pydriller
import sys

extensions=[".java"]
#id=sys.argv[1]
#gitRepo=sys.argv[2]


id='284e98744ebb926b3230282866c344aec8ad76ab'
gitRepo='https://github.com/R-luigi99/Prova.git'

from sklearn import tree


import warnings

warnings.filterwarnings('ignore')




for c in pydriller.Repository(path_to_repo=gitRepo,single=id,only_no_merge=True).traverse_commits():
    authorDate = c.author_date.date()
    authorday = authorDate.weekday()
    numberOfModifiedFiles = c.files
    insertions = c.insertions
    deletions = c.deletions
    totalLines = c.lines
    ore = c.author_date.astimezone().hour
    oreinminuti = 60 * ore
    orario = c.author_date.astimezone().minute
    timestamp = oreinminuti + orario
    complexity = c.dmm_unit_complexity


if complexity is None:
    complexity = 0.5



#Xnew nuova tupla/nuovo commit
Xnew=[[authorday,timestamp,numberOfModifiedFiles,insertions,deletions,totalLines,complexity]]


tables = pd.read_csv("table.csv", sep=",")
car = tables.shape[1] - 1
numpy_array = tables.values
x_train = numpy_array[:, : car]
y_train = numpy_array[:, car]

modello=DecisionTreeClassifier(class_weight='balanced', max_depth=10)


modello.fit(x_train,y_train)
#il load deve essere in uno script separato per ora resta qua
from joblib import dump, load
dump(modello, 'prova.sav') #caricamento
model2 = load('prova.sav')

#stampo albero di decisione
text_representation = tree.export_text(model2)
#print(text_representation)
with open("decistion_tree.log", "w") as fout:
    fout.write(text_representation)

ynew = model2.predict(Xnew)
print(Xnew)
if ynew == 0.0:
    print("commit buono")
else:
    print("commit con possibile bug")
