
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

    answer = ai("describe state of task. if it's solved reply <<SOLVED>>\n", solutions)
    language = ai("create new language for this\n"+answer)
    solutions.append(answer)
    solutions.append(language)
    language = ai("validate solution with provided language. reply <<SOLVED>> if it would cover original task.\n", solutions)





