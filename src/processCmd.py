"""
    Add a task
    Remove a task
    Speak a recap of tasks by day in a week
"""
from pandas import *
import csv
import nltk #NLP library
from nltk.corpus import stopwords
import spacy #NLP library
from nltk.tokenize import word_tokenize
 
stopwords = set(stopwords.words('english'))
nlp = spacy.load("en_core_web_md") #trained models


#prepare nostopword list
def noStopword (tasks):
    noStopwordTasks =[]
    for task in tasks:
        tokTask = tokenize(task[0])
        noStopwordTasks.append(tokTask)
    return noStopwordTasks

#preprocessing token + remove stopwords
def tokenize(task):
    word_token = word_tokenize(task)
    tokenizedTask = ""
    for word in word_token:
        if word not in stopwords:
            tokenizedTask += word + ' '
    return tokenizedTask

#check if new task is similar to already existed tasks in list
def checkSimilar(newTask, noStopwordsTasks):
    try:
        #preprocess step: remove stop words
        tokTask = tokenize(newTask)
        #check similarities
        for task in noStopwordsTasks:
            nlpTask = nlp(task)
            nlpTokTask = nlp(tokTask)
            similarity = nlpTask.similarity(nlpTokTask)
            if similarity >0.75: #threshold set as 0.8
                similarTask = task
                return True,similarTask
        return False,0
    except:
        pass


#add task, check for similarities before adding to list
def addTask(task, tasks):
    try:
        if len(tasks)>=1:
            result = checkSimilar(task, tasks)
        if result[0] == False or len(tasks)==0:
            todoList = recapTask()
            writeList=[]
            for ta in todoList:
                writeList.append(ta[0])
            writeList.append(task)
            with open("todo-list.csv", "w", newline='') as f:
                csvWriter = csv.writer(f)
                for w in writeList:
                    csvWriter.writerow([w])
                return "added"
        else:
            return "duplicate"
    except:
        pass

#remove task, also check for similarities
def removeTask(task, tasks):
    try:
        if len(tasks) ==0:
            return "empty"
        else:
            result = checkSimilar(task, tasks)
            if result[0] == True:
                todoList = recapTask()
                writeList=[]
                for taske in todoList:
                    if taske[0] == task:
                        todoList.remove(taske)
                    else:
                        writeList.append(taske[0])
                with open("todo-list.csv", "w", newline='') as f:
                    csvWriter = csv.writer(f)
                    for w in writeList:
                        csvWriter.writerow([w])
                    return "removed"
            else:
                return "not exist" 
    except:
        pass

def recapTask():
    try:
        todoList=[]
        with open('todo-list.csv', 'r') as f:
            csvReader = csv.reader(f)
            for row in csvReader:
                todoList.append(row)
            return todoList
    except:
        pass