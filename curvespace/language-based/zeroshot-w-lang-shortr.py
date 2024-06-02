
from core.mincore import sendWithMessage as ai
from core.mechanistic_layers import BinaryConstruct as Bin

task = "find which fields of project in current folder could be improved"

solutions = list()
languages = list()
answer = ai("+ <<SOLVED>>?\n"+task)
solutions.append(task)
language = ai("create new language for this\n" + task)
solutions.append(language)
while("SOLVED" not in answer):

    answer = ai("describe state of task, what was done so far, and prediction for how much work is left in ideal scenario.", solutions)
    language = ai("create new language for this\n"+answer)
    solutions.append(answer)
    solutions.append(language)
    language = ai("implement and validate solution with provided language. reply <<SOLVED>> if it's solved.\n", solutions)





