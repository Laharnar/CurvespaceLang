
from core.mincore import sendWithMessage as ai
from core.mechanistic_layers import BinaryConstruct as Bin

task = "find which fields of project in current folder could be improved"

solutions = list()
languages = list()
answer = ai("+ <<SOLVED>>?\n"+task)
solutions.append(task)
language = ai("create new language for this\n" + task)
solutions.append(language)
cyclicAnswer = answer
cyclicLanguage = language
while("SOLVED" not in answer):


    path = ai("describe state of task, what was done so far, and prediction for how much work is left in ideal scenario.", [task, cyclicAnswer, "using language to complete task", cyclicLanguage])
    language = ai("create new language for this", [task, path])
    solutions.append(path)
    solutions.append(language)
    answer = ai("implement and validate solution with provided language. reply <<SOLVED>> if it's solved.\n", [task, path, cyclicLanguage])
    cyclicAnswer = answer
    cyclicLanguage = language




