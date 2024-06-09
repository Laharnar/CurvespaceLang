
from core.mincore import sendWithMessage as ai
from core.mechanistic_layers import BinaryConstruct as Bin

task = "come up with good idea of assembly table for multiple people to work on a final product. ideas with few potential solutions for pieces, and correct material. there can be missing ideas in plan, requiring some iteration with design team."

solutions = list()
languages = list()
answer = ai("+ <<SOLVED>>?\n"+task)
solutions.append(task)
language = ai("create new language for this\n" + task)
solutions.append(language)
while("SOLVED" not in answer):

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



