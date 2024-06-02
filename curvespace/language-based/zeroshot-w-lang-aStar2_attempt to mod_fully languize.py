
from core.mincore import sendWithMessage as ai
from core.mechanistic_layers import BinaryConstruct as Bin

task = "find which fields of project in current folder could be improved"

solutions = list()
languages = list()
answer = ai(task)
solutions.append(task)
language = ai("create new language for this\n" + task)
solutions.append(language)
while("SOLVED" not in answer):

    #[answer, "using language to complete task", language] --> works(better?) but only implements language. also loses some small part of language... isnt binded to task, so it wont show how to do it. could be GOOD ENOUGH, in open ended approach
    #[task, "using language to complete task", language] --> loses focus
    answer = ai("describe state of task, what was done so far, and prediction for how much work is left in ideal scenario.", [task, "using language to complete task", language])
    language = ai("create new language for this", [task, answer])# removing re-lang branches out
    solutions.append(answer)
    solutions.append(language)
    answer = ai("implement and validate solution with provided language. reply <<SOLVED>> if it's solved.\n", solutions)
    solutions.append(answer)




