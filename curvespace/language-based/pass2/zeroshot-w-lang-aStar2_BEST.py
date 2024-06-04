
from core.mincore import sendWithMessage as ai
from core.mechanistic_layers import BinaryConstruct as Bin

task = "read folder for files, analyze them and send them to database for link of which is in specific folder found on C:."

def aiLang(task, canZeroShot=True):
    solutions = list()
    languages = list()
    answer = ai("+add <<SOLVED>> if its solved.=>\n"+task)
    steps=1
    if(canZeroShot and "SOLVED" in answer):
        return answer
    solutions.append(task)
    language = ai("create new language for this\n" + task)
    solutions.append(language)
    steps=2
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
        steps+=3
    print("steps", steps)
    return answer

aiLang(task)