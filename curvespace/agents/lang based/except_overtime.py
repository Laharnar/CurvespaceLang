import core.mincore as core
from core.mechanistic_layers import BinaryConstruct

task = "im trying to create code for project, that has bunch of things solved in it, can be loaded, and i can perform modifications and calculations in."
task2 = "describe logical language"
history = dict()
i = 0
while(True):
    answer1 = core.aiLang(task, False, OUTPUT="long")
    answer2 = core.aiLang(task2, False, OUTPUT="long")

    summ2=""
    summ1=""
    xx = sum([[summ2, summ1], answer1], [])
    summ1 = core.ai("summarize state, what was done so far, how much until it's ideally connected to communication language", xx)
    mini = list(answer2)
    xx = sum([[summ1, summ2], answer2], [])
    summ2 = core.ai("summarize state, what was done so far, how much until it's ideally connected to logic language", xx)
    ans = core.ai("say <<SOLVED>> if languages are together enough that they dont need additional work", [summ1, summ2])
    if ("SOLVED" in ans and "NOT" not in ans):
        break
    history[task] = summ1
    task = core.ai("get next non-user task", history.keys())
    history[task2] = summ2
    task2 = core.ai("get next non-user task", history.keys())
    i+=1
    print(i)


answer = core.aiLang("figure out what to do with output of conversation about topic", False, OUTPUT="long")
todo, userInput = core.getTodosUserInc(answer)
stepsTaken = answer[-1]
lastSolution = answer[-2]
lastLang = answer[-3]
lastPrediction = answer[-4]
answer.append(todo)
answer.append(userInput)
answer = core.aiLang("create new interpreter language for composing lists and storing lists as blueprints", False, OUTPUT="long")
core.ai("extract important concepts", [answer])
answer = core.aiLang("create new interpreter language for composing lists and storing lists as blueprints", False, OUTPUT="long")
core.ai("extract important concepts", [answer])
answer = core.aiLang("create new interpreter language for composing lists from individual items and storing them as blueprints", False, OUTPUT="long")
core.ai("extract important concepts", [answer])
answer = core.aiLang("create new interpreter language for combining blueprints that have linear format(like text)", False, OUTPUT="long")
core.ai("extract important concepts", [answer])
answer = core.aiLang("create new interpreter language for composing lego blocks into new model", False, OUTPUT="long")
core.ai("extract important concepts", [answer])
answer = core.aiLang("create new interpreter language for combining lego models into new cohesive solution", False, OUTPUT="long")
core.ai("extract important concepts", [answer])


answer = core.aiLang("create code that would create necessary files", False, OUTPUT="long")
creation = core.ai("get code that creates files", answer)
bin = BinaryConstruct("", creation)
code = bin.codeall
#exec


