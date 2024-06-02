
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
    break
    # it feels like this has just the right balance of prioritization and openness. removing "task" loses some
    # creating new language for every step alleviates on previous failures
    # this specific solution just FEELS like something else, like much more solid
    # concept of interjecting languages work to guide more
    # "solved" and solution, help with guiding to goal
    answer = ai("describe state of task, what was done so far, and prediction for how much work is left in ideal scenario.", [task, answer, "using language to complete task", language])
    language = ai("create new language for this", [task, answer])
    solutions.append(answer)
    solutions.append(language)
    answer = ai("implement and validate solution with provided language. reply <<SOLVED>> if it's solved.\n", solutions)

#answer = ai("write report on solution to next person, on 1 page.", [answer])
answer = ai("create new language that describes solution, in a way to stand independently.", [task, answer])





