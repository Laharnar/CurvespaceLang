
from core.mincore import sendWithMessage as ai
from core.mechanistic_layers import BinaryConstruct as Bin

task = "find which fields of project in current folder could be improved"

solutions = list()
languages = list()
# adding solved seems to direct it to that solution more? it solves it but doesnt ouput code, but since solution is clear it might be enough for next step
answer = ai("+ <<SOLVED>>?\n"+task)
solutions.append(task)
language = ai("create new language for this\n" + task)
solutions.append(language)
while("SOLVED" not in answer):

    answer = ai("describe state, what was done so far, and prediction for how much work is left in ideal scenario.", [task, answer, "using language", language])
    language = ai("create new language for this", [task, answer])
    solutions.append(answer)
    solutions.append(language)
    answer = ai("implement and validate solution with provided language. reply <<SOLVED>> if it's solved.\n", solutions)
    solutions.append(answer)





