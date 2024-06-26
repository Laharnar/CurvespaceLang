import core.mincore as core
from core.mechanistic_layers import BinaryConstruct

task = "figure out what to do with output of conversation about topic"
history = list()
for i in range(5):
    history = history[-4:]
    answer = core.aiLang("progress on task \n"+task, False, OUTPUT="long", solutions=history)
    answer = core.ai("summarize what was done to stand independently, and what would ideally happend next step on path to converting it into logic", answer)
    history.append(answer)


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


