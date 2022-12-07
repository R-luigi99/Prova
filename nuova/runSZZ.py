#! /usr/bin/python3

import os
import sys

pythonCommand="python3"
language="java"

if len(sys.argv)<4:
    print("Syntax: %s repository projectname language" % sys.argv[0])
    exit(1)

path=sys.argv[1]
name=sys.argv[2]

bugFileName=name+"-bugs.json"
annotationFileName=name+"-annotations.json"


cmd1=pythonCommand+" SZZNoIssueTracker.py "+path+" "+language+" >"+bugFileName
print(cmd1,file=sys.stderr)
os.system(cmd1)

cmd2=pythonCommand+" SZZ.py "+bugFileName+" "+path+" "+language+" >"+annotationFileName
print(cmd2,file=sys.stderr)
os.system(cmd2)

os.system("gzip -f "+bugFileName)
os.system("gzip -f "+annotationFileName)


