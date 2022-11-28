import csv
import json

with open("sample.json", "r") as features:
    dictfeatures = json.load(features)

with open("idBadCommits.json", "r") as badcommits:
    dictbadcommits = json.load(badcommits)

keys = ["day", "time", "numberOfModifiedFiles", "insertions", "deletions", "totalLines", "complexity",
        "badCommit"]

commit_DF = {key: [] for key in keys}

for key in dictfeatures.keys():
    if dictfeatures[key]["complexity"] is not None:
        commit_DF["day"].append(dictfeatures[key]["day"])
        commit_DF["time"].append(dictfeatures[key]["time"])
        commit_DF["numberOfModifiedFiles"].append(dictfeatures[key]["numberOfModifiedFiles"])
        commit_DF["insertions"].append(dictfeatures[key]["insertions"])
        commit_DF["deletions"].append(dictfeatures[key]["deletions"])
        commit_DF["totalLines"].append(dictfeatures[key]["totalLines"])
        commit_DF["complexity"].append(dictfeatures[key]["complexity"])
        value = dictbadcommits.__contains__(key)
        if value:
            commit_DF["badCommit"].append("1")
        else:
            commit_DF["badCommit"].append("0")


with open("table.csv", "w", encoding="utf-8") as outfile2:
    writer2 = csv.writer(outfile2)
    writer2.writerow(commit_DF.keys())
    writer2.writerows(zip(*commit_DF.values()))
