#! /usr/bin/python3

import json
import sys
import re
import codecs
import datetime
import pydriller

class CommitData():
    def __init__(self,commitId,commitDate):
        self.commitId=commitId
        self.commitDate=commitDate


def isBug(msg,regexp):
    p=re.compile(regexp,re.IGNORECASE)
    if p.search(msg):
            return True
    return False


def getExtension(lang):
    extensions={"java":"java","python":"py","csharp":"cs"}
    return extensions[lang]

def isNotRevert(msg):
    p=re.compile("^revert",re.IGNORECASE)
    if not p.search(msg):
        return True
    return False


def getGit(directory):
    return pydriller.Git(directory)

def analyzeLog(gitRepo,bugRegExp,lang):
    allData={}
    dateFormat = "%Y-%m-%d %H:%M:%S +0000"
    bugIdCount=1
    #repo=pydriller.Repository(path_to_repo=gitRepo,only_no_merge=True,only_modifications_with_file_types=[".py"])
    #commits=repo.traverse_commits()
    for c in pydriller.Repository(path_to_repo=gitRepo,only_no_merge=True,only_modifications_with_file_types=[getExtension(lang)]).traverse_commits():
        commitDate=c.author_date
        commitId=c.hash
        message=c.msg
        print("Analyzing "+commitId,file=sys.stderr)
        if isBug(message,bugRegExp) and isNotRevert(message):
            try:
                commitDateObj=commitDate #   datetime.datetime.strptime(str(commitDate),'%a %b %d %H:%M:%S %Y %z')
                openDate=commitDateObj-datetime.timedelta(seconds=1)
                closedDate=commitDateObj+datetime.timedelta(seconds=1)
                status="closed"
                issueId=bugIdCount
                bugIdCount+=1
                issueData = {}
                issueData['creationdate'] = openDate.strftime(dateFormat)
                issueData['resolutiondate'] = closedDate.strftime(dateFormat)
                issueData['hash'] = str(commitId)
                issueData['commitdate'] = commitDateObj.strftime(dateFormat)
                issueData['message']=message
                allData[issueId] = issueData
            except Exception as e:
                #print("Exception" % str(e))
                continue

    json_data = json.dumps(allData,indent=2)
    return json_data



def parseLog(filename,bugRegExp):
    allData={}
    dateFormat = "%Y-%m-%d %H:%M:%S +0000"
    bugIdCount=1
    with codecs.open(filename, 'r',encoding="utf-8") as infile:
        data = infile.read()
        json_data = json.loads(data)
        for commit in json_data:
            try:
                cdata=commit['data']
                commitDate=cdata['CommitDate']
                commitId=cdata['commit']
                message=cdata['message']
                isFix=isBug(message,bugRegExp)
                if isFix:
                    #print(message)
                    commitDateObj=datetime.datetime.strptime(str(commitDate),'%a %b %d %H:%M:%S %Y %z')
                    openDate=commitDateObj-datetime.timedelta(seconds=1)
                    closedDate=commitDateObj+datetime.timedelta(seconds=1)
                    status="closed"
                    issueId=bugIdCount
                    bugIdCount+=1
                    issueData = {}
                    issueData['creationdate'] = openDate.strftime(dateFormat)
                    issueData['resolutiondate'] = closedDate.strftime(dateFormat)
                    issueData['hash'] = str(commitId)
                    issueData['commitdate'] = commitDateObj.strftime(dateFormat)
                    allData[issueId] = issueData
            except Exception as e:
                #print("Exception" % str(e))
                continue
    json_data = json.dumps(allData,indent=2)
    return json_data

if __name__ == '__main__':

    if len(sys.argv)<3:
        print ("Syntax %s repo language" % sys.argv[0])
        exit(1)

    with open("bugRegexp.txt") as f:
        bugRegExp=f.read()
        bugRegExp=bugRegExp.rstrip("\n")

    repo=sys.argv[1]
    language=sys.argv[2]
    s=analyzeLog(repo,bugRegExp,language)
    print(s)

