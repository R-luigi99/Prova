import sys

import pydriller
import json


gitRepo=sys.argv[1]

#gitRepo='/home/luigi/ingSoft/dubbo'
extensions=[".java"]


data = {}

for c in pydriller.Repository(path_to_repo=gitRepo,only_no_merge=True,
                              only_modifications_with_file_types=extensions).traverse_commits():
    issueData= {}
    commitMessage=c.msg
    
    author=c.author.name

    authorDate= c.author_date.date()
    authorday= authorDate.weekday()
    id = c.hash
    numberOfModifiedFiles= c.files
    insertions= c.insertions
    deletions= c.deletions
    totalLines= c.lines
    ore = c.author_date.astimezone().hour
    oreinminuti = 60 * ore
    orario = c.author_date.astimezone().minute
    timestamp = oreinminuti + orario
    complexity= c.dmm_unit_complexity

    issueData['commitMessage'] = commitMessage
    issueData['author'] = author
    issueData['day'] = authorday
    issueData['time'] = timestamp
    issueData['id'] = id
    issueData['numberOfModifiedFiles'] = numberOfModifiedFiles
    issueData['insertions'] = insertions
    issueData['deletions'] = deletions
    issueData['totalLines'] = totalLines
    issueData['complexity'] = complexity
    data[id] = issueData

    json_object = json.dumps(data, indent=2)

    with open("sample.json", "w") as outfile:
        outfile.write(json_object)

   
