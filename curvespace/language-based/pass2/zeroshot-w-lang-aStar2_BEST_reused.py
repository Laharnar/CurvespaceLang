
from core.mincore import sendWithMessage as ai
from core.mechanistic_layers import BinaryConstruct as Bin

task = "find which fields of project in current folder could be improved"

def runSparse(task, history):
    solutions = list()
    languages = list()
    answer = ai("+ <<SOLVED>>?\n"+task, history)
    solutions.append(task)
    language = ai("create new language for this\n" + task, history)
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
    return answer

answer1 = task
for i in range(3):
    history = list()
    answer = runSparse(answer1, history)
    history.append(answer)
    language = ai("create new language based on inspiration for this.", [answer1, answer])
    history.append(language)
    answer = ai("in context are new language, task, and solution to task. use new language to describe task and solution.", [task, answer, language])
    history.append(answer)
    answer1 = answer




