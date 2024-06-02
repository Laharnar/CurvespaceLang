
from core.mincore import sendWithMessage as ai
from core.mechanistic_layers import BinaryConstruct as Bin

task = "find which fields of project in current folder could be improved"

solutions = list()
languages = list()
while("SOLVED" not in answer):
    answer = ai("describe state of task. if it's solved reply <<SOLVED>>\n" + task, solutions)
    solutions.append(answer)

    language = ai("create new language for this task\n"+task)
    history = list()
    history.append(task)
    history.append(language)
    answer = ai("plan how to solve task, with language\n", history)
    history.append(answer)
    solution = ai("make a shot at solving task, as much as language allows\n", history)
    history.append(solution)
    languages.append(history)
    solutions.append(solution)




