
from core.mincore import *
from agents.gridshards.AnalysisGrid import *

task = "create chess in py"

def cycle(task, history):
    history = list()
    for i in range(3):
        history.append(ai("through context implement this\n"+task, history))
    return ai(task, history)

def chain(task):
    history = list()
    for i in range(3):
        history.append(ai(task, history))
    return ai(task, history)

def toLang(task):
    return ai("create new language that will support this", [task])

def redline():
    return ai("create language for creating red line -- a concept that explains something")

def trail(task, str):
    return ai("through context implement this \n"+str, [task])

red = redline()

cycle(task, trail(task, red))

chain(task)

